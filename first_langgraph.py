from typing import TypedDict
from langgraph.graph import StateGraph,END
class State(TypedDict):
    query:str
    category:str
def categorize(state:State):
    query=state["query"]
    if "internet" in query.lower():
        state["category"]="Technical"
    else:
        state["category"]="General"
    return state
workflow=StateGraph(State)
workflow.add_node("categorize",categorize)
workflow.set_entry_point("categorize")
workflow.add_edge("categorize", END)
app = workflow.compile()
result = app.invoke(
    {
        "query": "My internet is not working",
        "category": ""
    }
)
print(result)