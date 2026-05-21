def semantic_search(

    vector_db,

    query,

    k=15
):

    try:

        retriever = (
            vector_db.as_retriever(

                search_type="similarity",

                search_kwargs={
                    "k": k
                }
            )
        )

        return retriever.invoke(query)

    except Exception as e:

        print(
            f"\nSemantic Search Error: "
            f"{str(e)}"
        )

        return []