import operator
from typing import Annotated, TypedDict, List, Dict, Any

class AgentState(TypedDict):
    thread_id :str
    query: str

    subqueries: List[str]

    retrieved_docs: Annotated[
        List[Dict[str, Any]],
        operator.add
    ]

    analysis: Dict[str,Any]

    validation: Dict[str, Any]

    report: Dict[str,Any]

    citations: List[Dict[str, str]]

    errors: Annotated[
        List[str],
        operator.add
    ]

    retries: Dict[str, int]

    workflow_complete: bool

    next_agent: str

    vector_db: Any
    routing: Dict[str, str]
    human_feedback: str
    validator_feedback: str
    awaiting_human_approval: bool
    section_operation: Dict[str, Any]
    previous_report: Dict[str, Any]

    previous_analysis: Dict[str, Any]