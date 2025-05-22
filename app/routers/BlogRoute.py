from typing import List
from fastapi import APIRouter, Depends, status
from app.crud.BlogCrudOps import get_all, create, extract_one, update, delete, delete_all
from app.database_init import get_db
from app.schemas.BlogSchema import BlogCreate, BlogReturn
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/blog",
    tags=["blogs"]
)


@router.get("/", response_model=List[BlogReturn])
def get_all_blogs(db: Session = Depends(get_db)):
    return get_all(db)

@router.post("/", response_model=BlogReturn, status_code=status.HTTP_201_CREATED)
def create_blog(request: BlogCreate, db: Session = Depends(get_db)):
    return create(request, db)

@router.get("/{id}", response_model=BlogReturn)
def get_blog(id: int, db: Session = Depends(get_db)):
    return extract_one(id, db)

@router.put("/{id}", response_model=BlogReturn, status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: BlogCreate, db: Session = Depends(get_db)):
    return update(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return delete(id, db)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_blogs(db: Session = Depends(get_db)):
    return delete_all(db)
