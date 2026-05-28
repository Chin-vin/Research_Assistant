from langchain_groq import ChatGroq

import os

from dotenv import load_dotenv

from config.settings import (
    GROQ_API_KEY
)

from core.singletons import (

    get_fast_llm,

    get_reasoning_llm
)

# =====================================
# LOAD ENV
# =====================================

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

# =====================================
# MODEL NAMES
# =====================================

PRIMARY_MODEL = (
    "qwen/qwen3-32b"
)

FALLBACK_MODEL = (
    "llama-3.3-70b-versatile"
)

FAST_FALLBACK_MODEL = (
    "llama-3.1-8b-instant"
)

# =====================================
# SAFE MODEL CREATOR
# =====================================

def create_llm(

    primary_model,
    fallback_model,
    temperature=0,
    max_tokens=None
):

    try:

        print(
            f"\nUsing Primary Model: {primary_model}\n"
        )

        return ChatGroq(

            api_key=GROQ_API_KEY,

            model=primary_model,

            temperature=temperature,

            max_tokens=max_tokens,

            max_retries=2
        )

    except Exception as e:

        print(
            f"\nPrimary model failed: {e}\n"
        )

        print(
            f"\nSwitching to fallback model: {fallback_model}\n"
        )

        return ChatGroq(

            api_key=GROQ_API_KEY,

            model=fallback_model,

            temperature=temperature,

            max_tokens=max_tokens,

            max_retries=2
        )

# =====================================
# FAST TASKS
# Router
# Decomposition
# Validation
# =====================================

try:

    fast_llm = get_fast_llm()

except Exception as e:

    print(
        f"\nSingleton fast model failed: {e}\n"
    )

    fast_llm = ChatGroq(

        api_key=GROQ_API_KEY,

        model=FAST_FALLBACK_MODEL,

        temperature=0,

        max_retries=2
    )

# =====================================
# REASONING MODEL
# =====================================

try:

    reasoning_llm = get_reasoning_llm()

except Exception as e:

    print(
        f"\nSingleton reasoning model failed: {e}\n"
    )

    reasoning_llm = ChatGroq(

        api_key=GROQ_API_KEY,

        model=FALLBACK_MODEL,

        temperature=0.1,

        max_retries=2
    )

# =====================================
# REPORT GENERATION
# =====================================

report_llm = create_llm(

    primary_model=PRIMARY_MODEL,

    fallback_model=FALLBACK_MODEL,

    temperature=0.2,

    max_tokens=4000
)

# =====================================
# VALIDATION
# =====================================

validator_llm = create_llm(

    primary_model=PRIMARY_MODEL,

    fallback_model=FALLBACK_MODEL,

    temperature=0
)

# =====================================
# SUMMARIZATION
# =====================================

summary_llm = create_llm(

    primary_model=PRIMARY_MODEL,

    fallback_model=FALLBACK_MODEL,

    temperature=0
)