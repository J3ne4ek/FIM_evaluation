import jsonlines

def interactive_assessment(input_file, output_file):
    labels = []
    with jsonlines.open(input_file) as reader:
        for i, entry in enumerate(reader):
            for name in ["prefix", "suffix", "middle", "completion"]:
                print(f"=================")
                print(f"{name}:")
                print(f"=================")
                print(entry[name])

            while True:
                try:
                    label = int(input("Rate from 0 to 2: ").strip())
                    if label in [0, 1, 2]:
                        labels.append(label)
                        break
                    else:
                        print("Please enter a number between 0 and 2.")
                except ValueError:
                    print("Invalid input. Please enter an integer between 0 and 2.")


    with jsonlines.open(output_file, mode='w') as writer:
        for label in labels:
            writer.write({"human eval": label})


def main():
    input_file = "datasets/completions_tiny_starcoder_dataset.jsonl"
    output_file = "datasets/human_eval.jsonl"

    interactive_assessment(input_file, output_file)

if __name__ == "__main__":
    main()