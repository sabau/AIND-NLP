"""Bigram Model."""

import os
import re
import random
from collections import Counter

def compute_bigram_model(path, files):
    """Compute a bigram model for a given corpus, including unigram probabilities.

    Params
    ======
        path: directory where input files are located
        files: list of files, or a single string specifying regex pattern to match (e.g. r'.*\.txt')

    Returns
    =======
        p_unigrams: dict with frequency of single words (need not be normalized to [0, 1])
        p_bigrams: dict of dicts with frequency of bigrams (need not be normalized to [0, 1])

    """

    # Grab a list of all files in specified corpus
    if isinstance(files, str):
        files = [f for f in os.listdir(path) if re.match(files, f)]  # collect all matching filenames
    files = [os.path.join(path, f) for f in files]  # prepend path to each filename

    # TODO: Read in text from each file and combine into a single string
    corpus = ""
    for file in files:
        with open(file, 'r') as f:
            corpus += f.read() + "\n"
    
    # TODO: Clean and tokenize text (note that you may want to retain case and sentence delimiters)
    words = re.sub(r"\s+", " ", re.sub(r"[^a-zA-Z0-9\,\.\(\)]", " ", corpus)).split(" ")
    
    # TODO: Compute unigram probabilities
    p_unigrams = Counter(words)

    # TODO: Compute bigram probabilities
    bigrams = [(words[i], words[i + 1]) for i in range(len(words) - 1)]
    p_bigrams = {}
    for bigram in bigrams:
        if bigram[0] not in p_bigrams:
            p_bigrams[bigram[0]] = {}
        
        if bigram[1] not in p_bigrams[bigram[0]]:
            p_bigrams[bigram[0]][bigram[1]] = 0
        
        p_bigrams[bigram[0]][bigram[1]] += 1
        

    return p_unigrams, p_bigrams


def generate_sequence(p_unigrams, p_bigrams, num_words=100, seed_word=None):
    """Generate a random sequence of words, given unigram and bigram probabilities."""

    # If seed_word is not given, pick one randomly based on unigram probabilities
    if seed_word is None:
        seed_word = random.choices(list(p_unigrams.keys()), weights=list(p_unigrams.values()))[0]
    seq = [seed_word]
    for i in range(num_words):
        seq.append(random.choices(list(p_bigrams[seq[-1]].keys()), weights=list(p_bigrams[seq[-1]].values()))[0])
    return seq


def test_run():
    # Compute bigram model
    p_unigrams, p_bigrams = compute_bigram_model(path='.', files=['carroll-alice.txt'])

    # Check most common unigrams (single words)
    print("10 most common unigrams:")
    sorted_unigrams = sorted(p_unigrams.items(), key=lambda item: item[1], reverse=True)  # each item = (i, count)
    for word, count in sorted_unigrams[:10]:
        print("{}\t{}".format(word, count))

    # Check most common bigrams (pairs of words)
    all_bigrams = [(i, j, count) for i in p_bigrams.keys() for j, count in p_bigrams[i].items()]
    sorted_bigrams = sorted(all_bigrams, key=lambda item: item[2], reverse=True)  # each item = (i, j, count)
    print("10 most common bigrams:")
    for i, j, count in sorted_bigrams[:10]:
        print("{}\t{}\t{}".format(i, j, count))

    # Generate a sample sequence of words
    seq = generate_sequence(p_unigrams, p_bigrams, seed_word="Alice")
    print(" ".join(seq))


if __name__ == "__main__":
    test_run()
