
import streamlit as st
from agent import run_agent, proactive
from langchain_core.messages import ToolMessage, AIMessage

st.set_page_config(page_title="AIFS – AI Fashion Stylist", page_icon="🧥")

st.title("🧥 AI Fashion Stylist (AIFS)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input for user message
if user_input := st.chat_input("What are you looking for today?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display agent response
    with st.chat_message("assistant"):
        with st.status("🧠 AIFS is thinking...", state="running") as status:
            response = run_agent(user_input)

            # Extract final message content
            final_msg = response["messages"][-1].content

            # Detect tool usage
            used_tools = set()

            for msg in response["messages"]:
                if isinstance(msg, AIMessage):
                    for call in msg.tool_calls or []:
                        used_tools.add(call.get("name", "Unknown Tool"))

            for tool_name in used_tools:
                status.write(f"🔧 Tool used: `{tool_name}`", state="running")

            status.update(label="✅ AIFS has responded", state="complete")

        # Show final assistant reply
        st.session_state.messages.append({"role": "assistant", "content": final_msg})
        st.markdown(final_msg)

with st.sidebar:
    st.header("👩‍💼 Admin Panel")
    admin_input = st.text_area("Proactive Prompt", placeholder="e.g. Summer collection is in – suggest an outfit")
    if st.button("Send Proactive Message"):
        if admin_input.strip():
            with st.chat_message("admin"):
                st.markdown(f"📣 *Admin Triggered:* {admin_input}")
            response = proactive(admin_input)
            st.session_state.messages.append({"role": "assistant", "content": response['messages'][-1].content})
            st.rerun()
        else:
            st.warning("Please enter a proactive message.")
