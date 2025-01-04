# GPT-4o Research Assistant

The GPT-4o Research Assistant is a powerful tool designed to leverage GPT-4o in assisting with academic research. It searches for academic papers on ArXiv, identifies the most promising paper based on a given search term, downloads the paper, extracts its contents, and then summarizes it. The tool also suggests a new search term for subsequent research, creating an automated research exploration chain.

## Features

- **Organized Research Storage**:

  - Creates a structured `research_papers` directory
  - Organizes papers in subdirectories based on search terms
  - Saves both PDFs and their summaries in respective folders
- **ArXiv Integration**:

  - Queries the ArXiv database for academic papers
  - Supports customizable number of results (default: 10)
  - Automatically filters out previously selected papers
- **Intelligent Paper Selection**:

  - Uses GPT-4O to analyze and choose the most interesting paper
  - Provides reasoning for paper selection
  - Handles paper deduplication across iterations
- **Automated Processing**:

  - Downloads selected papers in PDF format
  - Extracts and processes text content
  - Generates concise summaries using GPT-4O
  - Suggests new research directions
- **User-Friendly Output**:

  - Colored terminal output for better readability
  - Clear progress indicators
  - Detailed error messages
  - Structured file organization

## ❤️ Support & Get 400+ AI Projects

This is one of 400+ fascinating projects in my collection! [Support me on Patreon](https://www.patreon.com/c/echohive42/membership) to get:

- 🎯 Access to 400+ AI projects (and growing daily!)
  - Including advanced projects like [2 Agent Real-time voice template with turn taking](https://www.patreon.com/posts/2-agent-real-you-118330397)
- 📥 Full source code & detailed explanations
- 📚 1000x Cursor Course
- 🎓 Live coding sessions & AMAs
- 💬 1-on-1 consultations (higher tiers)
- 🎁 Exclusive discounts on AI tools & platforms (up to $180 value)

## Directory Structure

```
research_papers/
    └── search_term_sanitized/         # First 30 chars of search term
        ├── paper_title.pdf            # Downloaded paper
        └── paper_title_summary.txt    # GPT-generated summary
```

## Setup

1. **Environment Setup**:

   ```bash
   pip install -r requirements.txt
   ```
2. **API Key Configuration**:

   - Set your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

## Usage

1. **Basic Usage**:

   ```bash
   python main.py
   ```

   - Default search term: "coding ability of large language models"
   - Default number of iterations: 3
2. **Configuration**:
   Modify the constants in `main.py` to customize:

   - `MODEL`: GPT model to use (default: "gpt-4o")
   - `MAX_RESULTS`: Number of papers to fetch (default: 10)
   - `NUMBER_OF_TURNS`: Research iterations (default: 3)
   - `INITIAL_SEARCH_TERM`: Starting search term

## Features in Detail

### Paper Selection

- Fetches papers from ArXiv based on search term
- GPT-4O analyzes paper summaries and selects the most promising one
- Provides explanation for the selection

### Paper Processing

- Downloads PDF automatically
- Extracts text content
- Generates comprehensive summary
- Saves both PDF and summary in organized folders

### Research Chain

- Analyzes paper content to suggest new research directions
- Automatically uses suggested terms for next iteration
- Maintains research continuity while exploring new areas

### Error Handling

- Robust error handling throughout the process
- Clear error messages with colored output
- Graceful failure recovery

## Limitations

- Text extraction limited to first 100,000 characters per paper
- Maximum of 10 papers retrieved per search
- Requires stable internet connection for ArXiv and API access

### [Search all my videos](https://www.echohive.live/)

### [Support my work and download source code for 100+ projects](https://www.patreon.com/echohive42)

Become a patron to access exclusive content and support ongoing projects.
