import io
import json
import random

import boto3
import numpy as np

s3 = boto3.client('s3')


def generate_sentence(chain, max_length):
    word = random.choice(list(chain.keys()))
    sentence = [word]

    while len(sentence) < max_length:
        if word in chain:
            next_words = list(chain[word].keys())
            next_word_probs = list(chain[word].values())
            word = np.random.choice(next_words, p=next_word_probs)
            sentence.append(word)
        else:
            break

    return ' '.join(sentence)


def generate_sentences(chain, average_length, std_dev_length, n_sentences):
    max_length = int(average_length + std_dev_length)
    return [generate_sentence(chain, max_length) for _ in range(n_sentences)]


def lambda_handler(event, context):
    bucket_name = event['bucket_name']
    file_key = event['file_key']

    # Read the JSON file from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    markov_chain_data = json.load(io.BytesIO(obj['Body'].read()))

    loaded_chain = markov_chain_data["markov_chain"]
    average_length = markov_chain_data["average_length"]
    std_dev_length = markov_chain_data["std_dev_length"]

    # Generate and return sentences
    n_sentences = event.get('n_sentences', 5)  # Default to 5 sentences if not specified
    generated_sentences = generate_sentences(loaded_chain, average_length, std_dev_length, n_sentences)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "generated_sentences": generated_sentences
        })
    }
