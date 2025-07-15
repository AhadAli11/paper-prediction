# Paper Predictor

## Overview

Paper Predictor is a tool designed to help students and educators identify the most important topics from academic syllabi and past exam papers. By leveraging Natural Language Processing (NLP) and semantic similarity models (Sentence-BERT), it automates the process of ranking topics based on their relevance to exam questions.

---

## Features

- **Supports Word (.docx) and PowerPoint (.pptx) syllabus files**
- **Extracts headings and content from syllabus files**
- **Extracts questions from quiz/midterm Word files**
- **Preprocesses text with lemmatization or stemming**
- **Ranks topics by semantic similarity to questions using Sentence-BERT**
- **Interactive web interface built with Streamlit**

---

## How It Works

1. **Upload syllabus and quiz/midterm files** via the web interface.
2. **Extract headings, content, and questions** from the documents.
3. **Preprocess the text** (cleaning, tokenization, stopword removal, lemmatization/stemming).
4. **Convert topics and questions to embeddings** using Sentence-BERT.
5. **Compute similarity scores** between topics and questions.
6. **Aggregate and rank topics** by their relevance to the questions.
7. **Display results** in an easy-to-read format.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd paper-predictor
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Make sure you have Python 3.8+ installed.

3. **Download NLTK data (first run will do this automatically):**
   - Required: `punkt`, `stopwords`, `wordnet`

---

## Usage

1. **Start the Streamlit app:**
   ```sh
   streamlit run main.py
   ```

2. **Upload your syllabus (.docx or .pptx) and quiz/midterm (.docx) files** using the web interface.

3. **Choose preprocessing options** (lemmatization or stemming).

4. **View extracted data and ranked topics** based on their relevance to your questions.

---

## File Structure

```
paper-predictor/
│
├── app/
│   ├── extractor.py         # Extracts headings/content/questions from files
│   ├── preprocessing.py     # Cleans and tokenizes text
│   ├── model.py             # Ranks topics using Sentence-BERT
│   ├── ui_streamlit.py      # Streamlit web interface
│
├── main.py                  # Entry point for the app
├── requirements.txt         # Python dependencies
```

---

## Example

1. **Upload syllabus and quiz files**
2. **See extracted headings and questions**
3. **Get a ranked list of topics most relevant to your exam questions**

---

## Limitations & Future Work

- Only supports English language documents
- Only .docx and .pptx formats for syllabus, .docx for questions
- No support for PDF files yet
- Future plans: add PDF support, improve extraction robustness, add more visualization options

---

## Credits

- Built using [Streamlit](https://streamlit.io/)
- NLP powered by [Sentence-BERT](https://www.sbert.net/)
- Text preprocessing with [NLTK](https://www.nltk.org/)

---

## License

This project is for educational purposes.
