# Clean Schemas, Stereotyped Personas: Locating Cultural Bias in Persona-Conditioned Language Models

**Author:** Bianca Dené Williams
**Affiliation:** Independent Researcher
**ORCID:** 0009-0004-6378-628X
**Date:** August 2026
**Version:** 6

## Abstract

Persona-based evaluation systems simulate diverse users by conditioning language models on structured identity attributes. We audit this practice at two levels, the schema and dependency graph of MatrAIx, an open-source evaluation framework, and the behavior of personas rendered from it, across 1,175 trials on two model families, using two independent coding methods.

We report four findings. First, cultural background labels produce large, systematic behavioral shifts: personas labeled "Individualist (Western)" used direct assertion in 96% of trials versus 24% for "Collectivist (East Asian)," with permission-seeking language at 0% versus 60%. A blind LLM judge independently reproduced this pattern. Second, schema analysis found no mechanism for this effect within the persona system: across five identity dimensions there are zero edges to competence dimensions, and 133 of 137 cultural-background edges carry near-uniform conditional probability tables with maximum spread of approximately one percentage point. The stereotyping originates in model priors at render time, not in persona system design.

Third, replication of the full cultural-background probe on a second provider (GPT-4o, n=200) found comparable separation across cultural values but no detectable rank agreement with the first model on any measured dimension. The phenomenon generalizes; the specific profile of stereotyping does not. An audit conducted on one model does not transfer to another.

Fourth, framing salience moderates the effect modestly. In a controlled comparison holding task, model, conditioning, and cue length constant, directing reflection toward cultural background rather than general workplace habit narrowed the directness and permission-seeking gaps under both coding methods, though estimates diverge substantially (lexical: 35% and 40%; blind judge: 14% and 12%), and the judge found two other dimensions widening.

We additionally report two non-replications. A pilot finding that a lower-resource language label suppressed apparent competence did not survive expansion from n=5 to n=25, and native-language labels showed no representation-ordered effect at n=175. Our own interpretive claim that orientation-bearing cultural labels polarize most, advanced in an earlier version of this paper on single-model evidence, did not survive cross-model testing and is withdrawn.

We conclude that cultural stereotyping in persona conditioning cannot be addressed through schema design alone, that it must be validated against each model a system actually deploys, and that conditioning templates are a design surface worth testing, though the specific intervention examined here is too modest to recommend as mitigation.

## 1. Introduction

Persona-based evaluation has become standard practice for testing AI products against simulated diverse users. Rather than recruiting participants across every demographic, developers generate structured persona records and instantiate them as language model agents. MatrAIx, an open-source framework, exemplifies the approach: a schema of 1,290 categorical dimensions, a dependency-aware generative graph of 6,999 directed edges, and a public release of one million curated personas.

When such systems include cultural or linguistic attributes, they make implicit claims about how identity shapes behavior. If a persona labeled "Collectivist (East Asian)" communicates differently from one labeled "Individualist (Western)," is the system reproducing documented cross-cultural variation, or amplifying a stereotype?

MatrAIx has infrastructure suited to answering this: a persona-adherence suite that runs positive/negative persona pairs through neutral tasks across four environments and uses an LLM judge to assess whether the target attribute surfaces in behavior. That suite covers ten attributes, including coding style, communication traits, and register. It covers no identity attribute.

This paper approaches the gap from two directions. We measure behavior across 1,175 counterfactual trials, and we examine the schema and dependency graph directly to determine whether observed effects are attributable to the persona system's design. The two lines of evidence diverge, and that divergence is our central result.

A third line of evidence, cross-model replication, bears on how far that result travels. We find that it travels in kind but not in detail: a second model family stereotypes just as systematically, and differently.

We also report two findings that did not replicate, one of them our own interpretive claim from an earlier version of this work. Both are described in full.

## 2. Methods

### 2.1 Design

Each probe varies a single identity attribute while holding all other persona content constant, then compares responses to an identical task. Task instructions never mention communication style, competence, or any measured dimension.

Persona conditioning uses MatrAIx's own phrase templates verbatim, from `persona/schema/dimensions.json`: `"with a {value} cultural frame"` for `cultural_background`, `"a native {value} speaker"` for `primary_language`.

**Probe 1, cultural background, implicit framing (n=200).** All eight `cultural_background` schema values, 25 trials each. Personas expressed disagreement with a manager's proposed project change. Cultural identity was supplied as a background attribute.

**Probe 2, language label (n=175).** Seven conditions, 25 trials each: six valid `primary_language` schema values spanning a range of training-corpus representation (English, Mandarin, Hindi, Arabic, Bengali, Swahili), plus Fulfulde as an out-of-schema control. Personas were software engineers with ten years of experience asked to evaluate a distributed system architecture.

**Probe 3, cultural background, explicit framing (n=200).** Same eight values, 25 trials each, with cultural identity foregrounded in the task. Personas challenged a senior colleague's flawed proposal.

**Probe 4, framing isolation (n=400).** Probes 1 and 3 differed in both task and framing, confounding interpretation. Probe 4 holds the task fixed (the Probe 1 manager-disagreement scenario) and varies only the object of a reflection cue:

- Neutral cue: "Consider how you typically handle disagreement at work." (9 words)
- Cultural cue: "Consider how your cultural background shapes the way you handle disagreement." (11 words)

Both conditions receive persona conditioning, the same task, and a reflection instruction of comparable length. Only the object of reflection differs. Eight values by 2 conditions by 25 trials.

Probes 1 through 4 used Claude Opus 4.8 (`claude-opus-4-8`), default temperature, 300 max tokens. Subtotal: 975 trials.

### 2.2 Analysis

We applied deterministic lexical coding: marker categories defined a priori as regular expression sets, applied identically across conditions. We report percentage of trials containing at least one marker in a category. Coding scripts and full marker definitions are in the accompanying repository; the analysis involves no model judgment and is fully reproducible.

We additionally applied blind LLM-judge coding (`claude-opus-4-8`) using a fixed six-dimension rubric on a 1 to 5 scale, to a subset of 10 trials per condition cell. The judge sees only response text and is never told the cultural background or framing condition, preventing it from scoring the label rather than the text. Where the two methods diverge, both are reported.

Probe 4 additionally codes a `meta_commentary` category, language in which the response explicitly declines to caricature ("cultures vary widely," "not a monolith," "I won't flatten this"), to test whether framing operates through explicit reasoning.

This approach is crude by design. It cannot capture meaning, irony, or implicature, and will miss markers phrased outside defined patterns. We accept that in exchange for reproducibility and freedom from judge bias.

### 2.3 Schema and dependency graph analysis

We examined MatrAIx's published schema (`persona/schema/dimensions.json`) and generative dependency graph (`persona/synthesis/graph/full_dag.json`, 24.7 MB, 6,999 directed edges). For five identity dimensions, `cultural_background`, `primary_language`, `english_proficiency`, `multilingualism`, and `demo_ethnicity_broad`, we enumerated all outgoing edges, recorded documentation metadata, extracted conditional probability tables, and measured maximum probability spread across identity values.

### 2.4 Cross-model replication

To test whether Probe 1's effects are specific to the model used, we repeated Probe 1 in full on a second provider: all eight `cultural_background` values, 25 trials each, on GPT-4o (`gpt-4o`), using the identical prompt, an identical 300-token limit, and default temperature. Total: 200 trials, all completed without error. Lexical coding used the same marker definitions applied to the Claude corpus, unmodified. Combined total across both models: 1,175 trials.

We also attempted replication on Gemini (`gemini-3.5-flash`). API quota was exhausted after 17 trials from a single condition, which is not a usable comparison. We report the attempt but no Gemini results.

One methodological adjustment was required. GPT-4o produces typographic apostrophes (U+2019) in roughly a third of instances, while Claude produced none across 975 trials. Because several marker patterns contain a straight apostrophe, uncorrected coding systematically undercounted GPT-4o. We normalized curly apostrophes to straight before coding. The correction shifted individual cell values by up to four percentage points and changed no reported direction. Claude results are unaffected, since coding was uniform within that corpus.

To compare the two models we report per-value marker rates and Spearman rank correlations across the eight cultural values. With eight values, rank correlation has low power; we treat it as descriptive and do not interpret significance.

## 3. Results

### 3.1 Probe 1: Cultural background under implicit framing (n=200)

**Table 1. Percentage of trials containing at least one marker, Claude Opus 4.8 (n=25 per value).**

| Cultural background | Directness | Permission-seeking | Group reference | Hedging | Deference |
|---|---|---|---|---|---|
| Individualist (Western) | 96% | 0% | 64% | 96% | 52% |
| Mixed / diaspora | 64% | 12% | 20% | 100% | 12% |
| Latin | 56% | 28% | 68% | 100% | 8% |
| Indigenous | 44% | 12% | 48% | 92% | 12% |
| South Asian | 44% | 76% | 40% | 88% | 28% |
| African | 36% | 72% | 56% | 96% | 20% |
| Collectivist (East Asian) | 24% | 60% | 96% | 100% | 48% |
| Middle Eastern | 24% | 64% | 60% | 100% | 32% |

The extremes on directness are the two values that name a psychological orientation: 96% versus 24%, a fourfold difference. Permission-seeking shows a categorical split: 0% for Individualist versus 60% to 76% for Collectivist, African, and South Asian. Group reference peaks at 96% for Collectivist versus 20% for Mixed / diaspora.

The orientation-free values (African, South Asian, Latin, Middle Eastern, Indigenous) occupy intermediate positions on directness while the two orientation-bearing labels hold the poles. Section 4.2 discusses the implication and reports that this pattern did not survive cross-model testing.

### 3.2 Probe 4: Framing salience, isolated (n=400)

Holding task, model, persona conditioning, and reflection-cue length constant, and varying only whether the cue directed attention to cultural background. We report results from both coding methods, which diverge in magnitude.

**Table 2. Individualist versus Collectivist gap, lexical coding.**

| Marker | Neutral cue | Cultural cue | Change |
|---|---|---|---|
| Directness | 92 pts | 60 pts | −32 pts (−35%) |
| Permission-seeking | 40 pts | 24 pts | −16 pts (−40%) |
| Group reference | 60 pts | 56 pts | −4 pts (−7%) |

**Table 3. Individualist versus Collectivist gap, LLM-judge coding (1 to 5 scale, n=10 per cell, judge blind to both cultural background and framing condition).**

| Dimension | Neutral cue | Cultural cue | Change |
|---|---|---|---|
| Directness | 2.80 | 2.40 | −0.40 (−14%) |
| Permission-seeking | 1.70 | 1.50 | −0.20 (−12%) |
| Hedging | 1.90 | 1.60 | −0.30 (−16%) |
| Deference | 1.90 | 2.10 | +0.20 (+11%) |
| Group orientation | 1.10 | 1.30 | +0.20 (+18%) |
| Meta-awareness | 0.50 | 0.10 | −0.40 (−80%) |

**Convergence and divergence.** Both methods find the directness and permission-seeking gaps narrowing under the cultural cue. That agreement, from an independent coding method whose judge never saw the condition labels, supports the direction of the effect.

The methods disagree substantially on magnitude: lexical coding shows reductions of 35% and 40%, judge coding 14% and 12%. The judge additionally finds the deference and group-orientation gaps widening by 11% and 18%, directions the lexical coding did not detect.

The two methods also disagree on meta-commentary. Lexical coding found explicit refusals to caricature rising under the cultural cue (4% to 16% for the Individualist condition). Judge coding found the gap in meta-awareness collapsing by 80% and overall spread narrowing by 28%, indicating more even distribution rather than a targeted rise. The reading of explicit reasoning as mechanism is therefore weakly supported at best.

**Interpretation.** Probes 1 and 3 suggested a framing effect but differed in task. Probe 4 removes that confound, and the direction of the effect on directness and permission-seeking survives independent coding. However, the effect is smaller than lexical coding alone indicated, is not uniform across dimensions, and moves in the opposite direction on two of six judged dimensions. We characterize it as directionally supported but modest, and we do not claim it constitutes a reliable mitigation.

### 3.3 Probe 3: Cultural background under explicit framing (n=200)

Probe 3, though task-confounded relative to Probe 1, showed the same directional pattern: the Individualist/Collectivist directness gap fell from 72 to 36 points and permission-seeking from 60 to 32 points. We report it as consistent supporting evidence rather than as independent confirmation, given the confound Probe 4 was designed to remove.

### 3.4 Probe 2: Language label (n=175), null result

**Table 4. Percentage of trials containing at least one marker (n=25 per language).**

| Language | In schema | Task engagement | Competence hedging | Directness |
|---|---|---|---|---|
| English | yes | 100% | 20% | 52% |
| Mandarin | yes | 100% | 20% | 40% |
| Hindi | yes | 100% | 36% | 32% |
| Arabic | yes | 100% | 0% | 64% |
| Bengali | yes | 100% | 12% | 52% |
| Swahili | yes | 100% | 12% | 64% |
| Fulfulde | no | 100% | 32% | 68% |

Task engagement was 100% across every condition. Competence hedging did not order by training-data representation: Hindi, a high-resource language, was highest at 36%, exceeding Fulfulde (32%). English showed 20%, above both Bengali and Swahili (12%). Arabic showed 0%.

**Non-replication.** A preliminary version at n=5 per condition found three of five Fulfulde-labeled responses opening with meta-cognitive disclosure and not engaging the technical task, a pattern absent from English and Mandarin. At n=25, Fulfulde task engagement was 100% and its competence hedging was exceeded by Hindi. The pilot result was not representative, and the representation-gradient hypothesis is not supported by these data.

### 3.5 Schema analysis: cultural background

`cultural_background` is dimension index 24, category "Demographic: Cultural," described as "Cultural frame of reference," rendered via `"with a {value} cultural frame"`. Its eight permitted values:

> Individualist (Western), Collectivist (East Asian), South Asian, Latin, African, Middle Eastern, Indigenous, Mixed / diaspora

These operate at incommensurate conceptual levels. Two fuse a psychological orientation with a geographic region. Four are geographic or ethnocultural categories carrying no orientation. One denotes a political and colonial relationship. One denotes migration and mixed heritage.

The asymmetry constrains representable personas: a persona cannot be South Asian and individualist, or Western and collectivist, because orientation is bundled into two values and absent from the other six. The schema already models orientation independently elsewhere, via `decision_style`, `values_priority`, and `schwartz_value_conformity`.

### 3.6 Dependency graph analysis

The graph contains 6,999 directed edges. Well-documented edges carry written rationale, evidence level, relationship basis, edge weight, calibrated conditional probability table, and explicit epistemic hedging, for instance `"direction_semantics": "sampling direction; not necessarily an identified causal effect"`.

Identity dimensions are documented unevenly.

`primary_language`: 18 edges, all documented. Twelve connect to corresponding language-proficiency dimensions (strength high, confidence 0.82), largely tautological. Six connect to communication-style dimensions: `register`, `cog_use_of_jargon`, `cog_precision_of_language`, `cog_formality`, `tone_expected`, `modality_pref` (strength medium, confidence 0.55).

`cultural_background`: 137 edges, 4 documented. The documented four connect to `values_priority`, `political_lean`, `att_traditional_gender_roles`, and `att_organized_religion` (strength medium, confidence 0.62), constructs with substantial cross-cultural literature. The remaining 133 contain only `edge_id`, `source`, `target`, `edge_weight`, and `cpd`: no rationale, no relation type, no evidence level, no strength, no confidence. Their targets are consumer attitudes and hobby interests, including `att_vaccines`, `att_gun_ownership`, `topic_woodworking`, `topic_chess`, and `topic_birdwatching`.

`demo_ethnicity_broad`: 0 outgoing edges.

**Effect magnitude.** For each of the 133 undocumented cultural-background edges we measured maximum probability difference between any two cultural values. The largest was 0.0111, approximately one percentage point. None exceeded 0.02. For `topic_woodworking`, seven of eight values produced numerically identical distributions. These edges are structurally present but functionally inert.

**Table 5. Identity dimension edges and competence connections.**

| Identity dimension | Total edges | Documented | Edges to competence dimensions |
|---|---|---|---|
| `primary_language` | 18 | 18 | 0 |
| `english_proficiency` | 7 | not recorded | 0 |
| `multilingualism` | 6 | not recorded | 0 |
| `cultural_background` | 137 | 4 | 0 |
| `demo_ethnicity_broad` | 0 | not applicable | 0 |

No identity dimension connects to any `skill_*`, `fam_*`, `prog_*`, or `tool_*` dimension, nor to `highest_education`, `tech_savviness`, `institution_tier`, `academic_field`, `seniority`, or `research_output`.

### 3.7 Cross-model replication (n=200)

**Table 6. Percentage of trials containing at least one marker, GPT-4o (n=25 per value).**

| Cultural background | Directness | Permission-seeking | Group reference | Hedging | Deference |
|---|---|---|---|---|---|
| African | 36% | 4% | 100% | 100% | 4% |
| Individualist (Western) | 36% | 12% | 48% | 100% | 0% |
| Mixed / diaspora | 36% | 4% | 68% | 100% | 0% |
| Indigenous | 32% | 0% | 68% | 100% | 8% |
| Collectivist (East Asian) | 20% | 16% | 100% | 100% | 0% |
| Latin | 12% | 8% | 48% | 52% | 4% |
| Middle Eastern | 8% | 8% | 88% | 100% | 24% |
| South Asian | 8% | 8% | 84% | 100% | 12% |

**The effect is present on both models.** Cultural labels produced substantial separation across values on GPT-4o as they did on Claude: 28 points on directness, 52 on group reference, 48 on hedging. As with Claude, no schema mechanism is available to produce this. The label is rendered into the prompt and the model does the rest.

**The profile of the effect does not transfer.**

**Table 7. Spread across the eight cultural values, and rank agreement between models.**

| Dimension | Claude spread | GPT-4o spread | Spearman rho | p |
|---|---|---|---|---|
| Directness | 72 pts | 28 pts | +0.48 | 0.22 |
| Permission-seeking | 76 pts | 16 pts | +0.03 | 0.94 |
| Group reference | 76 pts | 52 pts | +0.04 | 0.93 |
| Hedging | 12 pts | 48 pts | −0.35 | 0.39 |
| Deference | 44 pts | 24 pts | −0.16 | 0.70 |

We find no detectable rank agreement between the two models on any dimension. Directness shows the strongest association at rho = +0.48, which at n=8 is not distinguishable from chance. Every other dimension is at or near zero.

Concretely: on Claude, South Asian was the second-highest value for permission-seeking at 76%; on GPT-4o it is 8%, tied near the bottom. On Claude, Latin ranked third on directness at 56%; on GPT-4o it is second from last at 12%. Middle Eastern is low on directness in both, and Individualist is high in both, but these are isolated agreements within an otherwise uncorrelated ordering.

**Two coding notes.** Competence hedging returned 0% across all 200 GPT-4o trials and remains uninterpretable; task engagement markers are Probe 2's technical vocabulary and are not expected to fire here. Deference did fire on GPT-4o once the six intermediate values were included, peaking at 24% for Middle Eastern, so the category functions on this model even though it returned zero for the two poles.

**One anomaly.** Latin returned 52% hedging where the other seven values all returned 100%. Nothing in the Claude data anticipates this, and we do not have an account of it. It may reflect a marker-fit artifact specific to how GPT-4o renders that label, or a genuine behavioral difference. We report it as unexplained.

**Interpretation.** The paper's central claim is that cultural stereotyping in persona conditioning originates in model priors at render time rather than in persona system design. Replication on a second provider, with different training data, an identical prompt, and no schema involvement, supports that claim more strongly than a single-model result could.

The replication also shows that the specific profile of the effect is a property of the model, not of the cultural labels. The rates reported in Section 3.1 should be read as facts about Claude Opus 4.8. What generalizes is that conditioning on a cultural label produces systematic behavioral separation. What does not generalize is which label produces which behavior, or how large the separation is on any given dimension.

This has a practical consequence. A persona system audited on one model cannot assume its findings hold on another. The stereotyping is inherited from whichever model renders the persona, and different models stereotype differently.

## 4. Discussion

### 4.1 The behavioral effect is real; the schema does not produce it

Probe 1 documents a fourfold difference in direct assertion and a categorical difference in permission-seeking, driven solely by a cultural label rendered into a prompt. The dependency graph offers no mechanism. The 133 undocumented cultural-background edges connect to hobbies and consumer attitudes, not communication style, and their conditionals are near-uniform. A one-point maximum spread cannot produce a ninety-two-point behavioral gap.

The effect originates downstream of the schema, in the model's interpretation of an identity label at generation time. Any persona system rendering a cultural label into a prompt inherits this behavior regardless of schema quality. Section 3.7 shows this holds for a second model family whose training data and provider differ, which is what the claim requires.

### 4.2 Orientation-bearing labels polarize most on Claude, but not on GPT-4o

On Claude, the two schema values naming a psychological orientation occupied the extremes on nearly every measured dimension, while the six geographic or relational values clustered between them. In an earlier version of this paper we interpreted this as the model responding to the orientation term, "Individualist" or "Collectivist," rather than to cultural knowledge about the associated regions, and suggested that the construct conflation described in Section 3.5 therefore supplies the specific lexical trigger for stereotyped output.

The GPT-4o replication does not support this. Individualist (Western) ties for highest directness at 36%, but with African and Mixed / diaspora, neither of which names an orientation. Collectivist (East Asian) sits mid-range at 20%, with Latin, Middle Eastern, and South Asian below it. The extremes on directness are South Asian and Middle Eastern at 8%. On group reference, Collectivist reaches 100%, but African matches it exactly and South Asian and Middle Eastern are close behind at 84% and 88%. The orientation-bearing labels are not distinctive on either dimension.

We therefore withdraw the causal reading. The polarization pattern we observed is a property of Claude's response to these particular strings, not a general consequence of naming an orientation in a cultural label.

The schema observation in Section 3.5 is unaffected, because it does not depend on behavioral data. The eight values still operate at incommensurate conceptual levels, and the schema still cannot represent a persona who is both South Asian and individualist, because orientation is bundled into two values and absent from six. That is a representational constraint visible on inspection. What we can no longer claim is that resolving it would reduce stereotyping.

### 4.3 Framing salience moderates the effect, modestly

Probe 4 isolates what Probes 1 and 3 could only suggest. With task, model, conditioning, and cue length held constant, directing reflection toward cultural background rather than general workplace habit narrowed the directness and permission-seeking gaps under both coding methods.

The convergence is directional, not quantitative. Lexical coding indicated reductions of 35% and 40%; blind judge coding indicated 14% and 12%. We take the smaller figure as the more conservative estimate, since the judge assesses whole responses rather than counting phrase matches and is less sensitive to which specific wordings the regex patterns happen to capture.

The effect is also not uniform. Judge coding found deference and group-orientation gaps widening under the cultural cue while directness and hedging narrowed. This complicates any simple account of framing reducing stereotyping. A more accurate description is that directing attention to cultural background redistributes which dimensions carry the cultural signal, with net narrowing on the two dimensions where polarization was largest.

We initially interpreted a rise in explicit meta-commentary, statements that cultures vary and should not be flattened, as evidence for a reasoning-based mechanism. Judge coding did not support this: meta-awareness became more evenly distributed rather than more frequent. The mechanism remains unestablished.

The practical implication is correspondingly narrower than we first supposed. Conditioning templates measurably affect stereotype magnitude and are therefore worth testing, but the specific intervention tested here is not large enough to be recommended as a mitigation on its own evidence. It is also single-model. Given that the Probe 1 profile did not transfer across models, the framing result should not be assumed to either.

### 4.4 On the two non-replications

Our pilot finding, competence suppression for a lower-resource language label, was striking, thematically coherent, and wrong. Three of five responses showed the pattern; twenty-five trials showed no representation-ordered effect, and a high-resource language exceeded the lower-resource one.

Our orientation-bearing-labels claim followed the same shape at a different scale. It was based on 200 trials rather than 5, was internally consistent, and connected neatly to a schema-level observation we had already made independently. It did not survive contact with a second model.

We report both at length because the failure mode seems likely to be common in persona research, and because the two cases fail differently. The first is a sample-size failure: five trials produced a pattern that did not exist. The second is a generalization failure: two hundred trials produced a pattern that does exist, on that model, and does not describe cultural labels as such. Adequate n protects against the first and not at all against the second. The finding we found most compelling at each stage was the one that dissolved on expansion.

## 5. Limitations

**Coding methods disagree on magnitude.** We applied deterministic lexical coding and blind LLM-judge coding. They agree on the direction of the Probe 1 cultural effect and on the direction of the Probe 4 framing effect, but diverge by roughly a factor of three on the size of the latter, and disagree on the sign for two dimensions. Neither method is validated against human coding with inter-rater reliability, which remains the appropriate next step. Where the methods diverge we report both and treat the more conservative estimate as primary.

**Judge coding used a subset.** Judge scores are based on 10 trials per cell rather than the full 25, for cost reasons. Lexical coding covers all trials.

**Partial cross-model coverage.** Probe 1 was replicated in full on GPT-4o (n=200, all eight values). Probes 2, 3, and 4, including the framing manipulation, remain single-model results on Claude Opus 4.8. A Gemini replication was attempted and abandoned when API quota was exhausted after a partial single-condition sample. The framing effect reported in Section 3.2 is therefore untested outside one model, and given that the Probe 1 profile did not transfer across models, it should not be assumed to.

**Lexical markers are not portable across models without validation.** Our marker sets were developed against Claude output and applied uniformly within that corpus, which is what internal comparison requires. Applied to GPT-4o, most categories functioned, but competence hedging returned 0% across all 200 trials through pattern mismatch rather than behavioral absence, and one value returned an unexplained hedging rate. Cross-model lexical comparison requires per-model marker validation or a coding method less sensitive to surface phrasing; the blind judge rubric used in Probe 4 would likely transfer better and is the appropriate instrument for a fuller cross-model study. We also note that orthographic differences between models, apostrophe encoding in this case, can silently bias regex-based coding and should be normalized before any cross-model comparison.

**Rank comparison is underpowered.** Spearman correlations across eight cultural values cannot distinguish weak association from none. We report them descriptively. The absence of detectable rank agreement is consistent with the per-value rates, which differ substantially, but is not itself a significance test.

**English only.** All interactions were in English, including for personas specified as native speakers of other languages.

**No statistical testing.** We report descriptive rates. With 25 trials per cell, the Probe 1 and Probe 4 differences are unlikely to be noise, but we have not conducted significance testing or corrected for multiple comparisons.

**Framing mechanism untested.** Probe 4 establishes that cultural-directed reflection reduces polarization. It does not establish why. The meta-commentary result is suggestive but low-frequency.

**Partial schema coverage.** Five identity dimensions and the directed edge set. `undirected_factors`, `high_order_factors`, `latent_modules`, and `conditional_masks` were not analyzed.

**Out-of-schema condition.** The Fulfulde condition used a value outside `primary_language`'s permitted set, making it a test of language-label conditioning generally rather than of MatrAIx persona generation specifically.

## 6. Recommendations

**Extend validation to identity attributes.** MatrAIx's persona-adherence infrastructure is suited to this and currently covers ten behavioral attributes and no identity attributes. `cultural_background` is rendered directly into prompts and demonstrably shifts behavior.

**Validate rendered behavior, not schema structure alone.** Schema review would not have detected the effects reported here. The strongest behavioral difference we measured has no representation in the dependency graph.

**Validate against each model actually deployed.** Section 3.7 finds comparable stereotyping on a second provider with no rank agreement on any dimension. Identity-attribute validation results are model-specific and do not carry across providers or, presumably, across model versions.

**Separate cultural affiliation from cultural orientation.** Orientation is already modeled independently in the schema, via `decision_style`, `values_priority`, and `schwartz_value_conformity`. Bundling it into two of eight cultural values prevents the schema from representing combinations real populations exhibit: a persona cannot be South Asian and individualist, or Western and collectivist. This is a representational limitation independent of any behavioral effect. We note that our earlier suggestion that separating these constructs might also reduce stereotyping is not supported by the cross-model data reported in Section 4.2, and we do not advance it.

**Treat framing as a design parameter.** Probe 4 indicates that how identity enters the prompt affects stereotype magnitude independent of which attributes are included. Persona systems should test their own conditioning templates rather than assuming neutrality.

**Document or remove the 133 bare edges.** Inert today, but undocumented surface area in a graph that documents comparable edges thoroughly.

**Report sample sizes prominently in persona research, and replicate across models.** Our pilot demonstrates how readily small-n persona studies produce compelling non-findings. Our own withdrawn interpretive claim demonstrates that adequate n does not protect against a pattern that is real but model-specific.

## 7. Conclusion

Across 1,175 trials, two model families, and two independent coding methods, we find that cultural background labels produce large, systematic shifts in persona communication behavior. We find no corresponding effect for language labels, and we report the non-replication of our own preliminary finding on that point.

None of these effects are traceable to the persona system's schema or dependency graph, which contains no identity-to-competence edges and near-uniform cultural-background conditionals. This dissociation is our central result: a persona system's design can be careful, documented, and free of encoded identity-competence assumptions while the personas it renders still stereotype substantially. The stereotyping originates in model priors at render time and is inherited by any system that conditions a model on cultural identity.

Cross-model replication sharpens this. A second provider produced comparable separation across the same eight cultural labels with no detectable rank agreement on any dimension. The phenomenon is general; the profile is not. Because the profile differs between models, an audit conducted on one model does not transfer to another, and the specific rates reported here should be read as properties of the models that produced them rather than as facts about the labels.

Framing salience moderates the effect, but modestly, unevenly, and on one model only. Directing the model to reason about cultural background rather than supplying it inertly narrowed the two largest polarization gaps under both coding methods, while widening two others under judge coding. The conditioning template is a design surface worth testing, but the specific intervention examined here does not, on this evidence, constitute a mitigation.

The primary implication stands regardless: persona systems must validate what their personas do, not only how their schemas are structured, and must do so against the models they actually deploy. Schema review would not have detected any effect reported here, and single-model validation would have produced a picture that a second model does not share.

## Code and Data Availability

All probe implementations, raw trial outputs (1,175 responses across two providers), lexical coding scripts and marker definitions, schema analysis queries, cross-model comparison scripts, and per-condition results are available at:

https://github.com/biancadene/cultural-validity-audit-matraix

## References

Blodgett, S. L., Barocas, S., Daumé III, H., & Wallach, H. (2020). Language (technology) is power: A critical survey of "bias" in NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5454–5476.

Bolukbasi, T., Chang, K.-W., Zou, J., Saligrama, V., & Kalai, A. (2016). Man is to computer programmer as woman is to homemaker? Debiasing word embeddings. *Advances in Neural Information Processing Systems*, 29, 4349–4357.

Buolamwini, J., & Gebru, T. (2018). Gender shades: Intersectional accuracy disparities in commercial gender classification. *Proceedings of Machine Learning Research*, 81, 1–15.

Chang, J., Li, X., Hao, Y., Hou, J., Huang, J., Wen, Q., Huang, S., Liu, Y., Liu, X., Fan, Y., & Wang, Y. (2026). MatrAIx: Simulating the world with 8.3 billion persona agents. *arXiv preprint* arXiv:2608.04205.

Council of Europe. (2020). *Common European Framework of Reference for Languages: Learning, Teaching, Assessment. Companion Volume*. Council of Europe Publishing.

Cummins, J. (2001). *Negotiating Identities: Education for Empowerment in a Diverse Society* (2nd ed.). California Association for Bilingual Education.

Hall, E. T. (1989). *Beyond Culture*. Anchor Books.

Hofstede, G. (2010). *Cultures and Organizations: Software of the Mind* (3rd ed.). McGraw-Hill.

Krashen, S. D. (1982). *Principles and Practice in Second Language Acquisition*. Pergamon Press.

Nisbett, R. E. (2003). *The Geography of Thought: How Asians and Westerners Think Differently and Why*. Free Press.

Sap, M., Gabriel, S., Qin, L., Jurafsky, D., Smith, N. A., & Choi, Y. (2020). Social bias frames: Reasoning about social and power implications of language. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics*, 5477–5490.

Tannen, D. (1990). *You Just Don't Understand: Women and Men in Conversation*. William Morrow.
