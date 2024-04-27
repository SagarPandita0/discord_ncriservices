from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.by_date_search import router as by_date_search_router
from .api.chat_exporter import router as chat_exporter_router
from .api.keyword_search import router as keyword_search_router
from .api.author_search import router as author_search_router
from .logging_config import setup_logging

app = FastAPI()
setup_logging()
app.include_router(chat_exporter_router)
app.include_router(keyword_search_router)
app.include_router(by_date_search_router)
app.include_router(author_search_router)

# middleware only added for GUI interaction, to be removed in future!
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
