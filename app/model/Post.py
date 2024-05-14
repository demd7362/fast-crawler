class Post:
    def __init__(self, recommends: int, url: str, ip: str, views: int, date: str, subject: str, writer: str, title: str):
        self.recommends = recommends
        self.url = url
        self.ip = ip
        self.views = views
        self.date = date
        self.subject = subject
        self.writer = writer
        self.title = title

    def __lt__(self, other):
        return (self.views, self.recommends) < (other.views, other.recommends)
