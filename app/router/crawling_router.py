
from fastapi import APIRouter

from app.service.dcinside_crawling_service import crawl_recommend_posts
from app.service.post_analyze_service import get_top_posts

router = APIRouter()


@router.get('/api/crawl/{gallery_id}')
async def crawling_router(gallery_id: str):
    posts = await crawl_recommend_posts(gallery_id)
    top_views, top_likes = get_top_posts(posts)

    return {
        'topViews': top_views,
        'topLikes': top_likes
    }
