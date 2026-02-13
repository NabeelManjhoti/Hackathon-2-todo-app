"""Agent runner for OpenAI chatbot with MCP tool integration."""

import json
from typing import Any, Dict, List

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.services.agent_config import get_system_prompt
from src.services.mcp_tools import add_task, list_tasks, complete_task
from src.utils.retry import retry_with_backoff
from src.utils.timeout import with_timeout
from src.logger import structured_logger


# Initialize OpenAI client
openai_client = AsyncOpenAI(api_key=settings.openai_api_key)


# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID (UUID)",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title",
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description",
                    },
                },
                "required": ["user_id", "title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID (UUID)",
                    },
                    "status_filter": {
                        "type": "string",
                        "enum": ["all", "active", "completed"],
                        "description": "Filter tasks by status",
                    },
                },
                "required": ["user_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID (UUID)",
                    },
                    "task_id": {
                        "type": "string",
                        "description": "Task ID (UUID)",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        },
    },
]


async def execute_tool_call(
    session: AsyncSession,
    tool_name: str,
    tool_args: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute a tool call and return the result.

    Args:
        session: Database session
        tool_name: Name of the tool to execute
        tool_args: Arguments for the tool

    Returns:
        Tool execution result
    """
    try:
        if tool_name == "add_task":
            return await add_task(
                session=session,
                user_id=tool_args.get("user_id"),
                title=tool_args.get("title"),
                description=tool_args.get("description", "")
            )
        elif tool_name == "list_tasks":
            return await list_tasks(
                session=session,
                user_id=tool_args.get("user_id"),
                status_filter=tool_args.get("status_filter", "all")
            )
        elif tool_name == "complete_task":
            return await complete_task(
                session=session,
                user_id=tool_args.get("user_id"),
                task_id=tool_args.get("task_id")
            )
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}",
                "data": None
            }
    except Exception as e:
        structured_logger.log("ERROR", f"Tool execution failed: {tool_name}", error=str(e))
        return {
            "status": "error",
            "message": f"Tool execution failed: {str(e)}",
            "data": None
        }


@retry_with_backoff(max_attempts=3)
async def call_openai_agent(
    messages: List[Dict[str, Any]],
    tools: List[Dict[str, Any]]
) -> Any:
    """Call OpenAI API with retry logic.

    Args:
        messages: Conversation messages
        tools: Tool definitions

    Returns:
        OpenAI API response
    """
    response = await openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.7,
        max_tokens=1000,
    )
    return response


async def run_agent(
    session: AsyncSession,
    user_id: str,
    conversation_history: List[Dict[str, Any]],
    user_message: str
) -> Dict[str, Any]:
    """Run the OpenAI agent with conversation history and user message.

    Args:
        session: Database session
        user_id: User ID
        conversation_history: Previous messages in OpenAI format
        user_message: New user message

    Returns:
        Dictionary with response text and tool_calls
    """
    try:
        # Build messages list
        messages = [
            {"role": "system", "content": get_system_prompt()},
            *conversation_history,
            {"role": "user", "content": user_message}
        ]

        # Call OpenAI API with timeout
        response = await with_timeout(
            call_openai_agent(messages, TOOL_DEFINITIONS),
            timeout_seconds=float(settings.chat_timeout_seconds),
            error_message="AI service timeout"
        )

        # Extract response
        assistant_message = response.choices[0].message
        response_text = assistant_message.content or ""
        tool_calls_data = []

        # Process tool calls if present
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Execute tool
                tool_result = await execute_tool_call(session, tool_name, tool_args)

                # Record tool call
                tool_calls_data.append({
                    "tool_name": tool_name,
                    "parameters": tool_args,
                    "result": tool_result,
                    "status": tool_result.get("status", "error")
                })

                structured_logger.log(
                    "INFO",
                    f"Tool executed: {tool_name}",
                    user_id=user_id,
                    status=tool_result.get("status")
                )

        return {
            "response": response_text,
            "tool_calls": tool_calls_data if tool_calls_data else None
        }

    except Exception as e:
        structured_logger.log("ERROR", "Agent execution failed", error=str(e))
        raise
