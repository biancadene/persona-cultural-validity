# Cultural Stereotyping in Persona-Conditioned Language Models

Code, data, and paper for an independent audit of identity-attribute conditioning in [MatrAIx](https://arxiv.org/abs/2608.04205), an open-source persona-based AI evaluation framework.

**Paper:** [`paper/cultural_validity_audit_v6.pdf`](paper/cultural_validity_audit_v6.pdf) ([markdown source](paper/cultural_validity_audit_v6.md))
**DOI:** [10.5281/zenodo.21970218](https://doi.org/10.5281/zenodo.21970218)

## Overview

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. When those attributes include culture and language, the resulting behavior may reflect real cross-cultural variation or amplified stereotype, and most systems do not check which.

MatrAIx validates ten behavioral attributes (coding style, communication traits, register) through counterfactual persona-adherence testing. It validates no identity attribute. This work examines that gap from three directions: 1,175 behavioral trials across two model families, direct analysis of the system's schema and generative dependency graph, and cross-model replication.

The behavioral and structural evidence diverge, and that divergence is the central result. Cultural labels produce large behavioral effects. The persona system's design does not cause them.

## Findings

1,175 trials: 975 on `claude-opus-4-8` across four counterfactual probes, plus 200 on `gpt-4o` replicating Probe 1, with schema and dependency graph analysis.

| Probe | Question | Finding |
|---|---|---|
| **1: Cultural background, implicit framing** (n=200, Claude) | Does a cultural label shift communication behavior? | Yes, substantially. Direct assertion appeared in 96% of "Individualist (Western)" trials versus 24% for "Collectivist (East Asian)"; permission-seeking in 0% versus 60%. |
| **4: Framing isolation** (n=400, Claude) | Does framing salience moderate the effect, with task held constant? | Directionally yes, modestly. Both coding methods find the directness and permission-seeking gaps narrowing under a cultural reflection cue, but disagree on magnitude by roughly a factor of three (lexical 35% and 40%; blind judge 14% and 12%), and the judge finds two other dimensions widening. Not recommended as mitigation on this evidence. |
| **3: Cultural background, explicit framing** (n=200, Claude) | Same question, task-confounded | Same direction as Probe 4. Reported as supporting evidence only; Probe 4 exists to remove the confound. |
| **2: Language label** (n=175, Claude) | Does a native-language label affect task confidence? | No. Task engagement was 100% across all seven languages. Competence hedging did not order by training-data representation: Hindi (36%) exceeded Fulfulde (32%) and English (20%). |
| **Cross-model replication** (n=200, GPT-4o) | Does the Probe 1 effect transfer to another model? | In kind, not in detail. GPT-4o shows comparable separation across cultural values (28 pts directness, 52 pts group reference) but no detectable rank agreement with Claude on any dimension (Spearman rho between +0.48 and −0.35, all p > 0.2). |
| **Schema / dependency graph** | Do these effects originate in MatrAIx's design? | No. Across five identity dimensions there are zero edges to competence dimensions. No `cultural_background` edge differentiates cultural values by more than 0.0111, and the four edges carrying documented cross-cultural rationale differentiate them by exactly zero. There is no schema contribution to subtract. |

**Headline:** Cultural labels rendered into prompts produce large behavioral shifts that the persona schema does not cause and cannot prevent. The effect appears on both models tested; which label produces which behavior does not transfer between them. An audit performed on one model does not describe another.

**The stronger reading.** Two instruments that rank the same eight categories with correlations at or near zero on every dimension are not measuring a shared construct. Persona systems are nonetheless used as measurement instruments, on the assumption that a cultural label tracks something real about the population it names. This work found no evidence for that assumption and some against it. The paper develops this in section 4.5, and section 4.6 argues why it should be expected: the behaviors measured here (directness, deference, hedging, permission-seeking) are treated in politeness research as mitigation strategies selected by power distance, social distance, and size of imposition within a specific interaction, all of which a persona system can specify directly and none of which a cultural label captures.

## Two non-replications, reported in full

Both are kept visible rather than quietly removed, because the failure modes are instructive and they fail differently.

**The Fulfulde pilot.** An earlier version of this work led with a striking result: a persona labeled with a lower-resource native language disengaged from a technical task and questioned its own competence, in 3 of 5 trials. At n=25 the effect vanished. Task engagement was 100%, and a high-resource language (Hindi) hedged more. This is a sample-size failure. Five trials produced a pattern that did not exist.

**The orientation-bearing-labels claim.** Versions 3 through 5 of this paper argued that polarization concentrates in the two schema values naming a psychological orientation, "Individualist (Western)" and "Collectivist (East Asian)," and that this construct conflation supplies the specific lexical trigger for stereotyped output. On GPT-4o, Individualist ties for highest directness with two geographic values, Collectivist sits mid-range with three geographic values below it, and the extremes are South Asian and Middle Eastern. The claim is withdrawn in v6 and reported as a non-replication. This is a generalization failure. Two hundred trials produced a pattern that is real on that model and does not describe cultural labels as such.

Adequate sample size protects against the first failure and not at all against the second.

## Repository structure

```
.
├── paper/
│   ├── cultural_validity_audit_v6.md       # source
│   └── cultural_validity_audit_v6.pdf      # formatted, matches the Zenodo deposit
├── probes/
│   ├── probe1_expanded.py                  # 8 cultural values x 25, implicit framing
│   ├── probe2_expanded.py                  # 7 languages x 25, in/out-of-schema
│   ├── probe3_expanded.py                  # 8 cultural values x 25, explicit framing
│   ├── probe4_framing.py                   # 8 values x 2 cues x 25, task held constant
│   ├── probe1_cultural_background.py       # original pilot (n=10/condition)
│   ├── probe2_language_label.py            # original pilot (n=5/condition)
│   └── probe3_assertiveness.py             # original pilot (n=5/condition)
├── crossmodel_probe1.py                    # Probe 1 replication, OpenAI + Gemini
├── analyze_schema.py                       # schema and dependency graph analysis
├── analyze_lexical.py                      # deterministic marker coding
├── analyze_judge.py                        # LLM-judge rubric coding
├── analyze_probe4.py                       # Probe 4 lexical comparison
├── analyze_judge_probe4.py                 # Probe 4 judge comparison
├── compare_models.py                       # cross-model comparison
└── results/
    ├── probe1_expanded/                    # 200 trials + lexical + judge analysis
    ├── probe2_expanded/                    # 175 trials + lexical_analysis.json
    ├── probe3_expanded/                    # 200 trials + lexical_analysis.json
    ├── probe4_framing/                     # 400 trials + framing + judge analysis
    ├── crossmodel_probe1.jsonl             # raw cross-model trials, all providers
    ├── crossmodel_openai_norm.jsonl        # OpenAI trials, apostrophe-normalized
    ├── schema_analysis.json                # analyze_schema.py output
    └── [pilot result directories]
```

Raw trial outputs are JSONL, one response per line, including condition, trial number, model, and full text.

## Method

**Conditioning.** Personas are conditioned using MatrAIx's own phrase templates verbatim, from `persona/schema/dimensions.json`:

- `cultural_background` → `"with a {value} cultural frame"`
- `primary_language` → `"a native {value} speaker"`

Probe conditions use MatrAIx's exact schema values. All eight `cultural_background` values are tested. Six of twelve valid `primary_language` values are tested, plus Fulfulde as an out-of-schema control.

**Tasks are neutral.** Instructions never mention communication style, competence, or any measured dimension. Observed differences arise from persona conditioning alone.

**Coding is deterministic.** `analyze_lexical.py` counts seven marker categories defined a priori as regex sets, applied identically across conditions. No model judgment. Marker definitions are in the script and reproduced in the output JSON. This is crude by design, since it cannot capture meaning or implicature, but it is fully reproducible and free of judge bias.

An LLM-judge layer (`analyze_judge.py`) applies a 1 to 5 rubric across six dimensions. The judge sees only response text, never the condition label. Where the two methods diverge, the paper reports both and treats the more conservative estimate as primary.

**Models.** Probes 1 through 4 used `claude-opus-4-8` (975 trials, 0 errors). Cross-model replication used `gpt-4o` (200 trials, 0 errors). Both at default temperature, 300 max tokens. A Gemini replication was attempted and abandoned on quota exhaustion after 17 trials from a single condition; those trials are present in the raw JSONL but are not analyzed.

**One cross-model coding caveat.** GPT-4o emits typographic apostrophes (U+2019) in roughly a third of instances; Claude emitted none across 975 trials. Any regex marker containing a straight apostrophe therefore undercounts GPT-4o silently. Text is normalized before coding. Anyone doing cross-model lexical comparison should check this before trusting their numbers.

## Reproducing

```
pip install anthropic openai google-genai
```

```
$env:ANTHROPIC_API_KEY = "your-key"
$env:OPENAI_API_KEY = "your-key"
```

Run probes (each writes JSONL incrementally):

```
python probes/probe1_expanded.py
python probes/probe2_expanded.py
python probes/probe3_expanded.py
python probes/probe4_framing.py
```

Cross-model replication (checks provider access before spending quota, resumable):

```
python crossmodel_probe1.py --check
python crossmodel_probe1.py --provider openai
```

Analyze:

```
python analyze_lexical.py results/probe1_expanded/trial_results.jsonl cultural_background
python analyze_lexical.py results/probe2_expanded/trial_results.jsonl language
python analyze_lexical.py results/probe3_expanded/trial_results.jsonl cultural_background
python analyze_probe4.py results/probe4_framing/trial_results.jsonl
python analyze_lexical.py results/crossmodel_openai_norm.jsonl cultural_background
```

Optional LLM-judge layer (costs API credits; `--per-condition` caps trials):

```
python analyze_judge.py results/probe1_expanded/trial_results.jsonl cultural_background --per-condition 10
python analyze_judge_probe4.py results/probe4_framing/trial_results.jsonl --per-condition 10
```

Schema and dependency graph analysis (reproduces paper sections 3.5 and 3.6 from a local MatrAIx clone):

```
python analyze_schema.py /path/to/MatrAIx-Persona-8B --json results/schema_analysis.json
```

## Limitations

- **Lexical coding is crude.** Marker prevalence is not validated construct measurement. Responses may express deference or directness in phrasings outside the defined patterns.
- **Markers are not portable across models without validation.** Applied to GPT-4o, most categories functioned, but competence hedging returned 0% across all 200 trials through pattern mismatch rather than behavioral absence. Cross-model comparison needs per-model marker validation or a coding method less sensitive to surface phrasing.
- **Partial cross-model coverage.** Only Probe 1 was replicated. Probes 2, 3, and 4, including the framing manipulation, remain single-model results.
- **Rank comparison is underpowered.** Spearman correlations across eight values cannot distinguish weak association from none.
- **English only.** All interactions were in English, including for personas specified as native speakers of other languages.
- **No significance testing.** Descriptive rates only; no correction for multiple comparisons.
- **Partial schema coverage.** Five identity dimensions and the directed edge set. Other graph structures were not analyzed.
- **The situational-variable alternative is untested.** Power distance, social distance, and imposition size were not manipulated, so this work cannot show they predict the behavior better than a cultural label does. That comparison is the obvious next experiment.
- **Construct validity is assessed on a narrow base.** The argument rests on rank agreement between two models, on one probe, with one task. It establishes that construct validity has not been demonstrated, not that it is unattainable.

## Relationship to MatrAIx

This is independent research using MatrAIx's public repository and released schema. It is offered as collaborative quality assurance.

MatrAIx is the case study here, not the subject. The effects reported originate at generation time and are inherited by any system that renders an identity label into a prompt, whatever the quality of the schema supplying it: persona-based evaluation frameworks, synthetic user research, simulated-participant UX testing, agent systems with demographic character specifications. That MatrAIx's design turns out to be careful is what makes the dissociation visible. The paper's recommendations are split accordingly, into those for any system conditioning on identity attributes (section 6.1) and those specific to MatrAIx (section 6.2).

The findings are, on balance, favorable to MatrAIx's design: its dependency graph contains no identity-to-competence edges, its documented edges carry rationale and explicit epistemic hedging, and its cultural-background conditionals are near-uniform. The behavioral effects reported here are not caused by that design and would not be prevented by fixing it. They are inherited from whichever model renders the persona.

The MatrAIx-specific recommendations are narrow: extend the existing validation suite to identity attributes, separate cultural affiliation from cultural orientation in the schema as a representational matter, and either document or remove the 133 inert undocumented edges while confirming whether the uniformity of the four documented ones is deliberate.

## Citation

```bibtex
@misc{williams2026cleanschemas,
  title     = {Clean Schemas, Stereotyped Personas: Locating Cultural Bias in
               Persona-Conditioned Language Models},
  author    = {Williams, Bianca Den{\'e}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21970218},
  note      = {https://github.com/biancadene/persona-cultural-validity}
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
