import nltk
import re
from typing import List, Dict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Download required NLTK data with error handling
try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')
except Exception as e:
    raise Exception(f"Failed to download NLTK resources: {str(e)}")

def preprocess_text(text: str, use_stemming: bool = False) -> List[str]:
    """
    Preprocess a single text string with tokenization, lemmatization/stemming, and cleaning.
    Args:
        text: Input text to preprocess.
        use_stemming: If True, use stemming instead of lemmatization.
    Returns:
        List of preprocessed tokens.
    """
    # Lowercase
    text = text.lower()
    
    # Remove special characters and punctuation, keep alphanumeric and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization or Stemming
    if use_stemming:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
    else:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Remove empty tokens
    tokens = [token for token in tokens if token.strip()]
    
    return tokens

def preprocess_heading_blocks(heading_blocks: List[Dict[str, str]], use_stemming: bool = False) -> List[Dict[str, List[str]]]:
    """
    Preprocess heading-content pairs from extract_topic_blocks.
    Args:
        heading_blocks: List of dictionaries with 'heading' and 'content' keys.
        use_stemming: If True, use stemming instead of lemmatization.
    Returns:
        List of dictionaries with preprocessed heading and content as token lists.
    """
    preprocessed_blocks = []
    
    for block in heading_blocks:
        preprocessed_blocks.append({
            'heading': preprocess_text(block['heading'], use_stemming),
            'content': preprocess_text(block['content'], use_stemming)
        })
    
    return preprocessed_blocks

def preprocess_questions(questions: List[str], use_stemming: bool = False) -> List[List[str]]:
    """
    Preprocess a list of questions from extract_questions_from_docx.
    Args:
        questions: List of question strings.
        use_stemming: If True, use stemming instead of lemmatization.
    Returns:
        List of preprocessed question tokens.
    """
    return [preprocess_text(question, use_stemming) for question in questions]