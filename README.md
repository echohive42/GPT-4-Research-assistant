
# GPT-4 Research Assistant

The GPT-4 Research Assistant is a tool designed to leverage the power of GPT-4 in assisting with academic research. It searches for academic papers on ArXiv, identifies the most promising paper based on a given search term, downloads the paper, extracts its contents, and then summarizes it. The tool also suggests a new search term for subsequent research.

## Features:
- **Search ArXiv Papers**: Queries the ArXiv database for academic papers based on a given search term.
- **Paper Selection**: Utilizes GPT-4 to choose the most interesting and promising paper from the search results.
- **PDF Download**: Downloads the selected paper in PDF format.
- **Content Extraction**: Extracts text from the downloaded PDF paper.
- **Paper Summary**: Summarizes the paper using GPT-4 and suggests a new search term for future research.

## How to Use:

1. **Setup**:
    - Ensure you have the required libraries installed (`requests`, and any other necessary libraries).
    - Setup the required API keys and configurations for GPT-4.

2. **Running the Tool**:
    - Set the initial search term (default is "coding ability of large language models").
    - Determine how many turns or iterations you'd like the tool to perform (default is 3).
    - Run the script.
    
3. **Output**:
    - The tool will print the title of the selected paper and its summary.
    - A new search term will be suggested for the next iteration.

## Limitations:
- The tool is currently set to retrieve a maximum of 10 papers from ArXiv per search.
- The content extraction is limited to the first 20,000 characters of the paper.
- The tool depends on external libraries and tools which need to be set up correctly.

## Future Work:
- Integration with other academic paper databases.
- Enhancements to the summarization process for more nuanced summaries.
- Additional features such as citation extraction and analysis.
