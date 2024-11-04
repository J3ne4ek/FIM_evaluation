import json
import os
from pathlib import Path
from git import Repo
import argparse


def clone_repo(git_repo_link, clone_path):
    if os.path.exists(clone_path):
        print(f"The folder '{clone_path}' already exists. Using the existing folder.")
    else:
        print(f"Cloning repository from {git_repo_link} into {clone_path}")
        Repo.clone_from(git_repo_link, clone_path)


def get_python_files(folder_path):
    return [str(file) for file in Path(folder_path).rglob('*.py')]


def filter_empty_lines(lines):
    return [line for line in lines if len(line.strip()) > 1]


def create_item(lines, file):
    return {'file_name': file, 'context': ''.join(lines)}


def create_code_completion_dataset(folder_path, min_length=5, max_length=30, with_test_files=False):
    dataset = []
    files = get_python_files(folder_path)
    mean_length = (min_length + max_length) // 2

    for file in files:
        if "test" in file and not with_test_files:
            continue

        with open(file, 'r') as f:
            lines = f.readlines()
            lines = filter_empty_lines(lines)
            if len(lines) < min_length:
                continue

        if len(lines) >= max_length:
            for i in range(0, len(lines), mean_length):
                sub_lines = lines[i:i + mean_length]
                if len(sub_lines) >= min_length:
                    dataset.append(create_item(sub_lines, file))
        else:
            dataset.append(create_item(lines, file))

    return dataset


def save_as_jsonl(dataset, output_path):
    with open(output_path, 'w') as f:
        for example in dataset:
            json.dump(example, f)
            f.write('\n')


def main():
    parser = argparse.ArgumentParser(description="Generate a code completion dataset from a Git repository.")
    parser.add_argument('--git_repo_link', type=str, help="URL of the Git repository to clone.")
    parser.add_argument('--output_path', type=str, default='datasets/code_dataset.jsonl', help="Path to save the generated JSONL dataset.")
    parser.add_argument('--clone_path', type=str, default='git_repo', help="Path to clone the repository.")
    parser.add_argument('--min_length', type=int, default=5, help="Minimum length of code snippet in lines.")
    parser.add_argument('--max_length', type=int, default=30, help="Maximum length of code snippet in lines.")
    parser.add_argument('--with_test_files', default=False, help="Include test files in the dataset.")

    args = parser.parse_args()

    clone_repo(args.git_repo_link, args.clone_path)
    dataset = create_code_completion_dataset(
        args.clone_path,
        min_length=args.min_length,
        max_length=args.max_length,
        with_test_files=args.with_test_files
    )

    save_as_jsonl(dataset, args.output_path)
    print(f"Dataset saved to {args.output_path}")

if __name__ == "__main__":
    main()
