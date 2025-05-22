from app.database_init import get_db
from app.models.BlogModel import Blog
from app.schemas.BlogSchema import BlogCreate
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException


def get_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs

def create(request: BlogCreate, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def extract_one(id:int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog: raise HTTPException(status_code=404, detail="Blog not found")
    return blog

def update(id:int, request: BlogCreate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog: raise HTTPException(status_code=404, detail="Blog not found")
    
    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)
    return blog

def delete(id:int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == id).first()
    if not blog: raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()
    return "Blog deleted successfully"

def delete_all(db: Session = Depends(get_db)):
    db.query(Blog).delete()
    db.commit()
    return "All blogs deleted successfully"
