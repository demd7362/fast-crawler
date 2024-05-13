from fastapi import FastAPI

from app.router.crawling_router import router as crawling_router

app = FastAPI()


app.include_router(crawling_router)
