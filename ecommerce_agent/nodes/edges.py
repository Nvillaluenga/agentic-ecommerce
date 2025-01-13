# TODO: move this to a edges folder
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
