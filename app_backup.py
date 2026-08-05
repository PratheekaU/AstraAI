import streamlit as st

# Configure the page
st.set_page_config(
    page_title="AstraAI",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AstraAI")
st.subheader("Your Intelligent Personal Assistant")

# Welcome message
st.write("""
Welcome to **AstraAI**!

I can help you with:
- 💻 Programming
- 🤖 Artificial Intelligence
- 📚 Learning
- ✍️ Writing
- 🌍 General Questions

This is Version 1 of AstraAI.
More exciting features are coming soon!
""")

# User input
user_input = st.text_input("Ask me anything:")

# Button
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        st.success(f"You asked: {user_input}")
        st.info("🚀 AI response will be added in the next version!")