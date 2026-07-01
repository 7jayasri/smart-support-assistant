import json
import os
from utils.helpers import generate_ticket, current_time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILE_PATH = os.path.join(BASE_DIR, "data", "tickets.json")



def update_existing_ticket(ticket):

    time = current_time()

    return ticket, time

def load_tickets():

    if not os.path.exists(FILE_PATH):

        return []

    with open(FILE_PATH, "r") as file:

        return json.load(file)

def save_tickets(tickets):

    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w") as file:
        json.dump(
            tickets,
            file,
            indent=4
        )

def create_new_ticket(category):

    tickets = load_tickets()

    ticket = generate_ticket()

    time = current_time()

    ticket_data = {

        "ticket_id": ticket,

        "category": category,

        "status": "Open",

        "created_at": time

    }

    tickets.append(ticket_data)

    save_tickets(tickets)

    return ticket, time