# Configure sqlite as external memory for the graph
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from ecommerce_agent.nodes.nodes import (call_model, should_summarize,
                                         summarize_conversation)
from ecommerce_agent.states.default_state import State
from ecommerce_agent.tools.retrieve_catalog import retrieve_catalog

db_path = "./state_db/example.db"

def init_graph():
    conn = sqlite3.connect(db_path, check_same_thread=False)

    # Here is our checkpointer 
    memory = SqliteSaver(conn)

    tools = [retrieve_catalog]

    # Define a new graph
    workflow = StateGraph(State)
    workflow.add_node("conversation", call_model)
    workflow.add_node(summarize_conversation)
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