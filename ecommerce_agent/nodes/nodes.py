import json

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.store.base import BaseStore

from ecommerce_agent.states.default_state import State


def call_model(model: BaseChatModel, state: State, config: RunnableConfig, store: BaseStore):
    # Chatbot instruction for choosing what to update and what tools to call
    MODEL_SYSTEM_MESSAGE = """You are a helpful chatbot. 

You are designed to be a shooping assistant, helping user to find what they want.

You have a long term memory which keeps track of the user's profile (general information about them), you also have access to a catalog of products that you can offer the client

Here is the current User Profile (may be empty if no information has been collected yet):
<user_profile>
{user_profile}
</user_profile>

Here is the current catalog of products (may be empty if you didn't retrieved it yet):
<product_catalog>
{product_catalog}
</product_catalog>

Here is the summary of the current conversation (may be empty if the conversation is not long enough yet):
<summary>
{summary}
</summary>


Here are your instructions for reasoning about the user's messages:

1. Reason carefully about the user's messages as presented below. 

2. If the catalog is not present and the user is interested in buying or looking for a specific product, get the catalog by calling the NextStepTool tool with the type `retrieve_catalog`

3. Always try to be consice and present products to the client to see if he is interested in some of them

4. Respond naturally to user user after a tool call was made, or if no tool call was made."""

    messages = state["messages"]

    # Get summary if it exists
    summary = state.get("summary", None)
    # Get catalog if exists
    catalog = state.get("catalog", None)
    product_catalog = json.dumps(catalog) if catalog else None

    # Get the user ID from the config
    user_id = config["configurable"]["user_id"]

    # Retrieve existing memory from the store
    namespace = ("user_profile", user_id)
    existing_memory = store.get(namespace, "user_memory")

    # Format the memories for the system prompt
    if existing_memory and existing_memory.value:
        memory_dict = existing_memory.value
        formatted_memory = json.dumps(memory_dict.json())
    else:
        formatted_memory = None

    system_message = MODEL_SYSTEM_MESSAGE.format(
        user_profile=formatted_memory, product_catalog=product_catalog, summary=summary)

    print(system_message)
    messages = [SystemMessage(content=system_message)] + messages
    response = model.invoke(messages)
    return {"messages": response}


def summarize_conversation(model: BaseChatModel, state: State):
    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt
    if summary:

        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )

    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}
