"""Error response schemas."""

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response format.

    Attributes:
        detail: Error message describing what went wrong
    """

    detail: str = Field(
        ...,
        description="Error message",
        examples=["Task not found", "Invalid input"],
    )
