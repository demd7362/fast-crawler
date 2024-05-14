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


# index.html 제공
@app.get("/")
@app.get("/index")
async def serve_index_html():
    return FileResponse("./frontend/build/index.html")


app.include_router(crawling_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=80)
