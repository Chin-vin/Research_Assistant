# from langchain_groq import ChatGroq

# import os

# from dotenv import load_dotenv

# load_dotenv()

# # -----------------------------------
# # API KEY
# # -----------------------------------

# GROQ_API_KEY = os.getenv(
#     "GROQ_API_KEY"
# )

# # -----------------------------------
# # FAST TASKS
# # Router
# # Decomposition
# # Validation
# # Summarization
# # -----------------------------------

# fast_llm = ChatGroq(

#     api_key=GROQ_API_KEY,

#     model="meta-llama/"
#         "llama-4-scout-17b-16e-instruct",

#     temperature=0,

#     max_retries=2
# )

# # -----------------------------------
# # DEEP ANALYSIS
# # -----------------------------------

# reasoning_llm = ChatGroq(

#     api_key=GROQ_API_KEY,

#     model="meta-llama/"
#         "llama-4-scout-17b-16e-instruct",

#     temperature=0.1,

#     max_retries=2
# )

# # -----------------------------------
# # REPORT GENERATION
# # -----------------------------------

# report_llm = ChatGroq(

#     api_key=GROQ_API_KEY,

#     model="meta-llama/"
#         "llama-4-scout-17b-16e-instruct",

#     temperature=0.2,

#     max_tokens=4000,

#     max_retries=2
# )

# # -----------------------------------
# # VALIDATION
# # -----------------------------------

# validator_llm = ChatGroq(

#     api_key=GROQ_API_KEY,

#     model="meta-llama/"
#         "llama-4-scout-17b-16e-instruct",

#     temperature=0,

#     max_retries=2
# )

# # -----------------------------------
# # SUMMARIZATION
# # -----------------------------------

# summary_llm = ChatGroq(

#     api_key=GROQ_API_KEY,

#     model="meta-llama/"
#         "llama-4-scout-17b-16e-instruct",

#     temperature=0,

#     max_retries=2
# ) 
from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY
)
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv(GROQ_API_KEY)
from core.singletons import (

    get_fast_llm,

    get_reasoning_llm
)

fast_llm = get_fast_llm()

reasoning_llm = get_reasoning_llm()
# Report generation model
report_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

# Validation model
validator_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Summarization model
summary_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)