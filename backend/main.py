from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import time
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
    "timestamp": None,
    "stats": None,  # Store stats after selecting users
    "uids": None,
    "category": None,  # Store category selected
    "newsletter_content": None,  # Store newsletter content
    "file_id": None,  # Store file_id
    "model_output": None,  # Store model output
}

stats_mockup = {
        "total_users": 69696,
        "expected_open_rate": 69,
        "mail_group": 6969,
        "whatsapp_group": 6969,
        "ignored_group": 69,
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
    # get uid file
    # read uid file
    # store uid file in memory
    # return file_id
    try:
        file_id = os.path.join(UPLOADS_DIR, uid_file.filename)  # ✅ Standardized file_id
        with open(file_id, "wb") as buffer:
            buffer.write(uid_file.file.read())

        database["uids"] = read_uid_file(file_id)
        database["file_id"] = file_id

        logging.info(f"File uploaded successfully: {file_id}")
        return {"message": "File uploaded successfully.", "file_id": file_id}  # ✅ Now we return the correct file_id
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

# Select Users - Runs model inference using stored UID data
@app.post("/select_users")
def select_users(request: UserSelectionRequest):
    # check if uid file is uploaded
    # if not, return error
    # if yes, continue
    # parse request -> into separate function
    # return stats to frontend, 
    if database["uids"] is None:
        raise HTTPException(status_code=400, detail="No UID file uploaded. Please upload a file first.")

    time.sleep(5)

    database["timestamp"] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    database["category"] = request.category.replace(" ", "_")
    database["open_rate"] = request.open_rate
    database["newsletter_content"] = request.newsletter_content if request.newsletter_content else ""

    logging.info(f"Processing user selection: category={database['category']}, open_rate={database['open_rate']}")

    # Mock stats (replace with model inference later)
    stats = stats_mockup
    database["stats"] = stats

    logging.info(f"Generated user selection stats: {stats}")

    return JSONResponse(content={"stats": stats, "zip_filename": f"{database['timestamp']}_{database['category']}_user_groups.zip"})


# Download User Groups - Generates CSV files and ZIP archive
@app.get("/download_user_groups")
def download_user_groups():
    if database["uids"] is None:
        logging.error("No UID file uploaded. Cannot proceed with download.")
        raise HTTPException(status_code=404, detail="No user selection data found. Run /select_users first.")

    logging.info(f"Generating user group files")
    zip_path, zip_filename = generate_user_group_files(database, STORAGE_DIR)

    logging.info(f"ZIP file ready for download: {zip_filename}")
    return download_zip_file(zip_path, zip_filename)
