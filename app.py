import streamlit as st
from google import genai
from dotenv import load_dotenv
import fitz
from PIL import Image
import os

# =====================================
# Load API Key
# =====================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="AstraAI",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# Session State
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.title("🤖 AstraAI")

    st.markdown("### Intelligent AI Assistant")

    st.success("🟢 Gemini Connected")

    page = st.radio(
        "Select Feature",
        [
            "💬 AI Chat",
            "📄 PDF Chat",
            "🖼️ Image Analysis",
            "📋 Resume Reviewer",
            "ℹ️ About"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Version 2.0")
    st.caption("Developer : Umesh")
    # =====================================
# AI CHAT
# =====================================

if page == "💬 AI Chat":

    st.title("💬 AI Chat")

    st.write("Ask anything. This chat does NOT use PDFs, images or resumes.")

    # Display Previous Chat History
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    chat_prompt = st.chat_input("Type your question...")

    if chat_prompt:

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": chat_prompt
            }
        )

        # Display User Message
        with st.chat_message("user"):
            st.markdown(chat_prompt)

        # Generate AI Response
        with st.chat_message("assistant"):

            with st.spinner("🤖 AstraAI is thinking..."):

                try:

                    response = client.models.generate_content(
                        model="models/gemini-3.5-flash-lite",
                        contents=chat_prompt
                    )

                    answer = response.text

                except Exception as e:

                    answer = f"❌ Error:\n\n{e}"

            st.markdown(answer)

        # Save Assistant Response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    # Clear Chat Button
    st.divider()

    if st.button("🗑️ Clear AI Chat"):

        st.session_state.messages = []

        st.rerun()
        # =====================================
# PDF CHAT
# =====================================

elif page == "📄 PDF Chat":

    st.title("📄 PDF Chat")

    st.write("Upload a PDF and ask questions only about this PDF.")

    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_chat"
    )

    if uploaded_pdf:

        pdf = fitz.open(
            stream=uploaded_pdf.read(),
            filetype="pdf"
        )

        pdf_text = ""

        for page_pdf in pdf:
            pdf_text += page_pdf.get_text()

        st.session_state.pdf_text = pdf_text

        st.success("✅ PDF Uploaded Successfully")

    if st.session_state.pdf_text:

        pdf_question = st.text_input(
            "Ask a question about this PDF",
            key="pdf_question"
        )

        if st.button("Ask PDF"):

            with st.spinner("📄 Reading PDF..."):

                prompt = f"""
You are an AI PDF Assistant.

Answer ONLY from the uploaded PDF.

If the answer is not available in the PDF, simply say:

'I couldn't find this information in the uploaded PDF.'

PDF:

{st.session_state.pdf_text}

Question:

{pdf_question}
"""

                try:

                    response = client.models.generate_content(
                        model="models/gemini-3.5-flash-lite",
                        contents=prompt
                    )

                    st.markdown("### 🤖 AstraAI")
                    st.write(response.text)

                except Exception as e:

                    st.error(e)

        st.divider()

        st.subheader("📊 PDF Statistics")

        words = len(st.session_state.pdf_text.split())
        chars = len(st.session_state.pdf_text)

        col1, col2 = st.columns(2)

        col1.metric("Words", words)
        col2.metric("Characters", chars)

        if st.button("🗑️ Clear PDF"):

            st.session_state.pdf_text = ""

            st.rerun()
            # =====================================
# IMAGE ANALYSIS
# =====================================

elif page == "🖼️ Image Analysis":

    st.title("🖼️ Image Analysis")

    st.write("Upload one or more images and ask questions only about those images.")

    uploaded_images = st.file_uploader(
        "Upload Images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="image_upload"
    )

    if uploaded_images:

        st.success(f"✅ {len(uploaded_images)} image(s) uploaded successfully.")

        for img in uploaded_images:
            image = Image.open(img)
            st.image(image, caption=img.name, use_container_width=True)

        image_question = st.text_input(
            "Ask about uploaded image(s)",
            key="image_question"
        )

        if st.button("🔍 Analyze Image"):

            with st.spinner("🖼️ AstraAI is analyzing image..."):

                try:

                    contents = []

                    for img in uploaded_images:
                        image = Image.open(img)
                        contents.append(image)

                    if image_question.strip() == "":
                        contents.append(
                            "Describe these image(s) in detail."
                        )
                    else:
                        contents.append(image_question)

                    response = client.models.generate_content(
                        model="models/gemini-3.5-flash-lite",
                        contents=contents
                    )

                    st.markdown("### 🤖 AstraAI")

                    st.write(response.text)

                except Exception as e:

                    st.error(e)

        if st.button("🗑️ Clear Images"):

            st.rerun()

    else:

        st.info("Please upload at least one image.")
        # =====================================
# RESUME REVIEWER
# =====================================

elif page == "📋 Resume Reviewer":

    st.title("📋 Resume Reviewer")

    st.write("Upload your resume and get an ATS-style review.")

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume_upload"
    )

    if uploaded_resume:

        pdf = fitz.open(
            stream=uploaded_resume.read(),
            filetype="pdf"
        )

        resume_text = ""

        for page_pdf in pdf:
            resume_text += page_pdf.get_text()

        st.session_state.resume_text = resume_text

        st.success("✅ Resume Uploaded Successfully")

    if st.session_state.resume_text:

        if st.button("📊 Review Resume"):

            prompt = f"""
You are an ATS Resume Expert.

Review this resume.

Provide the report in the following format:

# ATS Score
(Give score out of 100)

# Strengths

# Weaknesses

# Missing Skills

# Grammar Suggestions

# Formatting Suggestions

# Project Feedback

# Final Verdict

Resume:

{st.session_state.resume_text}
"""

            with st.spinner("📋 Reviewing Resume..."):

                try:

                    response = client.models.generate_content(
                        model="models/gemini-3.5-flash-lite",
                        contents=prompt
                    )

                    st.success("✅ Resume Reviewed")

                    st.markdown(response.text)

                except Exception as e:

                    st.error(e)

        if st.button("🗑️ Clear Resume"):

            st.session_state.resume_text = ""

            st.rerun()
            # =====================================
# ABOUT
# =====================================

elif page == "ℹ️ About":

    st.title("🤖 About AstraAI")

    st.markdown("""
## AstraAI

AstraAI is an intelligent AI assistant developed using
Google Gemini and Streamlit.

### Features

✅ AI Chat

✅ PDF Chat

✅ Image Analysis

✅ Resume Reviewer

### Technologies

- Python
- Streamlit
- Google Gemini API
- PyMuPDF
- Pillow

### Developer

Umesh

Version : 2.0
""")

# =====================================
# FOOTER
# =====================================

st.divider()

st.markdown(
"""
<div style='text-align:center;color:gray;'>

Built with ❤️ using Python • Streamlit • Google Gemini

© 2026 AstraAI

</div>
""",
unsafe_allow_html=True
)