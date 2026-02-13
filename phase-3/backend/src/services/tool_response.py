"""Base tool response structure for consistent MCP tool returns."""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class ToolResponse(BaseModel):
    """Standard response structure for all MCP tools.

    Attributes:
        status: Operation status - "success" or "error"
        message: Human-readable confirmation or error message
        data: Optional additional data (task details, list of tasks, etc.)
    """

    status: str  # "success" or "error"
    message: str
    data: Optional[Dict[str, Any]] = None

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Task created successfully",
                "data": {"task_id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }


def success_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create a success response.

    Args:
        message: Success message
        data: Optional additional data

    Returns:
        Dictionary with status, message, and data
    """
    return ToolResponse(status="success", message=message, data=data).model_dump()


def error_response(message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create an error response.

    Args:
        message: Error message
        data: Optional additional error details

    Returns:
        Dictionary with status, message, and data
    """
    return ToolResponse(status="error", message=message, data=data).model_dump()
