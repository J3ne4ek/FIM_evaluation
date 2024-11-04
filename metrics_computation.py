import json
import argparse
from metrics.metrics import (ExactMatchMetric, ChrfMetric, LevenshteinMetric,
                            PrefixSimilarityMetric, MatchedRatioMetric)


class MetricsEvaluator:
    def __init__(self, data_path):
        with open(data_path) as f:
            self.data = [json.loads(line) for line in f]

        self.metrics = {
            'exact_match': ExactMatchMetric(),
            'chrf': ChrfMetric(),
            'levenshtein': LevenshteinMetric(),
            'prefix_similarity': PrefixSimilarityMetric(),
            'matched_ratio': MatchedRatioMetric()
        }

    def evaluate(self):
        results = []
        for example in self.data:
            target = example['middle']
            prediction = example['completion']

            result = {name: metric.calculate(prediction, target) for name, metric in self.metrics.items()}
            results.append(result)
        return results

    def calculate_averages(self, results):
        avg_results = {f'avg_{name}': sum(res[name] for res in results) / len(results) for name in self.metrics}
        return avg_results


def main():
    parser = argparse.ArgumentParser(description="Metric computation")
    parser.add_argument('--input_path', type=str, default='datasets/completions_tiny_starcoder_dataset.jsonl',
                        help="Path to input JSONL dataset.")
    parser.add_argument('--output_path', type=str, default='datasets/labels.jsonl',
                        help="Path to save the generated JSONL dataset.")

    args = parser.parse_args()

    evaluator = MetricsEvaluator(args.input_path)
    results = evaluator.evaluate()

    # save labels for datasets
    with open(args.output_path, 'w') as f:
        for result in results:
            json.dump(result, f)
            f.write('\n')

    avg_results = evaluator.calculate_averages(results)
    for name, avg in avg_results.items():
        print(f"{name.capitalize()}: {avg}")


if __name__ == "__main__":
    main()