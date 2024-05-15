from datetime import datetime,time
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.base.Bases import Post, CrawlingLog
from app.config.database_config import get_db
from app.model.PostModel import PostModel
from app.service.dcinside_crawling_service import crawl_recommend_posts
from app.service.post_analyze_service import get_top_data

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
        now = datetime.now()
        today_start = datetime.combine(now.date(), time.min)  # 오늘 00시 00분
        today_end = datetime.combine(now.date(), time.max)  # 오늘 23시 59분 59초

        result = session.execute(
            select(CrawlingLog)
            .where(
                CrawlingLog.crawled_at >= today_start,
                CrawlingLog.crawled_at <= today_end,
                CrawlingLog.gallery_id == gallery_id
            )
        )
        today_crawling_log = result.scalar()
        if today_crawling_log and today_crawling_log.posts:
            top_likes = []
            top_views = []
            for post in today_crawling_log.posts:
                if post.type == 'like':
                    top_likes.append(PostModel(
                        recommends=post.recommends,
                        url=post.url,
                        ip=post.ip,
                        views=post.views,
                        date=str(post.date),
                        subject=post.subject,
                        writer=post.writer,
                        title=post.title,
                    ))
                elif post.type == 'view':
                    top_views.append(PostModel(
                        recommends=post.recommends,
                        url=post.url,
                        ip=post.ip,
                        views=post.views,
                        date=str(post.date),
                        subject=post.subject,
                        writer=post.writer,
                        title=post.title,
                    ))

            crawl_data = CrawlData(topLikes=top_likes, topViews=top_views)
            response = CrawlResponse(data=crawl_data, detail="Crawling and analysis completed successfully")
            return response
        posts = await crawl_recommend_posts(gallery_id)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for the given gallery ID")
        top_views, top_likes = get_top_data(posts)
        crawling_log = CrawlingLog(
            gallery_id=gallery_id,
            crawled_at=now,
        )
        session.add(crawling_log)
        session.commit()  # crawling_log의 pk 생성을 위해 먼저 커밋
        view_posts = list(map(lambda x: Post(
            recommends=x.recommends,
            url=x.url,
            ip=x.ip,
            views=x.views,
            date=x.date,
            subject=x.subject,
            writer=x.writer,
            title=x.title,
            type='view',
            crawling_log_id=crawling_log.id
        ), top_views))
        session.add_all(view_posts)
        like_posts = list(map(lambda x: Post(
            recommends=x.recommends,
            url=x.url,
            ip=x.ip,
            views=x.views,
            date=x.date,
            subject=x.subject,
            writer=x.writer,
            title=x.title,
            type='like',
            crawling_log_id=crawling_log.id
        ), top_likes))
        session.add_all(like_posts)

        session.commit()
        crawl_data = CrawlData(topLikes=top_likes, topViews=top_views)
        response = CrawlResponse(data=crawl_data, detail="Crawling and analysis completed successfully")
        return response
    finally:
        session.close()
