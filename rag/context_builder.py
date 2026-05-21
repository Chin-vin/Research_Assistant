def build_rag_context(

    documents,

    max_chars=12000
):

    context = ""

    total = 0

    for idx, doc in enumerate(documents):

        chunk = f"""

SOURCE ID: {idx + 1}

TITLE:
{doc.get('title')}

URL:
{doc.get('url')}

CONTENT:
{doc.get('content')}
"""

        if total + len(chunk) > max_chars:

            break

        context += chunk

        total += len(chunk)

    return context