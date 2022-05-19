# wordsim
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task wordsim_sim --aggregation median
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task wordsim_rel --aggregation median

# sentiment
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task sentiment --aggregation median

# NLI (commitmentbank)
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task commitmentbank --aggregation median

# affective text
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_anger --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_disgust --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_fear --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_joy --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_sadness --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_surprise --aggregation mean
PYTHONPATH=. python src/scripts/agreement/compute_agreements.py --task affectivetext_valence --aggregation mean
