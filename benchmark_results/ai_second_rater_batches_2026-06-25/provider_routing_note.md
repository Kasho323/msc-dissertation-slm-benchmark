# AI Second-Rater Provider Routing Note

**Date:** 2026-06-25

The installed `claude.cmd` client reported an authenticated session, but the user-level Claude settings configured an Anthropic-compatible endpoint at Xiaomi MiMo. As a result, batch 01 was processed by `mimo-v2.5-pro`, not by an Anthropic Claude model.

Actions taken:

1. Processing stopped after the first 30 anonymous rows.
2. No model identity key or personal data was included in the exported rows.
3. The first-batch results are quarantined and must not be described as Claude ratings.
4. A test that excluded the user-level endpoint returned HTTP 401, confirming that direct Anthropic authentication is not currently available.
5. No remaining batch should be submitted until the second-rater provider is explicitly selected.

The batch 01 output may be used only if Xiaomi MiMo is explicitly approved as the AI second rater. Otherwise, it should be replaced.
