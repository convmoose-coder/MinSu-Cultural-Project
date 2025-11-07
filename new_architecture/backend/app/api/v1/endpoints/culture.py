from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.culture import FolkCulture
from app.schemas.culture import FolkCultureCreate, FolkCultureResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[FolkCultureResponse])
def read_cultures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cultures = db.query(FolkCulture).offset(skip).limit(limit).all()
    return cultures

@router.post("/", response_model=FolkCultureResponse)
def create_culture(culture: FolkCultureCreate, db: Session = Depends(get_db)):
    db_culture = FolkCulture(**culture.dict())
    db.add(db_culture)
    db.commit()
    db.refresh(db_culture)
    return db_culture

@router.get("/{culture_id}", response_model=FolkCultureResponse)
def read_culture(culture_id: int, db: Session = Depends(get_db)):
    culture = db.query(FolkCulture).filter(FolkCulture.id == culture_id).first()
    if culture is None:
        raise HTTPException(status_code=404, detail="Culture not found")
    return culture

@router.put("/{culture_id}", response_model=FolkCultureResponse)
def update_culture(culture_id: int, culture: FolkCultureCreate, db: Session = Depends(get_db)):
    db_culture = db.query(FolkCulture).filter(FolkCulture.id == culture_id).first()
    if db_culture is None:
        raise HTTPException(status_code=404, detail="Culture not found")
    
    for key, value in culture.dict().items():
        setattr(db_culture, key, value)
    
    db.commit()
    db.refresh(db_culture)
    return db_culture

@router.delete("/{culture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_culture(culture_id: int, db: Session = Depends(get_db)):
    culture = db.query(FolkCulture).filter(FolkCulture.id == culture_id).first()
    if culture is None:
        raise HTTPException(status_code=404, detail="Culture not found")
    
    db.delete(culture)
    db.commit()
    return None