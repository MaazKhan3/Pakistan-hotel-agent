from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Amenity(BaseModel):
    """Model for hotel amenities."""
    name: str
    description: Optional[str] = None
    is_available: bool = True

class ContactInfo(BaseModel):
    """Model for hotel contact information."""
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    address: str
    city: str
    region: str

class PriceRange(BaseModel):
    """Model for hotel price range."""
    min_price: float
    max_price: float
    currency: str = "PKR"
    price_per_night: bool = True

class Hotel(BaseModel):
    """Model for hotel information."""
    id: str
    name: str
    description: str
    star_rating: int = Field(ge=1, le=5)
    contact_info: ContactInfo
    price_range: PriceRange
    amenities: List[Amenity]
    images: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "hotel_123",
                "name": "Skardu Grand Hotel",
                "description": "Luxury hotel with mountain views",
                "star_rating": 4,
                "contact_info": {
                    "phone": "+92-123-4567890",
                    "email": "info@skardugrand.com",
                    "website": "https://skardugrand.com",
                    "address": "123 Main Street",
                    "city": "Skardu",
                    "region": "Gilgit-Baltistan"
                },
                "price_range": {
                    "min_price": 5000,
                    "max_price": 15000,
                    "currency": "PKR",
                    "price_per_night": True
                },
                "amenities": [
                    {
                        "name": "Wi-Fi",
                        "description": "Free high-speed internet",
                        "is_available": True
                    }
                ]
            }
        } 