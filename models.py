from typing import Optional, Dict, Any
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field, computed_field

class StoreData(BaseModel):
    name: Optional[str] = None
    menus: list = []
    rating_count: int = 0
    id: Optional[str] = None
    rating_stars: Optional[float] = None
    fssai_id: Optional[str] = None
    lat: Optional[float] = None
    phone_number: Optional[str] = None
    address_full: Optional[str] = None
    cuisines: Optional[str] = None
    is_available: bool = False
    min_order_amount: Optional[float] = None
    address_area: Optional[str] = None
    lng: Optional[float] = None
    city: Optional[str] = None

class LocationData(BaseModel):
    id: str
    name: str

class PlatformData(BaseModel):
    id: str
    name: str

class BrandData(BaseModel):
    id: str
    name: str

class AggregatorData(Document):
    biz_id: str
    brand: Optional[Dict[str, Any]] = None  # Brand data as dictionary
    city: str
    data: Dict[str, Any]  # Store data as dictionary
    location: Dict[str, Any]  # Location data as dictionary
    message: str
    platform: Dict[str, Any]  # Platform data as dictionary
    status: str
    store_id: str
    timestamp: datetime

    @computed_field
    @property
    def store_data_id(self) -> Optional[str]:
        try:
            if isinstance(self.data, dict) and 'store' in self.data:
                store = self.data['store']
                if isinstance(store, dict) and 'id' in store:
                    return store['id']
        except (KeyError, TypeError, AttributeError):
            pass
        return None

    class Settings:
        name = "aggregator_data"
        use_state_management = True

class AggregatorDataResponse(BaseModel):
    biz_id: str
    brand: Optional[Dict[str, Any]] = None
    city: str
    data: Dict[str, Any]
    location: Dict[str, Any]
    message: str
    platform: Dict[str, Any]
    status: str
    store_id: str
    timestamp: datetime
    store_data_id: Optional[str] = None 