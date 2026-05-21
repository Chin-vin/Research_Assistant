import arxiv

MAX_RESULTS = 2


def search_arxiv(query: str):

    results = []

    try:

        client = arxiv.Client(
            page_size=MAX_RESULTS,
            delay_seconds=5,
            num_retries=3
        )

        search = arxiv.Search(
            query=query,
            max_results=MAX_RESULTS,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = client.results(search)

        for paper in papers:

            results.append({
                "title": paper.title,
                "content": paper.summary[:800],
                "url": paper.entry_id
            })

    except Exception as e:
        print(f"Arxiv Search Error: {e}")

    return results