import logging
from pathlib import Path
import sys
import time
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scraping.booking_scraper import BookingScraper
from scraping.data_processor import HotelDataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(project_root / "logs" / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Run the complete data collection and processing pipeline."""
    try:
        # Create necessary directories
        (project_root / "logs").mkdir(exist_ok=True)
        (project_root / "data" / "raw").mkdir(parents=True, exist_ok=True)
        (project_root / "data" / "processed").mkdir(parents=True, exist_ok=True)
        
        # Step 1: Scrape hotel data
        logger.info("Starting data collection phase...")
        scraper = BookingScraper()
        try:
            cities = [
                "Islamabad",
                "Karachi",
                "Lahore",
                "Peshawar",
                "Quetta",
                "Skardu",
                "Gilgit",
                "Murree"
            ]
            
            for city in cities:
                logger.info(f"Scraping hotels in {city}")
                scraper.scrape_city(city)
                time.sleep(5)  # Be nice to the server
                
        finally:
            scraper.close()
            
        # Step 2: Process the collected data
        logger.info("Starting data processing phase...")
        processor = HotelDataProcessor()
        processed_hotels = processor.process_all_files()
        
        logger.info(f"Pipeline completed successfully. Processed {len(processed_hotels)} hotels.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_pipeline() 