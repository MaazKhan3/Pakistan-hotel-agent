from pathlib import Path
from typing import List, Dict, Any
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HotelAgent:
    def __init__(self, data_dir: str = "../data"):
        """Initialize the hotel agent with necessary components."""
        self.data_dir = Path(data_dir)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.data_dir / "vector_store")
        )
        self.collection = self.client.get_or_create_collection(
            name="hotels",
            metadata={"hnsw:space": "cosine"}
        )
        
    def process_query(self, query: str) -> List[Dict[str, Any]]:
        """Process a natural language query about hotels."""
        # Generate query embedding
        query_embedding = self.model.encode(query).tolist()
        
        # Search the vector store
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        return self._format_results(results)
    
    def _format_results(self, results: Dict) -> List[Dict[str, Any]]:
        """Format the search results into a structured response."""
        formatted_results = []
        for i in range(len(results['ids'][0])):
            metadata = results['metadatas'][0][i]
            formatted_results.append({
                'hotel_id': results['ids'][0][i],
                'name': metadata.get('name', ''),
                'description': metadata.get('description', ''),
                'star_rating': metadata.get('star_rating'),
                'contact_info': metadata.get('contact_info', {}),
                'price_range': metadata.get('price_range', {}),
                'amenities': metadata.get('amenities', []),
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        return formatted_results
    
    def add_hotel(self, hotel_data: Dict[str, Any]) -> None:
        """Add a new hotel to the vector store."""
        # Generate embedding for hotel description
        description = f"{hotel_data['name']} {hotel_data['description']}"
        embedding = self.model.encode(description).tolist()
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            metadatas=[hotel_data],
            ids=[str(hotel_data['id'])]
        )
    
    def load_processed_data(self, file_path: str) -> None:
        """Load processed hotel data from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                hotels = json.load(f)
            
            for hotel in hotels:
                self.add_hotel(hotel)
                
            logger.info(f"Loaded {len(hotels)} hotels from {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {str(e)}")

def main():
    """Main entry point for the hotel agent."""
    agent = HotelAgent()
    
    # Example usage
    query = "Find me 3-star hotels in Skardu with Wi-Fi under PKR 5,000"
    results = agent.process_query(query)
    logger.info(f"Query results: {results}")

if __name__ == "__main__":
    main() 