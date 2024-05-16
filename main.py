from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.router.crawling_router import router as crawling_router

app = FastAPI()

# 정적 파일 제공 설정
app.mount("/static", StaticFiles(directory="./frontend/build/static"), name="static")

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 포함
app.include_router(crawling_router)


@app.get("/{full_path:path}")
async def serve_index_html(full_path: str):
    # API 요청인 경우 처리하지 않음
    if full_path.startswith("/api/"):
        return None
    return FileResponse("./frontend/build/index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
