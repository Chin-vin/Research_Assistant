def build_citation_map(documents):

    citations = []

    for idx, doc in enumerate(documents):

        citations.append({

            "source_id":
                idx + 1,

            "title":
                doc.get(
                    "title",
                    ""
                ),

            "url":
                doc.get(
                    "url",
                    ""
                )
        })

    return citations