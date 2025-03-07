import pandas as pd
import json
import os
import shutil
from fastapi.responses import FileResponse

# Mock data for user group files
mail_file_content_mockup = "id,email\n1,test1@mail.com\n2,test2@mail.com"
wa_file_content_mockup = "id,phone\n1,+1234567890\n2,+0987654321"
ignore_file_content_mockup = "id,reason\n1,No interaction\n2,Opted out"

def read_uid_file(file_path):
    """ Reads UID file and returns a list of UIDs. Supports CSV, JSON, and XLSX. """
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path, engine="openpyxl")  # Safe XLSX reading
    else:
        raise ValueError("Unsupported file format. Please upload CSV, JSON, or XLSX.")

    # Ensure 'Uid' column exists
    if "Uid" not in df.columns:
        raise ValueError("Invalid file format. Missing 'Uid' column.")

    return df["Uid"].tolist()

def save_metadata(metadata, file_path):
    """ Saves metadata as a JSON file. """
    with open(file_path, "w") as f:
        json.dump(metadata, f, indent=4)

def generate_user_group_files(folder_name, timestamp, category, stats):
    """ Creates CSV files for user groups and metadata in the specified folder. """
    os.makedirs(folder_name, exist_ok=True)

    # Assigning mockup values to actual content variables
    mail_file_content = mail_file_content_mockup
    wa_file_content = wa_file_content_mockup
    ignore_file_content = ignore_file_content_mockup

    csv_data = {
        os.path.join(folder_name, f"{timestamp}_{category}_mail.csv"): mail_file_content,
        os.path.join(folder_name, f"{timestamp}_{category}_wa.csv"): wa_file_content,
        os.path.join(folder_name, f"{timestamp}_{category}_ignore.csv"): ignore_file_content,
    }

    for filename, content in csv_data.items():
        with open(filename, "w") as f:
            f.write(content)

    metadata_path = os.path.join(folder_name, "metadata.json")
    save_metadata(stats, metadata_path)

def create_zip_file(folder_name, storage_path):
    """ Creates a ZIP archive of the folder and moves it to storage. """
    zip_filename = f"{folder_name}_user_groups.zip"
    zip_path = os.path.join(storage_path, zip_filename)
    shutil.make_archive(folder_name, 'zip', folder_name)
    shutil.move(f"{folder_name}.zip", zip_path)
    shutil.rmtree(folder_name)  # Cleanup
    return zip_path, zip_filename

def download_zip_file(zip_path, zip_filename):
    """ Returns the ZIP file as a response for download. """
    return FileResponse(zip_path, media_type='application/zip', filename=zip_filename)