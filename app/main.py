from fastapi import FastAPI
from .api.chatExporter import router as chat_exporter_router
from .api.keywordSearch import router as keyword_search_router
from .api.byDateSearch import router as by_date_search_router
app = FastAPI()

app.include_router(chat_exporter_router)
app.include_router(keyword_search_router)
app.include_router(by_date_search_router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
