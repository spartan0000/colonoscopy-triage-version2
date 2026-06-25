from typing import List, Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class Polyp(BaseModel):
    location: Literal[
        "cecum",
        "ascending_colon",
        "hepatic_flexure",
        "transverse_colon",
        "splenic_flexure",
        "descending_colon",
        "sigmoid_colon",
        "rectum",
        "anus"
    ] | None = None
    size: Annotated[int | None, Field(ge=0)] = None # size in millimeters
    type: Literal[
        "adenoma",
        "tubulovillous_or_villous_adenoma",
        "sessile_serrated_polyp",
        "hyperplastic_polyp",
        "normal_colonic_mucosa"
    ] | None = None
    dysplasia: Literal["none", "low_grade", "high_grade"] | None = None
    resection: Literal["complete", "piecemeal", "not_resected", "unknown"] | None = None
    retrieval: Literal["complete", "incomplete", "unknown"] | None = None

class BostonBowelPrepScore(BaseModel):
    total: Annotated[int | None, Field(ge=0, le=9)] = None
    right: Annotated[int | None, Field(ge=0, le=3)] = None
    transverse: Annotated[int | None, Field(ge=0, le=3)] = None
    left: Annotated[int | None, Field(ge=0, le=3)] = None

class Colonoscopy(BaseModel):
    date: str | None = None  # YYYY-MM-DD format
    number_of_polyps: Annotated[int | None, Field(ge=0)] = None
    cecum_reached: bool | None = None
    bostonBowelPrepScore: BostonBowelPrepScore | None = None
    polyps: List[Polyp] = Field(default_factory=list)

class ColonoscopySummary(BaseModel):
    extraction_successful: bool = True
    patient_name: str | None = None
    patient_NHI: str | None = None
    patient_age: Annotated[int | None, Field(ge=0)] = None
    indication: Literal[
        "sps",
        "ibd",
        "family_history_category_1",
        "family_history_category_2",
        "family_history_category_3",
        "family_history_unknown",
        "positive_faecal_immunochemical_test",
        "anaemia",
        "rectal_bleeding",
        "change_in_bowel_habit",
        "abdominal_pain",
        "weight_loss",
        "surveillance_for_previous_polyps",
        "screening",
        "other",
        "unknown"
    ] = "unknown"
    colonoscopy: List[Colonoscopy] = Field(default_factory=list)