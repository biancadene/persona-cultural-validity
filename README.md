# Cultural Stereotyping in Persona-Conditioned Language Models

Code, data, and paper for an independent audit of identity-attribute conditioning in [MatrAIx](https://github.com/MatrAIx-ai/MatrAIx-Persona-8B), an open-source persona-based AI evaluation framework.

**Paper:** [`paper/cultural_validity_audit_v3.md`](paper/cultural_validity_audit_v3.md)

## Overview

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. When those attributes include culture and language, the resulting behavior may reflect real cross-cultural variation or amplified stereotype — and most systems do not check which.

MatrAIx validates ten behavioral attributes (coding style, communication traits, register) through counterfactual persona-adherence testing. It validates no identity attribute. This work examines that gap from two directions: 575 behavioral trials, and direct analysis of the system's schema and generative dependency graph.

The two lines of evidence diverge. Cultural labels produce large behavioral effects. The persona system's design does not cause them.

## Findings

575 trials across three counterfactual probes, plus schema and dependency graph analysis.

| Probe | Question | Finding |
|---|---|---|
| **1: Cultural background, implicit framing** (n=200) | Does a cultural label shift communication behavior? | Yes, substantially. Direct assertion appeared in 96% of "Individualist (Western)" trials vs. 24% for "Collectivist (East Asian)"; permission-seeking in 0% vs. 60%. Polarization concentrates in the two schema values that name a psychological orientation. |
| **3: Cultural background, explicit framing** (n=200) | Does framing salience moderate the effect? | Yes. Foregrounding cultural context within the task halved the directness gap (72 → 36 points) and permission-seeking gap (60 → 32 points). Probes differ in task as well as framing, so this is suggestive rather than isolated. |
| **2: Language label** (n=175) | Does a native-language label affect task confidence? | **No.** Task engagement was 100% across all seven languages. Competence-hedging did not order by training-data representation — Hindi (36%) exceeded Fulfulde (32%) and English (20%). A pilot finding at n=5 suggesting competence suppression for Fulfulde **did not replicate**. |
| **Schema / dependency graph** | Do these effects originate in MatrAIx's design? | No. Across five identity dimensions there are zero edges to competence dimensions. 133 of 137 `cultural_background` edges are undocumented but functionally inert (max probability spread ≈0.011). |

**Headline:** Cultural labels rendered into prompts produce large behavioral shifts that the persona schema does not cause and cannot prevent. How identity is framed appears to moderate the effect.

### A note on the non-replication

An earlier version of this work led with a striking pilot result: a persona labeled with a lower-resource native language (Fulfulde) disengaged from a technical task and questioned its own competence, in 3 of 5 trials. At n=25 the effect vanished — task engagement was 100%, and a high-resource language (Hindi) hedged more.

That finding is reported in the paper as non-replicating. It is left visible rather than quietly removed, because the failure mode is instructive: small-n persona studies readily produce vivid, quotable results that do not survive expansion.

## Repository Structure

```
.
├── paper/
│   ├── cultural_validity_audit.md          # v1 (superseded — pre-schema-analysis)
│   └── cultural_validity_audit_v3.md       # current
├── probes/
│   ├── probe1_expanded.py                  # 8 cultural values × 25, implicit framing
│   ├── probe2_expanded.py                  # 7 languages × 25, in/out-of-schema
│   ├── probe3_expanded.py                  # 8 cultural values × 25, explicit framing
│   ├── probe1_cultural_background.py       # original pilot (n=10/condition)
│   ├── probe2_language_label.py            # original pilot (n=5/condition)
│   └── probe3_assertiveness.py             # original pilot (n=5/condition)
├── analyze_lexical.py                      # deterministic marker coding
├── analyze_judge.py                        # LLM-judge rubric coding (optional layer)
└── results/
    ├── probe1_expanded/                    # 200 trials + lexical_analysis.json
    ├── probe2_expanded/                    # 175 trials + lexical_analysis.json
    ├── probe3_expanded/                    # 200 trials + lexical_analysis.json
    ├── probe1_cultural_background/         # pilot results
    ├── probe2_language_label/              # pilot results
    └── probe3_assertiveness/               # pilot results
```

Raw trial outputs are JSONL, one response per line, including condition, trial number, model, and full text.

## Method

**Conditioning.** Personas are conditioned using MatrAIx's own phrase templates verbatim, from `persona/schema/dimensions.json`:
- `cultural_background` → `"with a {value} cultural frame"`
- `primary_language` → `"a native {value} speaker"`

Probe conditions use MatrAIx's exact schema values. All eight `cultural_background` values are tested. Six of twelve valid `primary_language` values are tested, plus Fulfulde as an out-of-schema control.

**Tasks are neutral.** Instructions never mention communication style, competence, or any measured dimension. Observed differences arise from persona conditioning alone.

**Coding is deterministic.** `analyze_lexical.py` counts seven marker categories defined a priori as regex sets, applied identically across conditions. No model judgment. Marker definitions are in the script and reproduced in the output JSON. This is crude by design — it cannot capture meaning or implicature — but it is fully reproducible and free of judge bias.

An optional LLM-judge layer (`analyze_judge.py`) applies a 1–5 rubric across six dimensions. The judge sees only response text, never the condition label.

**Model.** All 575 trials used `claude-opus-4-8`, default temperature, 300 max tokens. 575 successful, 0 errors.

## Reproducing

```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-key"
```

Run probes (each writes JSONL incrementally):

```bash
python probes/probe1_expanded.py
python probes/probe2_expanded.py
python probes/probe3_expanded.py
```

Analyze:

```bash
python analyze_lexical.py results/probe1_expanded/trial_results.jsonl cultural_background
python analyze_lexical.py results/probe2_expanded/trial_results.jsonl language
python analyze_lexical.py results/probe3_expanded/trial_results.jsonl cultural_background
```

Optional LLM-judge layer (costs API credits; `--per-condition` caps trials):

```bash
python analyze_judge.py results/probe1_expanded/trial_results.jsonl cultural_background --per-condition 10
```

Schema analysis was performed directly against a local clone of the MatrAIx repository. Queries are documented in the paper, §2.3 and §3.5.

## Limitations

- **Lexical coding is crude.** Marker prevalence is not validated construct measurement. Responses may express deference or directness in phrasings outside the defined patterns.
- **The framing comparison is confounded.** Probes 1 and 3 differ in task as well as framing. A clean test would hold the task fixed.
- **Single model, single provider.** Effects attributed to model priors need cross-provider replication.
- **English only.** All interactions were in English, including for personas specified as native speakers of other languages.
- **No significance testing.** Descriptive rates only; no correction for multiple comparisons.
- **Partial schema coverage.** Five identity dimensions and the directed edge set. Other graph structures were not analyzed.

## Relationship to MatrAIx

This is independent research using MatrAIx's public repository and released schema. It is offered as collaborative quality assurance.

The findings are, on balance, favorable to MatrAIx's design: its dependency graph contains no identity-to-competence edges, its documented edges carry rationale and explicit epistemic hedging, and its cultural-background conditionals are near-uniform. The behavioral effects reported here are not caused by that design and would not be prevented by fixing it.

The recommendations that follow are narrow: extend the existing validation suite to identity attributes, separate cultural affiliation from cultural orientation in the schema, and either document or remove 133 inert undocumented edges.

## Citation

```bibtex
@misc{williams2026framing,
  title  = {Framing Salience Moderates Cultural Stereotyping in Persona-Conditioned
            Language Models: A Schema-Level and Behavioral Audit},
  author = {Williams, Bianca Den{\'e}},
  year   = {2026},
  note   = {https://github.com/biancadene/cultural-validity-audit-matraix}
}
```

Please also cite MatrAIx:

```bibtex
@article{chang2026matraix,
  title  = {MatrAIx: Simulating the World with 8.3 Billion Persona Agents},
  author = {Chang, Jianheng and Li, Xiaomin and Hao, Yuexing and Huang, Jintao
            and Wen, Qianfeng and Huang, Shirley and Liu, Yifan and Liu, Xiaoyi
            and Fan, Yilan and Wang, Yijun},
  year   = {2026},
  eprint = {2608.04205},
  archivePrefix = {arXiv}
}
```

## License

MIT
