from models.llm_registry import (
    reasoning_llm
)

MAX_CONTEXT_DOCS = 10

MAX_CONTEXT_CHARS = 5000


def build_context(documents):

    if not documents:

        return "No documents retrieved."

    unique_contents = set()

    raw_context = ""

    # =====================================
    # BUILD RAW CONTEXT
    # =====================================

    for idx, doc in enumerate(
        documents[:MAX_CONTEXT_DOCS]
    ):

        content = doc.get(
            "content",
            ""
        ).strip()

        if not content:

            continue

        # ---------------------------------
        # DUPLICATE FILTER
        # ---------------------------------

        normalized = content[:300]

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

        raw_context += f"""

SOURCE_ID: {idx + 1}

TITLE:
{title}

EXACT_URL:
{source}

CONTENT:
{content}

"""

    # =====================================
    # HARD LIMIT SAFETY
    # =====================================

    raw_context = raw_context[
        :MAX_CONTEXT_CHARS
    ]

    print(
        f"\nRaw Context Length: "
        f"{len(raw_context)}"
    )

    # =====================================
    # CONTEXT COMPRESSION
    # =====================================

    try:

        compression_prompt = f"""

        You are a research context compressor.

        Compress the following retrieved
        research documents into a highly
        information-dense research context.

        CRITICAL RULES:

        1. Preserve ALL EXACT_URL values exactly.
        2. NEVER modify URLs.
        3. NEVER shorten URLs.
        4. NEVER remove SOURCE_ID fields.
        5. NEVER invent citations.
        6. NEVER rewrite references.
        7. Keep TITLE and EXACT_URL unchanged.
        8. Only compress CONTENT sections.
        9. Preserve source-to-content mapping.

        Preserve:
        - key findings
        - important entities
        - methodologies
        - technical details
        - comparisons
        - statistics
        - conclusions

        Remove:
        - redundancy
        - repeated explanations
        - filler content

        Keep the final compressed context
        under 5000 words.

        DOCUMENTS:
        {raw_context}

        """

        response = reasoning_llm.invoke(
            compression_prompt
        )

        compressed_context = (
            response.content
        )

        print(
            f"\nCompressed Context Length: "
            f"{len(compressed_context)}"
        )

        print("\n===== COMPRESSED CONTEXT =====")

        print(compressed_context)

        return compressed_context

    except Exception as e:

        print(
            f"\nContext Compression Error: "
            f"{str(e)}"
        )

        return raw_context[:6000]
# # MAX_DOCS = 5

# # MAX_DOC_LENGTH = 600


# # def build_context(documents):

# #     if not documents:

# #         return "No documents retrieved."

# #     context_sections = []

# #     unique_contents = set()

# #     for idx, doc in enumerate(
# #         documents[:MAX_DOCS]
# #     ):

# #         content = doc.get(
# #             "content",
# #             ""
# #         ).strip()

# #         if not content:

# #             continue

# #         normalized = content[:200]

# #         if normalized in unique_contents:

# #             continue

# #         unique_contents.add(
# #             normalized
# #         )

# #         title = doc.get(
# #             "title",
# #             "Untitled"
# #         )

# #         source = doc.get(
# #             "url",
# #             "Unknown Source"
# #         )

# #         trimmed_content = content[
# #             :MAX_DOC_LENGTH
# #         ]

# #         section = f"""

# # SOURCE {idx + 1}

# # TITLE:
# # {title}

# # REFERENCE:
# # {source}

# # CONTENT:
# # {trimmed_content}

# # """

# #         context_sections.append(
# #             section
# #         )

# #     final_context = "\n".join(
# #         context_sections
# #     )

# #     print(
# #         f"\nFinal Context Length: "
# #         f"{len(final_context)}"
# #     )

# #     return final_context
# from models.llm_registry import (
#     reasoning_llm
# )

# MAX_CONTEXT_DOCS = 10

# MAX_CONTEXT_CHARS = 12000


# def build_context(documents):

#     if not documents:

#         return "No documents retrieved."

#     unique_contents = set()

#     raw_context = ""

#     # =====================================
#     # BUILD RAW CONTEXT
#     # =====================================

#     for idx, doc in enumerate(
#         documents[:MAX_CONTEXT_DOCS]
#     ):

#         content = doc.get(
#             "content",
#             ""
#         ).strip()

#         if not content:

#             continue

#         # ---------------------------------
#         # DUPLICATE FILTER
#         # ---------------------------------

#         normalized = content[:300]

#         if normalized in unique_contents:

#             continue

#         unique_contents.add(
#             normalized
#         )

#         title = doc.get(
#             "title",
#             "Untitled"
#         )

#         source = doc.get(
#             "url",
#             "Unknown Source"
#         )

#         raw_context += f"""

# SOURCE {idx + 1}

# TITLE:
# {title}

# REFERENCE:
# {source}

# CONTENT:
# {content}

# """

#     # =====================================
#     # HARD LIMIT SAFETY
#     # =====================================

#     raw_context = raw_context[
#         :MAX_CONTEXT_CHARS
#     ]

#     print(
#         f"\nRaw Context Length: "
#         f"{len(raw_context)}"
#     )

#     # =====================================
#     # CONTEXT COMPRESSION
#     # =====================================

#     try:

#         compression_prompt = f"""

#         You are a research context compressor.

#         Compress the following retrieved
#         research documents into a highly
#         information-dense research context.

#         Preserve:
#         - key findings
#         - important entities
#         - methodologies
#         - technical details
#         - comparisons
#         - statistics
#         - conclusions
#         - citations/references relevance

#         Remove:
#         - redundancy
#         - repeated explanations
#         - filler content

#         Keep the final compressed context
#         under 10000 words.

#         DOCUMENTS:
#         {raw_context}

#         """

#         response = reasoning_llm.invoke(
#             compression_prompt
#         )

#         compressed_context = (
#             response.content
#         )

#         print(
#             f"\nCompressed Context Length: "
#             f"{len(compressed_context)}"
#         )

#         return compressed_context

#     except Exception as e:

#         print(
#             f"\nContext Compression Error: "
#             f"{str(e)}"
#         )

#         # ---------------------------------
#         # FALLBACK
#         # ---------------------------------

#         return raw_context[:6000]