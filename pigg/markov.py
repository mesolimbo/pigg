import json
from collections import defaultdict

import numpy as np
import pandas as pd


def generate_markov_chain(csv_path, output_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Extract the sentences into a list
    sentences = df['Topic'].tolist()

    # Initialize the Markov chain
    markov_chain = defaultdict(lambda: defaultdict(int))

    # Build the Markov chain from the sentences
    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words) - 1):
            markov_chain[words[i]][words[i + 1]] += 1

    # Calculate average length and standard deviation of the sentences
    lengths = [len(sentence.split()) for sentence in sentences]
    average_length = np.mean(lengths)
    std_dev_length = np.std(lengths)

    # Convert counts to probabilities
    markov_chain_prob = {}

    for word, transitions in markov_chain.items():
        total = sum(transitions.values())
        markov_chain_prob[word] = {next_word: count / total for next_word, count in transitions.items()}

    # Add the average length and standard deviation to the JSON object
    markov_chain_data = {
        "average_length": average_length,
        "std_dev_length": std_dev_length,
        "markov_chain": markov_chain_prob
    }

    # Convert the Markov chain data to a JSON object
    markov_chain_json = json.dumps(markov_chain_data, indent=4)

    # Save the JSON object to a file
    with open(output_path, 'w') as f:
        f.write(markov_chain_json)

    print(f"Markov chain model with statistics has been saved to '{output_path}'")
