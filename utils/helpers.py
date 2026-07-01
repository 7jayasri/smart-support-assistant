import random
from datetime import datetime


def generate_ticket():
    return f"TKT-{random.randint(1000,9999)}"


def current_time():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")


def ask_llm(llm, prompt):

    response = llm.invoke(prompt)

    return response.content.strip()


def generate_response_with_ticket(response, ticket, time):

    return (
        response
        + f"\n\n🎫 Ticket ID: {ticket}"
        + f"\n🕒 Time: {time}"
    )