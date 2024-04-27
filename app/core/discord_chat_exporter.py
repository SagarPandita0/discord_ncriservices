import subprocess
import os
import logging
from datetime import datetime, timedelta

from app.core.data_importer import load_json_to_db


def export_discord_chats(channel_id, token):
    """
    Export Discord chats from a specific channel and load them into a database.

    Args:
        channel_id (str): The ID of the Discord channel to export chats from.
        token (str): The Discord token for authentication.

    Returns:
        dict: A dictionary with a message indicating the success or failure of the export and database loading process.

    Raises:
        ValueError: If token or channel_id is not provided.
        Exception: If any subprocess error occurs or if the output file is not found.

    """
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
        logging.info("command: %s", command)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info("RESULT: %s", result.stdout)
        if result.returncode == 0:
            load_json_to_db(output_path)
            return {
                "message": "Data exported and loaded into the database successfully."
            }
        else:
            logging.error("Export failed: %s", result.stderr)
            return {"message": "Failed to export chat data."}
    except subprocess.CalledProcessError as e:
        logging.error("Subprocess error: %s", e)
        raise Exception("%s", e) from e
    except FileNotFoundError as e:
        logging.error("File not found error: %s", e)
        raise Exception("Output file not found: %s", e.filename) from e
