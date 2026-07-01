import random
from datetime import datetime
from typing import TypedDict
from langgraph.graph import StateGraph,END
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
class State(TypedDict):
    query: str
    history:str
    category: str
    sentiment: str
    response:str
    ticket_id:str
    timestamp:str


def categorize(state):
    prompt = f"""
    Categorize the customer query into ONLY one category:
    Technical
    Billing
    General
    Conversation History:{state["history"]}
    Current Query:{state["query"]}
    Return only the category name.
    """
    response = llm.invoke(prompt)
    state["category"] = response.content.strip() 
    return state 
def analyze_sentiment(state):
    prompt = f"""
    Analyze the sentiment of this customer query.
    Possible outputs:
    Positive
    Neutral
    Negative
    Conversation History:{state["history"]}
    Current Query:{state["query"]}
    
    Return only the sentiment.
    """
    response = llm.invoke(prompt)
    state["sentiment"] = response.content.strip()
    return state

def handle_query(state):

    prompt = f"""
    You are a customer support agent.

    Category: {state['category']}
    Conversation History:{state["history"]}
    Current Customer Query:{state["query"]}
    Rules:
    - Keep response under 40 words.
    - Be professional.
    - Be concise.

    Generate a professional support response.
    """

    response = llm.invoke(prompt)

    state["response"] = response.content

    return state


def escalate(state):

    prompt = f"""
    The customer is frustrated.

    Conversation History:{state["history"]}
    Current Query:{state["query"]}
    Rules:
    - Keep response under 40 words.
    - Apologize briefly.
    - Inform the user the issue is escalated.

    Generate a  response .
    """
    ticket = f"TKT-{random.randint(1000,9999)}"

    time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    state["ticket_id"] = ticket

    state["timestamp"] = time

    response = llm.invoke(prompt)

    state["response"] = (
        response.content
        + f"\n\n🎫 Ticket ID: {ticket}"+ f"\n🕒 Time: {time}"
    )

    return state

def route_query(state: State):

    if state["sentiment"] == "Negative":
        return "escalate"

    return "handle_query"

workflow = StateGraph(State)

workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_query", handle_query)
workflow.add_node("escalate",escalate)

workflow.set_entry_point("categorize")

workflow.add_edge("categorize", "analyze_sentiment")
workflow.add_conditional_edges(
    "analyze_sentiment",route_query,
    {
        "escalate":"escalate",
        "handle_query":"handle_query"
    }
)
workflow.add_edge("escalate",END)
workflow.add_edge("handle_query",END)

app = workflow.compile()
def run_agent(query,history):
    result = app.invoke(
        {
            "query": query,
            "history":history,
            "category": "",
            "sentiment": "",
            "response": "",
            "ticket_id": "",
            "timestamp": "",
        }
    ) 

    return result