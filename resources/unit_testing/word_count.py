""" Counts occurrences of words in a sentence """

import re
from collections import Counter

def count_words(sentence: str) -> dict:
    """Finds all alphanumeric words/contractions and counts them."""
    # Matches words, numbers, and contractions like "don't"
    pattern = r"[A-Za-z0-9']+"
    
    # Extract all matches into a list
    words = re.findall(pattern, sentence.lower())
    
    clean_words = [cleaned for word in words if (cleaned := word.strip("'‘’ "))]
    
    # Counter automatically builds the frequency dictionary
    return dict(Counter(clean_words))