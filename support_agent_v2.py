import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from services.ticket_service import (create_new_ticket,update_existing_ticket)
from utils.helpers import (ask_llm,generate_response_with_ticket)
from utils.prompts import CATEGORY_PROMPT,SENTIMENT_PROMPT,HANDLE_QUERY_PROMPT,CREATE_TICKET_PROMPT,UPDATE_TICKET_PROMPT
load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
class State(TypedDict):

    query: str

    history: str

    category: str

    sentiment: str

    response: str

    ticket_id: str

    timestamp: str

    current_ticket: str
def categorize(state: State):

    prompt = CATEGORY_PROMPT.format(

        history=state["history"],

        query=state["query"]

    )

    state["category"] = ask_llm(llm, prompt)

    return state
def analyze_sentiment(state: State):

    prompt = SENTIMENT_PROMPT.format(

        history=state["history"],

        query=state["query"]

    )

    state["sentiment"] = ask_llm(llm, prompt)

    return state

def handle_query(state: State):

    prompt = HANDLE_QUERY_PROMPT.format(
        category=state["category"],
        history=state["history"],
        query=state["query"]
    )

    state["response"] = ask_llm(llm, prompt)

    return state
def handle_query(state: State):

    prompt = HANDLE_QUERY_PROMPT.format(
        category=state["category"],
        history=state["history"],
        query=state["query"]
    )

    state["response"] = ask_llm(llm, prompt)

    return state
def create_ticket(state: State):

    ticket, time = create_new_ticket(
        state["category"]
    )

    prompt = CREATE_TICKET_PROMPT.format(
        history=state["history"],
        query=state["query"]
    )

    response = ask_llm(llm, prompt)

    state["ticket_id"] = ticket
    state["timestamp"] = time

    state["response"] = generate_response_with_ticket(
        response,
        ticket,
        time
    )

    return state
def update_ticket(state: State):
    ticket, time = update_existing_ticket(
    state["current_ticket"]
    )

    

    prompt = UPDATE_TICKET_PROMPT.format(
        ticket=state["current_ticket"],
        history=state["history"],
        query=state["query"]
    )

    response = ask_llm(llm, prompt)

    state["ticket_id"] = ticket

    state["timestamp"] = time

    state["response"] = generate_response_with_ticket(
        response,
        ticket,
        time
    )

    return state
def decide_action(state: State):

    if state["sentiment"] != "Negative":
        return "handle_query"

    if state["current_ticket"] == "":
        return "create_ticket"

    return "update_ticket"
workflow = StateGraph(State)

workflow.add_node("categorize", categorize)
workflow.add_node("analyze_sentiment", analyze_sentiment)
workflow.add_node("handle_query", handle_query)
workflow.add_node("create_ticket", create_ticket)
workflow.add_node("update_ticket", update_ticket)
workflow.set_entry_point("categorize")
workflow.add_edge(
    "categorize",
    "analyze_sentiment"
)
workflow.add_conditional_edges(
    "analyze_sentiment",
    decide_action,
    {
        "handle_query": "handle_query",
        "create_ticket": "create_ticket",
        "update_ticket": "update_ticket"
    }
)
workflow.add_edge("handle_query", END)
workflow.add_edge("create_ticket", END)
workflow.add_edge("update_ticket", END)
app = workflow.compile()

def run_agent(query, history="", current_ticket=""):

    result = app.invoke(
        {
            "query": query,
            "history": history,
            "category": "",
            "sentiment": "",
            "response": "",
            "ticket_id": "",
            "timestamp": "",
            "current_ticket": current_ticket
        }
    )

    return result