# Ultimatum Game Task — Scientific Rationale
### Mind After Midnight Study | Sleep and Health Research Program
### Department of Psychiatry, University of Arizona

---

## Overview

This document describes the scientific rationale, theoretical background, and
clinical significance of the Ultimatum Game Task (UGT) as implemented for the
Mind After Midnight (MaM) study. For installation and technical documentation,
see README.md.

---

## The Mind After Midnight Study

The Mind After Midnight study is a clinical research investigation examining how
nocturnal wakefulness — being awake between approximately 1am and 4am — affects
cognitive control, emotional processing, and suicide risk. The study administered
a comprehensive neuropsychological battery at multiple timepoints across the
circadian cycle (morning at 9am, evening at 9pm, and overnight at 3am) to
characterize how cognitive and affective task performance fluctuates with time
of day in individuals with varying histories of suicidal ideation.

The UGT was administered as part of the behavioral decision-making component of
the battery, alongside the Balloon Analogue Risk Task (BART), prior to the
psychophysiological EEG tasks.

---

## What the UGT Measures

The Ultimatum Game is a well-validated economic decision-making paradigm drawn
from behavioral economics and neuroeconomics. It measures responses to fair and
unfair monetary offers in a simulated social exchange.

### Basic Structure

A **proposer** offers to split a fixed sum (in this implementation, $10) between
themselves and the participant. The participant must either:

- **Accept** → Both parties receive the proposed amounts
- **Reject** → Neither party receives anything

From the perspective of classical economic theory, any positive offer should be
accepted — receiving $1 is strictly better than receiving nothing. However,
participants routinely and predictably reject unfair offers, even at personal
financial cost. This irrational rejection of positive offers reflects the
influence of social-affective processes — specifically emotional responses to
perceived inequity, social norm enforcement, and irritability — on economic
decision-making.

### The Koenigs and Tranel Paradigm

This implementation follows the specific variant described by Koenigs and Tranel
(2007), who demonstrated that patients with ventromedial prefrontal cortex (vmPFC)
damage accepted unfair offers at higher rates than neurologically intact controls.
This finding revealed that the vmPFC plays a critical role in generating the
negative affect that motivates rejection of unfair offers — and that disrupting
this affective signal paradoxically produces more "rational" economic behavior.

The Koenigs and Tranel paradigm presents offers through a simulated social
interaction with a named partner whose identity is revealed after practice trials,
increasing ecological validity and social engagement.

---

## Primary Dependent Variable

The primary dependent variable is the **proportion of unfair offers accepted**.

Higher acceptance rates indicate reduced sensitivity to social inequity, potentially
reflecting blunted affective responding or impaired integration of social-emotional
signals into decision-making.

Lower acceptance rates indicate heightened sensitivity to unfairness, potentially
reflecting elevated irritability, social threat sensitivity, or emotional reactivity.

---

## Relevance to Nocturnal Suicidality

The UGT was selected for the MaM battery because it provides a behavioral window
into two psychological processes known to correlate positively with suicidal thinking:

### Perceived Social Rejection

The social framing of the Ultimatum Game — receiving offers from a named human
partner who proposes to keep the majority of a shared resource — directly activates
processes related to perceived social rejection and burdensomeness. These constructs
are central to the Interpersonal Theory of Psychological Suicide (IPTS), which
identifies perceived burdensomeness and thwarted belongingness as key proximal risk
factors for suicidal ideation.

By modeling decision-making in the presence of induced social rejection, the UGT
provides an ecologically valid behavioral probe of how suicidally vulnerable
individuals respond to interpersonal threat under varying circadian conditions.

### Irritability

Irritability is a well-documented risk factor for suicidal behavior, independently
associated with impulsive aggression and emotional dysregulation. The UGT reliably
induces irritability through repeated exposure to unfair offers — and the proportion
of rejections provides a behavioral index of how irritability translates into action.

Nocturnal wakefulness is known to amplify irritability and emotional reactivity.
The MaM study tested whether this nocturnal amplification of irritability is
behaviorally detectable in UGT performance at 3am relative to morning and evening.

---

## Why No Prior Time-of-Day Data Existed

At the time of the MaM study design, no full time-of-day characterization of UGT
performance existed in the literature, though studies had conducted repeat
assessments across morning, afternoon, and evening hours. The overnight window
(3am) had not been systematically examined. The MaM study was positioned to provide
the first overnight characterization of UGT performance — a gap in the literature
with direct relevance to understanding nocturnal suicidality.

---

## Task Design

- **5 fixed counterbalanced decks** — Each deck contains 22 trials with a fixed
  sequence of fair and unfair offers, counterbalanced across deck versions
- **Named partner with avatar** — Social realism is enhanced by displaying the
  partner's name and photo after practice trials, with a realistic "joining session"
  loading screen
- **Practice trials** — Configurable number of practice trials before the main task
- **Jittered inter-trial interval** — Randomized ITI prevents temporal prediction
- **Timeout handling** — If no response is given within the decision window, the
  partner receives the full stake, adding behavioral consequence to non-response
- **Total time on task** — Approximately 8–10 minutes

---

## Relationship to Other Battery Components

The UGT was positioned in the MaM battery alongside the BART (Balloon Analogue
Risk Task) to provide complementary decision-making measures:

**BART** — Measures risky decision-making under conditions of potential reward
versus loss, with no social component. Primary index: adjusted average pumps on
unexploded balloons.

**UGT** — Measures decision-making under conditions of social rejection and induced
irritability. Primary index: proportion of unfair offers accepted.

Together these tasks characterize two distinct but related dimensions of decision-
making vulnerability: pure risk tolerance (BART) and socially-modulated emotional
decision-making (UGT). Both have been independently associated with suicidal
thoughts and behaviors in prior research.

---

## Relationship to the Interpersonal Theory of Psychological Suicide (IPTS)

The IPTS (Joiner, 2005; Van Orden et al., 2010) proposes that suicidal desire
emerges from the co-occurrence of two interpersonal states:

1. **Thwarted belongingness** — The painful perception that one is alienated and
   does not belong
2. **Perceived burdensomeness** — The belief that one is a burden to others and
   that one's death would be a relief

The UGT's social rejection framing directly engages both constructs — unfair offers
activate feelings of social exclusion and devaluation that parallel the subjective
experience of thwarted belongingness and perceived burdensomeness. This makes the
UGT unusually well-suited as a behavioral probe of IPTS-relevant processes.

---

## Key References

Koenigs, M., & Tranel, D. (2007). Irrational economic decision-making after
ventromedial prefrontal damage: evidence from the Ultimatum Game. *Journal of
Neuroscience*, 27(4), 951–956.

Güth, W., Schmittberger, R., & Schwarze, B. (1982). An experimental analysis of
ultimatum bargaining. *Journal of Economic Behavior & Organization*, 3(4), 367–388.

Sanfey, A. G., Rilling, J. K., Aronson, J. A., Nystrom, L. E., & Cohen, J. D.
(2003). The neural basis of economic decision-making in the Ultimatum Game.
*Science*, 300(5626), 1755–1758.

Joiner, T. E. (2005). *Why people die by suicide*. Harvard University Press.

Van Orden, K. A., Witte, T. K., Cukrowicz, K. C., Braithwaite, S. R., Selby,
E. A., & Joiner, T. E. (2010). The interpersonal theory of suicide. *Psychological
Review*, 117(2), 575–600.

Bernstein, E. E., Curtiss, J. E., Wu, G. W., Barreira, P. J., & McNally, R. J.
(2019). Impaired cognitive control and suicidality. *Depression and Anxiety*,
36(5), 441–450.

Littlefield, A. K., Stevens, A. K., Cunningham, S., Jones, R. E., King, K. M.,
Schumacher, J. A., & Coffey, S. F. (2015). Stability and change in impulsivity
following treatment for alcohol use disorders: Contribution of UPPS-P facets.
*Addictive Behaviors*, 42, 199–202.

---

## Citation

If you use or adapt this task in your research, please cite the Mind After Midnight
study and this repository:

Sangpo, S. (2025). *Ultimatum Game Task — Mind After Midnight Study* [Software].
Sleep and Health Research Program, Department of Psychiatry, University of Arizona.
https://github.com/SurZen/ultimatum-game-task
