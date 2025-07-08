"""Custom knowledge module for Opper AI exploration"""

from opperai import Opper
from pydantic import BaseModel
from typing import Literal
import os
import json


class SupportTicket(BaseModel):
    ticket_id: str
    issue_description: str
    issue_resolution: str
    status: Literal["open", "in_progress", "resolved", "closed"]


class SuggestResolution(BaseModel):
    thoughts: str
    message: str
    reference_ticket_ids: list[int]


def main():
    opper = Opper(http_bearer=os.getenv("OPPER_API_KEY"))

    knowledge_base_name = "Tickets"
    try:
        kb = opper.knowledge.get_by_name(knowledge_base_name=knowledge_base_name)
    except Exception:
        kb = opper.knowledge.create(name=knowledge_base_name)

    ticket = SupportTicket(
        ticket_id="123",
        issue_description="I'm having trouble accessing my account. Whenever I try to log in, I receive an error message stating that my credentials are incorrect. I have tried resetting my password multiple times, but the issue persists. Please assist in resolving this matter as soon as possible.",
        issue_resolution="The issue was resolved by verifying the user's identity and resetting the account credentials from the backend. The user was able to log in successfully after the credentials were reset.",
        status="resolved",
    )

    opper.knowledge.add(
        knowledge_base_id=kb.id,
        key=ticket.ticket_id,  # unique key, will overwrite existing data with that key
        content=ticket.model_dump_json(),
        metadata={"source": "our_ticket_system", "status": ticket.status},
    )

    # Unfiltered query results
    unfiltered = opper.knowledge.query(
        knowledge_base_id=kb.id,
        query="Can't login",
        top_k=3,
    )

    # Filtered query results
    filtered_tickets = opper.knowledge.query(
        knowledge_base_id=kb.id,
        query="Can't login",
        top_k=3,
        filters=[
            {"field": "status", "operation": "=", "value": "resolved"},
            {"field": "source", "operation": "=", "value": "our_ticket_system"},
        ],
    )

    completion = opper.call(
        name="suggest_resolution",
        instructions="Given a user question and a list of potentially relevant past tickets, provide a suggestion for a resolution to the support agent",
        input={"past_tickets": filtered_tickets, "user_issue": "Can't login"},
        output_schema=SuggestResolution,
    )

    print("Unfiltered tickets from knowledge base query:")
    print(json.dumps([r.model_dump() for r in unfiltered], indent=2))
    print("\nFiltered tickets from knowledge base query:")
    print(json.dumps([r.model_dump() for r in filtered_tickets], indent=2))
    print("\nTask completion:")
    print(json.dumps(completion.json_payload, indent=2))


if __name__ == "__main__":
    main()
