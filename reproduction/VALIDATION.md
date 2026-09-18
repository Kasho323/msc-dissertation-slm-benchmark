# Reproduction validation — 18 September 2026

This release improves access and portability after submission. It does not
change the dissertation or the experimental evidence.

## Checks actually performed

| Check | Result |
|---|---|
| Original repository backup | Complete Git bundle retained locally before editing |
| Dissertation DOCX/PDF and protected historical records | 1,375 file hashes checked; zero changes |
| Historical credential scan | 1,402 reachable Git blobs scanned for private keys and common credential formats; no matches (not a guarantee against every possible secret) |
| Python / supported PowerShell entry points | Syntax checks passed |
| Main check using only Python standard library | Passed |
| Clean, independently named checkout directory (including spaces) | All retained-file and numerical checks passed |
| New isolated Python 3.10 environment | Pinned analysis packages installed from package index; full analysis passed |
| Final observations | 720 raw JSON responses, 6 x 40 x 3 answer records, no recorded errors |
| Rating coverage | 240 unique AI-rated answers, 30 matched independent human-rated answers |
| Regenerated tables | System summary, blinding key and quality table match retained CSV contents |
| Human-AI association | Spearman rho 0.7992658480979864 reproduced |
| Agreement intervals | Original 20,000-resample analysis executed successfully |
| Q2 truncation sensitivity | Original 32/8-question subset analysis executed successfully |
| Q035 exclusion | C5 3.4487179487, C6 3.4358974359; small ordering reversal reproduced |
| Corpus | All four retained PDF SHA-256 values checked |
| D1 source download | Official arXiv v4 download matches the benchmark PDF byte for byte |
| GGUF files | All six local files match current Appendix A SHA-256 values |
| Experiment dependency consistency | Existing Windows Python 3.10 environment: `pip check` passed |
| Live end-to-end smoke test | C1, Q001, one repetition, four PDFs uploaded; completed with zero errors |

The smoke test used the pinned upstream backend already installed locally and
the retained model files. It exercised the supported portable runner and its
explicit `-AppDir` / `-LlamaDir` arguments. Its output is separate from the June
dataset. This release did **not** rerun all 720 generations, install the entire
large backend environment from scratch, or obtain new human/AI ratings.
Fresh analysis installation and existing-backend execution are different checks.

## File integrity and line endings

`provenance/retained_files_sha256.json` lists 1,347 retained evidence files.
Each value is an array of accepted SHA-256 hashes: the original Git blob and,
where different, its original Windows working-copy representation. The 1,290
differences between those representations were independently checked to be
**CRLF versus LF only**. Both hashes are retained rather than rewriting original
evidence to satisfy a check. Binary files use exact hashes. `.gitattributes`
prevents further line-ending conversion of the retained evidence on checkout.
This is an integrity check, not a new claim about source authenticity.

## Known boundaries

- Original retrieval-model revision IDs were not logged. The retained local
  retrieval-model files are now hashed, but their revision is not invented.
- The upstream application is pinned by commit and fetched from its own repo;
  it was not relicensed or copied into this repository.
- Corpus snapshots are historical research inputs. Dynamic websites are not
  silently substituted, and old ICO guidance is not presented as current advice.
- Timings and RSS are observations on the recorded laptop. A new run need not
  reproduce them exactly; fixed seeds do not guarantee all software/hardware
  combinations yield identical outputs.
- Statistical reproduction uses archived ratings. It is not a claim that a
  current external AI judge or a new human rater would assign identical scores.
- Historical runbooks and writing notes remain dated evidence. The supported
  entry points are the root README and `reproduction/EXPERIMENTS.md`.

The original 1,403-file state remains accessible at commit
`9dfe890bf1fa9071bca3c7693a03fa75a533a4c4`. The extra public-reproduction files
do not retroactively change the dissertation's inventory count.
