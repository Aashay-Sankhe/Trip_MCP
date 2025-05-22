from pydantic import BaseModel


class BlogCreate(BaseModel):
    title: str
    body: str


class BlogReturn(BlogCreate):
    
    class Config:
        from_attributes = True
    
    