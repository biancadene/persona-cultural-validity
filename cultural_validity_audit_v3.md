# Framing Salience Moderates Cultural Stereotyping in Persona-Conditioned Language Models: A Schema-Level and Behavioral Audit

**Author:** Bianca Dené Williams
**Affiliation:** State College of Florida
**Date:** August 2026

## Abstract

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. We audit this practice at two levels — the persona schema and dependency graph of MatrAIx, an open-source evaluation framework, and the behavior of personas rendered from it — across 575 trials. We report three findings. First, cultural background labels produce large, systematic behavioral shifts: personas labeled "Individualist (Western)" used direct assertion in 96% of trials versus 24% for "Collectivist (East Asian)," and permission-seeking language appeared in 0% versus 60% respectively. Second, this polarization is moderated by framing: holding values and model constant, making cultural context explicit within the task rather than supplying it as a background attribute halved the directness gap (72 to 36 percentage points) and the permission-seeking gap (60 to 32 points). Third, and contrary to our own preliminary results, native-language labels produced no representation-ordered effect: task engagement was 100% across all seven language conditions, and competence-hedging was highest for Hindi (36%), a high-resource language, exceeding both Fulfulde (32%) and English (20%). A pilot finding of competence suppression for a lower-resource language did not survive expansion from n=5 to n=25 and is reported here as non-replicating. Schema analysis found no mechanism for any of these effects in the persona system itself: across five identity dimensions there are zero edges to competence dimensions, and 133 of 137 cultural-background edges carry near-uniform conditional probability tables with maximum spread of approximately one percentage point. We conclude that cultural stereotyping in persona conditioning originates in model priors at render time, is sensitive to how identity is framed, and cannot be addressed through schema design alone.

## 1. Introduction

Persona-based evaluation has become standard practice for testing AI products against simulated diverse users. Rather than recruiting participants across every demographic, developers generate structured persona records and instantiate them as language model agents. MatrAIx, an open-source framework, exemplifies the approach: a schema of 1,290 categorical dimensions, a dependency-aware generative graph of 6,999 directed edges, and a public release of one million curated personas.

When such systems include cultural or linguistic attributes, they make implicit claims about how identity shapes behavior. This raises a validation question. If a persona labeled "Collectivist (East Asian)" communicates differently from one labeled "Individualist (Western)," is the system reproducing documented cross-cultural variation, or amplifying a stereotype?

MatrAIx has infrastructure well-suited to answering this: a persona-adherence suite that runs positive/negative persona pairs through neutral tasks across four environments and uses an LLM judge to assess whether the target attribute surfaces in observed behavior. That suite covers ten attributes — coding style, communication traits, and register. It covers no identity attribute.

This paper approaches the gap from two directions. We measure behavior across 575 counterfactual trials, and we examine the schema and dependency graph directly to determine whether observed effects are attributable to the persona system's design. The two lines of evidence diverge, and that divergence is our central result.

We also report a finding that did not replicate. An earlier pilot at n=5 per condition suggested that a persona labeled with a lower-resource native language disengaged from technical tasks and questioned its own competence. At n=25 this effect disappeared. We report it because the pattern is instructive about the fragility of small-sample persona findings.

## 2. Methods

### 2.1 Design

Each probe varies a single identity attribute while holding all other persona content constant, then compares responses to an identical task. Task instructions never mention communication style, competence, or any measured dimension; observed differences must arise from persona conditioning.

Persona conditioning uses MatrAIx's own phrase templates verbatim, as specified in `persona/schema/dimensions.json`: `"with a {value} cultural frame"` for `cultural_background`, and `"a native {value} speaker"` for `primary_language`.

**Probe 1 — Cultural background, implicit framing (n=200).** All eight `cultural_background` schema values, 25 trials each. Personas were asked to express disagreement with a manager's proposed project change. Cultural identity was supplied as a background attribute; the task itself did not reference culture.

**Probe 2 — Language label (n=175).** Seven language conditions, 25 trials each: six valid `primary_language` schema values spanning a range of representation in typical training corpora (English, Mandarin, Hindi, Arabic, Bengali, Swahili), plus Fulfulde as an out-of-schema control. Fulfulde is not a permitted `primary_language` value in MatrAIx; it was included to test whether any effect required schema validity. Personas were specified as software engineers with ten years of experience and asked to evaluate a distributed system architecture — a task with no language dependency.

**Probe 3 — Cultural background, explicit framing (n=200).** Identical eight values and 25 trials each, but with cultural identity foregrounded in the task itself. Personas were asked to directly challenge a senior colleague's flawed proposal. Comparison against Probe 1 isolates the effect of framing salience, holding values, model, and measurement constant.

All trials used Claude Opus 4.8 (`claude-opus-4-8`) at default temperature, max 300 tokens. Total: 575 trials, 575 successful, 0 errors.

### 2.2 Analysis

We applied deterministic lexical coding: seven marker categories (hedging, directness, permission-seeking, group reference, deference, competence-hedging, task engagement) defined a priori as regular expression sets, applied identically to all conditions. We report both marker rate per 100 words and percentage of trials containing at least one marker in a category. The coding script and full marker definitions are included in the accompanying repository; the analysis is fully reproducible and involves no model judgment.

This approach is crude by design. It cannot capture meaning, irony, or implicature, and it will miss markers phrased outside the defined patterns. We accept that limitation in exchange for reproducibility and freedom from judge bias. Section 5 discusses the tradeoff.

### 2.3 Schema and dependency graph analysis

We examined MatrAIx's published schema (`persona/schema/dimensions.json`) and generative dependency graph (`persona/synthesis/graph/full_dag.json`, 24.7 MB, 6,999 directed edges). For five identity dimensions — `cultural_background`, `primary_language`, `english_proficiency`, `multilingualism`, `demo_ethnicity_broad` — we enumerated all outgoing edges, recorded documentation metadata, extracted conditional probability tables, and measured the maximum probability spread each edge induces across identity values.

## 3. Results

### 3.1 Probe 1: Cultural background under implicit framing (n=200)

Cultural background labels produced large and systematic differences in communication behavior.

**Table 1. Percentage of trials containing at least one marker, by cultural background value (n=25 each).**

| Cultural background | Directness | Permission-seeking | Group reference | Hedging | Deference |
|---|---|---|---|---|---|
| Individualist (Western) | **96%** | **0%** | 64% | 96% | 52% |
| Mixed / diaspora | 64% | 12% | 20% | 100% | 12% |
| Latin | 56% | 28% | 68% | 100% | 8% |
| Indigenous | 44% | 12% | 48% | 92% | 12% |
| South Asian | 44% | 76% | 40% | 88% | 28% |
| African | 36% | 72% | 56% | 96% | 20% |
| Collectivist (East Asian) | **24%** | **60%** | **96%** | 100% | 48% |
| Middle Eastern | 24% | 64% | 60% | 100% | 32% |

The two extremes on directness are the two values that name a psychological orientation: Individualist (Western) at 96% and Collectivist (East Asian) at 24% — a fourfold difference. Permission-seeking shows a categorical split: 0% for Individualist versus 60–76% for Collectivist, African, and South Asian. Group reference peaks at 96% for Collectivist versus 20% for Mixed / diaspora.

Notably, the orientation-free values (African, South Asian, Latin, Middle Eastern, Indigenous) cluster in intermediate positions on directness, while the two orientation-bearing labels occupy the poles. Section 4.2 discusses the significance of this pattern for schema design.

### 3.2 Probe 3: Cultural background under explicit framing (n=200)

Holding cultural values, model, and measurement constant, foregrounding cultural context within the task substantially reduced polarization.

**Table 2. Framing comparison, Individualist versus Collectivist conditions.**

| Marker | Probe 1 (implicit) | Probe 3 (explicit) | Change in gap |
|---|---|---|---|
| Directness: Individualist | 96% | 80% | |
| Directness: Collectivist | 24% | 44% | |
| **Directness gap** | **72 pts** | **36 pts** | **−50%** |
| Permission-seeking: Individualist | 0% | 0% | |
| Permission-seeking: Collectivist | 60% | 32% | |
| **Permission-seeking gap** | **60 pts** | **32 pts** | **−47%** |
| Group reference: Individualist | 64% | 36% | |
| Group reference: Collectivist | 96% | 68% | |
| **Group reference gap** | **32 pts** | **32 pts** | **0%** |

The directness and permission-seeking gaps roughly halve. Group reference is unchanged. Absolute rates decline across both conditions for group reference, suggesting the explicit-framing task shifted overall register rather than selectively suppressing stereotype on that dimension.

Qualitatively, Probe 3 responses frequently included explicit meta-commentary declining to caricature — for example, "Real East Asian workplace contexts vary widely, but I'll play this authentically without collapsing it into 'never disagree.'" No such commentary appeared in Probe 1.

We note an important confound: Probe 1 and Probe 3 use different tasks (disagreeing with a manager versus challenging a senior colleague), not solely different framing. The tasks are structurally similar but not identical, so the framing effect is not cleanly isolated. Section 5 addresses this.

### 3.3 Probe 2: Language label (n=175) — null result

Language labels produced no representation-ordered effect.

**Table 3. Percentage of trials containing at least one marker, by native language (n=25 each).**

| Language | In schema | Task engagement | Competence hedging | Directness |
|---|---|---|---|---|
| English | yes | 100% | 20% | 52% |
| Mandarin | yes | 100% | 20% | 40% |
| Hindi | yes | 100% | **36%** | 32% |
| Arabic | yes | 100% | 0% | 64% |
| Bengali | yes | 100% | 12% | 52% |
| Swahili | yes | 100% | 12% | 64% |
| Fulfulde | **no** | 100% | 32% | 68% |

Task engagement was 100% across every condition. Every one of the 175 responses addressed the technical task.

Competence hedging did not order by training-data representation. Hindi, a high-resource language, showed the highest rate at 36%, exceeding Fulfulde (32%). English, the highest-resource language, showed 20% — above both Bengali and Swahili (12% each). Arabic showed 0%.

**Non-replication of pilot finding.** A preliminary version of this probe at n=5 per condition found that three of five Fulfulde-labeled responses opened with meta-cognitive disclosure and did not engage the technical task, a pattern absent from English and Mandarin conditions. At n=25, Fulfulde task engagement was 100% and competence hedging (32%) was exceeded by Hindi. The pilot result was not representative. We report this explicitly: the striking pattern that motivated this probe did not survive expansion, and the representation-gradient hypothesis is not supported by these data.

### 3.4 Schema analysis: cultural background

`cultural_background` is dimension index 24, category "Demographic: Cultural," described as "Cultural frame of reference," rendered via `"with a {value} cultural frame"`. Its eight permitted values are:

> Individualist (Western), Collectivist (East Asian), South Asian, Latin, African, Middle Eastern, Indigenous, Mixed / diaspora

These operate at incommensurate conceptual levels. Two fuse a psychological orientation with a geographic region. Four are geographic or ethnocultural categories carrying no orientation. One denotes a political and colonial relationship (Indigenous). One denotes migration and mixed heritage.

The asymmetry constrains representable personas: a persona cannot be South Asian *and* individualist, or Western *and* collectivist, because orientation is bundled into two values and absent from the other six. Cultural affiliation and cultural orientation are distinct constructs, and the schema already models orientation independently elsewhere — `decision_style`, `values_priority`, `schwartz_value_conformity`.

### 3.5 Dependency graph analysis

The graph contains 6,999 directed edges. Well-documented edges carry substantial metadata: written rationale, evidence level, relationship basis, edge weight, calibrated conditional probability table, and explicit epistemic hedging — for instance `"direction_semantics": "sampling direction; not necessarily an identified causal effect"` and `"causal_claim": "weak_causal_prior"`.

Identity dimensions are documented unevenly.

**`primary_language`: 18 edges, all documented.** Twelve connect to corresponding language-proficiency dimensions (strength high, confidence 0.82) — largely tautological. Six connect to communication-style dimensions: `register`, `cog_use_of_jargon`, `cog_precision_of_language`, `cog_formality`, `tone_expected`, `modality_pref` (strength medium, confidence 0.55).

**`cultural_background`: 137 edges, 4 documented.** The documented four connect to `values_priority`, `political_lean`, `att_traditional_gender_roles`, and `att_organized_religion` (strength medium, confidence 0.62) — constructs with substantial cross-cultural literature. The remaining 133 contain only `edge_id`, `source`, `target`, `edge_weight`, and `cpd`: no rationale, no relation type, no evidence level, no strength, no confidence. Their targets are consumer attitudes and hobby interests — `att_vaccines`, `att_gun_ownership`, `topic_woodworking`, `topic_chess`, `topic_birdwatching`, and similar.

**`demo_ethnicity_broad`: 0 outgoing edges.** Ethnicity exists as a schema dimension but plays no role in the generative graph.

**Effect magnitude.** For each of the 133 undocumented cultural-background edges we measured the maximum probability difference induced between any two cultural values. The largest across all 133 was 0.0111 — approximately one percentage point. No edge exceeded 0.02. For `topic_woodworking`, seven of eight cultural values produced numerically identical distributions. These edges are structurally present but functionally inert.

**Table 4. Identity dimension edges and competence connections.**

| Identity dimension | Total edges | Documented | Edges to competence dimensions |
|---|---|---|---|
| `primary_language` | 18 | 18 | 0 |
| `english_proficiency` | 7 | — | 0 |
| `multilingualism` | 6 | — | 0 |
| `cultural_background` | 137 | 4 | 0 |
| `demo_ethnicity_broad` | 0 | — | 0 |

No identity dimension connects to any `skill_*`, `fam_*`, `prog_*`, or `tool_*` dimension, nor to `highest_education`, `tech_savviness`, `institution_tier`, `academic_field`, `seniority`, or `research_output`.

## 4. Discussion

### 4.1 The behavioral effect is real; the schema does not produce it

Probe 1 documents a fourfold difference in direct assertion and a categorical difference in permission-seeking, driven solely by a cultural label rendered into a prompt. The dependency graph offers no mechanism. The 133 undocumented cultural-background edges connect to hobbies and consumer attitudes, not to communication style, and their conditional probability tables are near-uniform — a one-percentage-point maximum spread cannot account for a seventy-two-point behavioral gap.

The effect originates downstream of the schema, in the language model's interpretation of an identity label at generation time. Any persona system rendering a cultural label into a prompt inherits this behavior regardless of how carefully its schema is built.

### 4.2 Orientation-bearing labels polarize most

The two schema values that name a psychological orientation occupy the extremes on nearly every measured dimension, while the six geographic or relational values cluster in between. This is consistent with the model responding to the orientation term — "Individualist," "Collectivist" — rather than to cultural knowledge about the associated regions.

If so, the construct conflation identified in §3.4 is not merely a taxonomic untidiness. It supplies the model with the very words most likely to trigger stereotyped output, bundled inseparably into two of eight values. Separating affiliation from orientation, as the schema already does elsewhere, would remove that trigger and permit combinations real populations exhibit.

### 4.3 Framing salience moderates the effect

The Probe 1 versus Probe 3 comparison suggests that how identity enters the prompt matters as much as whether it does. When cultural context was foregrounded within the task, the model frequently produced explicit meta-commentary resisting caricature, and measured polarization on directness and permission-seeking approximately halved.

This is the most actionable finding here, and it points toward mitigation that does not require schema changes: persona conditioning that makes cultural context salient and available for reasoning appears to elicit less stereotyped output than conditioning that supplies it as an inert background attribute. We stress that this is suggestive rather than established — the two probes used different tasks, and the mechanism is untested.

### 4.4 On the non-replication

Our pilot finding — competence suppression for a lower-resource language label — was striking, thematically coherent, and wrong. Three of five responses showed the pattern; twenty-five trials showed no representation-ordered effect at all, and a high-resource language exceeded the lower-resource one.

We report this at length because we believe the failure mode is common in persona-based research. Small-sample persona studies generate vivid, quotable, narratively satisfying results, and language model outputs vary enough that five trials can easily produce a pattern that does not exist. Our own experience here is a caution: the finding we found most compelling was the one that dissolved on expansion.

## 5. Limitations

**Lexical coding is crude.** Marker counts cannot capture meaning, indirection, or context. A response may communicate deference without any matched pattern, or match a directness pattern while hedging heavily around it. We chose reproducibility over sensitivity; a complementary LLM-judge coding layer, and human coding with inter-rater reliability, would strengthen the behavioral claims. Reported percentages should be read as marker prevalence, not as validated construct measurement.

**Framing comparison is confounded.** Probes 1 and 3 differ in both framing and task. The framing interpretation is plausible but not isolated. A clean test would hold the task fixed and vary only whether cultural context is foregrounded.

**Single model.** All 575 trials used one model from one provider. Effects attributed to model priors require cross-provider replication to establish generality.

**English only.** All interactions were in English, including for personas specified as native speakers of other languages. Conditioning and interacting in the persona's stated language may produce different results.

**No statistical testing.** We report descriptive rates. With 25 trials per condition, differences of the magnitude observed in Probe 1 are unlikely to be noise, but we have not conducted significance testing or corrected for multiple comparisons across seven marker categories and eight conditions.

**Partial schema coverage.** We examined five identity dimensions and the directed edge set. Other dimensions, and other graph structures (`undirected_factors`, `high_order_factors`, `latent_modules`, `conditional_masks`), were not analyzed.

**Out-of-schema condition.** The Fulfulde condition used a value outside `primary_language`'s permitted set, making it a test of language-label conditioning generally rather than of MatrAIx persona generation specifically.

## 6. Recommendations

**Extend validation to identity attributes.** MatrAIx's persona-adherence infrastructure is well suited to this and currently covers ten behavioral attributes and no identity attributes. `cultural_background` is rendered directly into prompts and demonstrably shifts behavior; it is the natural first candidate.

**Validate rendered behavior, not schema structure alone.** Schema review would not have detected the effects reported here. The strongest behavioral difference we measured has no representation in the dependency graph.

**Separate cultural affiliation from cultural orientation.** Orientation is already modeled independently in the schema. Bundling it into two of eight cultural values creates asymmetry, constrains representable personas, and — per §4.2 — may supply the specific lexical trigger for stereotyped output.

**Consider framing in persona conditioning.** Our results suggest identity supplied as an inert background attribute may elicit more stereotyped behavior than identity made explicit and available for reasoning. This warrants controlled investigation.

**Document or remove the 133 bare edges.** They are inert today, but they are undocumented surface area in a graph that documents comparable edges thoroughly.

**Report sample sizes prominently in persona research.** Our own pilot demonstrates how readily small-n persona studies produce compelling non-findings.

## 7. Conclusion

Across 575 trials we find that cultural background labels produce large, systematic shifts in persona communication behavior, that this polarization is concentrated in the two schema values naming a psychological orientation, and that it is approximately halved when cultural context is made explicit within the task rather than supplied as a background attribute. We find no corresponding effect for language labels, and we report the non-replication of our own preliminary finding on that point.

None of these effects are traceable to the persona system's schema or dependency graph, which contains no identity-to-competence edges and near-uniform cultural-background conditionals. The stereotyping originates in model priors at render time and is inherited by any system that conditions a model on cultural identity.

The practical implication is that persona systems must validate what their personas do, not only how their schemas are structured — and that how identity is framed in conditioning may be as consequential as which attributes are included. The infrastructure to test this already exists in the system we examined. It has not yet been pointed at identity.

## Code and Data Availability

All probe implementations, raw trial outputs (575 responses), lexical coding scripts and marker definitions, schema analysis queries, and per-condition results are available at: https://github.com/biancadene/cultural-validity-audit-matraix

## References

Hofstede, G. (2010). *Cultures and Organizations: Software of the Mind* (3rd ed.). McGraw-Hill.

Nisbett, R. E. (2003). *The Geography of Thought: How Asians and Westerners Think Differently...and Why*. Free Press.

Hall, E. T. (1989). *Beyond Culture*. Anchor Books.

Tannen, D. (1990). *You Just Don't Understand: Women and Men in Conversation*. William Morrow.

Chang, J., Li, X., Hao, Y., Hou, J., Huang, J., Wen, Q., Huang, S., Liu, Y., Liu, X., Fan, Y., & Wang, Y. (2026). MatrAIx: Simulating the World with 8.3 Billion Persona Agents. *arXiv preprint arXiv:2608.04205*.

Blodgett, S. L., Barocas, S., Daumé III, H., & Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5454–5476.

Sap, M., Gabriel, S., Qin, L., Jurafsky, D., Smith, N. A., & Choi, Y. (2020). Social bias frames: Reasoning about social and power implications of language. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5477–5490.

Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. *Proceedings of Machine Learning Research*, 81, 1–15.

Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V., & Kalai, A. (2016). Man is to computer programmer as woman is to homemaker? Debiasing word embeddings. *Advances in Neural Information Processing Systems*, 29, 4349–4357.

Cummins, J. (2001). *Negotiating Identities: Education for Empowerment in a Diverse Society* (2nd ed.). California Association for Bilingual Education.

Krashen, S. D. (1982). *Principles and Practice in Second Language Acquisition*. Pergamon Press.

Council of Europe. (2020). *Common European Framework of Reference for Languages: Learning, Teaching, Assessment*. Companion Volume. Council of Europe Publishing.
