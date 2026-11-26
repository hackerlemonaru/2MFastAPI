from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))


Base.metadata.create_all(engine)
app = FastAPI()


class ItemIn(BaseModel):
    name: str
    note: Optional[str] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    return [{"id": i.id, "name": i.name} for i in db.query(Item).order_by(Item.id)]


@app.post("/items", status_code=201)
def add_item(body: ItemIn, db: Session = Depends(get_db)):
    it = Item(name=body.name)
    db.add(it)
    db.commit()
    return {"id": it.id, "name": it.name}


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    it = db.get(Item, item_id)
    if it is None:
        raise HTTPException(status_code=404, detail="no such item")
    return {"id": it.id, "name": it.name}
