
from st_keyup import st_keyup
import streamlit as st

import re
from collections import defaultdict
from operator import itemgetter

from utils import footer


st.set_page_config(page_title='AI VIETNAM', page_icon='https://scontent-ams2-1.xx.fbcdn.net/v/t39.30808-6/326762542_533351005436945_3355631653176967012_n.png?_nc_cat=1&ccb=1-7&_nc_sid=5f2048&_nc_ohc=J2pKQDyGdRgAX_FLksV&_nc_ht=scontent-ams2-1.xx&oh=00_AfDN3M3ADdj9HUK4qGIkj-F77QU6P5hja1XkdcjQQtUg2w&oe=6563863F')


@st.cache_data
def preprocess_text(text):
    """
    Preprocess text by removing punctuation and converting to lowercase.
    Only allowed characters (including Vietnamese characters and digits) are kept.

    Parameters:
    text (str): The text to be preprocessed.

    Returns:
    str: The preprocessed text.
    """
    # Define allowed characters including Vietnamese characters and some punctuation
    allowed_chars = " _abcdefghijklmnopqrstuvwxyz0123456789áàảãạâấầẩẫậăắằẳẵặóòỏõọôốồổỗộơớờởỡợéèẻẽẹêếềểễệúùủũụưứừửữựíìỉĩịýỳỷỹỵđ "

    # Convert to lowercase and filter out non-allowed characters
    text = text.lower()
    return ''.join(char for char in text if char in allowed_chars)

@st.cache_data
def most_frequent(lst_words):
    """
    Find the most frequent element in a list.

    Parameters:
    lst_words (list): The list to search through.

    Returns:
    Any: The most frequent element in the list.
    """
    counter = 0
    word = lst_words[0]

    for index in range(len(lst_words)):
        current_word = lst_words[index]

        curr_frequency = lst_words.count(current_word)

        if curr_frequency > counter:
            counter = curr_frequency
            word = current_word

    return word


@st.cache_data
def create_suggestion_lists(text):
    """
    Create two lists: one for unique words and another for lists of corresponding next words.
    This is used to build a simple predictive text model.

    Parameters:
    text (list): A list of sentences.

    Returns:
    tuple: Two lists, one containing unique words and the other containing lists of next words.
    """
    unique_words = []  # To store unique words
    next_words = []  # To store lists of next words for each unique word
    most_frequency_words = []  # To store the most frequent word for each unique word

    # Process each sentence in the text
    for sentence in text:
        sentence = preprocess_text(sentence)  # Preprocess the sentence
        words = sentence.split()  # Split into words

        # Iterate through words to build the lists
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]

            # Add word to unique_words list if not present, and its next word to next_words
            if current_word not in unique_words:
                unique_words.append(current_word)
                next_words.append([next_word])
            else:
                # If word is already in unique_words, add next word to its corresponding list
                index = unique_words.index(current_word)
                next_words[index].append(next_word)

    # Find the most frequent word for each unique word
    for index in range(len(next_words)):
        if len(next_words[index]) == 0:
            continue

        most_frequency_word = most_frequent(next_words[index])
        most_frequency_words.append(most_frequency_word)

    return unique_words, most_frequency_words


@st.cache_data
def load_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    return data
    
#################################################
st.title("Word Suggestions App")

# load data
with st.spinner("Loading data"):
    data = load_data('data.txt')
    
    # Create the unique words list and their corresponding next words lists
    unique_words, most_frequency_words = create_suggestion_lists(data)

# Input word
inputs = st_keyup("Enter text to check suggestions:", placeholder='Type something...', key='0')


# Handle input
if ' ' in inputs or inputs:
    # Process input
    inputs = inputs.strip()
    inputs = inputs.split(' ')[-1]
        
    # Preprocess the input word
    processed_inputs = preprocess_text(inputs)
        
    # Check if the preprocessed input word is in the list of unique words
    if processed_inputs in unique_words:
        # Find the index of the input word in the list of unique words
        index = unique_words.index(processed_inputs)

        result = most_frequency_words[index]

        st.success(result)
    else:
        # Print a message indicating no suggestions are available
        st.warning(f"No suggestions found for '{inputs}'.")
        
        
#################################################
footer()
