# model.py
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util

# Load pre-trained Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, and good for similarity

def get_most_similar_topics(
    preprocessed_headings: List[Dict[str, List[str]]],
    preprocessed_questions: List[List[str]]
) -> List[Tuple[str, float]]:
    """
    Rank all topics from most to least important by aggregating similarity scores across all questions.

    Args:
        preprocessed_headings: List of dicts with 'heading' (tokens) and 'content' (tokens).
        preprocessed_questions: List of question tokens.

    Returns:
        List of tuples: [(topic_heading, aggregated_score), ...], sorted by aggregated_score in descending order.
    """
    # Convert token lists back to text
    topic_texts = [
        ' '.join(block['heading']) + ' ' + ' '.join(block['content'])
        for block in preprocessed_headings
    ]
    topic_headings = [
        ' '.join(block['heading']) for block in preprocessed_headings
    ]
    question_texts = [' '.join(q_tokens) for q_tokens in preprocessed_questions]

    # Compute embeddings
    topic_embeddings = model.encode(topic_texts, convert_to_tensor=True)
    question_embeddings = model.encode(question_texts, convert_to_tensor=True)

    # Initialize a dictionary to store aggregated scores for each topic
    topic_scores_dict = {heading: 0.0 for heading in topic_headings}

    # Compute cosine similarities for each question against all topics
    for question_emb in question_embeddings:
        cosine_scores = util.cos_sim(question_emb, topic_embeddings)[0]
        # Add the similarity score of each topic to its aggregated total
        for topic_heading, score in zip(topic_headings, cosine_scores.tolist()):
            topic_scores_dict[topic_heading] += score

    # Convert the dictionary to a list of tuples and sort by aggregated score
    topic_scores_sorted = sorted(
        topic_scores_dict.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return topic_scores_sorted