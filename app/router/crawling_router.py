import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter

router = APIRouter()


@router.get('/crawl')
async def route_for_crawl() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get('https://gall.dcinside.com/mgallery/board/lists',
                                    params={'id': 'github', 'exception_mode': 'recommend'}, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})
        content = response.text
    soup = BeautifulSoup(content, "html.parser")

    texts = [em.text for em in soup.find_all('em')]

    return {"title": None,
            "texts": texts
            }
