import httpx
from bs4 import BeautifulSoup
from typing import List

from app.model.Post import Post

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
mgallery_url = 'https://gall.dcinside.com/mgallery/board/lists'
gallery_url = 'https://gall.dcinside.com/board/lists'
post_url_dict = {
    mgallery_url: 'https://gall.dcinside.com/mgallery/board/view',
    gallery_url: 'https://gall.dcinside.com/board/view'
}


async def crawl_recommend_posts(gallery_id: str) -> List[Post]:
    posts = []

    def get_post_url(url: str, post_no: str):
        return f'{post_url_dict[url]}?id={gallery_id}&no={post_no}'

    print(f'{gallery_id} gallery crawling start')

    async def get_post_rows(async_client: httpx.AsyncClient, url: str) -> List[Post]:
        response = await async_client.get(url=url,
                                          params={'id': gallery_id, 'exception_mode': 'recommend', 'page': page},
                                          headers={'User-Agent': user_agent})
        content = response.text
        soup = BeautifulSoup(content, "html.parser")
        return soup.find_all('tr', class_='us-post')

    defined_url = gallery_url
    async with httpx.AsyncClient() as client:
        for page in range(40, 10000000):
            print(f'{page} page parsing now...')
            post_rows = await get_post_rows(client, defined_url)
            if not post_rows:
                if len(posts) > 0:  # 마지막 페이지니 break
                    break
                else:  # 갤러리가 정의되지 않아서 posts가 비어있음
                    post_rows = await get_post_rows(client, mgallery_url)
                    if not post_rows:  # 메인도 마이너도 아니면 에러
                        raise RuntimeError(f'gallery id {gallery_id} is invalid')
                    defined_url = mgallery_url

            for row in post_rows:
                post_no = row.get('data-no', '')
                if not post_no:
                    continue

                recommend_element = row.find('td', class_='gall_recommend')
                recommend_count = recommend_element.get_text(strip=True)

                post_url = get_post_url(defined_url, post_no)

                view_element = row.find('td', class_='gall_count')
                views = view_element.get_text(strip=True)

                date_element = row.find('td', class_='gall_date')
                date = date_element.get('title', '')

                subject_element = row.find('td', class_='gall_subject')
                subject = subject_element.get_text(strip=True)

                writer_element = row.find('td', class_='gall_writer')
                writer = writer_element.get('data-nick')
                writer_ip = writer_element.get('data-ip')

                title_element = row.find('td', class_='gall_tit')
                title = title_element.find('a').get_text(strip=True)

                posts.append(Post(recommends=int(recommend_count),
                                  url=post_url,
                                  views=int(views),
                                  date=date,
                                  subject=subject,
                                  writer=writer,
                                  ip=writer_ip,
                                  title=title))
    print(f'{gallery_id} gallery parsing done')
    return posts
