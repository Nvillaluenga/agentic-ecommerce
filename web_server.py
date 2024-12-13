from fastapi import FastAPI, HTTPException, Request
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from ecommerce_agent.agent import init_graph

app = FastAPI()

# Initialize the graph at startup
graph = init_graph()

class GraphRequest(BaseModel):
    messages: list
    config: dict

@app.post("/invoke")
async def invoke_graph(request: GraphRequest):
    try:
        response = graph.invoke({"messages": request.messages}, request.config)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os

    import uvicorn
    port =  os.environ["PORT"]
    uvicorn.run(app, host="0.0.0.0", port=port)