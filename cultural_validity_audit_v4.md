# Framing Salience Moderates Cultural Stereotyping in Persona-Conditioned Language Models: A Schema-Level and Behavioral Audit

**Author:** Bianca Dené Williams
**Affiliation:** State College of Florida
**Date:** August 2026

## Abstract

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. We audit this practice at two levels — the schema and dependency graph of MatrAIx, an open-source evaluation framework, and the behavior of personas rendered from it — across 975 trials. We report three findings. First, cultural background labels produce large, systematic behavioral shifts: personas labeled "Individualist (Western)" used direct assertion in 96% of trials versus 24% for "Collectivist (East Asian)," with permission-seeking language at 0% versus 60%. Second, this polarization is causally moderated by framing salience. In a controlled comparison holding task, model, and persona conditioning constant, and supplying both conditions with a length-matched reflection cue, directing that reflection toward cultural background rather than toward general workplace habit reduced the directness gap by 35% (92 to 60 points) and the permission-seeking gap by 40% (40 to 24 points). Third, and contrary to our own preliminary results, native-language labels produced no representation-ordered effect: task engagement was 100% across seven language conditions, and competence-hedging was highest for Hindi (36%), exceeding both Fulfulde (32%) and English (20%). A pilot finding of competence suppression for a lower-resource language did not survive expansion from n=5 to n=25 and is reported as non-replicating. Schema analysis found no mechanism for any observed effect within the persona system: across five identity dimensions there are zero edges to competence dimensions, and 133 of 137 cultural-background edges carry near-uniform conditional probability tables with maximum spread of approximately one percentage point. We conclude that cultural stereotyping in persona conditioning originates in model priors at render time, cannot be addressed through schema design alone, but is measurably reduced when identity is made an object of reasoning rather than supplied as an inert attribute.

## 1. Introduction

Persona-based evaluation has become standard practice for testing AI products against simulated diverse users. Rather than recruiting participants across every demographic, developers generate structured persona records and instantiate them as language model agents. MatrAIx, an open-source framework, exemplifies the approach: a schema of 1,290 categorical dimensions, a dependency-aware generative graph of 6,999 directed edges, and a public release of one million curated personas.

When such systems include cultural or linguistic attributes, they make implicit claims about how identity shapes behavior. If a persona labeled "Collectivist (East Asian)" communicates differently from one labeled "Individualist (Western)," is the system reproducing documented cross-cultural variation, or amplifying a stereotype?

MatrAIx has infrastructure suited to answering this: a persona-adherence suite that runs positive/negative persona pairs through neutral tasks across four environments and uses an LLM judge to assess whether the target attribute surfaces in behavior. That suite covers ten attributes — coding style, communication traits, register. It covers no identity attribute.

This paper approaches the gap from two directions. We measure behavior across 975 counterfactual trials, and we examine the schema and dependency graph directly to determine whether observed effects are attributable to the persona system's design. The two lines of evidence diverge, and that divergence is our central result.

We also report a finding that did not replicate, and a claim that survived a controlled test after initially resting on a confounded comparison. Both are described in full.

## 2. Methods

### 2.1 Design

Each probe varies a single identity attribute while holding all other persona content constant, then compares responses to an identical task. Task instructions never mention communication style, competence, or any measured dimension.

Persona conditioning uses MatrAIx's own phrase templates verbatim, from `persona/schema/dimensions.json`: `"with a {value} cultural frame"` for `cultural_background`, `"a native {value} speaker"` for `primary_language`.

**Probe 1 — Cultural background, implicit framing (n=200).** All eight `cultural_background` schema values, 25 trials each. Personas expressed disagreement with a manager's proposed project change. Cultural identity was supplied as a background attribute.

**Probe 2 — Language label (n=175).** Seven conditions, 25 trials each: six valid `primary_language` schema values spanning a range of training-corpus representation (English, Mandarin, Hindi, Arabic, Bengali, Swahili), plus Fulfulde as an out-of-schema control. Personas were software engineers with ten years of experience asked to evaluate a distributed system architecture.

**Probe 3 — Cultural background, explicit framing (n=200).** Same eight values, 25 trials each, with cultural identity foregrounded in the task. Personas challenged a senior colleague's flawed proposal.

**Probe 4 — Framing isolation (n=400).** Probes 1 and 3 differed in both task and framing, confounding interpretation. Probe 4 holds the task fixed (the Probe 1 manager-disagreement scenario) and varies only the object of a reflection cue:

- *Neutral cue:* "Consider how you typically handle disagreement at work." (9 words)
- *Cultural cue:* "Consider how your cultural background shapes the way you handle disagreement." (11 words)

Both conditions receive persona conditioning, the same task, and a reflection instruction of comparable length. Only the object of reflection differs. Eight values × 2 conditions × 25 trials.

All trials used Claude Opus 4.8 (`claude-opus-4-8`), default temperature, 300 max tokens. Total: 975 trials.

### 2.2 Analysis

We applied deterministic lexical coding: marker categories defined a priori as regular expression sets, applied identically across conditions. We report percentage of trials containing at least one marker in a category. Coding scripts and full marker definitions are in the accompanying repository; the analysis involves no model judgment and is fully reproducible.

Probe 4 additionally codes a `meta_commentary` category — language in which the response explicitly declines to caricature ("cultures vary widely," "not a monolith," "I won't flatten this") — to test whether framing operates through explicit reasoning.

This approach is crude by design. It cannot capture meaning, irony, or implicature, and will miss markers phrased outside defined patterns. We accept that in exchange for reproducibility and freedom from judge bias.

### 2.3 Schema and dependency graph analysis

We examined MatrAIx's published schema (`persona/schema/dimensions.json`) and generative dependency graph (`persona/synthesis/graph/full_dag.json`, 24.7 MB, 6,999 directed edges). For five identity dimensions — `cultural_background`, `primary_language`, `english_proficiency`, `multilingualism`, `demo_ethnicity_broad` — we enumerated all outgoing edges, recorded documentation metadata, extracted conditional probability tables, and measured maximum probability spread across identity values.

## 3. Results

### 3.1 Probe 1: Cultural background under implicit framing (n=200)

**Table 1. Percentage of trials containing at least one marker (n=25 per value).**

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

The extremes on directness are the two values that name a psychological orientation: 96% versus 24%, a fourfold difference. Permission-seeking shows a categorical split: 0% for Individualist versus 60–76% for Collectivist, African, and South Asian. Group reference peaks at 96% for Collectivist versus 20% for Mixed / diaspora.

The orientation-free values (African, South Asian, Latin, Middle Eastern, Indigenous) occupy intermediate positions on directness while the two orientation-bearing labels hold the poles. Section 4.2 discusses the implication.

### 3.2 Probe 4: Framing salience, isolated (n=400)

Holding task, model, persona conditioning, and reflection-cue length constant, and varying only whether the cue directed attention to cultural background:

**Table 2. Individualist versus Collectivist gap, by reflection cue.**

| Marker | Neutral cue | Cultural cue | Change |
|---|---|---|---|
| **Directness** | 92 pts | 60 pts | **−32 pts (−35%)** |
| **Permission-seeking** | 40 pts | 24 pts | **−16 pts (−40%)** |
| Group reference | 60 pts | 56 pts | −4 pts (−7%) |

Directness and permission-seeking polarization fell substantially. Group reference was essentially unchanged.

Across all eight cultural values rather than the two extremes, spread narrowed for directness (92 → 64 pts) and hedging (12 → 8 pts), while permission-seeking spread widened (56 → 72 pts) — indicating the effect is not a uniform compression of all cross-condition variation.

`meta_commentary` — explicit refusal to caricature — rose under the cultural cue, most visibly for the Individualist condition (4% → 16%). Responses under the cultural cue more frequently included statements resembling "cultural background shapes this but individuals vary widely." This is consistent with framing operating through explicit reasoning rather than through tone alone, though the marker rates are low and this should be treated as suggestive.

**Interpretation.** Probes 1 and 3 suggested a framing effect but differed in task. Probe 4 removes that confound. The reduction persists at comparable magnitude, supporting a causal reading: making cultural identity an object of reasoning, rather than an inert background attribute, measurably reduces stereotyped output on directness and permission-seeking. The effect is dimension-specific, not global.

### 3.3 Probe 3: Cultural background under explicit framing (n=200)

Probe 3, though task-confounded relative to Probe 1, showed the same directional pattern: the Individualist/Collectivist directness gap fell from 72 to 36 points and permission-seeking from 60 to 32 points. We report it as consistent supporting evidence rather than as independent confirmation, given the confound Probe 4 was designed to remove.

### 3.4 Probe 2: Language label (n=175) — null result

**Table 3. Percentage of trials containing at least one marker (n=25 per language).**

| Language | In schema | Task engagement | Competence hedging | Directness |
|---|---|---|---|---|
| English | yes | 100% | 20% | 52% |
| Mandarin | yes | 100% | 20% | 40% |
| Hindi | yes | 100% | **36%** | 32% |
| Arabic | yes | 100% | 0% | 64% |
| Bengali | yes | 100% | 12% | 52% |
| Swahili | yes | 100% | 12% | 64% |
| Fulfulde | **no** | 100% | 32% | 68% |

Task engagement was 100% across every condition. Competence hedging did not order by training-data representation: Hindi, a high-resource language, was highest at 36%, exceeding Fulfulde (32%). English showed 20%, above both Bengali and Swahili (12%). Arabic showed 0%.

**Non-replication.** A preliminary version at n=5 per condition found three of five Fulfulde-labeled responses opening with meta-cognitive disclosure and not engaging the technical task, a pattern absent from English and Mandarin. At n=25, Fulfulde task engagement was 100% and its competence hedging was exceeded by Hindi. The pilot result was not representative, and the representation-gradient hypothesis is not supported by these data.

### 3.5 Schema analysis: cultural background

`cultural_background` is dimension index 24, category "Demographic: Cultural," described as "Cultural frame of reference," rendered via `"with a {value} cultural frame"`. Its eight permitted values:

> Individualist (Western), Collectivist (East Asian), South Asian, Latin, African, Middle Eastern, Indigenous, Mixed / diaspora

These operate at incommensurate conceptual levels. Two fuse a psychological orientation with a geographic region. Four are geographic or ethnocultural categories carrying no orientation. One denotes a political and colonial relationship. One denotes migration and mixed heritage.

The asymmetry constrains representable personas: a persona cannot be South Asian *and* individualist, or Western *and* collectivist, because orientation is bundled into two values and absent from the other six. The schema already models orientation independently elsewhere — `decision_style`, `values_priority`, `schwartz_value_conformity`.

### 3.6 Dependency graph analysis

The graph contains 6,999 directed edges. Well-documented edges carry written rationale, evidence level, relationship basis, edge weight, calibrated conditional probability table, and explicit epistemic hedging — for instance `"direction_semantics": "sampling direction; not necessarily an identified causal effect"`.

Identity dimensions are documented unevenly.

**`primary_language`: 18 edges, all documented.** Twelve connect to corresponding language-proficiency dimensions (strength high, confidence 0.82) — largely tautological. Six connect to communication-style dimensions: `register`, `cog_use_of_jargon`, `cog_precision_of_language`, `cog_formality`, `tone_expected`, `modality_pref` (strength medium, confidence 0.55).

**`cultural_background`: 137 edges, 4 documented.** The documented four connect to `values_priority`, `political_lean`, `att_traditional_gender_roles`, `att_organized_religion` (strength medium, confidence 0.62) — constructs with substantial cross-cultural literature. The remaining 133 contain only `edge_id`, `source`, `target`, `edge_weight`, `cpd`: no rationale, no relation type, no evidence level, no strength, no confidence. Their targets are consumer attitudes and hobby interests — `att_vaccines`, `att_gun_ownership`, `topic_woodworking`, `topic_chess`, `topic_birdwatching`.

**`demo_ethnicity_broad`: 0 outgoing edges.**

**Effect magnitude.** For each of the 133 undocumented cultural-background edges we measured maximum probability difference between any two cultural values. The largest was 0.0111 — approximately one percentage point. None exceeded 0.02. For `topic_woodworking`, seven of eight values produced numerically identical distributions. These edges are structurally present but functionally inert.

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

Probe 1 documents a fourfold difference in direct assertion and a categorical difference in permission-seeking, driven solely by a cultural label rendered into a prompt. The dependency graph offers no mechanism. The 133 undocumented cultural-background edges connect to hobbies and consumer attitudes, not communication style, and their conditionals are near-uniform — a one-point maximum spread cannot produce a ninety-two-point behavioral gap.

The effect originates downstream of the schema, in the model's interpretation of an identity label at generation time. Any persona system rendering a cultural label into a prompt inherits this behavior regardless of schema quality.

### 4.2 Orientation-bearing labels polarize most

The two schema values naming a psychological orientation occupy the extremes on nearly every measured dimension, while the six geographic or relational values cluster between them. This is consistent with the model responding to the orientation term — "Individualist," "Collectivist" — rather than to cultural knowledge about the associated regions.

If so, the construct conflation in §3.5 is not merely taxonomic untidiness. It supplies the model with precisely the words most likely to trigger stereotyped output, bundled inseparably into two of eight values. Separating affiliation from orientation, as the schema already does elsewhere, would remove that trigger and permit combinations real populations exhibit.

### 4.3 Framing salience moderates the effect

Probe 4 isolates what Probes 1 and 3 could only suggest. With task, model, conditioning, and cue length held constant, directing reflection toward cultural background rather than general workplace habit reduced directness polarization by 35% and permission-seeking polarization by 40%.

The effect is dimension-specific: group reference barely moved, and permission-seeking spread across all eight values actually widened even as the two-value gap narrowed. This argues against a simple "reflection makes output blander" account and for something more targeted — though the mechanism remains untested.

The rise in explicit meta-commentary under the cultural cue is suggestive of a reasoning-based mechanism: prompted to consider culture, the model more often states that cultures vary and declines to caricature. Marker rates are low, and this warrants direct investigation rather than inference.

The practical implication is that mitigation may be available without schema changes. Persona conditioning that makes cultural context available for reasoning appears to elicit less stereotyped output than conditioning that supplies it inertly.

### 4.4 On the non-replication

Our pilot finding — competence suppression for a lower-resource language label — was striking, thematically coherent, and wrong. Three of five responses showed the pattern; twenty-five trials showed no representation-ordered effect, and a high-resource language exceeded the lower-resource one.

We report this at length because the failure mode seems likely to be common in persona research. Small-sample persona studies generate vivid, quotable results, and model outputs vary enough that five trials can readily produce a pattern that does not exist. The finding we found most compelling was the one that dissolved on expansion.

## 5. Limitations

**Lexical coding is crude.** Marker prevalence is not validated construct measurement. Responses may express deference or directness in phrasings outside the defined patterns. A complementary LLM-judge layer and human coding with inter-rater reliability would strengthen the behavioral claims.

**Single model.** All 975 trials used one model from one provider. Effects attributed to model priors require cross-provider replication.

**English only.** All interactions were in English, including for personas specified as native speakers of other languages.

**No statistical testing.** We report descriptive rates. With 25 trials per cell, the Probe 1 and Probe 4 differences are unlikely to be noise, but we have not conducted significance testing or corrected for multiple comparisons.

**Framing mechanism untested.** Probe 4 establishes that cultural-directed reflection reduces polarization. It does not establish why. The meta-commentary result is suggestive but low-frequency.

**Partial schema coverage.** Five identity dimensions and the directed edge set. `undirected_factors`, `high_order_factors`, `latent_modules`, and `conditional_masks` were not analyzed.

**Out-of-schema condition.** The Fulfulde condition used a value outside `primary_language`'s permitted set, making it a test of language-label conditioning generally rather than of MatrAIx persona generation specifically.

## 6. Recommendations

**Extend validation to identity attributes.** MatrAIx's persona-adherence infrastructure is suited to this and currently covers ten behavioral attributes and no identity attributes. `cultural_background` is rendered directly into prompts and demonstrably shifts behavior.

**Validate rendered behavior, not schema structure alone.** Schema review would not have detected the effects reported here. The strongest behavioral difference we measured has no representation in the dependency graph.

**Separate cultural affiliation from cultural orientation.** Orientation is already modeled independently in the schema. Bundling it into two of eight cultural values constrains representable personas and, per §4.2, may supply the specific lexical trigger for stereotyped output.

**Treat framing as a design parameter.** Probe 4 indicates that how identity enters the prompt affects stereotype magnitude independent of which attributes are included. Persona systems should test their own conditioning templates rather than assuming neutrality.

**Document or remove the 133 bare edges.** Inert today, but undocumented surface area in a graph that documents comparable edges thoroughly.

**Report sample sizes prominently in persona research.** Our own pilot demonstrates how readily small-n persona studies produce compelling non-findings.

## 7. Conclusion

Across 975 trials we find that cultural background labels produce large, systematic shifts in persona communication behavior; that this polarization concentrates in the two schema values naming a psychological orientation; and that it is reduced by roughly 35–40% when the prompt directs the model to reason about cultural background rather than supplying it as an inert attribute — a result established under controlled conditions holding task, model, and cue length constant. We find no corresponding effect for language labels, and we report the non-replication of our own preliminary finding on that point.

None of these effects are traceable to the persona system's schema or dependency graph, which contains no identity-to-competence edges and near-uniform cultural-background conditionals. The stereotyping originates in model priors at render time and is inherited by any system that conditions a model on cultural identity.

Two implications follow. Persona systems must validate what their personas do, not only how their schemas are structured. And because the effect responds to framing, the conditioning template itself is a design surface worth testing — mitigation may be available without touching the schema at all.

## Code and Data Availability

All probe implementations, raw trial outputs (975 responses), lexical coding scripts and marker definitions, schema analysis queries, and per-condition results are available at: https://github.com/biancadene/cultural-validity-audit-matraix

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
