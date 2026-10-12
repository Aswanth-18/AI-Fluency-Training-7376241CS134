# Assessment Day 4 — Local AI Coding Assistant

## Objective

Estimate the memory requirements of open language models, compare quantization and context length, review model licences, and recommend a suitable model for an 8 GB laptop.

## Files

- `vram_estimate.py` — Calculates weights, KV cache, total memory, and fit verdicts.
- `analysis.md` — Contains the scenario, calculations, model comparisons, observations, and recommendation.
- `screenshots/` — Contains actual estimator output, Ollama output, and model-card evidence.

## Run

```bash
python vram_estimate.py
```

## Submission

Push the complete assessment to GitHub and submit the repository URL.

Note: Memory values from the estimator are approximate. Actual model suitability must be verified against available system memory, runtime measurements, model capabilities, and the exact licence.