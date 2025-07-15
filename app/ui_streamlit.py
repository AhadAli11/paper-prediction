import streamlit as st
import tempfile
import os
from typing import List, Dict
from app.extractor import extract_topic_blocks, extract_questions_from_docx
from app.preprocessing import preprocess_heading_blocks, preprocess_questions
from app.model import get_most_similar_topics

# ==========================
# Process Files
# ==========================

def process_files(syllabus_files, quiz_files, use_stemming: bool = False) -> tuple[List[Dict[str, List[str]]], List[List[str]]]:
    """Process uploaded files to extract and preprocess headings, content, and questions"""
    all_headings = []
    all_questions = []

    # Process syllabus files (.docx or .pptx)
    for uploaded_file in syllabus_files or []:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        headings = extract_topic_blocks(tmp_path)
        preprocessed_headings = preprocess_heading_blocks(headings, use_stemming)
        all_headings.extend(preprocessed_headings)
        os.unlink(tmp_path)

    # Process quiz/midterm files (.docx only)
    for uploaded_file in quiz_files or []:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name

        # Extract and preprocess headings for both .docx and .pptx
        headings = extract_topic_blocks(tmp_path)
        preprocessed_headings = preprocess_heading_blocks(headings, use_stemming)
        all_headings.extend(preprocessed_headings)

        # Extract and preprocess questions only for .docx
        if tmp_path.lower().endswith('.docx'):
            questions = extract_questions_from_docx(tmp_path)
            preprocessed_questions = preprocess_questions(questions, use_stemming)
            all_questions.extend(preprocessed_questions)

        os.unlink(tmp_path)

    return all_headings, all_questions

# ==========================
# Streamlit App
# ==========================

def main():
    st.set_page_config(page_title="Papers Predictor", layout="wide")
    st.title("📚 Papers predictor: Important topic finder")
    st.write("Upload syllabus (.docx or .pptx) and quiz/midterm (.docx) documents to extract and preprocess headings, content, and questions.")

    # Display option before processing
    display_data = st.radio(
        "Do you want to see the extracted data (headings, content, and questions)?",
        options=["Yes", "No"],
        index=0
    )

    # Preprocessing option
    use_stemming = st.checkbox("Use Stemming (instead of Lemmatization)", value=False)

    # Create two columns for file uploads
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Syllabus (Word or PowerPoint)")
        syllabus_files = st.file_uploader(
            "Choose syllabus document(s) (.docx or .pptx)",
            type=["docx", "pptx"],
            accept_multiple_files=True,
            key="syllabus_uploader"
        )

    with col2:
        st.subheader("Upload Quiz/Midterm (Word)")
        quiz_files = st.file_uploader(
            "Choose quiz/midterm document(s) (.docx)",
            type=["docx"],
            accept_multiple_files=True,
            key="quiz_uploader"
        )

    if st.button("Extract and Preprocess Content"):
        if not (syllabus_files or quiz_files):
            st.warning("No files uploaded.")
        else:
            with st.spinner("Processing files..."):
                heading_blocks, questions = process_files(syllabus_files, quiz_files, use_stemming)

            # Display based on user choice
            if display_data == "Yes":
                # Display preprocessed heading-content pairs
                if heading_blocks:
                    st.success(f"Extracted and preprocessed {len(heading_blocks)} heading blocks:")
                    for block in heading_blocks:
                        st.subheader(' '.join(block['heading']))
                        st.write(' '.join(block['content']))
                        st.markdown("---")
                else:
                    st.warning("No headings found in uploaded files.")

                # Display preprocessed questions
                if questions:
                    st.success(f"Extracted and preprocessed {len(questions)} questions from quiz/midterm files:")
                    for i, question_tokens in enumerate(questions, 1):
                        st.write(f"{i}. {' '.join(question_tokens)}")
                    st.markdown("---")
                else:
                    st.warning("No questions found in uploaded quiz/midterm files.")

            # Display the ranked list of all topics if both headings and questions exist
            if heading_blocks and questions:
                topic_rankings = get_most_similar_topics(heading_blocks, questions)
                st.subheader("📌 Topic Rankings (Most to Least Important):")
                for rank, (topic, score) in enumerate(topic_rankings, 1):
                    st.write(f"{rank}. **{topic}** (Aggregated Similarity Score: {score:.4f})")
                st.markdown("---")
            elif not heading_blocks:
                st.warning("No headings found, cannot determine topic rankings.")
            elif not questions:
                st.warning("No questions found, cannot determine topic rankings.")

if __name__ == "__main__":
    main()