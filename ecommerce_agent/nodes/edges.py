from typing import Literal

from ecommerce_agent.states.default_state import State


def should_summarize(state: State) -> Literal["conversation", "summarize_conversation"]:
    """Return the next node to execute."""

    messages = state["messages"]

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"

    # Otherwise we can just end
    return "conversation"


def get_tools_edge_condition(
    next_node: str,
):
    def tools_edge_condition(state: State, messages_key: str = "messages") -> Literal["tools", next_node]:
        if isinstance(state, list):
            ai_message = state[-1]
        elif isinstance(state, dict) and (messages := state.get(messages_key, [])):
            ai_message = messages[-1]
        elif messages := getattr(state, messages_key, []):
            ai_message = messages[-1]
        else:
            raise ValueError(
                f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            ai_message.tool_calls[0]
            return "tools"
        return next_node
    return tools_edge_condition
