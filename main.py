from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import Session
import models

# initiliaze FastAPI
app = FastAPI()

db = Session()


class Item(BaseModel):  # serializer
    id: int
    name: str
    description: str
    price: float
    on_offer: bool

    class Config:
        orm_mode = True


@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    new_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer,
    )

    db_item = db.query(models.Item).filter(models.Item.name == new_item.name).first()
    if db_item is not None:
        raise HTTPException(status_code=400, detail="item already exists")

    db.add(new_item)
    db.commit()

    return new_item


@app.get("/item/{item_id}")
def get_by_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    return item


@app.put("/item/{item_id}/update")
def update_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    db.commit()
    return item


@app.delete("/item/{item_id}/remove")
def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!"
        )
    db.delete(item_to_delete)
    db.commit()
    return item_to_delete
