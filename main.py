import requests
from gpt_tools import GPTChat
from arxiv_tools import get_arxiv_papers
from pdf_tools import extract_text_from_pdf
import re
from termcolor import colored
import os

# Constants
MODEL = "gpt-4o"
MAX_RESULTS = 10
MAX_TEXT_LENGTH = 100000
NUMBER_OF_TURNS = 3
INITIAL_SEARCH_TERM = "coding ability of large language models"
PAPERS_DIR = "research_papers"

def sanitize_folder_name(name, max_length=30):
    """Sanitize folder name and limit length"""
    # Remove invalid characters and replace with underscore
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", name)
    # Replace spaces with underscores
    sanitized = sanitized.replace(" ", "_")
    # Limit length while keeping whole words
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rsplit('_', 1)[0]
    return sanitized

def create_papers_directory(search_term):
    """Create directory for papers based on search term"""
    folder_name = sanitize_folder_name(search_term)
    folder_path = os.path.join(PAPERS_DIR, folder_name)
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(colored(f"✓ Created directory: {folder_path}", "green"))
        return folder_path
    except Exception as e:
        print(colored(f"✗ Error creating directory: {str(e)}", "red"))
        raise

def download_pdf(url, filename, folder_path):
    try:
        print(colored(f"→ Downloading PDF from: {url}", "yellow"))
        response = requests.get(url)
        response.raise_for_status()
        
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(colored(f"✓ PDF downloaded successfully: {file_path}", "green"))
        return file_path
            
    except requests.exceptions.RequestException as e:
        error_msg = f"✗ Error downloading PDF: {str(e)}"
        print(colored(error_msg, "red"))
        raise

def main(search_term, chosen_paper):
    try:
        print(colored("\n=== Starting New Research Iteration ===", "cyan"))
        print(colored(f"→ Current search term: {search_term}", "yellow"))

        # Create directory for this search term
        papers_folder = create_papers_directory(search_term)

        # Initialize GPT chat model
        gpt_chooser = GPTChat(
            "You are a helpful assistant that chooses the most interesting academic paper. pick a paper which you find most useful and interesting and promising, explain briefly why(do not use any numbers in your explanation) then return the number of the paper you chose.",
            model=MODEL
        )

        # Get papers from ArXiv
        papers = get_arxiv_papers(search_term, max_results=MAX_RESULTS)
        if not papers:
            print(colored("✗ No papers found. Please try again.", "red"))
            return search_term, chosen_paper

        # Print titles and remove previously chosen paper
        for paper in papers[:]:
            if chosen_paper and chosen_paper.title == paper.title:
                papers.remove(paper)
            else:
                print(colored(f"• {paper.title}", "cyan"))

        # Get GPT's choice
        summaries = str({i: paper.summary for i, paper in enumerate(papers)})
        print(colored("\n→ Asking GPT to choose a paper...", "yellow"))
        reason_and_number = gpt_chooser.get_completion(summaries)

        # Parse the chosen paper number
        try:
            chosen_number = int(re.findall(r'\d+', reason_and_number)[0])
            chosen_paper = papers[chosen_number]
        except (IndexError, ValueError) as e:
            print(colored(f"✗ Error parsing GPT's choice: {str(e)}", "red"))
            return search_term, chosen_paper

        # Download and process the chosen paper
        valid_filename = re.sub(r'[\\/*?:"<>|]', "_", chosen_paper.title)
        pdf_file_path = download_pdf(chosen_paper.pdf_url, f"{valid_filename}.pdf", papers_folder)

        # Extract and process text
        text = extract_text_from_pdf(pdf_file_path)
        text = text[:MAX_TEXT_LENGTH]

        # Get GPT's summary
        print(colored("\n→ Getting paper summary from GPT...", "yellow"))
        gpt_summarizer = GPTChat(
            "You are a helpful assistant that summarizes academic papers. summarize the paper in a few sentences. also return a new promising search term for future research. return the search term as Search term: search term.",
            model=MODEL
        )
        summary = gpt_summarizer.get_completion(text)

        # Save summary to a text file
        summary_file = os.path.join(papers_folder, f"{valid_filename}_summary.txt")
        try:
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Paper Title: {chosen_paper.title}\n\n")
                f.write(f"Summary:\n{summary}")
            print(colored(f"✓ Summary saved to: {summary_file}", "green"))
        except Exception as e:
            print(colored(f"✗ Error saving summary: {str(e)}", "red"))

        # Extract new search term
        try:
            match = re.search(r'Search term:(.*)', summary, re.IGNORECASE)
            if match:
                search_term = match.group(1).strip().replace('"', '')
                print(colored(f"\n✓ New search term: {search_term}", "green"))
            else:
                print(colored("✗ Could not extract new search term", "red"))
        except Exception as e:
            print(colored(f"✗ Error extracting search term: {str(e)}", "red"))

        return search_term, chosen_paper

    except Exception as e:
        print(colored(f"✗ Error in main process: {str(e)}", "red"))
        return search_term, chosen_paper

if __name__ == "__main__":
    print(colored("=== GPT-4 Research Assistant ===", "cyan"))
    print(colored("→ Initializing...", "yellow"))
    
    # Create main research papers directory
    try:
        os.makedirs(PAPERS_DIR, exist_ok=True)
        print(colored(f"✓ Created main papers directory: {PAPERS_DIR}", "green"))
    except Exception as e:
        print(colored(f"✗ Error creating main directory: {str(e)}", "red"))
        raise
    
    chosen_paper = None
    search_term = INITIAL_SEARCH_TERM
    
    for i in range(NUMBER_OF_TURNS):
        print(colored(f"\n=== Research Turn {i+1}/{NUMBER_OF_TURNS} ===", "cyan"))
        search_term, chosen_paper = main(search_term, chosen_paper)