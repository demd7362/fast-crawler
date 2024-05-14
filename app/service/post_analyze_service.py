import heapq

from typing import List

from app.model.Post import Post


def get_top_posts(posts: List[Post]):
    top_views = heapq.nlargest(10, posts, key=lambda post: post.views)
    top_likes = heapq.nlargest(10, posts, key=lambda post: post.recommends)
    return top_views, top_likes

# 예시 사용법
