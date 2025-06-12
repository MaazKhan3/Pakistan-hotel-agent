import logging
from pathlib import Path
import json
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HotelDataProcessor:
    def __init__(self, raw_data_dir: str = "../data/raw", processed_data_dir: str = "../data/processed"):
        """Initialize the data processor."""
        self.raw_data_dir = Path(raw_data_dir)
        self.processed_data_dir = Path(processed_data_dir)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        
    def process_all_files(self):
        """Process all raw data files in the raw data directory."""
        raw_files = list(self.raw_data_dir.glob("*.json"))
        all_hotels = []
        
        for file_path in raw_files:
            try:
                logger.info(f"Processing {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    hotels = json.load(f)
                
                processed_hotels = [self._process_hotel(hotel) for hotel in hotels]
                processed_hotels = [h for h in processed_hotels if h is not None]
                all_hotels.extend(processed_hotels)
                
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
        
        self._save_processed_data(all_hotels)
        return all_hotels
    
    def _process_hotel(self, hotel: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single hotel entry."""
        try:
            # Clean and normalize the data
            processed = {
                "id": hotel.get("id", ""),
                "name": self._clean_text(hotel.get("name", "")),
                "description": self._clean_text(hotel.get("description", "")),
                "star_rating": self._normalize_rating(hotel.get("star_rating")),
                "contact_info": self._process_contact_info(hotel.get("contact_info", {})),
                "price_range": self._process_price_range(hotel.get("price_range", {})),
                "amenities": self._process_amenities(hotel.get("amenities", [])),
                "images": hotel.get("images", []),
                "source": hotel.get("source", "unknown"),
                "scraped_at": hotel.get("scraped_at", datetime.now().isoformat())
            }
            
            # Validate required fields
            if not all([processed["name"], processed["contact_info"]["city"]]):
                logger.warning(f"Skipping hotel due to missing required fields: {hotel.get('name')}")
                return None
                
            return processed
            
        except Exception as e:
            logger.error(f"Error processing hotel {hotel.get('name')}: {str(e)}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text fields."""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,-]', '', text)
        return text.strip()
    
    def _normalize_rating(self, rating: Any) -> int:
        """Normalize hotel rating to 1-5 scale."""
        if not rating:
            return 3  # Default to 3 stars if no rating available
        try:
            rating = float(rating)
            return max(1, min(5, round(rating)))
        except (ValueError, TypeError):
            return 3
    
    def _process_contact_info(self, contact_info: Dict[str, Any]) -> Dict[str, Any]:
        """Process and normalize contact information."""
        return {
            "phone": self._clean_text(contact_info.get("phone", "")),
            "email": self._clean_text(contact_info.get("email", "")),
            "website": self._clean_text(contact_info.get("website", "")),
            "address": self._clean_text(contact_info.get("address", "")),
            "city": self._clean_text(contact_info.get("city", "")),
            "region": self._clean_text(contact_info.get("region", ""))
        }
    
    def _process_price_range(self, price_range: Dict[str, Any]) -> Dict[str, Any]:
        """Process and normalize price range."""
        min_price = price_range.get("min_price")
        max_price = price_range.get("max_price")
        
        if not min_price and not max_price:
            return {
                "min_price": 0.0,
                "max_price": 0.0,
                "currency": "PKR",
                "price_per_night": True
            }
            
        return {
            "min_price": float(min_price) if min_price else 0.0,
            "max_price": float(max_price) if max_price else float(min_price) * 1.2 if min_price else 0.0,
            "currency": price_range.get("currency", "PKR"),
            "price_per_night": price_range.get("price_per_night", True)
        }
    
    def _process_amenities(self, amenities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and normalize amenities."""
        processed_amenities = []
        for amenity in amenities:
            if not isinstance(amenity, dict):
                continue
                
            processed_amenities.append({
                "name": self._clean_text(amenity.get("name", "")),
                "description": self._clean_text(amenity.get("description", "")),
                "is_available": bool(amenity.get("is_available", True))
            })
        return processed_amenities
    
    def _save_processed_data(self, hotels: List[Dict[str, Any]]):
        """Save processed data to JSON and CSV files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_path = self.processed_data_dir / f"processed_hotels_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(hotels, f, ensure_ascii=False, indent=2)
            
        # Save as CSV
        csv_path = self.processed_data_dir / f"processed_hotels_{timestamp}.csv"
        df = pd.DataFrame(hotels)
        df.to_csv(csv_path, index=False)
        
        logger.info(f"Saved {len(hotels)} processed hotels to {json_path} and {csv_path}")

def main():
    """Main function to process all hotel data."""
    processor = HotelDataProcessor()
    processor.process_all_files()

if __name__ == "__main__":
    main() 