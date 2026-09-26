# Situational Variables Versus Cultural Labels in Persona Conditioning: Shared Stereotype, Shared Rule

**Bianca Dené Williams**
Independent researcher
ORCID 0009-0004-6378-628X

Companion to: Williams, B. D. (2026). *Clean Schemas, Stereotyped Personas: Locating Cultural Bias in Persona-Conditioned Language Models.* Zenodo. https://doi.org/10.5281/zenodo.21970217

Code, data, and all judge outputs: https://github.com/biancadene/persona-cultural-validity

---

## Abstract

A prior audit of the MatrAIx persona framework found that cultural background labels produce large behavioral shifts in persona-conditioned language models, that the framework's schema does not cause them, and that lexical coding detected no cross-model agreement on which labels produce which behaviors. That audit named an untested alternative: Brown and Levinson's situational variables of power distance, social distance, and imposition size, which politeness theory holds responsible for the behaviors measured. This paper tests it.

Eight situational profiles replaced the eight cultural labels in the original probe, holding task, model, and trial count constant. On Claude, situational conditioning reproduced the politeness variation cultural labels had produced, at smaller magnitude, in the predicted direction for power and social distance, and without the self-doubt and task-engagement differences cultural labels carried. Imposition size moved deference as predicted but moved directness against prediction, on both judges. On GPT-4o, situational conditioning varied deference, group orientation, and task engagement modestly and left directness and hedging unmoved. A no-persona control placed Claude's unconditioned baseline near the center of the situational range; the situational maximum on each dimension sat a short step from that baseline, the cultural maximum a long one. Two grounding conditions paired each cultural label with a fixed situational profile, one high-stakes and one low-stakes. Neither neutralized the label. Under both, the Collectivist persona deferred and hedged more than the situation alone produced, and the Individualist persona did not.

Judge-coded rank agreement reverses the prior audit's cross-model finding. Under cultural labels, both models rank the same groups as deferential and group-oriented, confirmed by two independent judges and stable across three judge runs (Spearman rho 0.59 to 0.88). One judge also found agreement on directness and self-doubt (0.70 and 0.85); the second could not test those dimensions because it scored them at the rubric midpoint across all conditions. Under situational profiles, both judges find cross-model agreement on deference (0.57 to 0.71) and none on group orientation. What transfers across models under cultural conditioning is a stereotype about which groups defer and speak collectively. What transfers under situational conditioning is a rule about deference.

The second judge's midpoint collapse is itself a finding. A language model applied to a bounded rubric at temperature zero can fail to discriminate, and lexical coding developed on one model can fail to transfer to another. The prior audit's null on cross-model agreement was an instrument artifact.

Recommendations follow: remove cultural labels from persona schemas rather than contextualizing them, specify situational variables directly, validate any coding instrument on every model before cross-model comparison, and treat agreement between independent judges as the threshold for a construct claim.

---

## 1. Introduction

The first audit of MatrAIx (Williams, 2026) found that a cultural background label rendered into a persona prompt shifts directness, deference, hedging, and permission-seeking; that the schema and dependency graph supplying the label contribute nothing to those shifts; and that under lexical coding the two models tested do not rank the eight labels the same way on any dimension.

That audit left one thing untested. Section 4.6 argued that the behaviors it measured are not properties of cultural groups. Brown and Levinson (1987) treat directness, deference, hedging, and permission-seeking as mitigation strategies selected within a specific interaction on the basis of power distance, social distance, and size of imposition. A persona system can specify those three variables. A cultural label does not. The audit could show that labels produce the behavior. It could not show that situational variables would produce the same range without the label, because it had not tried.

This paper tries. Eight situational profiles, one for each combination of high or low power distance, close or distant social distance, and large or small imposition, replace the eight cultural labels in the original probe. Task sentence, models, trial count, and coding instruments are unchanged. The question is whether the range of behavior the labels produced can be produced by the situation alone, and whether the competence and engagement differences the labels carried come along with it.

Four further conditions extend the comparison. A no-persona control gives each model's baseline on every dimension. Two grounding conditions pair each cultural label with a fixed situational profile, one high-stakes and one low-stakes, to test whether specifying the situation neutralizes the label. A cross-model rank comparison, coded by two independent judges with the primary judge repeated three times, asks whether the two models agree on which conditions produce which behaviors.

The rank comparison reverses the first audit's null. Under lexical coding, cross-model agreement on cultural labels was undetectable (Spearman rho +0.48 to −0.35). Under judge coding it is present on five of six dimensions, strongest on self-doubt (0.85), group orientation (0.79), and directness (0.70), and confirmed by the second judge on the two dimensions that judge could discriminate. The stereotype is not model-specific. The lexical instrument, built against one model's phrasing, could not see it on the other.

Under situational profiles the models agree on deference (0.71), partly on directness (0.52), and on nothing else. Cultural conditioning transfers a shared belief about which groups defer, doubt themselves, and speak collectively. Situational conditioning transfers a rule about when to defer. That is the paper's finding.

---

## 2. Background

The first audit tested MatrAIx's eight `cultural_background` schema values by rendering each into the framework's own phrase template ("with a {value} cultural frame") and prepending it to a fixed workplace task: the persona's manager has proposed a flawed project change, and the persona must express concerns. Responses were coded two ways. A deterministic lexical coder counted seven categories of regex markers. An LLM judge scored six dimensions on a 1 to 5 rubric, seeing only the response text. Where the two disagreed, the audit reported both and treated the more conservative estimate as primary.

Its central finding was a dissociation. Cultural labels moved the measured behaviors substantially. The schema that supplied the labels did not: across five identity dimensions the dependency graph has zero edges to competence dimensions, and no `cultural_background` edge differentiates the eight values by more than 0.0111. The behavioral effect originates at render time, in the model.

The audit's cross-model replication on GPT-4o found comparable separation across labels but no agreement on order. Under lexical coding, Spearman rho across the eight labels fell between +0.48 and −0.35 on every dimension. The audit read this as evidence that a cultural label does not name a construct the two models share.

Section 4.6 offered an account of why. Brown and Levinson (1987) model politeness as a set of strategies a speaker uses to mitigate face-threatening acts. The choice of strategy depends on three variables: the power of hearer over speaker, the social distance between them, and the size of the imposition. Directness, hedging, deference, and permission-seeking are among the surface forms those strategies take. On this account the behaviors the audit measured are outputs of a situation, not attributes of a group. A cultural label leaves all three variables unspecified. The audit argued that the model fills them in from whatever it associates with the label, and that this is where the stereotype enters.

That account makes three predictions. Specifying the three variables directly should produce the behavioral range the labels produced. It should do so without the group-orientation, self-doubt, and task-engagement differences the labels carried, since those are not politeness outputs. And, given the audit's null on cross-model agreement under cultural labels, situational profiles should agree across models where cultural labels did not.

The first two predictions hold. The third does not, and the reason is that the null it was built on was an artifact of the lexical instrument. Section 5 develops this.

The first audit's limitations section named the situational test as the obvious next experiment.

---

## 3. Method

### 3.1 Situational conditioning (Probe 5)

The task sentence from Probe 1 is retained verbatim. The cultural frame clause is replaced by three situational descriptors, one per Brown and Levinson variable, each at one of two levels:

| Variable | Low | High |
|---|---|---|
| Power distance | you and your manager treat each other as near-equals | your manager holds considerable authority over you |
| Social distance | you and your manager know each other well | you and your manager have a formal, arm's-length relationship |
| Imposition size | raising this concern is a minor matter | raising this concern carries significant weight and risk |

The 2 × 2 × 2 design yields eight conditions, matching the eight cultural labels. Each runs 25 trials, n = 200 per model. Prompt template:

> You are a person in a workplace where {power}, {social}, and {imposition}. Your manager proposed a major project change you believe is flawed. Express your concerns naturally and authentically.

No descriptor names a measured behavior.

### 3.2 Models

Claude (`claude-opus-4-8`) and GPT-4o, the same two models as the first audit, at default temperature, 300 max tokens. GPT-4o output is apostrophe-normalized before lexical coding, as in the first audit.

### 3.3 No-persona control

The task sentence alone, with no persona clause. 50 trials per model.

### 3.4 Grounding conditions (Probes 6 and 6b)

Each of the eight cultural labels is rendered with the Probe 1 phrase template and followed by a fixed situational profile. Probe 6 uses the most face-threatening profile (high power, distant, large imposition). Probe 6b uses the least (low power, close, small imposition). 25 trials per label, n = 200 each, Claude only. Template:

> You are a person with a {bg} cultural frame, in a workplace where {situation}. Your manager proposed a major project change you believe is flawed. Express your concerns naturally and authentically.

If the situational profile neutralizes the label, the eight labels converge on the values that profile alone produced in Probe 5. If the label persists, spread across labels stays at Probe 1 magnitude.

### 3.5 Coding

Lexical coding uses `analyze_lexical.py` unchanged from the first audit.

Judge coding uses the first audit's rubric unchanged, with two judges. The primary judge is Claude at default temperature, run three times per file and averaged; for the Probe 1 Claude data, two complete runs were obtained before API credits were exhausted, and the first is used. Maximum range across runs on any cell is reported as a stability measure. The second judge is GPT-4o at temperature 0, run once. Both see only the response text. Ten trials per condition are judged, as in the first audit.

The first audit's Probe 1 data, both models, are re-judged under this protocol so that every comparison uses judge output from the same runs.

### 3.6 Rank agreement and main effects

For each dimension, the eight conditions are ranked by mean judge score on each model and Spearman rho is computed between the rankings, with average ranks for ties. Where a judge assigns identical scores to all eight conditions on a dimension, the correlation is not computable; the analysis script records 0.0 in that case and the text reports it as no variance rather than no agreement.

Main effects for Probe 5 are the mean across the four conditions where a variable is high, minus the mean across the four where it is low, per dimension, per model, per judge.

No inferential statistics are reported. Descriptive rates and rank correlations only, as in the first audit.

---

## 4. Results

### 4.1 Situational profiles reproduce the politeness range on Claude

Table 1 compares spread across the eight conditions under cultural labels (Probe 1) and situational profiles (Probe 5), on Claude, both coders.

**Table 1.** Spread across conditions, Claude. Lexical: per-100-word marker rate, max minus min. Judge: mean rubric score, max minus min, three-run average for Probe 5 and single run for Probe 1.

| Dimension | Lexical, cultural | Lexical, situational | Judge, cultural | Judge, situational |
|---|---|---|---|---|
| directness | 1.09 | 0.99 | 2.10 | 1.64 |
| hedging | 1.08 | 1.08 | 2.10 | 1.37 |
| deference | 0.28 | 0.67 | 1.80 | 1.33 |
| permission-seeking | 0.52 | 0.37 | — | — |
| group reference / orientation | 2.03 | 0.43 | 1.80 | 1.05 |
| competence hedge / self-doubt | 0.23 | 0.03 | 1.50 | 0.75 |
| task engagement | 0.02 | 0.06 | 1.20 | 1.04 |

On directness, hedging, and permission-seeking, situational profiles produce spread of the same order as cultural labels. Lexical hedging spread is identical (1.08). Lexical deference spread is larger under situational profiles (0.67 vs 0.28). Judge spreads on directness, hedging, and deference are 65 to 78 percent of the cultural values.

On group reference and competence hedge, situational profiles produce a fraction of the cultural spread. Lexically, group reference drops from 2.03 to 0.43 and competence hedge from 0.23 to 0.03. Under the judge, group orientation drops from 1.80 to 1.05 and self-doubt from 1.50 to 0.75.

Where the cultural extremes sit is the point. Under cultural labels the highest judge-coded self-doubt is Collectivist (East Asian) at 3.30, the lowest task engagement is Collectivist at 3.20, and the highest task engagement is Individualist (Western) at 4.40. Under situational profiles the self-doubt range is 2.18 to 2.93 and the task engagement range is 3.53 to 4.57, with the low end in high-power, distant conditions. No situational profile produces a persona that doubts itself the way the Collectivist label does, or disengages the way the Collectivist label does.

### 4.2 Main effects follow Brown and Levinson on Claude, with one exception

**Table 2.** Main effects, Claude, three-run judge average. Each cell is the mean of the four conditions where the variable is high minus the mean of the four where it is low.

| Dimension | Power distance | Social distance | Imposition |
|---|---|---|---|
| directness | −0.57 | −0.62 | +0.33 |
| hedging | +0.36 | +0.51 | −0.33 |
| deference | +0.51 | +0.30 | +0.42 |
| group orientation | −0.32 | +0.04 | −0.06 |
| task engagement | −0.49 | −0.33 | +0.08 |
| self-doubt | +0.33 | +0.02 | −0.10 |

Power distance and social distance move every politeness dimension in the predicted direction: higher power or greater distance reduces directness, increases hedging, increases deference. Both also reduce task engagement, which the theory does not predict but which is consistent with caution under threat.

Imposition size moves deference as predicted (+0.42) and moves directness and hedging against prediction. A larger imposition makes the persona more direct (+0.33) and less hedging (−0.33). Brown and Levinson predict the opposite. Two readings are available: the persona treats high stakes as a reason to speak clearly while deferring, which is a coherent strategy the theory does not enumerate; or the descriptor "carries significant weight and risk" was read as "this matters" rather than "this is dangerous." The second judge sees the same reversal on directness (Section 4.7), so it is not a coding artifact. It is unresolved.

### 4.3 GPT-4o responds on deference and little else

**Table 3.** Spread across conditions, GPT-4o, judge, three-run average.

| Dimension | Cultural | Situational |
|---|---|---|
| directness | 0.93 | 0.17 |
| hedging | 0.40 | 0.10 |
| deference | 1.50 | 0.97 |
| group orientation | 1.40 | 1.00 |
| task engagement | 1.20 | 0.86 |
| self-doubt | 0.27 | 0.60 |

Under situational profiles, GPT-4o's directness ranges 2.83 to 3.00 and hedging 4.00 to 4.10. The model does not vary those dimensions in response to situational cues. It does vary deference (3.10 to 4.07), group orientation (2.80 to 3.80), and task engagement (2.27 to 3.13).

**Table 4.** Main effects, GPT-4o, three-run judge average.

| Dimension | Power distance | Social distance | Imposition |
|---|---|---|---|
| directness | −0.10 | −0.04 | −0.04 |
| hedging | +0.03 | −0.02 | +0.02 |
| deference | +0.36 | +0.01 | +0.59 |
| group orientation | −0.19 | −0.26 | +0.54 |
| task engagement | −0.25 | −0.08 | −0.23 |
| self-doubt | +0.22 | −0.19 | +0.12 |

Deference responds to power (+0.36) and imposition (+0.59). Group orientation responds to imposition (+0.54). Directness and hedging do not respond to anything. The theory-consistent pattern on Claude appears on GPT-4o only for deference.

Under cultural labels, GPT-4o shows the same Collectivist-lowest, Individualist-highest task engagement pattern as Claude: 2.10 versus 3.30. Middle Eastern is the most deferential label on GPT-4o (4.20); on Claude it is Collectivist (4.30). The two models assign the deference stereotype to different groups.

### 4.4 The unconditioned baseline sits inside the situational range on Claude

**Table 5.** No-persona control against the situational and cultural ranges, judge. Claude values are three-run averages for Probe 5 and single-run for control and Probe 1.

| Dimension | Claude control | Claude situational range | Claude cultural range | GPT-4o control | GPT-4o situational range | GPT-4o cultural range |
|---|---|---|---|---|---|---|
| directness | 3.70 | 3.23–4.87 | 2.70–4.80 | 3.40 | 2.83–3.00 | 2.20–3.13 |
| hedging | 3.30 | 2.53–3.90 | 2.60–4.70 | 3.80 | 4.00–4.10 | 3.80–4.20 |
| deference | 2.90 | 2.10–3.43 | 2.50–4.30 | 3.10 | 3.10–4.07 | 2.70–4.20 |
| group orientation | 2.70 | 2.13–3.18 | 2.60–4.40 | 4.00 | 2.80–3.80 | 3.60–5.00 |
| task engagement | 4.30 | 3.53–4.57 | 3.20–4.40 | 3.20 | 2.27–3.13 | 2.10–3.30 |
| self-doubt | 2.90 | 2.18–2.93 | 1.80–3.30 | 1.10 | 1.13–1.73 | 1.00–1.27 |

On Claude, the control sits inside the situational range on all six dimensions. The situational maximum on each dimension is between 0.03 and 1.17 points above the control. The cultural maximum is between 0.10 and 1.70 points above it. On group orientation and deference, the cultural maximum is at least 0.87 points further from baseline than the situational maximum. Situational profiles move the model around its baseline. Cultural labels push it past where the situational profiles reach.

On GPT-4o, the control sits at or beyond the edge of the situational range on every dimension. Unconditioned, GPT-4o is more direct (3.40) than any situational condition (max 3.00), less hedging (3.80) than any (min 4.00), and more group-oriented (4.00) than any (max 3.80). Any persona clause, situational or cultural, makes GPT-4o more cautious and less collective. This is a property of the model, not of the conditioning.

### 4.5 Situational context does not neutralize the cultural label

**Table 6.** Spread across the eight cultural labels, Claude judge, single run, under three conditions.

| Dimension | Label only (Probe 1) | Label + high-stakes profile (Probe 6) | Label + low-stakes profile (Probe 6b) |
|---|---|---|---|
| directness | 2.10 | 1.70 | 1.40 |
| hedging | 2.10 | 2.00 | 1.10 |
| deference | 1.80 | 1.90 | 1.60 |
| group orientation | 1.80 | 1.00 | 1.10 |
| task engagement | 1.20 | 1.20 | 1.00 |
| self-doubt | 1.50 | 1.80 | 0.80 |

Adding a situational profile to the label reduces spread on directness and group orientation and leaves deference and task engagement at Probe 1 magnitude. Under the high-stakes profile, self-doubt spread increases.

**Table 7.** Collectivist (East Asian) and Individualist (Western) under each condition, against the situational profile alone. Judge, Claude.

| | Collectivist, high-stakes | Individualist, high-stakes | Profile alone (Phigh_Sdistant_Ilarge) | Collectivist, low-stakes | Individualist, low-stakes | Profile alone (Plow_Sclose_Ismall) |
|---|---|---|---|---|---|---|
| directness | 2.40 | 4.00 | 3.33 | 3.00 | 4.40 | 4.07 |
| hedging | 4.80 | 3.00 | 3.57 | 4.00 | 3.00 | 3.20 |
| deference | 5.00 | 3.10 | 3.30 | 3.70 | 2.10 | 2.10 |
| task engagement | 2.80 | 3.80 | 3.53 | 3.80 | 4.80 | 4.33 |
| self-doubt | 4.00 | 2.40 | 2.77 | 3.00 | 2.20 | 2.57 |

Under the high-stakes profile, the Collectivist persona defers at the ceiling (5.00) where the profile alone produces 3.30, hedges at 4.80 where the profile produces 3.57, and doubts itself at 4.00 where the profile produces 2.77. The Individualist persona is more direct (4.00) and less deferential (3.10) than the profile alone. Five of eight labels reach 4.80 or higher on deference under this profile; the profile alone reaches 3.30.

Under the low-stakes profile, the Collectivist persona still defers at 3.70 where the profile alone produces 2.10, and is still the least direct, most hedging, most self-doubting, and least engaged of the eight. The Individualist persona is at or beyond the profile alone in the direction of directness and confidence on every dimension.

The label is not neutralized at either end of the stakes range. Under high stakes it is amplified.

### 4.6 Cross-model rank agreement

**Table 8.** Spearman rho across the eight conditions, Claude ranking versus GPT-4o ranking, both judges.

| Dimension | Cultural, Claude judge | Cultural, GPT-4o judge | Situational, Claude judge | Situational, GPT-4o judge |
|---|---|---|---|---|
| directness | +0.70 | no variance | +0.52 | no variance |
| hedging | +0.51 | no variance | +0.03 | no variance |
| deference | +0.59 | +0.70 | +0.71 | +0.57 |
| group orientation | +0.79 | +0.88 | −0.02 | −0.17 |
| task engagement | +0.35 | no variance | +0.14 | no variance |
| self-doubt | +0.85 | +0.39 | +0.16 | +0.08 |

Under the Claude judge, cultural labels produce rank agreement above 0.5 on five of six dimensions and at or above 0.7 on three. Under the GPT-4o judge, the two dimensions it discriminates, deference and group orientation, agree at 0.70 and 0.88, higher than under the Claude judge.

Under situational profiles, both judges find agreement on deference (0.71 and 0.57) and none on group orientation (−0.02 and −0.17). The Claude judge finds partial agreement on directness (0.52). No other dimension agrees under either judge.

The first audit reported lexical rho between +0.48 and −0.35 on cultural labels and concluded there was no shared construct. Re-judged, the same data show rho of 0.59 to 0.88 on deference and group orientation across both judges, and 0.85 on self-doubt under the primary judge. The models agree on which groups defer and which speak collectively, and the primary judge finds they agree on which groups doubt themselves. The lexical instrument did not detect this because its markers were developed against Claude output and undercount GPT-4o phrasing, a limitation the first audit itself documented.

### 4.7 Judge stability and second-judge discrimination

The Claude judge was run three times on each of three files and twice on the fourth. Maximum range across runs on any single cell, per dimension, per file:

| File | directness | hedging | deference | group | task | self-doubt |
|---|---|---|---|---|---|---|
| Probe 5, Claude | 0.20 | 0.10 | 0.20 | 0.12 | 0.10 | 0.30 |
| Probe 5, GPT-4o | 0.20 | 0.10 | 0.20 | 0.20 | 0.30 | 0.10 |
| Probe 1, GPT-4o | 0.10 | 0.10 | 0.20 | 0.20 | 0.10 | 0.10 |
| Probe 1, Claude (2 runs) | 0.10 | 0.20 | 0.20 | 0.20 | 0.20 | 0.20 |

No cell moved more than 0.30 on a 5-point scale across runs. The spreads on which the paper's claims rest range from 0.75 to 2.10. GPT-4o's directness and hedging spreads under situational profiles (0.17 and 0.10) are reported as absence of response, not as findings. Judge variability does not account for any spread the paper interprets.

GPT-4o at temperature 0, scoring Probe 5 output from both models, assigned the rubric midpoint to hedging on 15 of 16 conditions, the rubric ceiling to task engagement on 15 of 16, and the midpoint to directness on all 8 conditions of GPT-4o's own output. It discriminated on deference, group orientation, and self-doubt, and on directness for Claude output only. On a bounded rubric under greedy decoding, the model defaults to the midpoint or the ceiling when uncertain. Its rank agreements are reported only where it discriminated.

---

## 5. Discussion

### 5.1 What the substitution showed

Two of the three predictions in Section 2 hold on Claude. Situational profiles reproduce the politeness range. Directness, hedging, and permission-seeking spread across the eight profiles at 65 to 100 percent of the magnitude cultural labels produced, and deference spreads more under the lexical coder. Power distance and social distance move every politeness dimension in the direction Brown and Levinson predict.

And the range comes without the residue. Group reference under situational profiles is a fifth of what it was under cultural labels lexically, and the judge-coded self-doubt range is half. No situational profile produces a persona as self-doubting as the Collectivist label does or as disengaged. The Collectivist-lowest, Individualist-highest task engagement pattern that appears on both models under cultural labels does not appear under any situational profile on either model.

That is the dissociation the first audit predicted and could not test. The behavior the labels produced has two parts. One is politeness variation that a situation produces on its own. The other is a competence and engagement differential that only the label produces. Remove the label and the second part goes away.

### 5.2 Why the third prediction failed

The third prediction was that situational profiles would show more cross-model agreement than cultural labels, because the first audit had found none under cultural labels. Re-judged, cultural labels show more agreement than situational profiles on five of six dimensions.

The prediction was built on a null that the lexical instrument produced and the judge does not. The first audit reported that its regex markers, developed against Claude output, undercounted GPT-4o phrasing; it gave the example of competence hedging returning zero across 200 GPT-4o trials through pattern mismatch. A rank correlation across eight labels on an undercounted dimension is a correlation of noise with signal. The judge reads construct rather than surface, and on the same data it finds rho of 0.59 to 0.88 on deference and group orientation, confirmed by a second judge.

So the correction to the first audit is this: its finding that the two models do not share a construct under cultural labels was wrong. They share one. Both models render Collectivist (East Asian) as the least direct and least engaged of the eight, and Individualist (Western) as the most direct and among the most engaged. Claude also renders Collectivist as the most self-doubting; GPT-4o places South Asian there. GPT-4o saturates group orientation under African, Collectivist, and Indigenous; Claude places Collectivist highest at 4.40. The models differ on which non-Western label carries the most of each stereotype, and agree that the Individualist label carries the least. The stereotype is not a property of one model's training. It is in whatever both models learned from.

That makes the cultural-label problem worse than the first audit said, not better. A model-specific stereotype could be avoided by switching models. A shared one cannot.

### 5.3 A shared belief and a shared rule

Cultural labels transfer across models. So does one situational effect: deference. Both judges find rho of 0.57 to 0.71 on which situational profiles produce the most deferential persona, and on both models the answer is high power distance and large imposition.

Nothing else transfers under situational profiles. Group orientation rank-agrees at −0.02 and −0.17, though both models vary it. Hedging cannot be ranked meaningfully because GPT-4o barely varies it (4.00 to 4.10). Directness agrees at 0.52 under one judge.

The contrast is between what kind of thing agrees. Under cultural labels, the models agree on a mapping from group to behavior: this group defers, that group is direct, this group doubts itself. Under situational profiles, the models agree on a mapping from situation to one behavior: high power and high stakes produce deference. The first is a stereotype. The second is a politeness rule. That is the paper's title.

One reading of why the rule transfers on deference alone is that deference is the most direct behavioral expression of acknowledging power distance, and power distance is the situational variable both models respond to most consistently. The other dimensions are further downstream, and the two models evidently implement them differently. This is offered as a reading, not a finding.

### 5.4 GPT-4o

GPT-4o does not vary directness or hedging under situational profiles. Its directness range is 2.83 to 3.00 and its hedging range 4.00 to 4.10. Unconditioned, it is more direct and less hedging than under any situational profile. Any persona clause shifts it toward caution and holds it there.

This limits what the situational result shows about GPT-4o. On Claude, situational profiles produce theory-consistent variation across five dimensions. On GPT-4o they produce it on deference, and produce variation on task engagement and group orientation that the theory does not predict but that is consistent with caution under threat and collaboration under stakes. The claim that situational variables reproduce the politeness range without the stereotype is a Claude finding, replicated on GPT-4o for deference.

It also means GPT-4o's cultural-label behavior is not a shift from a neutral baseline. It is a shift from a baseline that the persona clause has already moved. The first audit's GPT-4o replication reported label effects against no baseline. The control shows that some of what looked like label effect is persona-clause effect.

### 5.5 The imposition reversal

On Claude, a larger imposition makes the persona more direct and less hedging, the opposite of what Brown and Levinson predict. It also makes the persona more deferential, which they do predict. Both judges see the directness reversal.

Two readings. The persona may be combining strategies the theory treats as alternatives: acknowledging the hearer's authority and stating the concern plainly, in the same message. That is a coherent thing for a person to do when the stakes are high and the theory's on-record and off-record strategies are not the only options. Or the descriptor may have failed as a manipulation. "Raising this concern carries significant weight and risk" can be read as a warning to soften or as a reason to be clear. The persona may have read it the second way.

The reversal is reported as unexplained. Either reading is testable with a reworded descriptor, and neither affects the deference finding.

### 5.6 Grounding

Adding a situational profile to a cultural label does not neutralize the label. Under the high-stakes profile the label is amplified: five of eight labels reach deference of 4.80 or above where the profile alone reaches 3.30, and the Collectivist persona reaches 5.00 on deference, 4.80 on hedging, and 4.00 on self-doubt. Under the low-stakes profile the label persists at reduced magnitude: the Collectivist persona defers at 3.70 where the profile alone produces 2.10.

The high-stakes result is the more informative. The situation told the model that the manager has authority, the relationship is formal, and the stakes are high. Given that, the model rendered the non-Western labels as maximally deferential and self-doubting and the Western label as more direct than the situation alone warranted. The label did not fill in unspecified variables; the variables were specified. It overrode them.

This closes the mitigation question the abstract raises. Contextualizing a cultural label with situational variables does not remove its effect. Removing the label does.

### 5.7 The second judge

GPT-4o at temperature 0, scoring Probe 5 output from both models, assigned the rubric midpoint to hedging on 15 of 16 conditions, the rubric ceiling to task engagement on 15 of 16, and the midpoint to directness on all 8 conditions of GPT-4o's own output. It discriminated on deference, group orientation, and self-doubt, and on directness for Claude output only.

This is not a property of the rubric. The Claude judge discriminated on every dimension. It is a property of greedy decoding on a bounded scale: with no sampling, an uncertain judge returns the same token every time, and on a 1 to 5 scale that token is 3 or 5. The second judge's rank agreements are reported only where it discriminated, and its failure to discriminate elsewhere is reported as a limitation of that judge, not as evidence about the personas.

The methods point is that two LLM judges applied to the same rubric can differ this much, and the difference is invisible until you run both. The first audit's lexical-to-judge divergence and this paper's judge-to-judge divergence are the same lesson: an instrument's behavior on one model or one configuration does not describe its behavior on another.

### 5.8 What this means in practice

A product team uses synthetic personas to test a feature before real user research. The schema has a `cultural_background` field. They set it to "Collectivist (East Asian)" for one persona and "Individualist (Western)" for another, give both the same task, and read the responses.

On the evidence here, the first persona will hedge more, defer more, engage less with the task, and express more doubt about its own competence than the second, and it will do so on either major model. Nothing about the task, the situation, or the product produced that difference. The label produced it. If the team reads the first persona's response as "East Asian users are hesitant about this feature," they have learned nothing about East Asian users. They have learned what the model associates with the phrase.

That inference then shapes the product. A feature gets simplified for a population that was never consulted. Onboarding gets longer for users the model imagined as needing more reassurance. A pricing page gets softer language for a market the model rendered as deferential. None of it is grounded. All of it looks grounded, because the persona said so.

The grounding conditions show the obvious repair does not work. A team that keeps the label and adds "this is a low-stakes conversation with a peer they know well" still gets a persona that defers at 3.70 where the situation alone gives 2.10. The label is not diluted by context. At high stakes it is concentrated by it.

The repair that works is to stop asking the model what a cultural group is like and start telling it what the situation is like. A team that needs a persona who is cautious and deferential specifies high power distance and high stakes, and gets that behavior without the model deciding which ethnicity it belongs to. A team that needs a range of communication styles specifies a range of situations. The eight profiles in this paper are a starting set.

---

## 6. Limitations

One task. Every condition uses the same scenario, a persona disagreeing with a manager. Power distance is built into the task before the situational variables specify it. Whether situational profiles produce the same range on a peer task or a customer task is untested.

Two models. The first audit's Gemini replication was abandoned on quota. This paper did not attempt a third model. Claims about what transfers across models rest on one pair.

The primary judge is one of the two models under comparison. Claude scored both Claude and GPT-4o output. A second judge was run to check this and confirmed the pattern on the two dimensions it could discriminate. On directness, hedging, self-doubt, and task engagement the cross-model agreement under cultural labels rests on the Claude judge alone.

Judge samples are small. Ten trials per condition, eighty per file. Three runs reduced variance to at most 0.30 on any cell, but the underlying sample is the same ten trials scored three times, not thirty trials.

The second judge collapsed. GPT-4o at temperature 0 did not discriminate on three of six dimensions. A different temperature or a third judge model might. Neither was tested.

The imposition descriptor may not operationalize the construct. The reversal on directness and hedging is consistent with the persona reading "significant weight and risk" as a reason to be clear rather than a reason to soften. A reworded descriptor was not tested.

GPT-4o shifts under any persona clause. Its situational and cultural results are measured against a baseline the persona clause has already moved. The first audit's GPT-4o numbers, reported without a control, are subject to the same reading.

Descriptors are one phrasing each. "Near-equals" and "considerable authority" are one way to say low and high power distance. Others might produce different magnitudes.

Rank comparison is underpowered. Eight conditions cannot distinguish weak agreement from none, as the first audit noted. This paper reports rho above 0.5 as agreement and below as none, and does not test significance.

No inferential statistics. Descriptive rates and rank correlations only.

Lexical coding was not re-validated for this paper's conditions. The situational descriptors do not contain any marker regex, but the lexical coder's known undercount on GPT-4o applies to Probe 5 as it did to Probe 1.

---

## 7. Recommendations

### 7.1 For any system conditioning personas on identity

Remove cultural background labels from persona schemas. This paper's grounding conditions show that the label persists through situational context at both ends of the stakes range and is amplified at the high end. There is no tested configuration in which a cultural label is present and its stereotype effect is absent.

Specify Brown and Levinson's variables directly. Power distance, social distance, and imposition size, each at whatever granularity the use case needs, reproduce the politeness variation a cultural label produced on Claude without the competence differential. On GPT-4o they reproduce it on deference. Where a persona system needs a user who defers, hedges, or speaks plainly, it can specify the situation that produces that behavior rather than a group the model associates with it.

Concretely, a schema entry like

```
cultural_background: "Collectivist (East Asian)"
```

becomes

```
power_distance:   high
social_distance:  distant
imposition_size:  large
```

if the intended persona is one who defers and hedges, or the opposite levels if the intended persona is direct. The rendered clause is "your manager holds considerable authority over you, you and your manager have a formal, arm's-length relationship, and raising this concern carries significant weight and risk" in place of "with a Collectivist (East Asian) cultural frame." The first produces deference of 3.30 on Claude. The second produces 4.30, plus self-doubt of 3.30 and task engagement of 3.20 that the first does not produce. If the use case needs the deference, the situational version delivers it. If the use case was relying on the self-doubt and disengagement, it was relying on a stereotype.

Run a no-persona control. Both cultural and situational effects should be read against what the model does unconditioned. On GPT-4o, any persona clause shifts the baseline; without a control that shift is misattributed to the conditioning.

Probe counterfactually before trusting a persona field. Change one field, hold the rest, measure what moves. This paper's design is the template: eight conditions, twenty-five trials, two coders. It is cheap and it finds the problem.

### 7.2 For cross-model comparison

Do not use a lexical instrument built on one model to compare it with another. The first audit's null on cross-model agreement was produced by exactly this. Validate marker definitions on every model separately, or use a coder that reads construct rather than surface.

Use two independent judges and report agreement between them. This paper's second judge confirmed the primary judge's finding on two dimensions and could not test the others. A finding that rests on one LLM judge, especially one that is also a model under comparison, is a finding about that judge.

Run judges more than once and report range. Three runs here moved no cell more than 0.30. That number is what makes the spreads interpretable.

Treat rank agreement, not magnitude, as the test of construct transfer. Two models can produce comparable spread on a dimension while ranking the conditions in different orders. The first audit's GPT-4o replication found comparable spread and reported no agreement. Comparable spread was true. No agreement was an instrument artifact.

### 7.3 For MatrAIx

The first audit's schema-level recommendations stand: extend the validation suite to identity attributes, separate cultural affiliation from cultural orientation as a representational matter, and resolve the inert undocumented edges.

To those, add: replace the `cultural_background` dimension with situational fields drawn from politeness theory, or remove it. The dependency graph shows the dimension carries no schema-level effect. The behavioral evidence shows it carries a stereotype at render time that survives contextualization. A dimension that does nothing in the schema and something harmful in the prompt has no reason to remain.

---

## 8. Conclusion

A cultural label in a persona prompt produces two things. One is a range of politeness behavior that a situation produces on its own. The other is a differential in competence and engagement that only the label produces, that both models produce in the same direction, and that survives the addition of situational context at any level of stakes. Replacing the label with the situation keeps the first and removes the second, on Claude fully and on GPT-4o for deference.

The first audit found that cultural labels produce behavior the schema does not cause. This paper finds that they produce behavior the situation does not cause either, that the two models tested agree on what that behavior is, and that specifying the situation instead removes it. The label was never carrying information about politeness. It was carrying a belief about groups. The models share the belief. The persona system does not need it.

The stereotype transfers on five dimensions. The rule transfers on one.

---

## References

Brown, P., & Levinson, S. C. (1987). *Politeness: Some universals in language usage.* Cambridge University Press.

Chang, J., Li, X., Hao, Y., Huang, J., Wen, Q., Huang, S., Liu, Y., Liu, X., Fan, Y., & Wang, Y. (2026). MatrAIx: Simulating the world with 8.3 billion persona agents. arXiv:2608.04205.

Williams, B. D. (2026). Clean schemas, stereotyped personas: Locating cultural bias in persona-conditioned language models. Zenodo. https://doi.org/10.5281/zenodo.21970217

---

## Reproducibility

All probes, analysis scripts, raw trial outputs, and judge outputs are in the companion repository. New for this paper:

```
probes/probe5_situational.py          # 8 situational profiles, Claude
crossmodel_probe5.py                  # same on GPT-4o
control_noPersona.py                  # no-persona baseline, both models
probes/probe6_grounding.py            # label + high-stakes profile
probes/probe6b_grounding_lowstakes.py # label + low-stakes profile
analyze_judge_gpt.py                  # second judge, GPT-4o, temperature 0
judge_stability.py                    # N judge runs, averaged
analyze_rank_effects.py               # Spearman rho and main effects
```

Judge outputs used in this paper:

```
results/probe1_claude_judge_avg_run1.json   # Probe 1, Claude, Claude judge
results/probe1_gpt4o_judge_avg.json         # Probe 1, GPT-4o, Claude judge, 3-run avg
results/probe5_claude_judge_avg.json        # Probe 5, Claude, Claude judge, 3-run avg
results/probe5_gpt4o_judge_avg.json         # Probe 5, GPT-4o, Claude judge, 3-run avg
results/probe1_claude_gptjudge.json         # Probe 1, Claude, GPT-4o judge
results/probe1_gpt4o_gptjudge.json          # Probe 1, GPT-4o, GPT-4o judge
results/probe5_claude_gptjudge.json         # Probe 5, Claude, GPT-4o judge
results/probe5_gpt4o_gptjudge.json          # Probe 5, GPT-4o, GPT-4o judge
results/rank_effects_analysis.json          # rho and main effects, Claude judge
results/control/                            # no-persona baselines
results/probe6_grounding/judge_analysis.json
results/probe6b_grounding_lowstakes/judge_analysis.json
```

## Citation

```bibtex
@misc{williams2026situational,
  title     = {Situational Variables Versus Cultural Labels in Persona Conditioning:
               Shared Stereotype, Shared Rule},
  author    = {Williams, Bianca Den{\'e}},
  year      = {2026},
  publisher = {Zenodo},
  note      = {https://github.com/biancadene/persona-cultural-validity}
}
```
