import re
from html import unescape


# Data preprocess
def expand_negations(text):
    
    # Define a list of negations to be expanded
    negations = ["can't", "don't", "won't", "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't",
                 "couldn't", "shouldn't", "mustn't", "mightn't", "doesn't", "didn't", "ain't", "aint", "shan't"]

    # Create a regular expression pattern to match negations
    negation_pattern = re.compile(r"\b(" + "|".join(negations) + r")\b")

    # Replace each negation with its expanded form
    expanded_text = negation_pattern.sub(lambda x: expand_single_negation(x.group(0)), text)

    return expanded_text

def expand_single_negation(negation):
    # Define a dictionary mapping each negation to its expanded form
    negation_expansions = {
        "can't": "cannot",
        "don't": "do not",
        "won't": "will not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mustn't": "must not",
        "mightn't": "might not",
        "doesn't": "does not",
        "didn't": "did not",
        "ain't": "not",
        "aint": "not",
        "shan't": "shall not"
    }

    return negation_expansions.get(negation, negation)
    
# Data cleaning from https://doi.org/10.3390/app131911104
def clean_text(text):
    
    # Step 1: Decoding HTML
    preprocessed_text = unescape(text)
    
    # Step 2: Removal of emoticons
    preprocessed_text = re.sub(r'[\U00010000-\U0010ffff]', '', preprocessed_text)
    
    # Step 3: Removal of mentions (usernames)
    preprocessed_text = re.sub(r'@\w+', '', preprocessed_text)
    
    # Step 4: Removal of URL links
    preprocessed_text = re.sub(r'https?://\S+|www\.\S+', '', preprocessed_text)
    
    # Step 5: Conversion to lower case
    preprocessed_text = preprocessed_text.lower()
    
    # Step 6: Expansion of negations
    preprocessed_text = expand_negations(preprocessed_text)
    
    # Step 7: Removal of hashtags, punctuation marks, numbers, and special characters
    preprocessed_text = re.sub(r'#[\w_]+', '', preprocessed_text)
    preprocessed_text = re.sub(r'[^a-zA-Z\s]', '', preprocessed_text)
    
    # Step 8: Removal of extra white spaces
    preprocessed_text = re.sub(r'\s+', ' ', preprocessed_text).strip()
    
    return preprocessed_text
    