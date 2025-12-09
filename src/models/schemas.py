from pydantic import BaseModel, Field
from typing import TypedDict, Annotated
import operator


class EvaluationSchema(BaseModel):
    """Schema for individual evaluation results"""
    feedback: str = Field(description='Detailed feedback for the essay')
    score: int = Field(description='Score out of 10', ge=0, le=10)


class UPSCState(TypedDict):
    """State schema for UPSC essay evaluation workflow"""
    essay: str
    api_key: str
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: Annotated[list[int], operator.add]
    avg_score: float


class EvaluationResult(BaseModel):
    """Final evaluation result schema"""
    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str
    overall_feedback: str
    individual_scores: list[int]
    avg_score: float
