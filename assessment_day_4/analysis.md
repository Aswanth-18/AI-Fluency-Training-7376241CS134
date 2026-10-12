# Assessment Day 4: Will It Fit, and May I Use It?

## 1. Scenario

The selected scenario is a local AI coding assistant for college students. It should explain Python programs, identify common programming errors, and generate simple code examples.

The target machine is a laptop with 8 GB of system RAM and no dedicated GPU assumed. The application is intended for individual educational use, with a possible future public GitHub release.

The memory budget is 8 GB in total, although the actual memory available to the model will be lower because the operating system and other applications also use RAM.

## 2. Concepts

### 2.1 Model Weights

Model weights store the learned parameters of a language model. Their approximate memory requirement depends on the number of parameters and the number of bytes used to represent each parameter.

The estimator uses:

Weights (GB) = Parameters (billions) × Bytes per parameter.

For an 8B model at Q4_K_M, the estimated weight memory is 8 × 0.57 = 4.56 GB.

Ignoring weight memory can lead to selecting a model that cannot load on the target machine. This formula is approximate because actual model files also contain metadata and other information.

### 2.2 Quantization

Quantization reduces the memory required to store model parameters by using fewer bits per parameter.

The estimator uses 0.57 bytes per parameter for Q4_K_M and 2 bytes per parameter for FP16. For an 8B model, this changes the estimated weight memory from 16 GB to 4.56 GB.

Quantization makes larger models more practical on limited hardware, but it may reduce output quality. The actual quality impact depends on the model, quantization method, and task.

### 2.3 KV Cache and Context Length

The KV cache stores intermediate attention information needed while processing a conversation. Its memory requirement increases with the context length.

The lab's approximate formula is:

KV cache (GB) = Parameters (billions) × Context (in thousands of tokens) × 0.02.

For an 8B model with an 8K context, the estimated KV cache is 8 × 8 × 0.02 = 1.28 GB.

When context length increases, weight memory stays constant while the KV cache increases. This matters when the coding assistant reads long source files or keeps adding previous questions and tool results to its conversation.

### 2.4 Model Cards

A model card provides information about a model's publisher, intended uses, limitations, context length, and sometimes its supported capabilities.

The official model card must be checked before selecting a model for the coding assistant. The exact version, tool-calling documentation, licence, and model size should be recorded.

Ignoring model-card information can lead to choosing a model that is unsuitable for coding, lacks documented tool-calling support, or has usage restrictions.

### 2.5 Open-Weight and Open-Source Licensing

Open-weight models make trained weights available, but this does not automatically mean the model is open-source under every definition or freely usable for every purpose.

The exact licence determines whether commercial use, redistribution, modification, and public deployment are allowed and whether extra conditions apply.

For this project, licence suitability must be checked against the intended educational use and possible public GitHub release. If the licence is unclear, the model should not be treated as automatically approved for use.

## 3. Memory Estimate Table

The Python estimator uses the Day 4 formula and evaluates six model configurations against an 8 GB budget.

Paste the actual output table from `vram_estimate.py` here.

| Model configuration | Parameters | Precision | Context | Estimated total | Fits estimated budget? |
|---|---:|---|---:|---:|---|
| Small model | 1.5B | Q4_K_M | 8K | 1.20 GB | Yes |
| Compact model | 3B | Q4_K_M | 8K | 2.41 GB | Yes |
| Mid model | 7B | Q4_K_M | 8K | 5.62 GB | Yes, with limited headroom |
| 8B model | 8B | Q4_K_M | 8K | 6.42 GB | Tight |
| 8B model | 8B | FP16 | 8K | 19.01 GB | No |
| 14B model | 14B | Q4_K_M | 8K | 11.24 GB | No |

These are formula-based estimates, not proof that a model will run successfully on the laptop.

## 4. Model Comparison

Compare at least three models from different families: Qwen, Mistral, and IBM Granite.

Record the following for each exact model version:

- Full model name and publisher.
- Total parameters and active parameters, if applicable.
- Context window.
- Exact licence name and conditions.
- Whether commercial use and redistribution are permitted.
- Whether tool calling is explicitly documented.
- Whether an Ollama or GGUF build is available.
- Actual Q4 download size.
- Estimated total memory for the chosen context.
- Whether it is suitable for the target laptop.
- Official model-card URL and date checked.

Use verified model-card and Ollama information to fill in the comparison table. Do not infer a licence from the model's family name.

## 5. Context-Length Experiment

For the same 8B Q4_K_M model, the estimated memory changes as follows:

| Context | Weights | KV cache | Total |
|---|---:|---:|---:|
| 4K | 4.56 GB | 0.64 GB | 5.72 GB |
| 8K | 4.56 GB | 1.28 GB | 6.42 GB |
| 16K | 4.56 GB | 2.56 GB | 7.83 GB |
| 32K | 4.56 GB | 5.12 GB | 10.65 GB |

The weights remain constant, but the KV cache increases as the context grows. At 32K, the estimated memory exceeds the 8 GB budget. Therefore, a smaller context may be more practical on the target laptop.

## 6. Quantization Experiment

For the same 8B model at an 8K context:

| Precision | Weights | KV cache | Total |
|---|---:|---:|---:|
| Q3_K_M | 3.44 GB | 1.28 GB | 5.19 GB |
| Q4_K_M | 4.56 GB | 1.28 GB | 6.42 GB |
| Q5_K_M | 5.44 GB | 1.28 GB | 7.39 GB |
| Q8_0 | 8.00 GB | 1.28 GB | 10.21 GB |
| FP16 | 16.00 GB | 1.28 GB | 19.01 GB |

Quantization changes the estimated weight memory while the KV cache remains constant in this experiment. Q4_K_M is a reasonable starting point for balancing memory use and quality, but a smaller model may be more practical when Windows and other applications need part of the available RAM.

## 7. Estimate Versus Reality

Record the output of `ollama list` and `ollama ps` for a model actually installed on a machine.

Explain whether the measured memory is close to the estimate. Differences can result from the actual quantized build, the context size used by the runner, architecture-specific KV cache requirements, and runtime overhead.

The processor information indicates whether the model is using CPU, GPU, or a split configuration. A model running entirely on the CPU may be usable but slower than one that fits in suitable GPU memory.

Insert your actual terminal observations here. If measurements are collected on another machine, identify that machine rather than presenting its results as your own.

## 8. Suitability Analysis

The final recommendation should name the selected model, exact version, quantization, context length, and licence.

The model must be small enough for the practical memory budget, sufficiently capable for basic programming assistance, and licensed for the intended use.

Name a runner-up and explain why it was not selected. State what change in available memory, context requirements, tool-calling needs, or distribution plans would change the recommendation.

Finalize this section only after verifying the model cards and comparing the measured memory against the estimates.

## 9. Conclusion

Memory and licensing are both essential when choosing an open model. Parameter count and quantization determine weight memory, while context length changes the KV cache requirement. The estimate helps reject unsuitable configurations before downloading them, but actual runtime measurements are necessary to verify that a model fits.

For a laptop with limited memory, model size and quantization may be the deciding factors. For an application released publicly or used commercially, licence permissions and redistribution conditions may be decisive even when the model fits comfortably.

The recommended model should therefore balance memory, quality, context length, documented capabilities, and licence compatibility with the intended use.