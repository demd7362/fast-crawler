import heapq

from typing import List, Tuple

from app.model.PostModel import PostModel


def get_top_data(posts: List[PostModel]) -> Tuple[List[PostModel], List[PostModel]]:
    top_views = heapq.nlargest(10, posts, key=lambda post: post.views)
    top_likes = heapq.nlargest(10, posts, key=lambda post: post.recommends)

    return top_views, top_likes
