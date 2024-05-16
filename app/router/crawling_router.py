from datetime import datetime, time
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


def get_response_as_exist_data(today_crawling_log):
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


def get_today_crawling_log(session: Session, gallery_id: str, date: datetime):
    return session.execute(
        select(CrawlingLog)
        .where(
            CrawlingLog.crawled_at == date,
            CrawlingLog.gallery_id == gallery_id
        )
    ).scalar()


def get_now_date_as_fixed():
    return datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)


@router.get('/api/crawl/{gallery_id}', response_model=CrawlResponse)
async def crawling_router(gallery_id: str, session: Session = Depends(get_db)):
    try:
        now = get_now_date_as_fixed()
        today_crawling_log = get_today_crawling_log(session, gallery_id, now)
        if today_crawling_log:
            return get_response_as_exist_data(today_crawling_log)
        posts = await crawl_recommend_posts(gallery_id)
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for the given gallery ID")
        top_views, top_likes = get_top_data(posts)
        crawling_log = CrawlingLog(
            gallery_id=gallery_id,
            crawled_at=now,
        )
        session.add(crawling_log)
        session.flush()  # 변경 사항을 데이터베이스에 반영
        session.refresh(crawling_log)  # 생성된 크롤링 로그의 ID를 가져옴
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
