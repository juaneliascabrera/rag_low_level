---
architecture: x86_32
component: tsx
mode: protected
tags: ['transactional_synchronization', 'lock_elision']
source: intel_sdm_vol1_chapter_17.md
---

# Intel SDM Volume 1 - Chapter 17

## CHAPTER 17

### PROGRAMMING WITH INTEL® TRANSACTIONAL SYNCHRONIZATION EXTENSIONS

|          |                                                               |      |
|----------|---------------------------------------------------------------|------|
| 17.1     | OVERVIEW .....                                                | 17-1 |
| 17.2     | INTEL® TRANSACTIONAL SYNCHRONIZATION EXTENSIONS .....         | 17-1 |
| 17.2.1   | HLE Software Interface .....                                  | 17-2 |
| 17.2.2   | RTM Software Interface .....                                  | 17-3 |
| 17.3     | INTEL® TSX APPLICATION PROGRAMMING MODEL .....                | 17-3 |
| 17.3.1   | Detection of Transactional Synchronization Support .....      | 17-3 |
| 17.3.1.1 | Detection of HLE Support .....                                | 17-3 |
| 17.3.1.2 | Detection of RTM Support .....                                | 17-3 |
| 17.3.1.3 | Detection of XTEST Instruction .....                          | 17-4 |
| 17.3.1.4 | Detection of Intel® TSX Suspend Load Address Tracking .....   | 17-4 |
| 17.3.2   | Querying Transactional Execution Status .....                 | 17-4 |
| 17.3.3   | Requirements for HLE Locks .....                              | 17-4 |
| 17.3.4   | Transactional Nesting .....                                   | 17-4 |
| 17.3.4.1 | HLE Nesting and Elision .....                                 | 17-4 |
| 17.3.4.2 | RTM Nesting .....                                             | 17-5 |
| 17.3.4.3 | Nesting HLE and RTM .....                                     | 17-5 |
| 17.3.5   | RTM Abort Status Definition .....                             | 17-5 |
| 17.3.6   | RTM Memory Ordering .....                                     | 17-6 |
| 17.3.7   | RTM-Enabled Debugger Support .....                            | 17-6 |
| 17.3.8   | Intel® TSX Suspend/Resume Load Address Tracking Support ..... | 17-6 |
| 17.3.9   | Programming Considerations .....                              | 17-6 |
| 17.3.9.1 | Instruction Based Considerations .....                        | 17-7 |
| 17.3.9.2 | Runtime Considerations .....                                  | 17-8 |
