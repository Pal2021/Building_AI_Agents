# JobHuntAgents

## Overview
JobHuntAgents is a Python-based application designed to facilitate job searches using various AI-powered search providers. The application is modular, allowing for easy integration of new search providers and services.

## Project Structure
```
JobHuntAgents
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── providers
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── duckduckgo.py
│   │   ├── tavily.py
│   │   └── exa.py
│   └── services
│       ├── __init__.py
│       └── search_service.py
├── .env.example
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd JobHuntAgents
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables by copying `.env.example` to `.env` and filling in the necessary API keys.

## Usage
1. Run the application:
   ```
   python app/main.py
   ```

2. Follow the prompts to enter your search queries.

## Providers
The application currently supports the following search providers:
- **DuckDuckGo**: Uses the DuckDuckGo API for search results.
- **Tavily**: Integrates with the Tavily AI API for optimized search results.
- **Exa**: Utilizes the Exa AI API for semantic search capabilities.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.