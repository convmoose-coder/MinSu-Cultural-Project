from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.culture import FolkCultureResponse, FolkCultureCreate
from app.models.culture import FolkCulture as FolkCultureModel

router = APIRouter()

@router.get("/search/", response_model=List[FolkCultureResponse])
def search_cultures(query: str, db: Session = Depends(get_db)):
    # 这里应该实现实际的搜索逻辑
    cultures = db.query(FolkCultureModel).filter(
        FolkCultureModel.name.contains(query) | 
        FolkCultureModel.description.contains(query) |
        FolkCultureModel.region.contains(query)
    ).all()
    return cultures