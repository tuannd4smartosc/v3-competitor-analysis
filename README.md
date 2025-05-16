# Nike Competitor Analysis Tool

A powerful application for generating comprehensive competitor analysis reports for Nike. The tool leverages AI to research, analyze, and create detailed reports comparing Nike with its competitors across different regions and time periods.

## Features

- **AI-Powered Research**: Automatically collects and analyzes information about Nike and its competitors
- **Comprehensive Reports**: Generates detailed reports focusing on promotional campaigns, pricing, market impact, and more
- **Web Interface**: User-friendly Streamlit dashboard for easy report generation
- **PDF Export**: Automatically converts reports to PDF format
- **Email Integration**: Sends completed reports via email

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nike-ai-compe.git
   cd nike-ai-compe/v3-competitor-analysis
   ```

2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```

3. Create a `.env` file in the project root with necessary API keys and configurations.

### Running the Application

#### Command Line Interface
```bash
poetry run python main.py
```

#### Web Interface
```bash
poetry run streamlit run app.py
```

## Report Structure

Each competitor analysis report includes:

1. Regions Launched
2. Campaign URLs
3. Campaign Overviews
4. Products Promoted or Launched
5. Pricing Information
6. Key Performance Indicators (KPIs)
7. Target Audience Analysis
8. Revenue Impact
9. Market Impact
10. Key Events & Timing
11. Competitive Impact
12. Reference Links
13. Strategic Action Plan

## Project Structure

- `app.py`: Streamlit web interface
- `main.py`: Command line interface
- `manager.py`: Core research management functionality
- `_agents/`: AI agent implementations
- `reports/`: Generated report storage
- `utils.py`: Utility functions
- `email_sender.py`: Email functionality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is proprietary and confidential.

## Acknowledgments

- Built using OpenAI's agent framework
- Developed by SmartOSC for Nike
