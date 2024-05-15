from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database_config import get_db
from app.model.PostModel import PostModel
from app.service.dcinside_crawling_service import crawl_recommend_posts
from app.service.post_analyze_service import get_top_posts

router = APIRouter()


class CrawlData(CamelModel):
    top_likes: List[PostModel]
    top_views: List[PostModel]


class CrawlResponse(BaseModel):
    data: Optional[CrawlData]
    detail: str


@router.get('/api/crawl/{gallery_id}', response_model=CrawlResponse)
async def crawling_router(gallery_id: str, session: Session = Depends(get_db)):
    try:
        posts = await crawl_recommend_posts(gallery_id, session)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for the given gallery ID")
        top_views, top_likes = get_top_posts(posts)
        crawl_data = CrawlData(topLikes=top_likes, topViews=top_views)
        response = CrawlResponse(data=crawl_data, detail="Crawling and analysis completed successfully")
        return response
    finally:
        session.close()
