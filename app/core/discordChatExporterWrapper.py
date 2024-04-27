import subprocess
import os
import logging
from datetime import datetime, timedelta

from app.core.dataImporter import load_json_to_db

def export_discord_chats(channel_id, token, output_dir="outputs"):
    if not token:
        raise ValueError("Discord token not found!")
    if not channel_id:
        raise ValueError("channel_id not found!")
    output_dir = "C:\\Users\\sagar\\Downloads\\ncriservices\\discord_ncriservices\\app\\outputs\\"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{channel_id}_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)
    seven_days_ago = datetime.now() - timedelta(days=7)
    date_after = seven_days_ago.strftime("%Y-%m-%d")
    command = [
        "dotnet",
        "C:\\Users\\sagar\\Downloads\\ncriservices\\discord_ncriservices\\DiscordChatExporterCLI\\DiscordChatExporter.Cli.dll",
        "export",
        "-t", token,
        "-c", channel_id,
        "--format", "Json",
        "--output", output_path,
        "--after", date_after
    ]
    
    try:
        logging.basicConfig(level=logging.INFO)
        logging.info(f"command: {command}")
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if result.returncode == 0:
            load_json_to_db(output_path)
            return {"message": "Data exported and loaded into the database successfully."}
        else:
            logging.error(f"Export failed: {result.stderr}")
            return {"message": "Failed to export chat data."}
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess error: {e}")
        raise Exception(f"{e}") from e
    except FileNotFoundError as e:
        logging.error(f"File not found error: {e}")
        raise Exception(f"Output file not found: {e.filename}") from e