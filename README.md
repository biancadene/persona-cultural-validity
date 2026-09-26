# Cultural Stereotyping in Persona-Conditioned Language Models

Code, data, and two papers from an independent audit of identity-attribute conditioning in [MatrAIx](https://arxiv.org/abs/2608.04205), an open-source persona-based AI evaluation framework.

**Paper 1:** [10.5281/zenodo.21970217](https://doi.org/10.5281/zenodo.21970217) — *Clean Schemas, Stereotyped Personas: Locating Cultural Bias in Persona-Conditioned Language Models*
**Paper 2:** [10.5281/zenodo.22983112](https://doi.org/10.5281/zenodo.22983112) — *Situational Variables Versus Cultural Labels in Persona Conditioning: Shared Stereotype, Shared Rule*

## Overview

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. When those attributes include culture and language, the resulting behavior may reflect real cross-cultural variation or amplified stereotype, and most systems do not check which.

MatrAIx validates ten behavioral attributes (coding style, communication traits, register) through counterfactual persona-adherence testing. It validates no identity attribute. The first paper examines that gap from three directions: 1,175 behavioral trials across two model families, direct analysis of the system's schema and generative dependency graph, and cross-model replication. It finds that cultural labels produce large behavioral effects and that the persona system's design does not cause them.

The second paper tests the alternative the first one named: replace the cultural label with the three situational variables politeness theory holds responsible for the behaviors measured. It finds that situational variables reproduce the politeness range without the competence stereotype, that adding situational context to a label does not remove the stereotype, and that the first paper's finding of no cross-model agreement was an instrument artifact. The stereotype is shared across models.

## Paper 1: Clean Schemas, Stereotyped Personas

1,175 trials: 975 on `claude-opus-4-8` across four counterfactual probes, plus 200 on `gpt-4o` replicating Probe 1, with schema and dependency graph analysis.

| Probe | Question | Finding |
|---|---|---|
| **1: Cultural background, implicit framing** (n=200, Claude) | Does a cultural label shift communication behavior? | Yes, substantially. Direct assertion appeared in 96% of "Individualist (Western)" trials versus 24% for "Collectivist (East Asian)"; permission-seeking in 0% versus 60%. |
| **4: Framing isolation** (n=400, Claude) | Does framing salience moderate the effect, with task held constant? | Directionally yes, modestly. Both coding methods find the directness and permission-seeking gaps narrowing under a cultural reflection cue, but disagree on magnitude by roughly a factor of three (lexical 35% and 40%; blind judge 14% and 12%), and the judge finds two other dimensions widening. Not recommended as mitigation on this evidence. |
| **3: Cultural background, explicit framing** (n=200, Claude) | Same question, task-confounded | Same direction as Probe 4. Reported as supporting evidence only; Probe 4 exists to remove the confound. |
| **2: Language label** (n=175, Claude) | Does a native-language label affect task confidence? | No. Task engagement was 100% across all seven languages. Competence hedging did not order by training-data representation: Hindi (36%) exceeded Fulfulde (32%) and English (20%). |
| **Cross-model replication** (n=200, GPT-4o) | Does the Probe 1 effect transfer to another model? | In kind, not in detail under lexical coding. GPT-4o shows comparable separation across cultural values (28 pts directness, 52 pts group reference) but no detectable rank agreement with Claude on any dimension (Spearman rho between +0.48 and −0.35, all p > 0.2). **Paper 2 revises this: re-judged, rank agreement is present. See below.** |
| **Schema / dependency graph** | Do these effects originate in MatrAIx's design? | No. Across five identity dimensions there are zero edges to competence dimensions. No `cultural_background` edge differentiates cultural values by more than 0.0111, and the four edges carrying documented cross-cultural rationale differentiate them by exactly zero. There is no schema contribution to subtract. |

**Headline:** Cultural labels rendered into prompts produce large behavioral shifts that the persona schema does not cause and cannot prevent. The effect appears on both models tested.

**Section 4.6 of the first paper** argues why: the behaviors measured (directness, deference, hedging, permission-seeking) are treated in politeness research (Brown & Levinson, 1987) as mitigation strategies selected by power distance, social distance, and size of imposition within a specific interaction, all of which a persona system can specify directly and none of which a cultural label captures. The second paper tests this.

### Two non-replications, reported in full

Both are kept visible rather than quietly removed, because the failure modes are instructive and they fail differently.

**The Fulfulde pilot.** An earlier version of this work led with a striking result: a persona labeled with a lower-resource native language disengaged from a technical task and questioned its own competence, in 3 of 5 trials. At n=25 the effect vanished. Task engagement was 100%, and a high-resource language (Hindi) hedged more. This is a sample-size failure. Five trials produced a pattern that did not exist.

**The orientation-bearing-labels claim.** Versions 3 through 5 of this paper argued that polarization concentrates in the two schema values naming a psychological orientation, "Individualist (Western)" and "Collectivist (East Asian)," and that this construct conflation supplies the specific lexical trigger for stereotyped output. On GPT-4o, Individualist ties for highest directness with two geographic values, Collectivist sits mid-range with three geographic values below it, and the extremes are South Asian and Middle Eastern. The claim is withdrawn and reported as a non-replication. This is a generalization failure. Two hundred trials produced a pattern that is real on that model and does not describe cultural labels as such.

Adequate sample size protects against the first failure and not at all against the second.

## Paper 2: Situational Variables Versus Cultural Labels

The first paper named an untested alternative: Brown and Levinson's situational variables of power distance, social distance, and imposition size. The second paper tests it by replacing the eight cultural labels with eight situational profiles (2 × 2 × 2), holding task, models, trial count, and coders constant. Four further conditions extend the comparison.

| Condition | Question | Finding |
|---|---|---|
| **Probe 5: situational profiles** (n=200 each, both models) | Do situational variables reproduce the politeness range cultural labels produced? | On Claude, yes, at 65 to 100% of cultural-label spread on directness, hedging, and permission-seeking, and without the self-doubt and task-engagement differential cultural labels carried. Power distance and social distance move every politeness dimension in the predicted direction. On GPT-4o, deference responds to power and imposition; directness and hedging do not move. |
| **No-persona control** (n=50 each, both models) | Where does each model sit unconditioned? | Claude's baseline sits inside the situational range on every dimension; cultural labels push past it. GPT-4o becomes more cautious under any persona clause at all. |
| **Probes 6 and 6b: label + situational profile** (n=200 each, Claude) | Does specifying the situation neutralize the label? | No. Under a high-stakes profile the label is amplified: five of eight labels reach deference of 4.80 or above where the profile alone gives 3.30. Under a low-stakes profile the Collectivist persona still defers at 3.70 where the profile alone gives 2.10. |
| **Cross-model rank agreement, cultural labels, re-judged** | Do the two models agree on which labels produce which behavior? | Yes. Under judge coding, rho is 0.51 to 0.85 on five of six dimensions, confirmed by a second judge on deference (0.70) and group orientation (0.88). The first paper's lexical null was an instrument artifact. |
| **Cross-model rank agreement, situational profiles** | Do the two models agree on which situations produce which behavior? | On deference only (0.71 Claude judge, 0.57 GPT-4o judge). Nothing else. |

**Headline:** Cultural labels transfer a shared stereotype across models. Both rank Collectivist (East Asian) as least direct and least engaged, Individualist (Western) as most direct and among the most engaged. Situational profiles transfer one shared rule: high power and high stakes produce deference. Adding situational context to a label does not remove the stereotype. Removing the label does.

**Correction to the first paper.** The first paper reported no cross-model rank agreement under cultural labels (lexical rho +0.48 to −0.35). Re-judged with the same rubric, agreement is present on five of six dimensions. The lexical instrument, developed against Claude output, undercounted GPT-4o phrasing and could not detect it. The stereotype is shared, not model-specific, which makes the cultural-label problem worse than the first paper said: a model-specific stereotype could be avoided by switching models. A shared one cannot.

**Methods finding.** GPT-4o as a second judge at temperature 0 collapsed to the rubric midpoint on hedging and to the ceiling on task engagement across nearly every condition. It discriminated on deference, group orientation, and self-doubt only. Two LLM judges applied to the same rubric can differ this much, and the difference is invisible until both are run.

**One unresolved result.** On Claude, a larger imposition makes the persona more direct and less hedging, the opposite of what Brown and Levinson predict, while also making it more deferential as predicted. Both judges see the directness reversal. The paper offers two readings and tests neither.

### Judge stability

The Claude judge was run three times per file (twice for Probe 1 Claude, credits exhausted). No cell moved more than 0.30 on a 5-point scale across runs. Averaged outputs are in `results/*_judge_avg.json`; individual runs in `results/*_judge_avg_run{1,2,3}.json`.

## Repository structure

```
.
├── paper/
│   ├── cultural_validity_audit_v7.md          # Paper 1, source
│   ├── cultural_validity_audit_v7.pdf         # Paper 1, matches Zenodo deposit
│   ├── situational_vs_cultural_v1.md          # Paper 2, source
│   └── situational_vs_cultural_v1.pdf         # Paper 2, matches Zenodo deposit
├── probes/
│   ├── probe1_expanded.py                     # 8 cultural values x 25, implicit framing
│   ├── probe2_expanded.py                     # 7 languages x 25, in/out-of-schema
│   ├── probe3_expanded.py                     # 8 cultural values x 25, explicit framing
│   ├── probe4_framing.py                      # 8 values x 2 cues x 25, task held constant
│   ├── probe5_situational.py                  # 8 B&L situational profiles x 25
│   ├── probe6_grounding.py                    # 8 labels + high-stakes profile x 25
│   ├── probe6b_grounding_lowstakes.py         # 8 labels + low-stakes profile x 25
│   ├── probe1_cultural_background.py          # original pilot (n=10/condition)
│   ├── probe2_language_label.py               # original pilot (n=5/condition)
│   └── probe3_assertiveness.py                # original pilot (n=5/condition)
├── crossmodel_probe1.py                       # Probe 1 replication, OpenAI + Gemini
├── crossmodel_probe5.py                       # Probe 5 replication, OpenAI
├── control_noPersona.py                       # no-persona baseline, both models
├── analyze_schema.py                          # schema and dependency graph analysis
├── analyze_lexical.py                         # deterministic marker coding
├── analyze_judge.py                           # LLM-judge rubric coding, Claude
├── analyze_judge_gpt.py                       # LLM-judge rubric coding, GPT-4o, temp 0
├── judge_stability.py                         # N judge runs, saved and averaged
├── analyze_rank_effects.py                    # Spearman rho and factorial main effects
├── analyze_probe4.py                          # Probe 4 lexical comparison
├── analyze_judge_probe4.py                    # Probe 4 judge comparison
├── compare_models.py                          # cross-model lexical comparison, Probe 1
├── requirements.txt
├── LICENSE
└── results/
    ├── probe1_expanded/                       # 200 trials + lexical analysis
    ├── probe2_expanded/                       # 175 trials + lexical_analysis.json
    ├── probe3_expanded/                       # 200 trials + lexical_analysis.json
    ├── probe4_framing/                        # 400 trials + framing + judge analysis
    ├── probe5_situational/                    # 200 trials + lexical analysis
    ├── probe6_grounding/                      # 200 trials + lexical + judge analysis
    ├── probe6b_grounding_lowstakes/           # 200 trials + lexical + judge analysis
    ├── control/                               # 50 trials per model + lexical + judge
    ├── crossmodel_probe1.jsonl                # raw Probe 1 cross-model trials
    ├── crossmodel_openai_norm.jsonl           # Probe 1 GPT-4o, apostrophe-normalized
    ├── crossmodel_probe5.jsonl                # raw Probe 5 cross-model trials
    ├── crossmodel_probe5_openai_norm.jsonl    # Probe 5 GPT-4o, apostrophe-normalized
    ├── probe1_claude_judge_avg_run{1,2}.json  # Claude judge, Probe 1 Claude, 2 runs
    ├── probe1_gpt4o_judge_avg.json            # Claude judge, Probe 1 GPT-4o, 3-run avg
    ├── probe5_claude_judge_avg.json           # Claude judge, Probe 5 Claude, 3-run avg
    ├── probe5_gpt4o_judge_avg.json            # Claude judge, Probe 5 GPT-4o, 3-run avg
    ├── probe1_claude_gptjudge.json            # GPT-4o judge, Probe 1 Claude
    ├── probe1_gpt4o_gptjudge.json             # GPT-4o judge, Probe 1 GPT-4o
    ├── probe5_claude_gptjudge.json            # GPT-4o judge, Probe 5 Claude
    ├── probe5_gpt4o_gptjudge.json             # GPT-4o judge, Probe 5 GPT-4o
    ├── rank_effects_analysis.json             # Spearman rho and main effects
    ├── cross_model_comparison.json            # Probe 1 lexical cross-model
    ├── schema_analysis.json                   # analyze_schema.py output
    └── [pilot result directories]
```

Raw trial outputs are JSONL, one response per line, including condition, trial number, model, and full text.

## Method

**Conditioning.** Personas are conditioned using MatrAIx's own phrase templates verbatim, from `persona/schema/dimensions.json`:

- `cultural_background` → `"with a {value} cultural frame"`
- `primary_language` → `"a native {value} speaker"`

Probe conditions use MatrAIx's exact schema values. All eight `cultural_background` values are tested. Six of twelve valid `primary_language` values are tested, plus Fulfulde as an out-of-schema control.

**Situational conditioning (Paper 2).** Probe 5 replaces the cultural frame clause with three descriptors, one per Brown and Levinson variable, each at one of two levels. No descriptor names a measured behavior. Probes 6 and 6b append a fixed situational profile to the cultural frame clause. The task sentence is identical across all probes.

**Tasks are neutral.** Instructions never mention communication style, competence, or any measured dimension. Observed differences arise from persona conditioning alone.

**Coding is deterministic.** `analyze_lexical.py` counts seven marker categories defined a priori as regex sets, applied identically across conditions. No model judgment. Marker definitions are in the script and reproduced in the output JSON. This is crude by design, since it cannot capture meaning or implicature, but it is fully reproducible and free of judge bias.

An LLM-judge layer applies a 1 to 5 rubric across six dimensions. The judge sees only response text, never the condition label. Paper 1 used Claude as judge, run once. Paper 2 uses two judges: Claude at default temperature, run three times and averaged (`judge_stability.py`), and GPT-4o at temperature 0, run once (`analyze_judge_gpt.py`). Where the two methods diverge, the papers report both and treat the more conservative estimate as primary.

**Models.** All probes used `claude-opus-4-8` for the primary model. Cross-model replication used `gpt-4o`. Both at default temperature, 300 max tokens. A Gemini replication was attempted for Probe 1 and abandoned on quota exhaustion after 17 trials from a single condition; those trials are present in the raw JSONL but are not analyzed.

**One cross-model coding caveat.** GPT-4o emits typographic apostrophes (U+2019) in roughly a third of instances; Claude emitted none. Any regex marker containing a straight apostrophe therefore undercounts GPT-4o silently. Text is normalized before coding. Anyone doing cross-model lexical comparison should check this before trusting their numbers.

**Judge output overwrite caveat.** `analyze_judge.py` writes `judge_analysis.json` into the source file's folder and overwrites on rerun. Files in `results/` directly (the cross-model JSONLs) share one output path. Use `judge_stability.py` or `analyze_judge_gpt.py --out` to preserve individual runs.

## Reproducing

```
pip install -r requirements.txt
```

```
$env:ANTHROPIC_API_KEY = "your-key"
$env:OPENAI_API_KEY = "your-key"
```

### Paper 1

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

Schema and dependency graph analysis (reproduces Paper 1 sections 3.5 and 3.6 from a local MatrAIx clone):

```
python analyze_schema.py /path/to/MatrAIx-Persona-8B --json results/schema_analysis.json
```

### Paper 2

Run probes:

```
python probes/probe5_situational.py
python crossmodel_probe5.py --check
python crossmodel_probe5.py
python control_noPersona.py
python probes/probe6_grounding.py
python probes/probe6b_grounding_lowstakes.py
```

Lexical analysis:

```
python analyze_lexical.py results/probe5_situational/trial_results.jsonl condition
python analyze_lexical.py results/crossmodel_probe5_openai_norm.jsonl condition
python analyze_lexical.py results/control/claude_trial_results.jsonl condition
python analyze_lexical.py results/control/openai_trial_results_norm.jsonl condition
python analyze_lexical.py results/probe6_grounding/trial_results.jsonl cultural_background
python analyze_lexical.py results/probe6b_grounding_lowstakes/trial_results.jsonl cultural_background
```

Primary judge, three runs averaged (240 Claude calls per file):

```
python judge_stability.py results/probe5_situational/trial_results.jsonl condition --runs 3 --out results/probe5_claude_judge_avg.json
python judge_stability.py results/crossmodel_probe5_openai_norm.jsonl condition --runs 3 --out results/probe5_gpt4o_judge_avg.json
python judge_stability.py results/probe1_expanded/trial_results.jsonl cultural_background --runs 3 --out results/probe1_claude_judge_avg.json
python judge_stability.py results/crossmodel_openai_norm.jsonl cultural_background --runs 3 --out results/probe1_gpt4o_judge_avg.json
```

Second judge, GPT-4o at temperature 0 (80 GPT-4o calls per file):

```
python analyze_judge_gpt.py results/probe5_situational/trial_results.jsonl condition --per-condition 10 --out results/probe5_claude_gptjudge.json
python analyze_judge_gpt.py results/crossmodel_probe5_openai_norm.jsonl condition --per-condition 10 --out results/probe5_gpt4o_gptjudge.json
python analyze_judge_gpt.py results/probe1_expanded/trial_results.jsonl cultural_background --per-condition 10 --out results/probe1_claude_gptjudge.json
python analyze_judge_gpt.py results/crossmodel_openai_norm.jsonl cultural_background --per-condition 10 --out results/probe1_gpt4o_gptjudge.json
```

Single-run judge for control and grounding probes:

```
python analyze_judge.py results/control/claude_trial_results.jsonl condition --per-condition 10
python analyze_judge.py results/control/openai_trial_results_norm.jsonl condition --per-condition 10
python analyze_judge.py results/probe6_grounding/trial_results.jsonl cultural_background --per-condition 10
python analyze_judge.py results/probe6b_grounding_lowstakes/trial_results.jsonl cultural_background --per-condition 10
```

Rank agreement and main effects (no API calls):

```
python analyze_rank_effects.py results/probe1_claude_judge_avg.json results/probe1_gpt4o_judge_avg.json results/probe5_claude_judge_avg.json results/probe5_gpt4o_judge_avg.json
python analyze_rank_effects.py results/probe1_claude_gptjudge.json results/probe1_gpt4o_gptjudge.json results/probe5_claude_gptjudge.json results/probe5_gpt4o_gptjudge.json
```

## Limitations

- **One task.** Every condition in both papers uses the same scenario, a persona disagreeing with a manager. Power distance is built into the task before any variable specifies it.
- **Two models.** Claims about what transfers across models rest on one pair. Gemini was attempted and abandoned.
- **The primary judge is one of the two models under comparison.** Claude scored both Claude and GPT-4o output. A second judge confirmed the pattern on the two dimensions it could discriminate.
- **Judge samples are small.** Ten trials per condition. Three runs reduced variance but scored the same ten trials.
- **The second judge collapsed.** GPT-4o at temperature 0 did not discriminate on three of six dimensions. A different temperature or a third judge model was not tested.
- **Lexical coding is crude and not portable across models.** Marker prevalence is not validated construct measurement, and markers developed on Claude undercount GPT-4o. Paper 2 shows this undercount was enough to produce a false null on cross-model agreement.
- **The imposition descriptor may not operationalize the construct.** The reversal on directness and hedging is consistent with the persona reading "significant weight and risk" as a reason to be clear rather than soften.
- **GPT-4o shifts under any persona clause.** Its results are measured against a baseline the persona clause has already moved.
- **Rank comparison is underpowered.** Eight conditions cannot distinguish weak agreement from none.
- **English only.** All interactions were in English.
- **No significance testing.** Descriptive rates and rank correlations only.
- **Partial schema coverage.** Five identity dimensions and the directed edge set. Other graph structures were not analyzed.

## Relationship to MatrAIx

This is independent research using MatrAIx's public repository and released schema. It is offered as collaborative quality assurance.

MatrAIx is the case study here, not the subject. The effects reported originate at generation time and are inherited by any system that renders an identity label into a prompt, whatever the quality of the schema supplying it: persona-based evaluation frameworks, synthetic user research, simulated-participant UX testing, agent systems with demographic character specifications. That MatrAIx's design turns out to be careful is what makes the dissociation visible.

The findings are, on balance, favorable to MatrAIx's design: its dependency graph contains no identity-to-competence edges, its documented edges carry rationale and explicit epistemic hedging, and its cultural-background conditionals are near-uniform. The behavioral effects reported here are not caused by that design and would not be prevented by fixing it. They are inherited from whichever model renders the persona.

Paper 1's MatrAIx-specific recommendations: extend the existing validation suite to identity attributes, separate cultural affiliation from cultural orientation in the schema as a representational matter, and either document or remove the 133 inert undocumented edges while confirming whether the uniformity of the four documented ones is deliberate.

Paper 2 adds one: replace the `cultural_background` dimension with situational fields drawn from politeness theory, or remove it. The dependency graph shows the dimension carries no schema-level effect. The behavioral evidence shows it carries a stereotype at render time that survives contextualization. A dimension that does nothing in the schema and something harmful in the prompt has no reason to remain.

## Citation

Paper 1:

```bibtex
@misc{williams2026cleanschemas,
  title     = {Clean Schemas, Stereotyped Personas: Locating Cultural Bias in
               Persona-Conditioned Language Models},
  author    = {Williams, Bianca Den{\'e}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21970217},
  note      = {https://github.com/biancadene/persona-cultural-validity}
}
```

Paper 2:

```bibtex
@misc{williams2026situational,
  title     = {Situational Variables Versus Cultural Labels in Persona Conditioning:
               Shared Stereotype, Shared Rule},
  author    = {Williams, Bianca Den{\'e}},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22983112},
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
