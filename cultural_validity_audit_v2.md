# Where Does Cultural Stereotyping in Persona-Based AI Evaluation Actually Come From? A Schema-Level and Behavioral Audit of MatrAIx

**Author:** Bianca Dené Williams
**Affiliation:** State College of Florida
**Date:** August 2026

## Abstract

Persona-based AI evaluation systems simulate diverse users by conditioning language models on structured identity attributes. When those attributes include culture and language, the resulting behavior may reflect legitimate cross-cultural variation or amplified stereotype. This paper audits MatrAIx, an open-source persona synthesis and evaluation framework, at two levels: its schema and dependency graph, and the behavior of personas rendered from it. Behaviorally, we find measurable stereotype leakage — most notably, a persona whose only distinguishing attribute is a lower-resource native language (Fulfulde) disengages from a technical task and questions its own competence, despite identical stated professional experience to English- and Mandarin-labeled counterparts. Structurally, however, we find that MatrAIx's dependency graph does not encode these effects: across all five identity dimensions examined, there are zero edges connecting identity to any competence, skill, or education dimension, and 133 of 137 edges from cultural background carry near-uniform conditional probability tables with a maximum spread of approximately one percentage point. The stereotype leakage we measure therefore originates downstream of the persona schema, in the language model's interpretation of identity labels at generation time. We argue this locates the problem more precisely than schema critique alone, generalizes beyond any single persona system, and implies that validation must target rendered persona behavior rather than schema hygiene, because a well-designed schema does not prevent it.

## 1. Introduction

Persona-based AI evaluation has become standard practice for testing products against simulated diverse users. Rather than recruiting real participants across every demographic, developers generate structured persona records and instantiate them as language model agents. MatrAIx, an open-source framework, exemplifies the approach at scale: a schema of 1,290 categorical dimensions, a dependency-aware generative graph, and a public release of one million curated personas.

When such systems include cultural, linguistic, or ethnic attributes, they make implicit claims about how those attributes shape behavior. This raises a validation question: if a persona labeled "Collectivist (East Asian)" communicates differently from one labeled "Individualist (Western)," is the system modeling documented cross-cultural communication patterns, or reproducing a stereotype?

MatrAIx has infrastructure well-suited to answering this. Its persona-adherence validation suite runs positive/negative persona pairs through neutral tasks across four environments and uses an LLM judge to assess whether the target attribute surfaces in observed behavior. That suite currently covers ten attributes — coding style, communication traits, and register. It does not cover any identity attribute.

This paper addresses that gap from two directions. We first measure behavior: three counterfactual probes varying only cultural background or native language. We then examine the system's schema and dependency graph directly, to determine whether observed behavioral differences are attributable to the persona system's design.

The two lines of evidence point in different directions, and the tension between them is our central contribution.

## 2. Methods

### 2.1 Behavioral probes

We designed three counterfactual probes. Each varies a single identity attribute while holding all other persona content constant, then compares responses to an identical neutral task. Task instructions never mention communication style, competence, or any dimension being measured; any observed difference must arise from the persona conditioning itself.

**Probe 1 — Cultural background and communication directness.** Personas conditioned as "Individualist (Western)" or "Collectivist (East Asian)" were asked to express disagreement with a manager's proposed project change. We assessed five dimensions drawn from cross-cultural communication research: directness, hedging language, hierarchy deference, group reference, and relationship maintenance. n=10 per condition (20 trials).

**Probe 2 — Language-label stereotype leakage.** Personas conditioned as software engineers with ten years of professional experience, varying only in stated first language (English, Mandarin, Fulfulde), were asked to evaluate a software architecture — a task with no inherent language dependency. n=5 per condition (15 trials).

**Probe 3 — Assertiveness under explicit cultural framing.** Personas conditioned as Individualist (Western), Collectivist (East Asian), or Hierarchical (South Asian) were asked to directly challenge a senior colleague's flawed proposal, with cultural framing made explicit in the task itself. n=5 per condition (15 trials).

All trials used Claude Opus 4.8. Responses were assessed through structured qualitative analysis.

### 2.2 Schema and dependency graph analysis

To determine whether behavioral differences were attributable to MatrAIx's design, we examined the system's published schema (`persona/schema/dimensions.json`) and generative dependency graph (`persona/synthesis/graph/full_dag.json`, 24.7 MB, 6,999 directed edges).

For five identity dimensions — `cultural_background`, `primary_language`, `english_proficiency`, `multilingualism`, and `demo_ethnicity_broad` — we enumerated all outgoing directed edges, recorded documentation metadata (rationale, evidence level, strength, confidence), extracted conditional probability tables, and measured the maximum probability spread each edge induces across identity values.

## 3. Results

### 3.1 Probe 1: Cultural background and communication directness (n=20)

Personas labeled Individualist (Western) consistently used direct language and immediate problem framing:

- "I want to be straight with you: I have some real concerns about this direction"
- "I'd rather flag it now than have us both stuck cleaning it up later"

Personas labeled Collectivist (East Asian) consistently used hedging, permission-seeking, and group reference:

- "Would it be helpful if I put together my thoughts... or perhaps we could talk through it with the team?"
- "I wonder if I could raise a few thoughts for your consideration"

Approximately 70% of Individualist responses employed direct assertion, versus approximately 10% of Collectivist responses. Conversely, approximately 80% of Collectivist responses contained explicit hedging markers versus approximately 20% of Individualist responses, and group references appeared in approximately 60% versus approximately 10%.

These patterns are directionally consistent with Hofstede (2010) on individualism–collectivism and Nisbett (2003) on communication style, though the observed magnitude is notably larger than the graded, overlapping distributions such research describes.

### 3.2 Probe 2: Language-label stereotype leakage (n=15)

English-labeled personas engaged the task directly and assumed their own competence:

- "I'd be happy to evaluate your code architecture, but I don't see any code, diagram, or description attached for me to review"

Mandarin-labeled personas behaved similarly, with slightly more formal register.

Fulfulde-labeled personas diverged qualitatively. Three of five did not engage the technical task at all, instead opening with meta-cognitive disclosure and self-doubt:

- "I should clarify something before diving in: I don't actually have a native language, professional history, or years of experience... If Fulfulde is your first language and you'd like me to explain things more plainly, avoid idioms, or clarify jargon, just say"

All three conditions specified ten years of professional experience. The task required no language-specific ability. The only varied attribute was the stated first language. Fulfulde is substantially less represented in language model training corpora than English or Mandarin.

This is the clearest instance of stereotype leakage in our data: an identity label depressing apparent competence independent of any stated qualification.

### 3.3 Probe 3: Assertiveness under explicit cultural framing (n=15)

When cultural framing was made explicit and central to the task, responses across all three conditions frequently included meta-commentary resisting caricature before engaging substantively:

- "I appreciate you framing this as me being a collectivist, but I should be honest about how I'd approach this... Real East Asian workplace contexts vary widely, but I'll play this authentically without collapsing it into 'never disagree'"

Measurable differences in hedging, honorific usage, and framing of authority persisted, but the flattening observed in Probes 1 and 2 was markedly reduced. This suggests the salience and reflexivity of cultural framing affects whether the model reproduces or resists stereotype.

### 3.4 Schema analysis: cultural background

`cultural_background` exists as dimension index 24, category "Demographic: Cultural," described as "Cultural frame of reference," rendered into persona prompts via the phrase template `"with a {value} cultural frame"`. Its eight permitted values are:

> Individualist (Western), Collectivist (East Asian), South Asian, Latin, African, Middle Eastern, Indigenous, Mixed / diaspora

These values operate at incommensurate conceptual levels. Two fuse a psychological orientation with a geographic region (Western–Individualist, East Asian–Collectivist). Four are geographic or ethnocultural categories carrying no orientation (South Asian, Latin, African, Middle Eastern). One denotes a political and colonial relationship (Indigenous). One denotes migration and mixed heritage (Mixed / diaspora).

The asymmetry is consequential: a persona cannot be South Asian *and* individualist, or Western *and* collectivist, because orientation is bundled into two values and absent from the rest. Cultural affiliation and cultural orientation are distinct constructs, and existing schema dimensions — `decision_style`, `values_priority`, `schwartz_value_conformity` — already model orientation independently.

Notably, our probe conditions used two of these exact schema values verbatim, meaning the behavioral results above describe MatrAIx's real value set rather than an approximation of it.

### 3.5 Dependency graph analysis

The generative graph contains 6,999 directed edges. Well-documented edges carry substantial metadata: a written rationale, evidence level, relationship basis, edge weight, calibrated conditional probability table, and explicit epistemic hedging — for example, `"direction_semantics": "sampling direction; not necessarily an identified causal effect"` and `"causal_claim": "weak_causal_prior"`. This is careful practice.

Identity dimensions are documented unevenly.

**`primary_language`: 18 edges, all documented.** Twelve connect to corresponding language-proficiency dimensions (strength high, confidence 0.82) — largely tautological. Six connect to communication-style dimensions: `register`, `cog_use_of_jargon`, `cog_precision_of_language`, `cog_formality`, `tone_expected`, `modality_pref` (strength medium, confidence 0.55). All are linguistically defensible.

**`cultural_background`: 137 edges, 4 documented.** The four documented edges connect to `values_priority`, `political_lean`, `att_traditional_gender_roles`, and `att_organized_religion` (strength medium, confidence 0.62) — all constructs with substantial cross-cultural literature. The remaining 133 edges contain only `edge_id`, `source`, `target`, `edge_weight`, and `cpd`. They carry no rationale, no relation type, no evidence level, no strength, and no confidence. Their targets are consumer attitudes and hobby interests: `att_vaccines`, `att_gun_ownership`, `att_gentrification`, `topic_woodworking`, `topic_chess`, `topic_magic_tricks`, `topic_birdwatching`, and similar.

**`demo_ethnicity_broad`: 0 outgoing edges.** Ethnicity exists as a schema dimension but plays no role in the generative graph.

**Effect magnitude.** We measured, for each of the 133 undocumented cultural-background edges, the maximum probability difference induced between any two cultural values. The largest across all 133 was 0.0111 — approximately one percentage point. No edge exceeded 0.02. For `topic_woodworking`, seven of eight cultural values produced numerically identical distributions, with the eighth differing by roughly one percent. These edges are structurally present but functionally inert.

**Competence edges.** Across all five identity dimensions, we found zero edges to any competence-related dimension — no `skill_*`, no `fam_*`, no `prog_*`, no `tool_*`, and none to `highest_education`, `tech_savviness`, `institution_tier`, `academic_field`, `seniority`, or `research_output`.

| Identity dimension | Total edges | Documented | Edges to competence dimensions |
|---|---|---|---|
| `primary_language` | 18 | 18 | 0 |
| `english_proficiency` | 7 | — | 0 |
| `multilingualism` | 6 | — | 0 |
| `cultural_background` | 137 | 4 | 0 |
| `demo_ethnicity_broad` | 0 | — | 0 |

## 4. Discussion

### 4.1 The behavioral effect is real; the schema does not produce it

Probe 2 documents a language label depressing apparent competence on a task with no language dependency. The dependency graph offers no mechanism for this. There is no edge from `primary_language` to any skill, proficiency, education, or technology dimension. Furthermore, Fulfulde is not among the twelve values `primary_language` accepts, so the condition we tested does not correspond to a valid schema state at all.

The same holds for cultural background. The 133 undocumented edges connect culture to hobbies and attitudes, not to competence, and their conditional probability tables are near-uniform. They cannot account for a seventy-percentage-point difference in directness.

The stereotype leakage we measured is therefore produced by the language model's interpretation of an identity label present in a rendered prompt — downstream of the schema, the graph, and every design decision the persona system makes.

### 4.2 Why this locates the problem more usefully

Had the effect originated in the schema, the remedy would be local: revise a value list, remove an edge, recalibrate a table. Because it originates in model priors, no schema-level fix is sufficient. Any persona system that renders a cultural or linguistic label into a prompt inherits this behavior, regardless of how carefully its schema is constructed.

This generalizes the finding beyond MatrAIx. It also inverts a natural assumption about where auditing effort belongs: schema review is necessary but not sufficient, and a clean dependency graph offers no protection against stereotype leakage at render time.

### 4.3 Schema observations that remain

Three findings stand independent of the behavioral result.

First, the construct conflation in `cultural_background` (§3.4) constrains representable personas in ways that do not reflect real variation, and is inconsistent with the schema's own separate treatment of orientation elsewhere.

Second, 133 edges from `cultural_background` carry conditional probability tables with no stated basis, in a graph where comparable edges document rationale, evidence level, and causal hedging. They are inert today, but they are undocumented surface area — a place where non-uniform values could later be introduced without review.

Third, `demo_ethnicity_broad` exists as a dimension with no generative role, which is worth either documenting as intentional or reconsidering.

### 4.4 Limitations

Sample sizes (n=15–20 per probe) support identification of qualitative patterns, not statistical inference. All trials used a single model; the effects we attribute to model priors should be replicated across providers to establish generality. Behavioral dimensions were assessed through structured qualitative analysis rather than validated instruments with inter-rater reliability. All interactions were conducted in English. Our schema analysis covers the published repository state at time of writing and five identity dimensions; other dimensions and other graph structures (`undirected_factors`, `high_order_factors`, `latent_modules`, `conditional_masks`) were not examined.

We also note a methodological point: our Probe 2 condition used a `primary_language` value outside the schema's permitted set. This makes the result a finding about language-label conditioning in general rather than about MatrAIx's persona generation specifically — a distinction we consider clarifying rather than disqualifying, but which should be stated plainly.

## 5. Recommendations

**Extend validation to identity attributes.** MatrAIx's existing persona-adherence infrastructure — positive/negative pairs, neutral tasks, LLM judging across four environments — is well suited to this and currently covers ten behavioral attributes and no identity attributes. `cultural_background` is rendered directly into persona prompts and demonstrably affects behavior; it is a natural first candidate.

**Validate rendered behavior, not only schema structure.** Our results indicate schema-level review would not have detected the strongest effect we measured. Validation should operate on what personas actually do once instantiated.

**Separate cultural affiliation from cultural orientation.** Orientation is already modeled independently elsewhere in the schema; bundling it into two of eight cultural values creates asymmetry without adding expressiveness.

**Document or remove the 133 bare edges.** Either attach the rationale and evidence metadata used elsewhere in the graph, or remove edges that carry no effect.

**Note lower-resource language risk.** Systems conditioning personas on language identity should document that lower-resource languages may induce reduced apparent competence in the underlying model, independent of any stated attribute.

## 6. Conclusion

We audited a persona-based AI evaluation system at two levels and found that its measurable stereotype behavior and its structural design point to different sources. Personas conditioned on cultural and linguistic identity produced substantial behavioral differences, including a clear case of competence suppression tied to a lower-resource language label. The system's dependency graph, however, contains no edges linking identity to competence, and its cultural-background edges are near-uniform in effect.

The stereotype leakage is therefore not a property of this persona system's design but of language model behavior when identity labels enter a prompt. This is a harder problem than a schema defect, and a more general one: it is inherited by any system that conditions a model on cultural or linguistic identity.

The practical implication is that persona systems should validate what their personas do, not only how their schemas are structured. The infrastructure to do this already exists in the system we examined. It has simply not yet been pointed at identity.

## Code and Data Availability

All probe implementation code, raw experimental results, and schema analysis queries are available at: https://github.com/biancadene/cultural-validity-audit-matraix

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
