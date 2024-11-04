import json
import random
import argparse

def spilt_context(context):
    split_start = random.randint(1, len(context) // 2)
    split_end = random.randint(split_start + 1, len(context) - 1)

    prefix = context[:split_start]
    middle = context[split_start:split_end]
    suffix = context[split_end:]

    return prefix, middle, suffix


def fim_splitting(input_path, output_path):
    dataset = []
    with open(input_path, 'r') as f:
        for line in f:
            example = json.loads(line.strip())
            prefix, middle, suffix = spilt_context(example["context"])
            dataset.append({"file_name": example["file_name"], "prefix" : prefix, "middle": middle, "suffix": suffix})

    with open(output_path, 'w') as f:
        for example in dataset:
            json.dump(example, f)
            f.write('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a dataset for FIM splitting.")
    parser.add_argument('--input_path', type=str, default="datasets/code_dataset.jsonl",
                        help="Path to input JSONL dataset.")
    parser.add_argument('--output_path', type=str, default='datasets/fim_split_dataset.jsonl',
                        help="Path to save the generated JSONL dataset.")
    args = parser.parse_args()

    fim_splitting(args.input_path, args.output_path)
