import pandas as pd
import json
import os
import shutil
import logging
from fastapi.responses import FileResponse

# Configure logging
LOG_FILE = "logs/file_processor.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Mock data for user group files
mail_file_content_mockup = "id,email\n1,test1@mail.com\n2,test2@mail.com"
wa_file_content_mockup = "id,phone\n1,+1234567890\n2,+0987654321"
ignore_file_content_mockup = "id,reason\n1,No interaction\n2,Opted out"


def read_cpid_file(file_path):
    """ Reads CPID file and returns a list of CPIDs. Supports CSV, JSON, and XLSX. """
    logging.info(f"Attempting to read CPID file: {file_path}")

    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)  

        elif file_path.endswith(".json"):
            with open(file_path, "r") as f:
                data = json.load(f)
            df = pd.DataFrame(data)  
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path, engine="openpyxl")
        else:
            logging.error(f"Unsupported file format: {file_path}")
            raise ValueError("Unsupported file format. Please upload CSV, JSON, or XLSX.")

        logging.info(f"Columns: {df.columns}")
        
        # Ensure 'clientID' column exists
        if "Клиент" in df.columns:
            df.rename(columns={"Клиент": "clientID"}, inplace=True)
            df = df[["clientID"]]

        # If there's only one column, rename it to clientID regardless of original name
        if len(df.columns) == 1:
            df.columns = ['clientID']

        # Ensure 'clientID' column exists
        if "clientID" not in df.columns:
            logging.error(f"Invalid file format, missing 'clientID' column: {file_path}")
            raise ValueError("Invalid file format. Missing 'clientID' column.")

        # Check if clientIDs have the expected format (containing hyphens)
        sample_ids = df['clientID'].head().tolist()
        has_hyphens = any('-' in str(id) for id in sample_ids)
        
        if not has_hyphens:
            logging.warning(
                f"ClientIDs are in incorrect format - no hyphens found in sample: {sample_ids}. "
                "Expected format example: 'ABCD1234-AB12-CD34-5678-000123ABC456'"
            )
            raise ValueError("ClientIDs are in incorrect format. Please upload a file with the correct format.")
        
        logging.info(f"Successfully read {len(df)} CPIDs from file: {file_path}")
        return df["clientID"].tolist()
    

    except Exception as e:
        logging.error(f"Error reading CPID file: {str(e)}")
        raise


def save_metadata(database, folder_path):
    """ Saves metadata as a JSON file inside the correct folder. """
    metadata_path = os.path.join(folder_path, "metadata.json")
    logging.info(f"Saving metadata to {metadata_path}")

    try:
        with open(metadata_path, "w") as f:
            json.dump(database, f, indent=4)
        logging.info(f"Metadata saved successfully: {metadata_path}")
    except Exception as e:
        logging.error(f"Failed to save metadata: {str(e)}")
        raise


def generate_user_group_files(database, storage_path):
    """ Creates CSV files and saves metadata inside the specified folder. """
    timestamp = database["timestamp"]
    category = database["category"]
    folder_name = f"{timestamp}_{category}"
    folder_path = os.path.join(storage_path, folder_name)

    logging.info(f"Creating user group files in: {folder_path}")
    os.makedirs(folder_path, exist_ok=True)

    try:
        # Assigning mockup values to actual content variables
        mail_file_content = mail_file_content_mockup
        wa_file_content = wa_file_content_mockup
        ignore_file_content = ignore_file_content_mockup

        csv_data = {
            os.path.join(folder_path, f"{timestamp}_{category}_mail.csv"): mail_file_content,
            os.path.join(folder_path, f"{timestamp}_{category}_wa.csv"): wa_file_content,
            os.path.join(folder_path, f"{timestamp}_{category}_ignore.csv"): ignore_file_content,
        }

        for filename, content in csv_data.items():
            with open(filename, "w") as f:
                f.write(content)
            logging.info(f"Created file: {filename}")

        save_metadata(database, folder_path)
        zip_path, zip_filename = create_zip_file(folder_path, storage_path)

        logging.info(f"User group files and ZIP archive created successfully: {zip_filename}")
        return zip_path, zip_filename

    except Exception as e:
        logging.error(f"Error generating user group files: {str(e)}")
        raise


def create_zip_file(folder_name, storage_path):
    """ Creates a ZIP archive of the folder and moves it to storage. """
    zip_filename = f"{folder_name}_user_groups.zip"
    zip_path = os.path.join(storage_path, zip_filename)

    logging.info(f"Creating ZIP file: {zip_filename}")

    try:
        shutil.make_archive(folder_name, 'zip', folder_name)
        shutil.move(f"{folder_name}.zip", zip_path)
        shutil.rmtree(folder_name)  # Cleanup
        logging.info(f"ZIP file created and moved to storage: {zip_path}")
        return zip_path, zip_filename

    except Exception as e:
        logging.error(f"Error creating ZIP file: {str(e)}")
        raise


def download_zip_file(zip_path, zip_filename):
    """ Returns the ZIP file as a response for download. """
    logging.info(f"Preparing ZIP file for download: {zip_filename}")

    if not os.path.exists(zip_path):
        logging.error(f"ZIP file not found: {zip_path}")
        raise FileNotFoundError(f"ZIP file {zip_filename} not found.")

    logging.info(f"ZIP file {zip_filename} is ready for download.")
    return FileResponse(zip_path, media_type='application/zip', filename=zip_filename)
