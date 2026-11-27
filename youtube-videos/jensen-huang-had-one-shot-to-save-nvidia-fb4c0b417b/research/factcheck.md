# Independent script fact check

Reviewed `script/script-en.txt` independently of its author under `.agents/skills/yt-research/SKILL.md`. Paragraph numbers below count the ten blank-line-separated narration paragraphs (script lines 1, 3, …, 19). The script was not edited. This report was subsequently updated after directly rereading the revised final script; the correction history below preserves the initial finding.

Source: `research/sources/acquired-huang-2023.txt`, Acquired, “NVIDIA CEO Jensen Huang,” October 16, 2023 (episode metadata at lines 469–473). Read the complete relevant exchanges at lines 19–59 and 224–241, their surrounding context at 210–250, and additional AI context at 60–92. There are no footnotes in those exchanges. All evidence line numbers refer to that saved transcript.

**Evidence limit:** SUPPORTED means the interview supports the claim or the script explicitly frames a counterfactual as unknown. It does not mean an independent historical or technical record corroborates the recollection. The financial runway, ICOS closure, prototype/production sequence and blend-mode count remain interview testimony. The host supplies the initial prototype and blend-mode framing; Huang supplies the emulation and direct-production recollection and acknowledges the blend omission.

| Para | Claim | Verdict | Evidence (line numbers, short quote) |
|---|---|---|---|
| 1 | The episode predates NVIDIA’s AI boom. | SUPPORTED | L19, 28 place the crisis in 1997; L63–64, 80 and 86 describe the later deep-learning period. |
| 1 | Waiting for a physical prototype “felt safer”; the usual testing cycle would have taken too long, in Huang’s account. | SUPPORTED | L37–42 describes the normal sequence and why it would exhaust the company’s resources. “Felt safer” is the narrator’s rhetorical assessment of conventional caution, not a quotation or documented report of Huang’s private feelings; he himself calls the alternative “crazy” at L50–52. L20 supplies the no-physical-prototype premise. |
| 1 | The company could not afford a failed design followed by another chip revision. | SUPPORTED | Huang, L37: the software/bug-fixing/second-tape-out sequence means “We would’ve been out of business already”; L41–42: “tape out just one time” / “if it’s not, we’ll be out of business.” This is his retrospective financial/timing assessment. |
| 1 | “You have six months to save NVIDIA”; one more test might endanger survival. | SUPPORTED | L19: “about six months of cash left”; L41: “if we only had six months.” The second-person opening is dramatization, and “What if” makes the extra-test consequence a question, not a proved counterfactual. L37–42 supports the underlying iteration constraint; the script does not claim all additional tests were harmful. |
| 2 | The crisis occurred in 1997. | SUPPORTED | Huang, L28: “That time—1997”; host, L19: “I believe it was 1997.” |
| 2 | The earlier graphics architecture was incompatible with Microsoft’s DirectX. | SUPPORTED | Huang, L24: NV1/NV2 used a different approach; L26: DirectX “was fundamentally incompatible with Nvidia’s architecture.” This is Huang’s characterization. |
| 2 | Huang called RIVA 128 a company reset. | SUPPORTED | L24 and L26: “RIVA 128 was … a reset of our company.” |
| 2 | The team had to change direction while running out of time. | SUPPORTED | L28: “running out of time … running out of money”; L29: “We’re not going to fight [DirectX].” |
| 3 | The normal sequence was fabrication, software development, finding/fixing bugs, then another tape-out. | SUPPORTED | Huang, L37 and L41: “build a chip, write the software, fix the bugs, tape out a new chip.” “Picture” marks the sequence as an explanation rather than a claim that NVIDIA completed those steps. |
| 3 | Huang said NVIDIA could not survive that sequence. | SUPPORTED | L37: “We would’ve been out of business already”; L41: “that method wasn’t going to work.” |
| 3 | Roughly six months were available. | SUPPORTED | Host, L19: “about six months of cash left”; Huang, L41: “if we only had six months.” This is recollection, not a verified cash ledger. |
| 3 | There was no time or money to redesign the chip and send it to the factory again. | SUPPORTED | L37: software development reveals bugs, then “we taped out the chip again” and “would’ve been out of business already”; L41: “tape out just one time.” Revised wording identifies a redesign cycle rather than limiting all physical production to one run. |
| 3 | The normal way of reducing technical risk created a survival risk. | SUPPORTED | Interpretation of L37–42: ordinary iterative development would exhaust the company’s resources. It does not assert a separately proven bankruptcy outcome. |
| 4 | Insisting on another physical test might reveal a problem or be rescued by more funding. | SUPPORTED | Explicit counterfactual: “imagine,” “Perhaps,” and “We cannot know.” L37–42 supplies the underlying time/resource constraint; the source does not establish either imagined outcome. These are possibilities, not reported events. |
| 4 | In Huang’s account the normal cycle meant going out of business. | SUPPORTED | L37, 39, 41. Attribution and conditional framing preserve the distinction between his assessment and an independently proven alternate history. |
| 5 | The answer began inside another failing company. | SUPPORTED | L36: ICOS was “shutting the company down because they had no customers”; L43: NVIDIA virtually prototyped the chip “by buying this emulator.” “Began” identifies this narrated solution, not a verified claim that every architectural decision originated at ICOS. |
| 5 | NVIDIA needed an emulator to exercise the design before receiving fabricated hardware. | SUPPORTED | L36: “technology called emulation”; L37 explains the need; L43: “virtually prototyped the chip.” “Imitate” is an adequate plain-language description here. |
| 5 | Huang contacted ICOS. | SUPPORTED | L36: “There was a company called ICOS. On the day that I called them…” |
| 5 | According to Huang, ICOS was shutting down that day because it had no customers. | SUPPORTED | L36: “they were just shutting the company down because they had no customers.” The script expressly attributes this recollection. |
| 5 | ICOS had inventory NVIDIA could buy. | SUPPORTED | L36: “I’ll buy what you have inventory.” The closing image of equipment inside a company “giving up” is figurative language, not evidence of a documented warehouse scene. |
| 6 | Huang/NVIDIA bought the emulator equipment. | SUPPORTED | L36: offer to buy inventory; L43: “by buying this emulator.” |
| 6 | The software team worked against a virtual version of the design. | SUPPORTED | L43: “Dwight and the software team … ran it on this emulator.” The emulator is real equipment; “virtual version” refers to the pre-silicon chip model, not a claim that the emulator was merely software. |
| 6 | Drivers, games and applications were tested before tape-out. | SUPPORTED | L56: “emulated the whole chip before we taped it out … QA on all the drivers … all the games we had … every VGA application we had.” |
| 6 | Emulation was very slow; Huang recalled waiting in the lab for Windows to draw. | SUPPORTED | L43: “sat in the lab waiting for Windows to paint”; L44–45 give conflicting approximate frame times, which the script wisely does not convert into an exact statistic. |
| 6 | The team moved testing earlier instead of simply omitting it. | SUPPORTED | L45: “Everything that we could have tested, we tested in advance”; L56 describes pre-tape-out software QA. |
| 7 | They taped out the design and went directly to production. | SUPPORTED | L54: “we taped that out and went directly to production”; L45–48 explains committing in advance. This describes the decision path, not proof that fabricated units bypassed all later screening or quality control. |
| 7 | This commitment preceded a finished, physically proven product. | SUPPORTED | Host L20: no physical prototype; Huang L43, 45–46, 54: virtual prototype, then tape-out/production. Do not expand this into a claim that there were no physical chips at any point. |
| 7 | Confidence came from emulation. | SUPPORTED | L56: “The reason … is because we emulated the whole chip before we taped it out.” |
| 7 | Huang recalled treating the design as perfect because there was no room for a second try. | SUPPORTED | L42: “if it’s not, we’ll be out of business … We get one shot”; L45: “I assumed that the chip was perfect.” The script correctly describes an assumption rather than proven perfection. |
| 8 | The product was not perfect. | SUPPORTED | L23: “We should have implemented all 32. But we built what we built.” |
| 8 | The hosts said it supported eight of 32 DirectX blend modes. | SUPPORTED | Host L20: “of the 32 DirectX blend modes, it supports 8 of them.” This verifies what the interview says; it does not independently verify the hardware/API capability count. |
| 8 | Huang acknowledged they should have implemented all 32 modes. | SUPPORTED | L23: “We should have implemented all 32.” |
| 8 | The eight-of-32 count does not mean three quarters of the entire chip was broken; it concerns one graphics-function category. | SUPPORTED | L20 explicitly limits the denominator to “DirectX blend modes.” The arithmetic cannot be generalized to chip functionality. This is a justified scope clarification, not an additional capability claim. |
| 8 | They had to sell and support the product they had. | SUPPORTED | Host L20: “convince the market to buy it” and developers to use those modes; Huang L23: “we had to make the best of it.” |
| 9 | NVIDIA survived the episode. | SUPPORTED | L53: “it worked”; L231–234: retrospective discussion of how the company continued designing chips. The interview with its current CEO also directly establishes subsequent existence. |
| 9 | The team changed architecture, brought software testing forward, and used emulation. | SUPPORTED | L24–29: architectural reset; L43, 45, 56: pre-tape-out emulation and software testing. |
| 9 | Huang rejected “just copy the gamble” as the lesson for founders. | SUPPORTED | L55–57: asked to “bet the company,” he replies “No, no,” and explains advance work. L226–229 cautions that smart actions can still fail. “Simply” appropriately limits the script’s paraphrase. |
| 9 | He described bringing future risks into the present for examination. | SUPPORTED | L57: “all the risky things … pull in in advance … everything in the future that we can simulate today, we prefetch it.” |
| 10 | A replacement company and an AI stoppage are unknown counterfactual outcomes. | SUPPORTED | The script says “Possibly” and “This story cannot establish that”; L228–229 itself stresses uncertain success. No claim that NVIDIA was indispensable to all AI is made. |
| 10 | NVIDIA later helped machine-learning work. | SUPPORTED | L64–71: AlexNet and CUDA/computer vision; L86–88: work with AI researchers and systems/software to advance their research. This is later history, not a claim that RIVA 128 was an AI accelerator. |
| 10 | The team first recognized its earlier architecture was wrong and changed direction. | SUPPORTED | L24: “completely the wrong answer”; L26–29: reset and commitment to DirectX. The statement that this was the “harder decision” is editorial interpretation, not measured or quoted testimony. |

## Revision history and final recheck

Initial check: **38 SUPPORTED, 1 OVERSTATED**, no other verdicts, across 39 rows. Paragraph 3’s original “only one manufacturing attempt they could afford” overstated the source’s one-design-iteration constraint.

Final-script recheck: the author replaced it with “no time or money to redesign the chip and send it to the factory again.” This now matches lines 37–42 and resolves the sole finding. Paragraph 1 now says “His company could not afford a failed design followed by another chip revision,” which matches the same evidence and narrows the risk appropriately. The new six-month second-person opening and “What if” question are separately checked above. Paragraph 1’s “In his account” explicitly attributes the ordinary-cycle assessment. Paragraph 5’s new “another failing company” opening matches Huang’s ICOS recollection at line 36 and is separately checked above. Paragraph 4’s “going out of business” is faithful to lines 37–42.

No required factual revisions remain. “Waiting for a physical prototype felt safer” is read as the narrator’s illustration of conventional caution. “Waiting for a physical prototype would seem safer” would remove any ambiguity about whose feeling is meant, but the current context does not present it as Huang’s speech or a sourced report of his thoughts.

## Technical and framing checks

- **Emulation versus simulation:** the script correctly uses “emulator” and “emulation” for the pre-silicon work (lines 36, 43, 56). Do not substitute the host’s generic “simulation” at line 20 for a technically specific account of the equipment. “Virtual version” is an accessible description of the chip model being exercised on an emulator.
- **Physical prototype to production:** supported as the interview’s reported decision sequence (lines 20, 43–46, 54). Do not claim that no later silicon testing, manufacturing verification, or quality control occurred; the source does not establish that. The revised paragraph 1 says “In his account”; paragraph 2 and subsequent attributions also identify the retrospective source.
- **RIVA blending:** paragraph 8 accurately attributes eight of 32 to the hosts and the acknowledgment to Huang. It avoids the false inference that the whole chip was 75% defective. Do not present this interview alone as independently verified API documentation.
- **Transform pipeline:** the script makes no fully hardware-accelerated transform/projection claim. Keep that claim out. The sweeping assertions at source lines 19 and 30 are not technical corroboration.
- **Hypothetical timeline:** paragraphs 1, 4 and 10 use questions/conditional possibilities and explicitly acknowledge uncertainty. The source supplies Huang’s belief about survival, not proof of what would have happened under another decision.

## Omissions and interpretation

The narration’s lesson about earlier testing is supported, but should remain a reading of this episode rather than a general success formula. Lines 228–229 stress that smart decisions can fail and that the market matters; lines 239–244 discuss luck, consumer demand, Quake and Unreal. The current script’s explicit uncertainty and rejection of copying the gamble prevent a materially misleading deterministic claim. Adding one brief acknowledgment of market timing would improve balance but is not necessary to correct an asserted false fact. The final “harder decision” is clearly editorial emphasis, not a source quotation or independently measurable finding.

No quotations have been invented, no external/paid service was used, and no new media was created.

## Verdict totals

Final revised script: SUPPORTED: **41**; NOT IN SOURCE: **0**; CONTRADICTED: **0**; OVERSTATED: **0**; FLAGGED: **0**. Total factual/conditional claim rows: **41**. Two additional rows document the changed opening and the changed ICOS introduction; the former OVERSTATED row is now SUPPORTED following revision.

Recording gate: **passed for the revised script against this interview**, with the evidence limits above. This is source fidelity review, not independent corroboration of Huang’s historical recollection.

Reviewed script SHA-256: `61130465e5668b575664771f77e4ca9bb93b456da8571b9ef9a4b213e84c23d7`.

Author completion note: after this review, paragraph 3's long sentence was split into two sentences for spoken readability; its six-month and redesign-cycle claims are unchanged.
