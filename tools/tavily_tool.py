from tavily import TavilyClient

import os
import time


MAX_RESULTS = 3


client = TavilyClient(
    api_key=os.getenv(
        "TAVILY_API_KEY"
    )
)


def tavily_search(query: str):

    results = []

    try:

        print(
            f"Searching Tavily: {query}"
        )

        response = client.search(

            query=query,

            max_results=MAX_RESULTS,

            search_depth="basic",

            include_answer=False,

            include_raw_content=False
        )

        search_results = response.get(
            "results",
            []
        )

        for item in search_results:

            results.append({

                "title":
                    item.get(
                        "title",
                        "No Title"
                    ),

                "content":
                    item.get(
                        "content",
                        ""
                    )[:800],

                "url":
                    item.get(
                        "url",
                        ""
                    )
            })

        time.sleep(1)

    except Exception as e:

        print(
            f"Tavily Search Error: {e}"
        )
    # print(results)
    return results