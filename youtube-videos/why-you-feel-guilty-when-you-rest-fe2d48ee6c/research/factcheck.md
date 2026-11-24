# Independent factual review

Reviewed on 2026-11-24 by a separate reviewer who did not write the script or research brief. The reviewer read the finished narration and the available source text, not just the claim register. No script or claim-register edits were made during this review.

**Status: ready for creator CONTENT REVIEW within the evidence limits below. This is not recording approval, a full-paper review, or scientific verification of every proposed explanation.**

Reviewed script: `script/script-en.txt`, 603 whitespace-delimited words, 15 paragraphs. Paragraph numbers below count nonempty blocks separated by blank lines. The final framing revision adds only “Imagine this.” to the previously reviewed version; the reviewer verified that removing that exact prefix reproduces the prior script's SHA-256.

SHA-256: `04bf801bef41dbefe28e0859e1ad64cb7c8d6ca288e925f9c885c8a4b508411d`

## Evidence actually read

- **S1:** Jeff Grabmeier, Ohio State News, 23 August 2021, *Think leisure is a waste? That may not bode well for your mental health*. Complete relevant article body read in `sources/leisure-institution.txt`, lines 30–58. This is an institutional research communication, not the journal paper. The association in narration paragraph 6 is reported at lines 38–46. The linked journal paper was not retrieved/read.
- **S2:** Crocker and Wolfe, *Contingencies of self-worth*, PMID 11488379. Complete available PubMed record and abstract read in `sources/self-worth-pubmed-xml.txt`, lines 1–12; the whole abstract is on line 8. This is abstract-level access to a theoretical review/model, not full-paper access.
- **S3:** Masicampo and Baumeister, *Consider it done! Plan making can eliminate the cognitive effects of unfulfilled goals*, PMID 21688924. Complete available PubMed record and abstract read in `sources/planning-pubmed-xml.txt`, lines 1–11; the whole abstract is on line 9. This is abstract-level access to experimental research, not full-paper access.

The reviewer also read the retrieval log collection: `access-attempts.json` preserves initial failures; `access-after-config.json` records the later successful institutional-page retrieval; `primary-access.json` records successful NCBI XML retrievals and a blocked DOI request; `journal-access.json` records the still-blocked journal page. The acquisition-time “retrieved-not-yet-read” statuses in those logs are historical; the reading scope above records what was subsequently inspected.

Initial proxy failures do not invalidate the subsequently available local text. Conversely, the existence of a DOI, a paper title, or a university summary is not evidence that a full paper was read. Methods, full results, statistical estimates, and study limitations beyond the available article/abstracts were not independently inspected. This review does not establish a literature consensus or clinical efficacy.

## Paragraph and claim review

`SUPPORTED` means the cited text supports the exact, limited assertion in narration. `UNVERIFIED` means the specific explanation is not established by the inspected sources. `FICTIONAL`, `EDITORIAL`, and `NORMATIVE` identify material that is not being presented here as a scientific finding; those labels are not evidence verdicts of efficacy.

| Para | Claim or content | Verdict | Evidence and limits |
| --- | --- | --- | --- |
| 1 | The protagonist hears someone, feels caught resting, and reaches for a plate. | FICTIONAL | The explicit “Imagine this.” cue establishes an invented second-person opening, not an observed participant or an estimate of how often people react this way. Three minutes is a story choice. |
| 2 | The person says hello; the protagonist volunteers an excuse; the plate was clean. | FICTIONAL | Original scene and dialogue, with no attribution to a real person, study, or quotation. |
| 3 | A planned twenty-minute break is postponed by a cup, trash, and drawer. | FICTIONAL | Illustrative sequence; twenty minutes is not a scientifically established dose of rest. |
| 4 | Finishing a chore briefly makes the protagonist's “I should be doing something” thought less pressing. | FICTIONAL | Acceptable as the invented character's inner response. None of S1–S3 establishes this precise chores-to-relief mechanism for viewers. The assertive “you care” wording needs to remain within the story's frame. |
| 5 | Waiting for every household task to be finished can make the stopping rule difficult to satisfy. | EDITORIAL | A conditional practical observation and kitchen joke, not a measured claim about retirement or universal household behavior. |
| 6, first sentence; C1 | “Research has linked seeing leisure as wasted time with enjoying it less.” | SUPPORTED | S1, `sources/leisure-institution.txt`, lines 38–40: “the more the participants believed leisure to be wasteful, the less they enjoyed leisure activities.” Lines 43–46 also describe an association for leisure pursued for fun. “Linked” preserves association and does not assert a cause of guilt. Support is at institutional-summary level. |
| 6, remaining sentences; C2 | Usefulness may become a condition for feeling okay; an unfinished chore may then feel like evidence of not doing enough. | UNVERIFIED as this specific explanation; qualified fictional application | S2, `sources/self-worth-pubmed-xml.txt`, line 8, describes self-esteem responding to “successes and failures in domains on which one has staked self-worth.” This supports the general theoretical idea, not a chores/rest-guilt mechanism or the audience's actual motive. “Maybe” and “That doesn't explain every case of guilt” keep the application tentative. Do not turn this into a finding that S2 demonstrated. |
| 7 | A fictional friend feels bad about an idle afternoon; the protagonist readily permits the friend a break. | FICTIONAL | Invented message and response, not evidence of a measured self/other difference. |
| 8 | The character applies different standards to their own rest and the friend's rest. | EDITORIAL | A comparison within the invented scenes, followed by a reflective question. It does not establish that everyone judges others more kindly, or that changing this standard treats guilt. |
| 9 | Caregiving, deadlines, demanding work, and unequal housework can require practical action or help. | NORMATIVE / contextual | Acknowledges real responsibilities and alternatives to internal reframing. “May call for” is cautious; no prevalence or treatment-effect claim is made. |
| 10 | Check what would actually go wrong during a short break and respond to an immediate need. | NORMATIVE | A proposed decision prompt, not a tested diagnostic instrument or a promise that twenty minutes is suitable for every situation. |
| 11; C3 | Write a task reminder and a specific return time. | NORMATIVE recommendation | S3, `sources/planning-pubmed-xml.txt`, line 9, reports specific plans eliminating measured “activation and interference effects” in its experiments. The same abstract says changes in goal-related emotions did not appear necessary for those cognitive effects. It does not establish that a written reminder relieves guilt or anxiety. The narration makes no such promise, so the suggestion is acceptable as an experiment, not a verified intervention. |
| 12 | Choose an enjoyable activity without requiring it to become productive. | NORMATIVE | A value choice, not a research-backed efficacy claim. S1 lines 54–57 report a different suggestion—framing leisure as useful—for some people holding wastefulness beliefs. The narration does not claim its own advice was tested or that the alternative never helps. |
| 13 | A guilty thought may remain; check urgency and try staying seated without requiring perfect performance. | NORMATIVE | A cautious invitation. It does not promise guilt will disappear. This is not evidence for exposure therapy, a clinical protocol, or a required duration of discomfort. “A slightly uncomfortable break still counts” is a value statement. |
| 14 | The protagonist tenses at the keys but leaves the plate and says they took a break. | FICTIONAL | Invented bodily reaction, action, and dialogue. No nervous-system explanation, diagnosed condition, or demonstrated intervention result is asserted. |
| 15 | The drawer remains unfinished while the character permits twenty minutes of rest. | FICTIONAL | A chosen story resolution, not a guarantee of a viewer's response or an experimentally established break duration. |

## Corrections, framing, and omissions

No factual wording correction is required for C1 in the reviewed version. Retain **“linked”**, the limitation about guilt, **“maybe”**, and the experiment framing. S1 establishes the reported leisure/enjoyment association; it does not directly explain guilt. S2 supplies a general model; it does not verify the usefulness/laundry explanation. S3 supplies limited cognitive-task background; it does not verify emotional or therapeutic benefits of the suggestion.

The final narration now starts paragraph 1 with **“Imagine this.”**, resolving the earlier framing recommendation. The fictional scenes in paragraphs 1–4 and 7–8 therefore have an explicit spoken cue rather than relying only on the private research brief. Paragraph 4's description of motives is reviewed as the fictional character's inner response, not a diagnosis of every listener. No further wording correction is required for the current content-review scope. The reviewer has not edited the narration. Any later script change must receive a new hash and an appropriate update to this review.

There are no unsupported statistics, named diagnoses, childhood-cause claims, quotations attributed to researchers, neurotransmitter explanations, or promises of a cure in the narration. A clinical warning is not needed merely because everyday guilt is discussed. The brief correctly identifies the absence of full-paper access; neither metadata nor the report should call this a comprehensive scientific explanation of rest guilt.

The title's broad “why” must be read alongside the script's limitation that this does not explain every case. Do not strengthen the title/description into a universal cause or imply that the practical suggestions were proven to eliminate guilt. The available sources do not justify those additions.

## Verdict counts and readiness

For the 16 rows above: **SUPPORTED 1; UNVERIFIED 1; FICTIONAL 7; EDITORIAL 2; NORMATIVE 5.** C3 also has an explicitly unverified efficacy boundary; the recommendation itself is not an empirical efficacy claim. Under the upstream comparison categories: **CONTRADICTED 0; OVERSTATED 0; FLAGGED 0; NOT IN SOURCE 0 as an unmarked research finding.** Fictional events and the qualified C2 application are not counted as supported research results.

The draft is ready for the creator's **CONTENT REVIEW**, with C2 retained as a possible interpretation and C3 retained as a suggestion. No contradiction was identified in the available material. This is a separate, independent review against an institutional article and abstracts, with the access limitations stated above. Recording and full animation remain subject to the creator's script approval and an authorized media request. This report grants neither.
