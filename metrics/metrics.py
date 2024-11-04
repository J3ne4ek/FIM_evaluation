from difflib import SequenceMatcher
import nltk
import Levenshtein
from abc import ABC, abstractmethod


class Metric(ABC):
    @abstractmethod
    def calculate(self, pred, target):
        pass

class ExactMatchMetric(Metric):
    def calculate(self, pred, target):
        return int(pred == target)

class ChrfMetric(Metric):
    def calculate(self, pred, target):
        return nltk.translate.chrf_score.sentence_chrf([target], pred)

class LevenshteinMetric(Metric):
    def calculate(self, pred, target):
        return Levenshtein.distance(pred, target)

class PrefixSimilarityMetric(Metric):
    def calculate(self, pred, target):
        matching_length = 0
        for pred_char, target_char in zip(pred, target):
            if pred_char == target_char:
                matching_length += 1
            else:
                break
        return matching_length / len(target) if target else 0.0

class MatchedRatioMetric(Metric):
    def calculate(self, pred, target):
        lcs_length = SequenceMatcher(None, pred, target).find_longest_match(0, len(pred), 0, len(target)).size
        return lcs_length / len(target) if target else 0.0
