from fastapi import APIRouter, HTTPException
from app.core.discordChatExporterWrapper import export_discord_chats
import os
import logging
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()
discord_token = os.getenv("DISCORD_TOKEN")

@router.get("/export-discord-chats/")
async def api_export_discord_chats(channel_id: str):
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Received channel_id: {channel_id}")
    try:
        logging.info(f"Received token: {discord_token}")
        chats = export_discord_chats(channel_id, discord_token)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
