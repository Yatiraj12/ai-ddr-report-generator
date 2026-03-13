from pydantic import BaseModel
from typing import List


class AreaObservation(BaseModel):
    area_name: str
    observation: str
    thermal_finding: str
    images: List[str]


class DDRReport(BaseModel):
    property_issue_summary: str
    area_wise_observations: List[AreaObservation]
    probable_root_cause: str
    severity_assessment: str
    recommended_actions: str
    additional_notes: str
    missing_or_unclear_information: str