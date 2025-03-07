from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import json
import logging
from datetime import datetime
from file_processor import read_uid_file, save_metadata, generate_user_group_files, create_zip_file, download_zip_file

# Get the absolute directory of main.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define paths relative to BASE_DIR
LOG_DIR = os.path.join(BASE_DIR, "logs")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# Ensure directories exist
for directory in [LOG_DIR, UPLOADS_DIR, STORAGE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Global variables for storing paths
LATEST_METADATA_FILE = os.path.join(BASE_DIR, "latest_metadata.json")

# Setup logging
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "backend.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to access backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Request model for selecting users
class UserSelectionRequest(BaseModel):
    category: str
    open_rate: int
    newsletter_content: str = None
    file_id: str = None  # Reference to uploaded file

# Upload UID File separately and return file ID
@app.post("/upload_uid_file")
def upload_uid_file(uid_file: UploadFile = File(...)):
    file_path = os.path.join(UPLOADS_DIR, uid_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(uid_file.file.read())
    logging.info(f"File uploaded: {file_path}")
    return {"file_id": file_path}

# Select Users - Runs model inference and returns stats
@app.post("/select_users")
def select_users(request: UserSelectionRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    category = request.category.replace(" ", "_")  # Replace spaces with underscores
    open_rate = request.open_rate
    newsletter_content = request.newsletter_content if request.newsletter_content else ""
    file_id = request.file_id

    logging.info(f"Processing user selection: category={category}, open_rate={open_rate}")

    # Process UID file if provided
    try:
        original_uids = read_uid_file(file_id) if file_id and os.path.exists(file_id) else "Client data placeholder"
        logging.info(f"Read UID file successfully: {file_id}")
    except Exception as e:
        logging.error(f"Error reading UID file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error reading UID file: {str(e)}")

    # Mock model inference (Replace this with real logic later)
    total_users = 69696
    mail_group = 6969
    whatsapp_group = 6969
    ignored_group = 69

    stats = {
        "total_users": total_users,
        "expected_open_rate": open_rate,
        "mail_group": mail_group,
        "whatsapp_group": whatsapp_group,
        "ignored_group": ignored_group,
    }

    logging.info(f"Generated user selection stats: {stats}")

    # Save metadata for later use in file generation
    metadata = {
        "datetime": timestamp,
        "category": category,
        "stats": stats,
        "newsletter_content": newsletter_content,
        "original_uids": original_uids,
    }
    save_metadata(metadata, LATEST_METADATA_FILE)
    logging.info("Metadata saved successfully.")

    return JSONResponse(content={"stats": stats, "zip_filename": f"{timestamp}_{category}_user_groups.zip"})

# Download User Groups - Generates CSV files and ZIP archive
@app.get("/download_user_groups")
def download_user_groups():
    if not os.path.exists(LATEST_METADATA_FILE):
        logging.error("Metadata file not found. Cannot proceed with download.")
        raise HTTPException(status_code=404, detail="No user selection data found. Run /select_users first.")

    with open(LATEST_METADATA_FILE, "r") as f:
        metadata = json.load(f)

    timestamp = metadata["datetime"]
    category = metadata["category"].replace(" ", "_")  # Ensure filename compatibility
    folder_name = f"{timestamp}_{category}"
    zip_filename = f"{folder_name}_user_groups.zip"
    zip_path = os.path.join(STORAGE_DIR, zip_filename)

    logging.info(f"Generating user group files for {folder_name}")
    generate_user_group_files(folder_name, timestamp, category, metadata)

    logging.info(f"Creating ZIP archive for {folder_name}")
    zip_path, zip_filename = create_zip_file(folder_name, STORAGE_DIR)

    logging.info(f"ZIP file ready for download: {zip_filename}")
    return download_zip_file(zip_path, zip_filename)