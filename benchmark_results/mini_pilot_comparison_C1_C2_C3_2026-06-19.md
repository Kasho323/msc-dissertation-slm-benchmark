# Controlled Mini Pilot Comparison

**Date:** 2026-06-19  
**Question set:** Q001-Q005 from the open-document benchmark set  
**Corpus:** D1-D4 final benchmark corpus  
**Backend settings:** `k=10`, `n=3`, `temperature=0.2`, `max_tokens=200`  
**llama-server flags:** `--ctx-size 4096 --parallel 1 --cache-ram 0 --no-cache-prompt --ctx-checkpoints 0`

This comparison uses the controlled C1 rerun, not the earlier default-server C1 pilot.

## Summary Table

| Config | Model | Mean Quality / 5 | Mean Latency (s) | Mean Memory (MiB) | Mean Tokens/s | Main Takeaway |
|---|---|---:|---:|---:|---:|---|
| C1 | Qwen2.5 0.5B Instruct Q4_K_M | 3.07 | 3.787 | 461.73 | 102.94 | Fastest and lightest, but has a severe provenance-question failure. |
| C2 | Llama 3.2 1B Instruct Q4_K_M | 2.83 | 5.180 | 884.77 | 74.24 | Makes terminology/conceptual errors despite larger model size. |
| C3 | Gemma 3 1B IT Q4_K_M | 3.67 | 5.910 | 866.92 | 60.37 | Best quality in this pilot, but slowest. |

## Interpretation

The mini pilot supports the dissertation's intended trade-off framing:

- C1 is the deployment-friendly option: low memory, fast responses, acceptable quality on several questions, but not robust.
- C2 does not clearly outperform C1 in this small sample and introduces terminology errors.
- C3 currently looks strongest for answer quality, especially for provenance-style explanation questions.

## Methodology Notes

The model server was started separately for each configuration and stopped after that model's five-question run. The backend and Streamlit frontend stayed running. The corpus was already loaded into the in-memory ChromaDB backend before these runs.

The earlier C2/C3 launch issue was caused by the model server being started inside a short-lived command context. The working method is to start `llama-server`, wait for `/health`, run the pilot immediately, then stop that model server before switching configurations.

## Next Decision

Before the full 40-question benchmark, confirm whether the final protocol should use the same llama-server flags shown above. This would make all configurations more comparable and avoids model-specific default context lengths.

