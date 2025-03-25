import streamlit as st
from agent import run_agent, proactive
from tools.display_item import extract_display_items
import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

st.set_page_config(page_title="AIFS – AI Fashion Stylist", page_icon="🧥")
st.title("🧥 AI Fashion Stylist (AIFS)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history (text only — no image parsing here)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "suggested_items" in msg and msg["suggested_items"]:
            st.subheader("🛍️ Suggested Items")
            num_cols = min(3, len(msg["suggested_items"]))
            cols = st.columns(num_cols)

            for i, item in enumerate(msg["suggested_items"]):
                with cols[i % num_cols]:
                    st.image(item["img_path"], use_container_width=True)
                    st.caption(item["title"])

# Handle user input
if user_input := st.chat_input("What are you looking for today?"):
    # Add user message to history and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the agent
    response = run_agent(user_input)

    final_msg = response["messages"][-1].content
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_msg,
        "suggested_items": extract_display_items(response["messages"])
    })

    st.rerun()

# Handle proactive admin messages
with st.sidebar:
    st.header("👩‍💼 Admin Panel")
    admin_input = st.text_area("Proactive Prompt", placeholder="e.g. Summer collection is in – suggest an outfit")

    if st.button("Send Proactive Message"):
        if admin_input.strip():
            with st.chat_message("admin"):
                st.markdown(f"📣 *Admin Triggered:* {admin_input}")

            response = proactive(admin_input)
            final_msg = response["messages"][-1].content
            st.session_state.messages.append({"role": "assistant", "content": final_msg, "suggested_items": extract_display_items(response["messages"])})

            st.rerun()
        else:
            st.warning("Please enter a proactive message.")
