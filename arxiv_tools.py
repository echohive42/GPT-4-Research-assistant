import arxiv
from termcolor import colored

def get_arxiv_papers(query, max_results=10):
    try:
        print(colored(f"→ Searching arXiv for: {query}", "yellow"))
        search = arxiv.Search(
            query=query,
            max_results=max_results,
        )
        papers = list(search.results())
        
        if not papers:
            print(colored("✗ No papers found", "red"))
            return []
            
        print(colored(f"✓ Found {len(papers)} papers", "green"))
        return papers
        
    except Exception as e:
        error_msg = f"✗ Error searching arXiv: {str(e)}"
        print(colored(error_msg, "red"))
        raise