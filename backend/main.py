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

# Store uploaded UID file content in memory
database = {
    "uids": None
}

# Request model for selecting users
class UserSelectionRequest(BaseModel):
    category: str
    open_rate: int
    newsletter_content: str = None
    file_id: str = None  # Reference to uploaded file

# Upload UID File separately and store in memory
@app.post("/upload_uid_file")
def upload_uid_file(uid_file: UploadFile = File(...)):
    try:
        file_id = os.path.join(UPLOADS_DIR, uid_file.filename)  # ✅ Standardized file_id
        with open(file_id, "wb") as buffer:
            buffer.write(uid_file.file.read())

        database["uids"] = read_uid_file(file_id)

        logging.info(f"File uploaded successfully: {file_id}")
        return {"message": "File uploaded successfully.", "file_id": file_id}  # ✅ Now we return the correct file_id
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

# Select Users - Runs model inference using stored UID data
@app.post("/select_users")
def select_users(request: UserSelectionRequest):
    if database["uids"] is None:
        raise HTTPException(status_code=400, detail="No UID file uploaded. Please upload a file first.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    category = request.category.replace(" ", "_")
    open_rate = request.open_rate
    newsletter_content = request.newsletter_content if request.newsletter_content else ""
    file_id = request.file_id  


    logging.info(f"Processing user selection: category={category}, open_rate={open_rate}")
    
    stats = {
        "total_users": 69696,
        "expected_open_rate": open_rate,
        "mail_group": 6969,
        "whatsapp_group": 6969,
        "ignored_group": 69,
    }
    
    metadata = {
        "datetime": timestamp,
        "category": category,
        "stats": stats,
        "newsletter_content": newsletter_content,
        "original_uids": database["uids"],
        "file_id": file_id,  
    }

    save_metadata(metadata, os.path.join(STORAGE_DIR, "latest_metadata.json"))
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