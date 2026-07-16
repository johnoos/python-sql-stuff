""" detects isogram phrases """
import re

def is_isogram(aword: str) -> bool:
    """ detects isogram phrases 
    checks for repeating alphabetic and - """
    lowercase_word = aword.lower()
    
    # lazy search for efficiency
    pattern = r'([a-z]).*?\1'

    duplicates_found = re.search(pattern, lowercase_word)
    if duplicates_found:
        return False
    return True




