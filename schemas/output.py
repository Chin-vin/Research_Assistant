from pydantic import BaseModel
from typing import List

class Citation(BaseModel):

    title: str

    url: str

from pydantic import (
    BaseModel,
    Field
)

from typing import List


class ValidationIssues(
    BaseModel
):

    missing_information: List[str] = Field(
        default_factory=list
    )

    unsupported_claims: List[str] = Field(
        default_factory=list
    )

    weak_sections: List[str] = Field(
        default_factory=list
    )


class RefinementPlan(
    BaseModel
):

    needs_refinement: bool = False

    refinement_type: str = ""

    refinement_focus: List[str] = Field(
        default_factory=list
    )

    feedback_for_retry: str = ""


class ValidationOutput(
    BaseModel
):

    research_sufficient: bool

    confidence_score: float

    issues: ValidationIssues = Field(
        default_factory=ValidationIssues
    )

    refinement: RefinementPlan = Field(
        default_factory=RefinementPlan
    )

    validation_summary: str = ""

class ReportOutput(BaseModel):

    title: str

    executive_summary: str

    findings: List[str]

    conclusion: str


from pydantic import BaseModel
from typing import List


from pydantic import BaseModel, Field
from typing import List


class DecompositionOutput(BaseModel):

    subqueries: List[str] = Field(
        description=(
            "List of concise search-friendly "
            "research subqueries"
        )
    )

class RetrievedDocument(BaseModel):

    title: str

    content: str

    url: str


class RetrievalOutput(BaseModel):

    documents: List[RetrievedDocument]

class DynamicSection(BaseModel):

    heading: str

    content: str

    citations: List[str] = Field(
        default_factory=list
    )


class AnalysisOutput(BaseModel):

    summary: str = ""

    confidence_score: float = 0.0

    key_findings: List[str] = Field(
        default_factory=list
    )

    dynamic_sections: List[
        DynamicSection
    ] = Field(
        default_factory=list
    )
    
from typing import (
    List,
    Optional
)

from pydantic import (
    BaseModel,
    Field
)

from pydantic import (
    BaseModel,
    Field
)

from typing import List


from pydantic import (
    BaseModel,
    Field
)

from typing import (
    List
)



# -----------------------------------
# DYNAMIC SECTION
# -----------------------------------

class ReportSection(BaseModel):

    heading: str

    content: str

    citations: List[str] = Field(
        default_factory=list
    )

# -----------------------------------
# MAIN REPORT
# -----------------------------------

class ReportOutput(BaseModel):

    # --------------------------------
    # FIXED ACADEMIC SECTIONS
    # --------------------------------

    title: str = ""

    abstract: str = ""

    keywords: List[str] = Field(
        default_factory=list
    )

    introduction: str = ""

    methodology: str = ""

    conclusion: str = ""

    references: List[str] = Field(
        default_factory=list
    )

    # --------------------------------
    # QUERY-ADAPTIVE SECTIONS
    # --------------------------------

    dynamic_sections: List[
        ReportSection
    ] = Field(
        default_factory=list
    )
class RoutingOutput(BaseModel):

    retrieval_mode: str


from pydantic import (
    BaseModel
)

from typing import Literal


class HumanIntentOutput(

    BaseModel
):

    target_agent: Literal[

        "decomposer",

        "router",

        "pdf_retriever",

        "analyzer",

        "validator",

        "reporter"
    ]

    reasoning: str