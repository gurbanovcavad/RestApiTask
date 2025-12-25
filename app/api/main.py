from ninja import NinjaAPI
from ninja import Schema
from typing import List, Optional

api = NinjaAPI(title="Oilfield Operations API", version="0.1.0")

class MockItem(Schema):
    id: int
    name: str
    description: Optional[str] = None 

mock_items_db: List[MockItem] = [
    MockItem(id=1, name="mock", description="example mock item"),
    MockItem(id=2, name="mock", description="example mock item"),
]

@api.get("/")
def hello(request):
    return {"message": "Oilfield API is running"}

@api.post("/mock_items", response=MockItem, tags=["Mock CRUD"])
def create_mock_item(request, item: MockItem):
    mock_items_db.append(item)
    return item

@api.get("/mock_items", response=List[MockItem], tags=["Mock CRUD"])
def list_mock_items(request):
    return mock_items_db 

@api.put("/mock_items/{item_id}", response=MockItem, tags=["Mock CRUD"])
def update_mock_item(request, item_id: int, updated: MockItem):
    for i, item in enumerate(mock_items_db):
        if item.id == item_id:
            mock_items_db[i] = updated
            return updated
    return updated

@api.delete("/mock_items/{item_id}", tags=["Mock CRUD"])
def delete_mock_item(request, item_id: int):
    for i, item in enumerate(mock_items_db):
        if item.id == item_id:
            mock_items_db.pop(i)
            return {"message": f"Mock item {item_id} deleted"}
    return {"message": f"Mock item {item_id} not found"}
