import requests
from gpt_tools import GPTChat
from arxiv_tools import get_arxiv_papers
from pdf_tools import extract_text_from_pdf
import re

def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

model = "gpt-4"

def main(search_term, chosen_paper):

    # Initialize GPT-3 chat model
    gpt_chooser = GPTChat("You are a helpful assistant that chooses the most interesting academic paper. pick a paper which you find most useful and interesting and promising, explain briefly why(do not use any numbers in your explanation) then return the number of the paper you chose.", model=model)
    # print(gpt_chooser.messages)

    # Get papers from ArXiv
    papers = list(get_arxiv_papers(search_term, max_results=10))
    if papers == []:
        print("No papers found. please try again.")
        exit()

    # print titles of papers
    # print(len(papers))  
    for paper in papers:            
        if chosen_paper and chosen_paper.title == paper.title:
            papers.remove(paper)
        else:
            print(paper.title) #pdf.summary #pdf.pdf_url

    # turn the summaries into a dictionary with numbers as the keys
    summaries = str({i: paper.summary for i, paper in enumerate(papers)})
    print("\n")
    reason_and_number = gpt_chooser.get_gpt3_response(summaries)

    # parse the number by finding a number in the response just in case gpt returns more than just the number
    chosen_number = re.findall(r'\d+', reason_and_number)[0]

    # do list comprehension to find the paper with the chosen number
    chosen_paper = papers[int(chosen_number)]

    # Download the chosen paper and save it
    valid_filename = re.sub(r'[\\/*?:"<>|]', "_", chosen_paper.title)
    pdf_file_path = f"{valid_filename}.pdf"
    download_pdf(chosen_paper.pdf_url, pdf_file_path)

    # Extract text from the paper
    text = extract_text_from_pdf(pdf_file_path)
    # get the first 20000 characters of the paper
    text = text[:20000]

    # Get GPT-3's summary of the paper
    print("\n\n")
    gpt_summarizer = GPTChat("You are a helpful assistant that summarizes academic papers. summarize the paper in a few sentences. also return a new promising search term for future research. return the search term as Search term: search term.", model=model)
    summary = gpt_summarizer.get_gpt3_response(text)

    try:
        match = re.search(r'Search term:(.*)', summary)
        if match:
            search_term = match.group(1)
    except:
        match = re.search(r'search term:(.*)', summary)
        if match:
            search_term = match.group(1)
    
    # remove any quote marks from the search term
    search_term = search_term.replace('"', '')


    # print(f"summary of {chosen_paper.title}: {summary}")

    return search_term, chosen_paper

if __name__ == "__main__":

    number_of_turns_for_research = 3
    chosen_paper = None
    search_term = "coding ability of large language models"
    for i in range(number_of_turns_for_research):
        search_term, chosen_paper = main(search_term, chosen_paper)