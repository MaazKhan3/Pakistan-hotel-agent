# Pakistan Hotel Agent

An intelligent agent for Pakistani hotel data collection and appointment scheduling.

## 🎯 Project Overview

This project implements an AI agent that:
1. Aggregates structured hotel data across Pakistan
2. Enables appointment bookings via Calendly integration
3. Answers user queries about hotels using local vector search

## 🏗️ Project Structure

```
.
├── agent/             # Core agent implementation
├── data/             # Raw and processed hotel data
├── notebooks/        # Jupyter notebooks for analysis
├── scraping/         # Web scraping scripts
├── scripts/          # Utility scripts
└── tests/            # Test files
```

## 🚀 Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 🛠️ Development

### Data Collection
- Run scraping scripts from the `scraping/` directory
- Data will be stored in `data/raw/`
- Processed data will be stored in `data/processed/`

### Running the Agent
```bash
python -m agent.main
```

### Running Tests
```bash
pytest
```

## 📝 Features

- Local vector search using FAISS/ChromaDB
- Sentence transformer embeddings
- Calendly integration for appointments
- Natural language query processing
- Comprehensive hotel data across Pakistan

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
