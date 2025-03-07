from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware  # Import CORS Middleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import json
import os
from datetime import datetime
import shutil
import pandas as pd

app = FastAPI()

# ✅ Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend to access backend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Global variable for storing last selected user data
LATEST_METADATA_FILE = "latest_metadata.json"
UPLOADS_DIR = "uploads"
STORAGE_DIR = "storage"
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(STORAGE_DIR, exist_ok=True)

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
    return {"file_id": file_path}

# Select Users - Runs model inference and returns stats
@app.post("/select_users")
def select_users(request: UserSelectionRequest):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    category = request.category.replace(" ", "_")  # Replace spaces with underscores
    open_rate = request.open_rate
    newsletter_content = request.newsletter_content if request.newsletter_content else ""
    file_id = request.file_id

    # If a file was uploaded, process it
    original_uids = None
    if file_id and os.path.exists(file_id):
        try:
            df = pd.read_csv(file_id)
            original_uids = df.iloc[:, 0].tolist()  # Assume first column contains UIDs
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading UID file: {str(e)}")
    else:
        original_uids = "Client data placeholder"

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

    # Save metadata for later use in file generation
    metadata = {
        "datetime": timestamp,
        "category": category,
        "stats": stats,
        "newsletter_content": newsletter_content,
        "original_uids": original_uids,
    }

    with open(LATEST_METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

    return JSONResponse(content={"stats": stats, "zip_filename": f"{timestamp}_{category}_user_groups.zip"})

# Download User Groups - Generates CSV files and ZIP archive
@app.get("/download_user_groups")
def download_user_groups():
    if not os.path.exists(LATEST_METADATA_FILE):
        raise HTTPException(status_code=404, detail="No user selection data found. Run /select_users first.")

    with open(LATEST_METADATA_FILE, "r") as f:
        metadata = json.load(f)

    timestamp = metadata["datetime"]
    category = metadata["category"].replace(" ", "_")  # Ensure filename compatibility
    folder_name = f"{timestamp}_{category}"
    zip_filename = f"{folder_name}_user_groups.zip"
    zip_path = os.path.join(STORAGE_DIR, zip_filename)

    os.makedirs(folder_name, exist_ok=True)

    # Mock CSV file contents
    csv_data = {
        f"{folder_name}/{timestamp}_{category}_mail.csv": "id,email\n1,test1@mail.com\n2,test2@mail.com",
        f"{folder_name}/{timestamp}_{category}_wa.csv": "id,phone\n1,+1234567890\n2,+0987654321",
        f"{folder_name}/{timestamp}_{category}_ignore.csv": "id,reason\n1,No interaction\n2,Opted out",
    }

    # Create mock CSV files
    for filename, content in csv_data.items():
        with open(filename, "w") as f:
            f.write(content)

    # Save metadata.json inside the folder
    metadata_path = f"{folder_name}/metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)

    # Create ZIP file with formatted name
    shutil.make_archive(folder_name, 'zip', folder_name)
    shutil.move(f"{folder_name}.zip", zip_path)  # Move ZIP to storage directory

    # Cleanup: remove temporary folder after zipping
    shutil.rmtree(folder_name)

    return FileResponse(zip_path, media_type='application/zip', filename=zip_filename)
