from fastapi import UploadFile

def image_search(file: UploadFile) -> dict:
    # TODO: Run CLIP / ResNet embedding + vector search
    return {
        "type": "image_search",
        "results": [
            {"title": "Blue T-Shirt", "price": 19.99, "url": "/product/123"},
            {"title": "Red Sneakers", "price": 89.99, "url": "/product/456"},
        ]
    }