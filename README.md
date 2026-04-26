# Sales Brochure Generator

An AI-powered tool that automatically generates professional sales brochures by scraping company websites and using Large Language Models to extract and synthesize key information.

## Overview

This project streamlines the creation of sales brochures by:
1. **Web Scraping**: Crawls company websites to extract landing page content and relevant links
2. **Intelligent Link Selection**: Uses LLM to identify the most relevant pages (About, Careers, etc.)
3. **Content Generation**: Leverages AI to create polished, professional brochures in Markdown format

Perfect for sales teams, recruiters, and business development professionals who need quick, AI-generated brochures without manual content compilation.

## Features

- 🕷️ **Automatic Web Scraping**: Extracts website content with BeautifulSoup
- 🤖 **AI-Powered Link Selection**: Intelligently identifies relevant company pages using LLM
- 📝 **Dynamic Brochure Generation**: Creates professional Markdown brochures with company culture, customer info, and career details
- 🎯 **Streaming Support**: Real-time brochure generation with live updates
- 🔧 **Flexible LLM Integration**: Works with any OpenAI-compatible API (OpenAI, Ollama, LM Studio, etc.)
- 📚 **Jupyter Notebook Interface**: Easy-to-use interactive notebook for brochure generation

## Project Structure

```
sales_brochure_ai/
├── notebooks/
│   └── brochure.ipynb          # Interactive Jupyter notebook for testing
├── src/
│   └── brochure_app/
│       ├── __init__.py         # Package exports
│       ├── scraper.py          # Website scraping logic
│       └── llm.py              # LLM integration and brochure generation
├── .env.example                # Environment variables template
├── pyproject.toml              # Project configuration and dependencies
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- pip or poetry

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd sales_brochure
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -e .
   ```
   
   Or with pip install all at once:
   ```bash
   pip install openai python-dotenv beautifulsoup4 requests
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your LLM provider details:
   ```env
   OPENAI_API_KEY='your-api-key'
   OPENAI_BASE_URL='https://api.openai.com/v1'  # or your provider's URL
   MODEL='gpt-4'  # or your preferred model
   ```

## Configuration

### Environment Variables

Set up your `.env` file with the following:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for your LLM provider | `sk-...` or `ollama` |
| `OPENAI_BASE_URL` | Base URL for LLM API | `https://api.openai.com/v1` or `http://localhost:11434/v1` |
| `MODEL` | Model name to use | `gpt-4`, `gpt-3.5-turbo`, `llama3.2` |

### Using Local LLM (Ollama)

For development with free, open-source models:

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)

2. **Start Ollama server**:
   ```bash
   ollama serve
   ```

3. **Pull a model**:
   ```bash
   ollama pull llama3.2
   ```

4. **Set `.env`**:
   ```env
   OPENAI_API_KEY='ollama'
   OPENAI_BASE_URL='http://localhost:11434/v1'
   MODEL='llama3.2'
   ```

## Usage

### Via Jupyter Notebook

1. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

2. **Open** `notebooks/brochure.ipynb`

3. **Run the notebook cells**:
   
   ```python
   # Cell 1: Set up imports
   import sys
   sys.path.insert(0, "../src")
   
   import os
   from dotenv import load_dotenv
   from openai import OpenAI
   from brochure_app import Website, create_brochure
   
   load_dotenv()
   openai = OpenAI(
       base_url=os.getenv("OPENAI_BASE_URL"), 
       api_key=os.getenv("OPENAI_API_KEY")
   )
   
   # Cell 2: Create a Website object
   w = Website("https://www.example.com/", "Example Company")
   
   # Cell 3: Generate brochure
   create_brochure(openai, os.getenv("MODEL"), w)
   
   # Or stream for real-time output
   stream_brochure(openai, os.getenv("MODEL"), w)
   ```

### Via Python Script

```python
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from openai import OpenAI
from brochure_app import Website, create_brochure, stream_brochure

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create brochure for a website
website = Website("https://www.maersk.com/", "Maersk")
stream_brochure(client, os.getenv("MODEL"), website)
```

## API Reference

### `Website` Class

```python
Website(url: str, name: str = "")
```

**Parameters:**
- `url` (str): The website URL to scrape
- `name` (str): Company name (optional)

**Attributes:**
- `url`: Original URL
- `name`: Company name
- `title`: Extracted page title
- `contents`: Main page content (first 2000 characters)
- `links`: List of all links found on the page

### `create_brochure()`

```python
create_brochure(client, model: str, website: Website)
```

Generates and displays a brochure synchronously.

### `stream_brochure()`

```python
stream_brochure(client, model: str, website: Website)
```

Generates and streams brochure content in real-time (best for notebooks).

### `select_relevant_links()`

```python
select_relevant_links(client, model: str, website: Website)
```

Uses LLM to identify the most relevant links for the brochure (About, Careers, etc.).

### `fetch_page_and_all_relevant_links()`

```python
fetch_page_and_all_relevant_links(client, model: str, website: Website)
```

Fetches landing page content and identifies all relevant linked pages.

## Example Output

The brochure generator produces Markdown output including:
- Company culture and values
- Customer information
- Product/service details
- Career opportunities and job listings
- Company history and achievements

## Troubleshooting

### `ModuleNotFoundError: No module named 'brochure_app'`

**Solution**: Add src to Python path in your notebook or script:
```python
import sys
sys.path.insert(0, "../src")  # In notebooks
# or
sys.path.insert(0, str(Path(__file__).parent / "src"))  # In scripts
```

### Connection refused to LLM provider

**Solution**: Ensure your LLM server is running:
- For Ollama: `ollama serve`
- Verify `OPENAI_BASE_URL` is correct
- Check firewall/network connectivity

### Empty or low-quality brochure content

**Solution**: 
- Ensure the website has enough scannable content
- Try with a different/more capable model
- Check that `OPENAI_API_KEY` has sufficient quota

## Dependencies

- **openai**: OpenAI Python client (works with any compatible API)
- **beautifulsoup4**: HTML parsing and web scraping
- **requests**: HTTP library for fetching web pages
- **python-dotenv**: Environment variable management
