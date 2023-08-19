import arxiv

def get_arxiv_papers(query, max_results=10):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
    )
    papers = search.get()
    return papers