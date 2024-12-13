from langgraph.graph import MessagesState

class State(MessagesState):
    summary: str
    catalog: str