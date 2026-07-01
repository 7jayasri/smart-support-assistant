CATEGORY_PROMPT = """
Categorize the customer query into ONLY one category.

Categories:
- Technical
- Billing
- General

Conversation History:
{history}

Current Query:
{query}

Return ONLY the category.
"""


SENTIMENT_PROMPT = """
Analyze the customer's sentiment.

Conversation History:
{history}

Current Query:
{query}

Possible outputs:
- Positive
- Neutral
- Negative

Return ONLY the sentiment.
"""


HANDLE_QUERY_PROMPT = """
You are a professional customer support agent.

Category:
{category}

Conversation History:
{history}

Current Customer Query:
{query}

Rules:
- Keep the response under 50 words.
- Be polite.
- Be concise.
- Provide a helpful solution whenever possible.

Generate ONLY the response.
"""


CREATE_TICKET_PROMPT = """
You are a customer support agent.

The customer is frustrated and requires human assistance.

Conversation History:
{history}

Current Query:
{query}

Rules:
- Apologize briefly.
- Inform the customer that the issue has been escalated.
- Keep the response under 50 words.

Generate ONLY the response.
"""


UPDATE_TICKET_PROMPT = """
You are a customer support agent.

Existing Ticket:
{ticket}

Conversation History:
{history}

Latest Customer Message:
{query}

Rules:
- Thank the customer.
- Inform them that their existing ticket has been updated.
- Keep the response under 50 words.

Generate ONLY the response.
"""