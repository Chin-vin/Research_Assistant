MAX_DOCS = 5

MAX_DOC_LENGTH = 600


def build_context(documents):

    if not documents:

        return "No documents retrieved."

    context_sections = []

    unique_contents = set()

    for idx, doc in enumerate(
        documents[:MAX_DOCS]
    ):

        content = doc.get(
            "content",
            ""
        ).strip()

        if not content:

            continue

        normalized = content[:200]

        if normalized in unique_contents:

            continue

        unique_contents.add(
            normalized
        )

        title = doc.get(
            "title",
            "Untitled"
        )

        source = doc.get(
            "url",
            "Unknown Source"
        )

        trimmed_content = content[
            :MAX_DOC_LENGTH
        ]

        section = f"""

SOURCE {idx + 1}

TITLE:
{title}

REFERENCE:
{source}

CONTENT:
{trimmed_content}

"""

        context_sections.append(
            section
        )

    final_context = "\n".join(
        context_sections
    )

    print(
        f"\nFinal Context Length: "
        f"{len(final_context)}"
    )

    return final_context