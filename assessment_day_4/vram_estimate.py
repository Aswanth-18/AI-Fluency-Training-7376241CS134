
"""Assessment Day 4: Memory estimator for a local coding assistant."""

BYTES_PER_PARAM = {
    "FP16": 2.00,
    "Q8_0": 1.00,
    "Q6_K": 0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}

KV_GB_PER_B_PER_1K = 0.02
OVERHEAD = 1.10

# Change this to the memory budget you want to evaluate.
AVAILABLE_GB = 8.0


def estimate(params_b, precision="Q4_K_M", context_k=8):
    """Return weights, KV cache and total estimated memory in GB."""

    if params_b <= 0:
        raise ValueError("Parameter count must be positive.")

    if context_k <= 0:
        raise ValueError("Context length must be positive.")

    if precision not in BYTES_PER_PARAM:
        raise ValueError("Unsupported precision.")

    weights_gb = params_b * BYTES_PER_PARAM[precision]
    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K
    total_gb = (weights_gb + kv_gb) * OVERHEAD

    return weights_gb, kv_gb, total_gb


def verdict(total_gb, available_gb):
    if total_gb <= available_gb * 0.7:
        return "Fits comfortably (estimate)"

    if total_gb <= available_gb:
        return "Fits, but tight (estimate)"

    return "Does NOT fit (estimate)"


def report(name, params_b, precision, context_k, available_gb):
    weights, kv, total = estimate(params_b, precision, context_k)

    print(
        f"{name:<22} "
        f"{params_b:>5.1f}B "
        f"{precision:<7} "
        f"{context_k:>3}K "
        f"{weights:>7.2f} GB "
        f"{kv:>7.2f} GB "
        f"{total:>7.2f} GB "
        f"{verdict(total, available_gb)}"
    )


def print_header():
    print(
        f"{'Model':<22} {'Params':>6} {'Precision':<7} "
        f"{'Context':>7} {'Weights':>10} {'KV cache':>10} "
        f"{'Total':>10} Verdict"
    )
    print("-" * 105)


def main():
    print(f"Scenario: Local AI Coding Assistant")
    print(f"Available memory budget: {AVAILABLE_GB:.1f} GB")
    print("All values are approximate estimates.\n")

    print("1. MODEL COMPARISON")
    print_header()

    configurations = [
        ("Small model", 1.5, "Q4_K_M", 8),
        ("Compact model", 3.0, "Q4_K_M", 8),
        ("Mid model", 7.0, "Q4_K_M", 8),
        ("8B Q4 model", 8.0, "Q4_K_M", 8),
        ("8B FP16 model", 8.0, "FP16", 8),
        ("14B Q4 model", 14.0, "Q4_K_M", 8),
    ]

    for name, params, precision, context in configurations:
        report(name, params, precision, context, AVAILABLE_GB)

    print("\n2. CONTEXT-LENGTH EXPERIMENT")
    print("Same 8B model, fixed Q4_K_M quantization.")
    print_header()

    for context in (4, 8, 16, 32):
        report("8B coding model", 8.0, "Q4_K_M",
               context, AVAILABLE_GB)

    print("\n3. QUANTIZATION EXPERIMENT")
    print("Same 8B model, fixed 8K context.")
    print_header()

    for precision in ("Q3_K_M", "Q4_K_M", "Q5_K_M", "Q8_0", "FP16"):
        report("8B coding model", 8.0, precision,
               8, AVAILABLE_GB)

    print("\n4. ESTIMATED FIT FOR A 6 GB BUDGET")
    report("Small model", 1.5, "Q4_K_M", 8, 6.0)
    report("Compact model", 3.0, "Q4_K_M", 8, 6.0)
    report("Mid model", 7.0, "Q4_K_M", 8, 6.0)


if __name__ == "__main__":
    main()
