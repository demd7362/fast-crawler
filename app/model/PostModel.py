from pydantic import BaseModel


class PostModel(BaseModel):
    recommends: int
    url: str
    ip: str
    views: int
    date: str
    subject: str
    writer: str
    title: str


    def __lt__(self, other):
        return (self.views, self.recommends) < (other.views, other.recommends)
