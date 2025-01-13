# Configure sqlite as external memory for the graph
import sqlite3
from functools import partial

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ecommerce_agent.nodes.edges import should_summarize
from ecommerce_agent.nodes.nodes import call_model, summarize_conversation
from ecommerce_agent.states.default_state import State

db_path = "./state_db/example.db"


def init_graph(model: BaseChatModel, tools: list):
    conn = sqlite3.connect(db_path, check_same_thread=False)

    # Here is our checkpointer
    memory = SqliteSaver(conn)

    # Define a new graph
    workflow = StateGraph(State)

    llm_with_tools = model.bind_tools(tools, parallel_tool_calls=False)
    call_llm_with_model = partial(call_model, llm_with_tools)

    workflow.add_node("conversation", call_llm_with_model)

    summarize_conversation_with_model = partial(summarize_conversation, model)

    workflow.add_node("summarize_conversation",
                      summarize_conversation_with_model)
    workflow.add_node("tools", ToolNode(tools))

    # Set the entrypoint as conversation
    workflow.add_conditional_edges(
        START,
        should_summarize,
    )
    workflow.add_edge("summarize_conversation", "conversation")
    workflow.add_conditional_edges(
        "conversation",
        tools_condition,
    )
    workflow.add_edge("tools", "conversation")

    # Compile
    graph = workflow.compile(checkpointer=memory)
    return graph
