from pydantic import BaseModel, Field


class TicketAnalysis(BaseModel):
    category: str = Field(
        description="The category of the customer issue"
    )

    priority: str = Field(
        description="The priority: low, medium, or high"
    )

    summary: str = Field(
        description="A short summary of the issue"
    )

    sentiment: str = Field(
        description="The customer's sentiment"
    )