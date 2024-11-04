import json
from transformers import (AutoModelForCausalLM, AutoTokenizer)
import argparse

def create_fim_prompt(prefix, suffix):
    return (
        f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
    )

def main():
    parser = argparse.ArgumentParser(description="Generate FIM completions")
    parser.add_argument('--model_name', type=str, default="bigcode/tiny_starcoder_py",
                        help="Model name to use.")
    parser.add_argument('--input_path', type=str, default='datasets/fim_split_dataset.jsonl',
                        help="Path to input JSONL dataset.")
    parser.add_argument('--output_path', type=str, default='datasets/completions_tiny_starcoder_dataset.jsonl',
                        help="Path to save the generated JSONL dataset.")
    parser.add_argument('--device', type=str, default='cuda',
                        help="Specify the device to use.")

    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_name, trust_remote_code=True).to(args.device)

    completions = []
    with open(args.input_path, 'r') as f:
        for line in f:
            example = json.loads(line.strip())
            input_text = create_fim_prompt(example['prefix'], example['suffix'])
            inputs = tokenizer.encode(input_text, return_tensors="pt").to(args.device)

            outputs = model.generate(inputs, max_new_tokens=256, pad_token_id=tokenizer.eos_token_id,)
            completion = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
            example['completion'] = completion
            completions.append(example)

    with open(args.output_path, 'w') as f:
        for example in completions:
            json.dump(example, f)
            f.write('\n')


if __name__ == "__main__":
    main()
