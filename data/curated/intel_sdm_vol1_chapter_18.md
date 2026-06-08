---
architecture: x86_32
component: cet
mode: protected
tags: ['control_flow_enforcement', 'shadow_stack']
source: intel_sdm_vol1_chapter_18.md
---

# Intel SDM Volume 1 - Chapter 18

## CHAPTER 18

### CONTROL-FLOW ENFORCEMENT TECHNOLOGY (CET)

|        |                                                                        |       |
|--------|------------------------------------------------------------------------|-------|
| 18.1   | INTRODUCTION .....                                                     | 18-1  |
| 18.1.1 | Shadow Stack .....                                                     | 18-1  |
| 18.1.2 | Indirect Branch Tracking .....                                         | 18-1  |
| 18.1.3 | Speculative Behavior when CET is Enabled .....                         | 18-2  |
| 18.2   | SHADOW STACKS .....                                                    | 18-2  |
| 18.2.1 | Shadow Stack Pointer and its Operand and Address Size Attributes ..... | 18-2  |
| 18.2.2 | Terminology .....                                                      | 18-2  |
| 18.2.3 | Supervisor Shadow Stack Token .....                                    | 18-3  |
| 18.2.4 | Shadow Stack Usage on Task Switch .....                                | 18-5  |
| 18.2.5 | Switching Shadow Stacks .....                                          | 18-5  |
| 18.2.6 | Constraining Execution at Targets of RET .....                         | 18-7  |
| 18.3   | INDIRECT BRANCH TRACKING .....                                         | 18-7  |
| 18.3.1 | No-track Prefix for Near Indirect CALL/JMP .....                       | 18-8  |
| 18.3.2 | Terminology .....                                                      | 18-9  |
| 18.3.3 | Indirect Branch Tracking .....                                         | 18-10 |

## CONTENTS

|                                                                                          | PAGE  |
|------------------------------------------------------------------------------------------|-------|
| 18.3.3.1 Control Transfers between CPL 3 and CPL < 3 .....                               | 18-10 |
| 18.3.3.2 Control Transfers within CPL 3 or CPL < 3 .....                                 | 18-10 |
| 18.3.4 Indirect Branch Tracking State Machine .....                                      | 18-11 |
| 18.3.5 INT3 Treatment .....                                                              | 18-12 |
| 18.3.6 Legacy Compatibility Treatment .....                                              | 18-12 |
| 18.3.6.1 Legacy Code Page Bitmap Format .....                                            | 18-13 |
| 18.3.7 Other Considerations .....                                                        | 18-13 |
| 18.3.7.1 Intel® Transactional Synchronization Extensions (Intel® TSX) Interactions ..... | 18-13 |
| 18.3.7.2 #CP(ENDBRANCH) Priority w.r.t #NM and #UD .....                                 | 18-13 |
| 18.3.7.3 #CP(ENDBRANCH) Priority w.r.t #BP and #DB .....                                 | 18-13 |
| 18.3.8 Constraining Speculation after Missing ENDBRANCH .....                            | 18-14 |
| 18.4 INTEL® TRUSTED EXECUTION TECHNOLOGY (INTEL® TXT) INTERACTIONS .....                 | 18-14 |
