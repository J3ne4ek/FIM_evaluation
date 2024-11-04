# FIM_evaluation

### Metrics
1. **_Exact Match._** This metric measures the proportion of predictions that exactly match the ground truth. 
    A prediction is considered correct only if it is identical to the reference.
   
   **Average value:** 0.0232
2. **_Character F-Score (CHRF)._** The Character F-Score is based on character n-grams and computes the harmonic mean of precision and recall at the character level.
   
    **Average value:** 0.322
3. **_Levenshtein Distance._** This metric quantifies the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another. It provides a measure of similarity between two strings.
    
   **Average value:** 501.90
4. **_Prefix Similarity._** This metric calculates the similarity between the beginning portions of two strings. It measures how much of the start of the predicted string matches the ground truth.
    
   **Average value:** 0.1281
5. **_Matched Ratio._** The matched ratio is a simple metric that calculates the proportion of tokens in the prediction that match tokens in the ground truth. It provides a direct measure of overlap.
   
   **Average value:** 0.2798
6. **_Human Evaluation._** This is a subjective assessment that was done by me. Each addition was rated from 0 to 2, where 2 is a very good addition, and 0 is a bad one. Most often, models received the highest score if the logic matches and if it was possible to connect the prefix and suffix
   
   **Average value:** 0.813 

A full report about metrics for each completion can be found in datasets/annotations.csv. 
All completions and middle targets are in datasets/completions_tiny_starcoder_dataset.jsonl

### Conclusions
The model does a good job of reconstructing the beginning of the string, but very often fails to connect to the suffix. Instead of making a connection, the model often duplicates similar code many times. This model would do better with short predictions, such as one-line ones.

Although the full match has the highest correlation with my score, this metric is almost worthless, since full matches are very rare. For the reasons described above, one can conclude that a good metric is prefix similarity. However, this model does not take into account the decrease in score due to the fact that the model continued to generate poorly related text at the end for a long time. The Levenshtein distance also correlates well enough with my answers, but it may be worth normalizing it so that the value out of context makes more sense.
