from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Project API",
    description="FastAPI Backend for Nuxt.js Frontend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Nuxt.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

class ItemResponse(BaseModel):
    success: bool
    data: Optional[Item] = None
    message: Optional[str] = None

# In-memory storage (replace with database in production)
items_db: List[Item] = [
    Item(id=1, name="Item 1", description="First item", price=10.99),
    Item(id=2, name="Item 2", description="Second item", price=20.99),
]

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Backend",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/items", response_model=List[Item])
async def get_items():
    return items_db

@app.get("/api/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item:
        return ItemResponse(success=True, data=item)
    return ItemResponse(success=False, message="Item not found")

@app.post("/api/items", response_model=ItemResponse)
async def create_item(item: Item):
    item.id = max([i.id for i in items_db if i.id is not None], default=0) + 1
    items_db.append(item)
    return ItemResponse(success=True, data=item, message="Item created successfully")

@app.put("/api/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    for idx, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            item.id = item_id
            items_db[idx] = item
            return ItemResponse(success=True, data=item, message="Item updated successfully")
    return ItemResponse(success=False, message="Item not found")

@app.delete("/api/items/{item_id}", response_model=ItemResponse)
async def delete_item(item_id: int):
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(idx)
            return ItemResponse(success=True, data=deleted_item, message="Item deleted successfully")
    return ItemResponse(success=False, message="Item not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
