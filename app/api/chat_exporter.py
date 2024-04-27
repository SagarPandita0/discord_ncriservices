import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query

from app.core.discord_chat_exporter import export_discord_chats

load_dotenv()
router = APIRouter()
discord_token = os.getenv("DISCORD_TOKEN")


@router.get("/export-discord-chats/")
async def api_export_discord_chats(channel_id: str = Query(...)):
    """
    Export Discord channel chats to Postgres.

    Args:
        channel_id (str): The ID of the Discord channel from which to export messages.

    Returns:
        dict: A dictionary with a message indicating the success or failure of the export and database loading process.

    Raises:
        HTTPException: If channel ID is not numeric or if any other error occurs during the export process.
    """
    logging.info("Received channel_id: %s", channel_id)
    if not channel_id.isdigit():
        raise HTTPException(status_code=400, detail="Channel ID must be numeric.")
    try:
        logging.info("Received token: %s", discord_token)
        chats = export_discord_chats(channel_id, discord_token)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
