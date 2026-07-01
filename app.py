import streamlit as st
## from support_agent_v1 import run_agent
from support_agent_v2 import run_agent
import time
st.set_page_config(
    page_title="Smart Support Assistant",
    page_icon="🤖"
)
with st.sidebar:

    st.title("🤖 Smart Support")

    st.markdown("---")

    st.success("🟢 Online")

    st.write("### AI Model")
    st.info("Llama 3.1")

    st.write("### Framework")
    st.info("LangGraph")

    st.write("### Provider")
    st.info("Groq")

    if "current_ticket" not in st.session_state:

        st.session_state.current_ticket = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []
        

    st.metric(
        "Conversation",
        len(st.session_state.messages)
    )
    st.markdown("---")

    st.subheader("Current Ticket")

    if st.session_state.current_ticket:

        st.success(st.session_state.current_ticket)

    else:

        st.info("No Active Ticket")

    
    st.markdown("---")

    if st.button("🗑️ New Chat"):

        st.session_state.messages = []
        st.session_state.current_ticket=""
        st.rerun()



st.title("🤖 Smart Support Assistant")
st.caption("AI-powered Customer Support using LangGraph + Groq")

def get_chat_history():

    lines = []

    for message in st.session_state.messages:

        role = message["role"].capitalize()

        content = message["content"]

        lines.append(f"{role}: {content}")

    return "\n".join(lines)



# ---------- Display Old Messages ----------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Chat Input ----------

query = st.chat_input("Describe your issue...")

if query:

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(query)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Generate response
    with st.spinner("🤖 Thinking...."):
        time.sleep(1)
        history = get_chat_history()

        result = run_agent(query,history,st.session_state.current_ticket)
        if result["ticket_id"]:
            st.session_state.current_ticket = result["ticket_id"]

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(result["response"])
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.success(f"📂 {result['category']}")

        with col2:
            st.info(f"😊 {result['sentiment']}")
        if result["ticket_id"]:

            st.warning(f"🎫 Ticket ID: {result['ticket_id']}")

            st.caption(f"🕒 {result['timestamp']}")

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["response"]
        }
    )