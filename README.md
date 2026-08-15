# Cultural Validity in Persona-Based AI Evaluation: An Audit of MatrAIx

This repository contains the code, raw results, and audit framework accompanying the paper *"Cultural Validity in Persona-Based AI Evaluation: A Framework and Audit of MatrAIx"* by Bianca Dené Williams.

**Paper:** [arXiv link — add once posted]

## Overview

This work audits [MatrAIx](https://github.com/MatrAIx-ai/MatrAIx-Persona-8B), an open-source persona synthesis and evaluation framework, for cultural and linguistic validity. MatrAIx validates 10 behavioral/cognitive persona attributes through counterfactual testing, but identity attributes (cultural background, primary language) currently receive no equivalent validation.

We propose a nine-area audit framework for cultural validity in persona systems (full framework in `/audit/`) and run three counterfactual probes to test whether identity attributes produce valid, research-consistent behavioral variation or stereotype-amplified behavior.

## Repository Structure

```
.
├── README.md
├── audit/
│   └── cultural_validity_audit_framework.md   # Full 9-area audit document
├── probes/
│   ├── probe1_cultural_background.py          # Directness/hedging by cultural background
│   ├── probe2_language_label.py               # Language-label stereotype leakage
│   └── probe3_assertiveness.py                # Assertiveness by cultural background
├── results/
│   ├── probe1_cultural_background/
│   │   └── trial_results.jsonl                # n=20 raw trial outputs
│   ├── probe2_language_label/
│   │   └── trial_results.jsonl                # n=15 raw trial outputs
│   └── probe3_assertiveness/
│       └── trial_results.jsonl                # n=15 raw trial outputs
└── paper/
    └── cultural_validity_audit.md             # Full paper text
```

## Findings Summary

| Probe | Question | Finding |
|---|---|---|
| 1: Cultural Background | Does cultural_background affect communication directness? | Yes — Individualist personas showed ~70% direct assertion vs. ~10% for Collectivist personas; pattern aligns with Hofstede (2010) individualism-collectivism research |
| 2: Language Label | Does stated L1 alone affect task confidence, independent of proficiency? | Yes — Fulfulde-labeled persona showed markedly reduced task engagement and increased self-doubt vs. English/Mandarin, despite identical stated qualifications. Evidence of stereotype leakage tied to training-data representation. |
| 3: Assertiveness | Does the model resist stereotype flattening when cultural context is explicit in the task? | Partially — model showed active meta-awareness and resistance to caricature when cultural framing was explicit, unlike the implicit-label conditions in Probes 1–2 |

## Reproducing the Experiments

### Requirements

```bash
pip install anthropic
```

### Setup

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Run a probe

```bash
python probes/probe1_cultural_background.py
python probes/probe2_language_label.py
python probes/probe3_assertiveness.py
```

Each script writes raw JSONL results to `results/<probe_name>/trial_results.jsonl`.

### Notes on reproducibility

- All experiments used `claude-opus-4-8`. Results may vary across models and providers.
- Sample sizes (n=15–20 per probe) are adequate for identifying qualitative patterns but not for robust statistical inference. See paper Limitations section.
- Behavioral dimensions (directness, hedging, group reference, etc.) were coded through manual qualitative analysis. Structured coding protocols with inter-rater reliability are a priority for follow-up work.

## Relationship to MatrAIx

This audit is independent research using MatrAIx's publicly released Persona 1M dataset and open-source codebase. It is offered as collaborative quality assurance, not as a critique of MatrAIx's underlying architecture — the goal is to strengthen validation coverage for identity attributes using the same rigor MatrAIx already applies to behavioral attributes.

If you are part of the MatrAIx team and would like to discuss these findings or collaborate on extending validation coverage, please open an issue or reach out.

## Citation

If you use this audit framework, probe methodology, or results, please cite:

```bibtex
@article{williams2026culturalvalidity,
  title={Cultural Validity in Persona-Based AI Evaluation: A Framework and Audit of MatrAIx},
  author={Williams, Bianca Den{\'e}},
  year={2026},
  eprint={ADD_ARXIV_ID},
  archivePrefix={arXiv}
}
```

Please also cite MatrAIx:

```bibtex
@article{chang2026matraix,
  title={MatrAIx: Simulating the World with 8.3 Billion Persona Agents},
  author={Chang, Jianheng and Li, Xiaomin and Hao, Yuexing and Hou, Jianheng and Huang, Jintao and Wen, Qianfeng and Huang, Shirley and Liu, Yifan and Liu, Xiaoyi and Fan, Yilan and Wang, Yijun},
  year={2026},
  eprint={2608.04205},
  archivePrefix={arXiv}
}
```

## License

MIT
