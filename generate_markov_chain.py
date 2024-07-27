from pigg.markov import generate_markov_chain

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python generate_markov_chain.py <input_csv_path> <output_json_path>")
        sys.exit(1)

    input_csv_path = sys.argv[1]
    output_json_path = sys.argv[2]

    generate_markov_chain(input_csv_path, output_json_path)
