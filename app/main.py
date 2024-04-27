from fastapi import FastAPI
from .api.chatExporter import router as chat_exporter_router
from .api.keywordSearch import router as keyword_search_router
from .api.byDateSearch import router as by_date_search_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(chat_exporter_router)
app.include_router(keyword_search_router)
app.include_router(by_date_search_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
