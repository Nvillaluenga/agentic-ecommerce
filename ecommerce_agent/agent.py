# Configure sqlite as external memory for the graph
import sqlite3
from functools import partial

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.store.memory import InMemoryStore

from ecommerce_agent.nodes.edges import (get_tools_edge_condition,
                                         should_summarize)
from ecommerce_agent.nodes.memory_node import write_memory
from ecommerce_agent.nodes.nodes import call_model, summarize_conversation
from ecommerce_agent.states.default_state import State

db_path = "./state_db/example.db"


def init_graph(model: BaseChatModel, tools: list):
    conn = sqlite3.connect(db_path, check_same_thread=False)

    # Change to a real DB
    across_thread_memory = InMemoryStore()

    # Here is our checkpointer
    memory = SqliteSaver(conn)

    # Define a new graph
    workflow = StateGraph(State)

    llm_with_tools = model.bind_tools(tools, parallel_tool_calls=False)
    call_llm_with_model = partial(call_model, llm_with_tools)

    workflow.add_node("conversation", call_llm_with_model)

    summarize_conversation_with_model = partial(summarize_conversation, model)
    write_memory_with_model = partial(write_memory, model)

    workflow.add_node("summarize_conversation",
                      summarize_conversation_with_model)
    workflow.add_node("tools", ToolNode(tools))
    workflow.add_node("write_memory", write_memory_with_model)

    # Set the entrypoint as conversation
    workflow.add_conditional_edges(
        START,
        should_summarize,
    )
    workflow.add_edge("summarize_conversation", "conversation")
    tools_condition = get_tools_edge_condition("write_memory")
    workflow.add_conditional_edges(
        "conversation",
        tools_condition,
    )
    workflow.add_edge("tools", "conversation")

    workflow.add_edge("write_memory", END)
    # Compile
    graph = workflow.compile(checkpointer=memory, store=across_thread_memory)
    return graph
