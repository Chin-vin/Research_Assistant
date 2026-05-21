def is_valid_query(query: str):

    invalid_patterns = [

        "Here are",

        "Subtopics",

        "```",

        "[",
        "]",

        "{",
        "}",

        ":"
    ]

    if len(query.strip()) < 5:
        return False

    for pattern in invalid_patterns:

        if pattern in query:
            return False

    return True