---
architecture: x86_32
component: x87_fpu
mode: protected
tags: ['fpu', 'floating_point', 'x87']
source: intel_sdm_vol1_chapter_8.md
---

# Intel SDM Volume 1 - Chapter 8

#define RETRY_LIMIT 10

int get_random_64(unsigned __int64 * arand)
{int i ;
  for (i = 0; i < RETRY_LIMIT; i++) {
    if(_rdrand64_step(arand) ) return SUCCESS;
  }
  return RETRY_LIMIT_EXCEEDED;
}
```

#### 7.3.17.2 RDSEED

The RDSEED instruction returns a random number. All Intel processors that support the RDSEED instruction indicate the availability of the RDSEED instruction via reporting CPUID.07H.00H:EBX.RDSEED[18] = 1.

RDSEED returns random numbers that are supplied by a cryptographically secure, enhanced non-deterministic random bit generator (Enhanced NRBG). The NRBG is designed to meet the NIST SP 800-90B and NIST SP800-90C standards.

In order for the hardware design to meet its security goals, the random number generator continuously tests itself and the random data it is generating. Runtime failures in the random number generator circuitry or statistically anomalous data occurring by chance will be detected by the self test hardware and flag the resulting data as being bad. In such extremely rare cases, the RDSEED instruction will return no data instead of bad data.

Under heavy load, with multiple cores executing RDSEED in parallel, it is possible for the demand of random numbers by software processes/threads to exceed the rate at which the random number generator hardware can supply them. This will lead to the RDSEED instruction returning no data transitorily. The RDSEED instruction indicates the occurrence of this situation by clearing the CF flag.

The RDSEED instruction returns with the carry flag set ( $CF = 1$ ) to indicate valid data is returned. It is recommended that software using the RDSEED instruction to get random numbers retry for a limited number of iterations while RDSEED returns  $CF = 0$  and complete when valid data is returned, indicated with  $CF = 1$ . This will deal with transitory underflows. A retry limit should be employed to prevent a hard failure in the NRBG (expected to be extremely rare) leading to a busy loop in software.

The intrinsic primitive for RDSEED is defined to address software's need for the common cases ( $CF = 1$ ) and the rare situations ( $CF = 0$ ). The intrinsic primitive returns a value that reflects the value of the carry flag returned by the underlying RDSEED instruction.



The x87 Floating-Point Unit (FPU) provides high-performance floating-point processing capabilities for use in graphics processing, scientific, engineering, and business applications. It supports the floating-point, integer, and packed BCD integer data types and the floating-point processing algorithms and exception handling architecture defined in the IEEE Standard 754 for Floating-Point Arithmetic.

This chapter describes the x87 FPU execution environment and instruction set. It also provides exception handling information that is specific to the x87 FPU. Refer to the following chapters or sections of chapters for additional information about x87 FPU instructions and floating-point operations:

- The Intel® 64 and IA-32 Architectures Software Developer's Manual, Volumes 2A, 2B, 2C, & 2D, provides detailed descriptions of x87 FPU instructions.
- Section 4.2.2, "Floating-Point Data Types," Section 4.2.1.2, "Signed Integers," and Section 4.7, "BCD and Packed BCD Integers," describe the floating-point, integer, and BCD data types.
- Section 4.9, "Overview of Floating-Point Exceptions," Section 4.9.1, "Floating-Point Exception Conditions," and Section 4.9.2, "Floating-Point Exception Priority," give an overview of the floating-point exceptions that the x87 FPU can detect and report.

## 8.1 X87 FPU EXECUTION ENVIRONMENT

The x87 FPU represents a separate execution environment within the IA-32 architecture (see Figure 8-1). This execution environment consists of eight data registers (called the x87 FPU data registers) and the following special-purpose registers:

- Status register.
- Control register.
- Tag word register.
- Last instruction pointer register.
- Last data (operand) pointer register.
- Opcode register.

These registers are described in the following sections.

The x87 FPU executes instructions from the processor's normal instruction stream. The state of the x87 FPU is independent from the state of the basic execution environment and from the state of SSE/SSE2/SSE3 extensions.

However, the x87 FPU and Intel MMX technology share state because the MMX registers are aliased to the x87 FPU data registers. Therefore, when writing code that uses x87 FPU and MMX instructions, the programmer must explicitly manage the x87 FPU and MMX state (see Section 9.5, "Compatibility with x87 FPU Architecture").

### 8.1.1 x87 FPU in 64-Bit Mode and Compatibility Mode

In compatibility mode and 64-bit mode, x87 FPU instructions function like they do in protected mode. Memory operands are specified using the ModR/M, SIB encoding that is described in Section 3.7.5, "Specifying an Offset."

### 8.1.2 x87 FPU Data Registers

The x87 FPU data registers (shown in Figure 8-1) consist of eight 80-bit registers. Values are stored in these registers in the double extended precision floating-point format shown in Figure 4-3. When floating-point, integer, or packed BCD integer values are loaded from memory into any of the x87 FPU data registers, the values are automatically converted into double extended precision floating-point format (if they are not already in that format). When computation results are subsequently transferred back into memory from any of the x87 FPU registers, the

results can be left in the double extended precision floating-point format or converted back into a shorter floating-point format, an integer format, or the packed BCD integer format. (See Section 8.2, "x87 FPU Data Types," for a description of the data types operated on by the x87 FPU.)

![Diagram of the x87 FPU Execution Environment showing data registers, control/status registers, and pointers.](60b089b85e598003112e72e9d4f19c5c_img.jpg)

The diagram illustrates the x87 FPU Execution Environment. At the top, a table titled "Data Registers" shows eight registers (R7 to R0). Each register is 80 bits wide, divided into a 1-bit Sign field, a 15-bit Exponent field (bits 79-63), and a 63-bit Significand field (bits 62-0). Below the data registers are three control/status registers: the Control Register (bits 15-0), the Status Register (bits 15-0), and the Tag Register (bits 15-0). To the right of these registers are two pointers: the Last Instruction Pointer (FCS:FIP) (bits 47-0) and the Last Data (Operand) Pointer (FDS:FDP) (bits 47-0). At the bottom right is the Opcode field (bits 10-0).

Diagram of the x87 FPU Execution Environment showing data registers, control/status registers, and pointers.

Figure 8-1. x87 FPU Execution Environment

The x87 FPU instructions treat the eight x87 FPU data registers as a register stack (see Figure 8-2). All addressing of the data registers is relative to the register on the top of the stack. The register number of the current top-of-stack register is stored in the TOP (stack TOP) field in the x87 FPU status word. Load operations decrement TOP by one and load a value into the new top-of-stack register, and store operations store the value from the current TOP register in memory and then increment TOP by one. (For the x87 FPU, a load operation is equivalent to a push and a store operation is equivalent to a pop.) Note that load and store operations are also available that do not push and pop the stack.

![Diagram of the x87 FPU Data Register Stack showing the stack structure and the current top register.](ed4a58048f06a1d37d2bd54da439fdb5_img.jpg)

The diagram shows the "FPU Data Register Stack" as a vertical stack of eight registers, numbered 0 to 7 from bottom to top. A "Growth Stack" arrow points downwards, indicating that the stack grows towards lower register numbers. The current top of the stack is register ST(0), which contains the value 011B. The registers are labeled ST(2), ST(1), and ST(0) on the right side. The "Top" field in the status word points to ST(0).

Diagram of the x87 FPU Data Register Stack showing the stack structure and the current top register.

Figure 8-2. x87 FPU Data Register Stack

If a load operation is performed when TOP is at 0, register wraparound occurs and the new value of TOP is set to 7. The floating-point stack-overflow exception indicates when wraparound might cause an unsaved value to be overwritten (see Section 8.5.1.1, "Stack Overflow or Underflow Exception (#IS)").

Many floating-point instructions have several addressing modes that permit the programmer to implicitly operate on the top of the stack, or to explicitly operate on specific registers relative to the TOP. Assemblers support these

register addressing modes, using the expression ST(0), or simply ST, to represent the current stack top and ST(i) to specify the *i*th register from TOP in the stack ( $0 \leq i \leq 7$ ). For example, if TOP contains 011B (register 3 is the top of the stack), the following instruction would add the contents of two registers in the stack (registers 3 and 5):

```
FADD ST, ST(2);
```

Figure 8-3 shows an example of how the stack structure of the x87 FPU registers and instructions are typically used to perform a series of computations. Here, a two-dimensional dot product is computed, as follows:

1. The first instruction (FLD value1) decrements the stack register pointer (TOP) and loads the value 5.6 from memory into ST(0). The result of this operation is shown in snap-shot (a).
2. The second instruction multiplies the value in ST(0) by the value 2.4 from memory and stores the result in ST(0), shown in snap-shot (b).
3. The third instruction decrements TOP and loads the value 3.8 in ST(0).
4. The fourth instruction multiplies the value in ST(0) by the value 10.3 from memory and stores the result in ST(0), shown in snap-shot (c).
5. The fifth instruction adds the value and the value in ST(1) and stores the result in ST(0), shown in snap-shot (d).

![Figure 8-3: Example x87 FPU Dot Product Computation. The diagram shows four snapshots (a, b, c, d) of the x87 FPU register stack. Each snapshot is a vertical stack of registers R0 through R7. In snapshot (a), R4 contains 5.6 and is labeled ST(0). In snapshot (b), R4 contains 13.44 and is labeled ST(0). In snapshot (c), R4 contains 13.44 and is labeled ST(1), while R3 contains 39.14 and is labeled ST(0). In snapshot (d), R4 contains 13.44 and is labeled ST(1), while R3 contains 52.58 and is labeled ST(0).](e179bec8994dabaa7dad4c913eb7fb41_img.jpg)

**Computation**  
Dot Product =  $(5.6 \times 2.4) + (3.8 \times 10.3)$

**Code:**  
FLD value1 ; (a) value1 = 5.6  
FMUL value2 ; (b) value2 = 2.4  
FLD value3 ; value3 = 3.8  
FMUL value4 ; (c) value4 = 10.3  
FADD ST(1) ; (d)

Figure 8-3: Example x87 FPU Dot Product Computation. The diagram shows four snapshots (a, b, c, d) of the x87 FPU register stack. Each snapshot is a vertical stack of registers R0 through R7. In snapshot (a), R4 contains 5.6 and is labeled ST(0). In snapshot (b), R4 contains 13.44 and is labeled ST(0). In snapshot (c), R4 contains 13.44 and is labeled ST(1), while R3 contains 39.14 and is labeled ST(0). In snapshot (d), R4 contains 13.44 and is labeled ST(1), while R3 contains 52.58 and is labeled ST(0).

**Figure 8-3. Example x87 FPU Dot Product Computation**

The style of programming demonstrated in this example is supported by the floating-point instruction set. In cases where the stack structure causes computation bottlenecks, the FXCH (exchange x87 FPU register contents) instruction can be used to streamline a computation.

### 8.1.2.1 Parameter Passing With the x87 FPU Register Stack

Like the general-purpose registers, the contents of the x87 FPU data registers are unaffected by procedure calls, or in other words, the values are maintained across procedure boundaries. A calling procedure can thus use the x87 FPU data registers (as well as the procedure stack) for passing parameter between procedures. The called procedure can reference parameters passed through the register stack using the current stack register pointer (TOP) and the ST(0) and ST(i) nomenclature. It is also common practice for a called procedure to leave a return value or result in register ST(0) when returning execution to the calling procedure or program.

When mixing MMX and x87 FPU instructions in the procedures or code sequences, the programmer is responsible for maintaining the integrity of parameters being passed in the x87 FPU data registers. If an MMX instruction is executed before the parameters in the x87 FPU data registers have been passed to another procedure, the parameters may be lost (see Section 9.5, "Compatibility with x87 FPU Architecture").

8.1.3 x87 FPU Status Register

The 16-bit x87 FPU status register (see Figure 8-4) indicates the current state of the x87 FPU. The flags in the x87 FPU status register include the FPU busy flag, top-of-stack (TOP) pointer, condition code flags, exception summary status flag, stack fault flag, and exception flags. The x87 FPU sets the flags in this register to show the results of operations.

![Diagram of the 16-bit x87 FPU Status Word. The word is represented as a horizontal bar with bit positions 15 down to 0. Bit 15 is labeled 'B'. Bits 14-13 are labeled 'C3'. Bits 11-10 are labeled 'TOP'. Bit 9 is labeled 'C2'. Bit 8 is labeled 'C1'. Bit 7 is labeled 'E'. Bit 6 is labeled 'S'. Bit 5 is labeled 'P'. Bit 4 is labeled 'U'. Bit 3 is labeled 'O'. Bit 2 is labeled 'Z'. Bit 1 is labeled 'D'. Bit 0 is labeled 'I'. Lines connect these bit fields to labels on the right: 'FPU Busy' points to bit 15; 'Top of Stack Pointer' points to bits 11-13; 'Condition Code' points to bits 14-13; 'Exception Summary Status' points to bit 7; 'Stack Fault' points to bit 6; 'Exception Flags' points to bit 5; 'Precision' points to bit 4; 'Underflow' points to bit 3; 'Overflow' points to bit 2; 'Zero Divide' points to bit 1; 'Denormalized Operand' points to bit 0; and 'Invalid Operation' points to bit 0.](7383c616236f02cd74e001b6d4145882_img.jpg)

Diagram of the 16-bit x87 FPU Status Word. The word is represented as a horizontal bar with bit positions 15 down to 0. Bit 15 is labeled 'B'. Bits 14-13 are labeled 'C3'. Bits 11-10 are labeled 'TOP'. Bit 9 is labeled 'C2'. Bit 8 is labeled 'C1'. Bit 7 is labeled 'E'. Bit 6 is labeled 'S'. Bit 5 is labeled 'P'. Bit 4 is labeled 'U'. Bit 3 is labeled 'O'. Bit 2 is labeled 'Z'. Bit 1 is labeled 'D'. Bit 0 is labeled 'I'. Lines connect these bit fields to labels on the right: 'FPU Busy' points to bit 15; 'Top of Stack Pointer' points to bits 11-13; 'Condition Code' points to bits 14-13; 'Exception Summary Status' points to bit 7; 'Stack Fault' points to bit 6; 'Exception Flags' points to bit 5; 'Precision' points to bit 4; 'Underflow' points to bit 3; 'Overflow' points to bit 2; 'Zero Divide' points to bit 1; 'Denormalized Operand' points to bit 0; and 'Invalid Operation' points to bit 0.

Figure 8-4. x87 FPU Status Word

The contents of the x87 FPU status register (referred to as the x87 FPU status word) can be stored in memory using the FSTSW/FNSTSW, FSTENV/FNSTENV, FSAVE/FNSAVE, and FXSAVE instructions. It can also be stored in the AX register of the integer unit, using the FSTSW/FNSTSW instructions.

8.1.3.1 Top of Stack (TOP) Pointer

A pointer to the x87 FPU data register that is currently at the top of the x87 FPU register stack is contained in bits 11 through 13 of the x87 FPU status word. This pointer, which is commonly referred to as TOP (for top-of-stack), is a binary value from 0 to 7. See Section 8.1.2, "x87 FPU Data Registers," for more information about the TOP pointer.

8.1.3.2 Condition Code Flags

The four condition code flags (C0 through C3) indicate the results of floating-point comparison and arithmetic operations. Table 8-1 summarizes the manner in which the floating-point instructions set the condition code flags. These condition code bits are used principally for conditional branching and for storage of information used in exception handling (see Section 8.1.4, "Branching and Conditional Moves on Condition Codes").

As shown in Table 8-1, the C1 condition code flag is used for a variety of functions. When both the IE and SF flags in the x87 FPU status word are set, indicating a stack overflow or underflow exception (#IS), the C1 flag distinguishes between overflow (C1 = 1) and underflow (C1 = 0). When the PE flag in the status word is set, indicating an inexact (rounded) result, the C1 flag is set to 1 if the last rounding by the instruction was upward. The FXAM instruction sets C1 to the sign of the value being examined.

The C2 condition code flag is used by the FPREM and FPREM1 instructions to indicate an incomplete reduction (or partial remainder). When a successful reduction has been completed, the C0, C3, and C1 condition code flags are set to the three least-significant bits of the quotient (Q2, Q1, and Q0, respectively). See “FPREM1—Partial Remainder” in Chapter 3, “Instruction Set Reference, A-L,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 2A, for more information on how these instructions use the condition code flags.

The FPTAN, FSIN, FCOS, and FSINCOS instructions set the C2 flag to 1 to indicate that the source operand is beyond the allowable range of  $\pm 2^{63}$  and clear the C2 flag if the source operand is within the allowable range.

Where the state of the condition code flags are listed as undefined in Table 8-1, do not rely on any specific value in these flags.

### 8.1.3.3 x87 FPU Floating-Point Exception Flags

The six x87 FPU floating-point exception flags (bits 0 through 5) of the x87 FPU status word indicate that one or more floating-point exceptions have been detected since the bits were last cleared. The individual exception flags (IE, DE, ZE, OE, UE, and PE) are described in detail in Section 8.4, “x87 FPU Floating-Point Exception Handling.” Each of the exception flags can be masked by an exception mask bit in the x87 FPU control word (see Section 8.1.5, “x87 FPU Control Word”). The exception summary status flag (ES, bit 7) is set when any of the unmasked exception flags are set. When the ES flag is set, the x87 FPU exception handler is invoked, using one of the techniques described in Section 8.7, “Handling x87 FPU Exceptions in Software.” (Note that if an exception flag is masked, the x87 FPU will still set the appropriate flag if the associated exception occurs, but it will not set the ES flag.)

The exception flags are “sticky” bits (once set, they remain set until explicitly cleared). They can be cleared by executing the FCLEX/FNCLEX (clear exceptions) instructions, by reinitializing the x87 FPU with the FINIT/FNINIT or FSAVE/FNSAVE instructions, or by overwriting the flags with an FRSTOR or FLDDENV instruction.

The B-bit (bit 15) is included for 8087 compatibility only. It reflects the contents of the ES flag.

**Table 8-1. Condition Code Interpretation**

| Instruction                                                                                                                                                                                                                 | C0                                                                           | C3 | C2                                                                 | C1                                   |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----|--------------------------------------------------------------------|--------------------------------------|
| FCOM, FCOMP, FCOMPP, FICOM, FICOMP, FTST, FUCOM, FUCOMP, FUCOMPP                                                                                                                                                            | Result of Comparison                                                         |    | Operands are not Comparable                                        | 0 or #IS                             |
| FCOMI, FCOMIP, FUCOMI, FUCOMIP                                                                                                                                                                                              | Undefined. (These instructions set the status flags in the EFLAGS register.) |    |                                                                    | #IS                                  |
| FXAM                                                                                                                                                                                                                        | Operand class                                                                |    |                                                                    | Sign                                 |
| FPREM, FPREM1                                                                                                                                                                                                               | Q2                                                                           | Q1 | 0 = reduction complete<br>1 = reduction incomplete                 | Q0 or #IS                            |
| F2XM1, FADD, FADDP, FBSTP, FCMOVcc, FIADD, FDIV, FDIVP, FDIVR, FDIVRP, FIDIV, FIDIVR, FIMUL, FIST, FISTP, FISUB, FISUBR, FMUL, FMULP, FPATAN, FRNDINT, FSCALE, FST, FSTP, FSUB, FSUBP, FSUBR, FSUBRP, FSQRT, FYL2X, FYL2XP1 | Undefined                                                                    |    |                                                                    | Roundup or #IS                       |
| FCOS, FSIN, FSINCOS, FPTAN                                                                                                                                                                                                  | Undefined                                                                    |    | 0 = source operand within range<br>1 = source operand out of range | Roundup or #IS (Undefined if C2 = 1) |
| FABS, FBLD, FCHS, FDECSTP, FILD, FINCSTP, FLD, Load Constants, FSTP (ext. prec.), FXCH, FXTRACT                                                                                                                             | Undefined                                                                    |    |                                                                    | 0 or #IS                             |

Table 8-1. Condition Code Interpretation (Contd.)

|                                                                               |                             |   |   |   |
|-------------------------------------------------------------------------------|-----------------------------|---|---|---|
| FLDENV, FRSTOR                                                                | Each bit loaded from memory |   |   |   |
| FFREE, FLDCW, FCLEX/FNCLEX, FNOP, FSTCW/FNSTCW, FSTENV/FNSTENV, FSTSW/FNSTSW, | Undefined                   |   |   |   |
| FINIT/FNINIT, FSAVE/FNSAVE                                                    | 0                           | 0 | 0 | 0 |

8.1.3.4 Stack Fault Flag

The stack fault flag (bit 6 of the x87 FPU status word) indicates that stack overflow or stack underflow has occurred with data in the x87 FPU data register stack. The x87 FPU explicitly sets the SF flag when it detects a stack overflow or underflow condition, but it does not explicitly clear the flag when it detects an invalid-arithmetic-operand condition.

When this flag is set, the condition code flag C1 indicates the nature of the fault: overflow (C1 = 1) and underflow (C1 = 0). The SF flag is a “sticky” flag, meaning that after it is set, the processor does not clear it until it is explicitly instructed to do so (for example, by an FINIT/FNINIT, FCLEX/FNCLEX, or FSAVE/FNSAVE instruction).

See Section 8.1.7, “x87 FPU Tag Word,” for more information on x87 FPU stack faults.

8.1.4 Branching and Conditional Moves on Condition Codes

The x87 FPU (beginning with the P6 family processors) supports two mechanisms for branching and performing conditional moves according to comparisons of two floating-point values. These mechanism are referred to here as the “old mechanism” and the “new mechanism.”

The old mechanism is available in the x87 FPU prior to the P6 family processors and in P6 family processors. This mechanism uses the floating-point compare instructions (FCOM, FCOMP, FCOMPP, FTST, FUCOMPP, FICOM, and FICOMP) to compare two floating-point values and set the condition code flags (C0 through C3) according to the results. The contents of the condition code flags are then copied into the status flags of the EFLAGS register using a two step process (see Figure 8-5):

- 1. The FSTSW AX instruction moves the x87 FPU status word into the AX register.
- 2. The SAHF instruction copies the upper 8 bits of the AX register, which includes the condition code flags, into the lower 8 bits of the EFLAGS register.

When the condition code flags have been loaded into the EFLAGS register, conditional jumps or conditional moves can be performed based on the new settings of the status flags in the EFLAGS register.

![Diagram showing the process of moving condition codes from the x87 FPU Status Word to the EFLAGS Register. It includes a table mapping Condition Codes (C0-C3) to Status Flags (CF, PF, ZF) and a flow diagram of the FSTSW AX and SAHF instructions.](790b3d1f6fbe3b4570cf1eec24db67f0_img.jpg)

The diagram illustrates the process of moving condition codes from the x87 FPU Status Word to the EFLAGS Register. It consists of three main parts: a mapping table, a flow diagram, and register bit-level details.

| Condition Code | Status Flag |
|----------------|-------------|
| C0             | CF          |
| C1             | (none)      |
| C2             | PF          |
| C3             | ZF          |

**Flow Diagram:**

- x87 FPU Status Word (bits 15-0):** Contains condition codes C3, C2, C1, and C0.
- FSTSW AX Instruction:** Copies the entire 16-bit status word into the **AX Register (bits 15-0)**.
- SAHF Instruction:** Copies the upper 8 bits of the AX Register (containing C3, C2, C1, C0) into the lower 8 bits of the **EFLAGS Register (bits 7-0)**.

**EFLAGS Register (bits 31-0):** The lower 8 bits (bits 7-0) are shown with flags ZF (bits 7-6), PF (bit 5), and CF (bits 4-3). Bit 1 is also indicated.

Diagram showing the process of moving condition codes from the x87 FPU Status Word to the EFLAGS Register. It includes a table mapping Condition Codes (C0-C3) to Status Flags (CF, PF, ZF) and a flow diagram of the FSTSW AX and SAHF instructions.

Figure 8-5. Moving the Condition Codes to the EFLAGS Register

The new mechanism is available beginning with the P6 family processors. Using this mechanism, the new floating-point compare and set EFLAGS instructions (FCOMI, FCOMIP, FUCOMI, and FUCOMIP) compare two floating-point values and set the ZF, PF, and CF flags in the EFLAGS register directly. A single instruction thus replaces the three instructions required by the old mechanism.

Note also that the FCMOVcc instructions (also new in the P6 family processors) allow conditional moves of floating-point values (values in the x87 FPU data registers) based on the setting of the status flags (ZF, PF, and CF) in the EFLAGS register. These instructions eliminate the need for an IF statement to perform conditional moves of floating-point values.

### 8.1.5 x87 FPU Control Word

The 16-bit x87 FPU control word (see Figure 8-6) controls the precision of the x87 FPU and rounding method used. It also contains the x87 FPU floating-point exception mask bits. The control word is cached in the x87 FPU control register. The contents of this register can be loaded with the FLDCW instruction and stored in memory with the FSTCW/FNSTCW instructions.

![Diagram of the 16-bit x87 FPU Control Word structure. The word is represented as a 16-bit register with bits 15 down to 0. Bits 15-12 are reserved (shaded). Bit 11 is 'X' (Exception Mask). Bits 10-9 are 'RC' (Rounding Control). Bits 8-7 are 'PC' (Precision Control). Bits 6-5 are 'P' (Precision Mask). Bits 4-3 are 'U' (Underflow Mask). Bits 2-1 are 'O' (Overflow Mask). Bit 0 is 'D' (Denormal Operand Mask). Bit 1 is 'Z' (Zero Divide Mask). Bit 2 is 'I' (Invalid Operation Mask). Bit 3 is 'M' (Mask). Bit 4 is 'M' (Mask). Bit 5 is 'M' (Mask). Bit 6 is 'M' (Mask). Bit 7 is 'M' (Mask). Bit 8 is 'M' (Mask). Bit 9 is 'M' (Mask). Bit 10 is 'M' (Mask). Bit 11 is 'M' (Mask). Bit 12 is 'M' (Mask). Bit 13 is 'M' (Mask). Bit 14 is 'M' (Mask). Bit 15 is 'M' (Mask).](6f7646fb94a459916885db7b5486488c_img.jpg)

The diagram illustrates the 16-bit x87 FPU Control Word structure. The word is represented as a 16-bit register with bits 15 down to 0. Bits 15-12 are reserved (shaded). Bit 11 is 'X' (Exception Mask). Bits 10-9 are 'RC' (Rounding Control). Bits 8-7 are 'PC' (Precision Control). Bits 6-5 are 'P' (Precision Mask). Bits 4-3 are 'U' (Underflow Mask). Bits 2-1 are 'O' (Overflow Mask). Bit 0 is 'D' (Denormal Operand Mask). Bit 1 is 'Z' (Zero Divide Mask). Bit 2 is 'I' (Invalid Operation Mask). Bit 3 is 'M' (Mask). Bit 4 is 'M' (Mask). Bit 5 is 'M' (Mask). Bit 6 is 'M' (Mask). Bit 7 is 'M' (Mask). Bit 8 is 'M' (Mask). Bit 9 is 'M' (Mask). Bit 10 is 'M' (Mask). Bit 11 is 'M' (Mask). Bit 12 is 'M' (Mask). Bit 13 is 'M' (Mask). Bit 14 is 'M' (Mask). Bit 15 is 'M' (Mask).

Diagram of the 16-bit x87 FPU Control Word structure. The word is represented as a 16-bit register with bits 15 down to 0. Bits 15-12 are reserved (shaded). Bit 11 is 'X' (Exception Mask). Bits 10-9 are 'RC' (Rounding Control). Bits 8-7 are 'PC' (Precision Control). Bits 6-5 are 'P' (Precision Mask). Bits 4-3 are 'U' (Underflow Mask). Bits 2-1 are 'O' (Overflow Mask). Bit 0 is 'D' (Denormal Operand Mask). Bit 1 is 'Z' (Zero Divide Mask). Bit 2 is 'I' (Invalid Operation Mask). Bit 3 is 'M' (Mask). Bit 4 is 'M' (Mask). Bit 5 is 'M' (Mask). Bit 6 is 'M' (Mask). Bit 7 is 'M' (Mask). Bit 8 is 'M' (Mask). Bit 9 is 'M' (Mask). Bit 10 is 'M' (Mask). Bit 11 is 'M' (Mask). Bit 12 is 'M' (Mask). Bit 13 is 'M' (Mask). Bit 14 is 'M' (Mask). Bit 15 is 'M' (Mask).

Figure 8-6. x87 FPU Control Word

When the x87 FPU is initialized with either an FINIT/FNINIT or FSAVE/FNSAVE instruction, the x87 FPU control word is set to 037FH, which masks all floating-point exceptions, sets rounding to nearest, and sets the x87 FPU precision to 64 bits.

#### 8.1.5.1 x87 FPU Floating-Point Exception Mask Bits

The exception-flag mask bits (bits 0 through 5 of the x87 FPU control word) mask the 6 floating-point exception flags in the x87 FPU status word. When one of these mask bits is set, its corresponding x87 FPU floating-point exception is blocked from being generated.

#### 8.1.5.2 Precision Control Field

The precision-control (PC) field (bits 8 and 9 of the x87 FPU control word) determines the precision (64, 53, or 24 bits) of floating-point calculations made by the x87 FPU (see Table 8-2). The default precision is double extended precision, which uses the full 64-bit significand available with the double extended precision floating-point format of the x87 FPU data registers. This setting is best suited for most applications, because it allows applications to take full advantage of the maximum precision available with the x87 FPU data registers.

Table 8-2. Precision Control Field (PC)

| Precision                           | PC Field |
|-------------------------------------|----------|
| Single Precision (24 bits)          | 00B      |
| Reserved                            | 01B      |
| Double Precision (53 bits)          | 10B      |
| Double Extended Precision (64 bits) | 11B      |

The double precision and single precision settings reduce the size of the significand to 53 bits and 24 bits, respectively. These settings are provided to support IEEE Standard 754 and to provide compatibility with the specifications of certain existing programming languages. Using these settings nullifies the advantages of the double extended precision floating-point format's 64-bit significand length. When reduced precision is specified, the rounding of the significand value clears the unused bits on the right to zeros.

The precision-control bits only affect the results of the following floating-point instructions: FADD, FADDP, FIADD, FSUB, FSUBP, FISUB, FSUBR, FSUBRP, FISUBR, FMUL, FMULP, FIMUL, FDIV, FDIVP, FIDIV, FDIVR, FDIVRP, FIDIVR, and FSQRT.

8.1.5.3 Rounding Control Field

The rounding-control (RC) field of the x87 FPU control register (bits 10 and 11) controls how the results of x87 FPU floating-point instructions are rounded. See Section 4.8.4, "Rounding," for a discussion of rounding of floating-point values; See Section 4.8.4.1, "Rounding Control (RC) Fields," for the encodings of the RC field.

8.1.6 Infinity Control Flag

The infinity control flag (bit 12 of the x87 FPU control word) is provided for compatibility with the Intel 287 Math Coprocessor; it is not meaningful for later version x87 FPU coprocessors or IA-32 processors. See Section 4.8.3.3, "Signed Infinities," for information on how the x87 FPU handles infinity values.

8.1.7 x87 FPU Tag Word

The 16-bit tag word (see Figure 8-7) indicates the contents of each the 8 registers in the x87 FPU data-register stack (one 2-bit tag per register). The tag codes indicate whether a register contains a valid number, zero, or a special floating-point number (NaN, infinity, denormal, or unsupported format), or whether it is empty. The x87 FPU tag word is cached in the x87 FPU in the x87 FPU tag word register. When the x87 FPU is initialized with either an FINIT/FNINIT or FSAVE/FNSAVE instruction, the x87 FPU tag word is set to FFFFH, which marks all the x87 FPU data registers as empty.

![Diagram of the x87 FPU Tag Word structure. It shows a 16-bit word divided into eight 2-bit tags, labeled TAG(7) through TAG(0). Bit 15 is the leftmost and bit 0 is the rightmost. Below the diagram is a legend for TAG Values: 00 — Valid, 01 — Zero, 10 — Special: invalid (NaN, unsupported), infinity, or denormal, 11 — Empty.](e6f1796192af886c62d27de5be37ef24_img.jpg)

15

0

TAG(7)TAG(6)TAG(5)TAG(4)TAG(3)TAG(2)TAG(1)TAG(0)

TAG Values

00 — Valid

01 — Zero

10 — Special: invalid (NaN, unsupported), infinity, or denormal

11 — Empty

Diagram of the x87 FPU Tag Word structure. It shows a 16-bit word divided into eight 2-bit tags, labeled TAG(7) through TAG(0). Bit 15 is the leftmost and bit 0 is the rightmost. Below the diagram is a legend for TAG Values: 00 — Valid, 01 — Zero, 10 — Special: invalid (NaN, unsupported), infinity, or denormal, 11 — Empty.

Figure 8-7. x87 FPU Tag Word

Each tag in the x87 FPU tag word corresponds to a physical register (numbers 0 through 7). The current top-of-stack (TOP) pointer stored in the x87 FPU status word can be used to associate tags with registers relative to ST(0).

The x87 FPU uses the tag values to detect stack overflow and underflow conditions (see Section 8.5.1.1, “Stack Overflow or Underflow Exception (#IS)”).

Application programs and exception handlers can use this tag information to check the contents of an x87 FPU data register without performing complex decoding of the actual data in the register. To read the tag register, it must be stored in memory using either the FSTENV/FNSTENV or FSAVE/FNSAVE instructions. The location of the tag word in memory after being saved with one of these instructions is shown in Figures 8-9 through 8-12.

Software cannot directly load or modify the tags in the tag register. The FLDENV and FRSTOR instructions load an image of the tag register into the x87 FPU; however, the x87 FPU uses those tag values only to determine if the data registers are empty (11B) or non-empty (00B, 01B, or 10B).

If the tag register image indicates that a data register is empty, the tag in the tag register for that data register is marked empty (11B); if the tag register image indicates that the data register is non-empty, the x87 FPU reads the actual value in the data register and sets the tag for the register accordingly. This action prevents a program from setting the values in the tag register to incorrectly represent the actual contents of non-empty data registers.

## 8.1.8 x87 FPU Instruction and Data (Operand) Pointers

The x87 FPU stores pointers to the instruction and data (operand) for the last non-control instruction executed. These are the x87 FPU instruction pointer and x87 FPU data (operand) pointers; software can save these pointers to provide state information for exception handlers. The pointers are illustrated in Figure 8-1 (the figure illustrates the pointers as used outside 64-bit mode; see below).

Note that the value in the x87 FPU data pointer is always a pointer to a memory operand. If the last non-control instruction that was executed did not have a memory operand, the value in the data pointer is undefined (reserved). If CPUID.07H.00H:EBX[6] = 1, the data pointer is updated only for x87 non-control instructions that incur unmasked x87 exceptions.

The contents of the x87 FPU instruction and data pointers remain unchanged when any of the following instructions are executed: FCLEX/FNCLEX, FLDCW, FSTCW/FNSTCW, FSTSW/FNSTSW, FSTENV/FNSTENV, FLDENV, and WAIT/FWAIT.

For all the x87 FPUs and Numeric Processor Extensions (NPXs) except the 8087, the x87 FPU instruction pointer points to any prefixes that preceded the instruction. For the 8087, the x87 FPU instruction pointer points only to the actual opcode.

The x87 FPU instruction and data pointers each consists of an offset and a segment selector:

- The x87 FPU Instruction Pointer Offset (FIP) comprises 64 bits on processors that support IA-32e mode; on other processors, it offset comprises 32 bits.
- The x87 FPU Instruction Pointer Selector (FCS) comprises 16 bits.
- The x87 FPU Data Pointer Offset (FDP) comprises 64 bits on processors that support IA-32e mode; on other processors, it offset comprises 32 bits.
- The x87 FPU Data Pointer Selector (FDS) comprises 16 bits.

The pointers are accessed by the FINIT/FNINIT, FLDENV, FRSTOR, FSAVE/FNSAVE, FSTENV/FNSTENV, FXRSTOR, FXSAVE, XRSTOR, XSAVE, and XSAVEOPT instructions as follows:

- FINIT/FNINIT. Each instruction clears FIP, FCS, FDP, and FDS.
- FLDENV, FRSTOR. These instructions use the memory formats given in Figures 8-9 through 8-12:
  - For each of FIP and FDP, each instruction loads the lower 32 bits from memory and clears the upper 32 bits.
  - If CR0.PE = 1, each instruction loads FCS and FDS from memory; otherwise, it clears them.
- FSAVE/FNSAVE, FSTENV/FNSTENV. These instructions use the memory formats given in Figures 8-9 through 8-12.
  - Each instruction saves the lower 32 bits of each FIP and FDP into memory. the upper 32 bits are not saved.
  - If CR0.PE = 1, each instruction saves FCS and FDS into memory. If CPUID.07H.00H:EBX[13] = 1, the processor deprecates FCS and FDS; it saves each as 0000H.
  - After saving these data into memory, FSAVE/FNSAVE clears FIP, FCS, FDP, and FDS.

- FXRSTOR, XRSTOR. These instructions load data from a memory image whose format depends on operating mode and the REX prefix. The memory formats are given in Tables 3-45, 3-48, and 3-49 in Chapter 3, “Instruction Set Reference, A-L,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 2A.
  - Outside of 64-bit mode or if REX.W = 0, the instructions operate as follows:
    - For each of FIP and FDP, each instruction loads the lower 32 bits from memory and clears the upper 32 bits.
    - Each instruction loads FCS and FDS from memory.
  - In 64-bit mode with REX.W = 1, the instructions operate as follows:
    - Each instruction loads FIP and FDP from memory.
    - Each instruction clears FCS and FDS.
- FXSAVE, XSAVE, and XSAVEOPT. These instructions store data into a memory image whose format depends on operating mode and the REX prefix. The memory formats are given in Tables 3-45, 3-48, and 3-49 in Chapter 3, “Instruction Set Reference, A-L,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 2A.
  - Outside of 64-bit mode or if REX.W = 0, the instructions operate as follows:
    - Each instruction saves the lower 32 bits of each of FIP and FDP into memory. The upper 32 bits are not saved.
    - Each instruction saves FCS and FDS into memory. If CPUID.07H.00H:EBX[13] = 1, the processor deprecates FCS and FDS; it saves each as 0000H.
  - In 64-bit mode with REX.W = 1, each instruction saves FIP and FDP into memory. FCS and FDS are not saved.

## 8.1.9 Last Instruction Opcode

The x87 FPU stores in the 11-bit x87 FPU opcode register (FOP) the opcode of the last x87 non-control instruction executed that incurred an unmasked x87 exception. (This information provides state information for exception handlers.) Only the first and second opcode bytes (after all prefixes) are stored in the x87 FPU opcode register. Figure 8-8 shows the encoding of these two bytes. Since the upper 5 bits of the first opcode byte are the same for all floating-point opcodes (11011B), only the lower 3 bits of this byte are stored in the opcode register.

### 8.1.9.1 Fopcode Compatibility Sub-mode

Some Pentium 4 and Intel Xeon processors provide program control over the value stored into FOP. Here, bit 2 of the IA32\_MISC\_ENABLE MSR enables (set) or disables (clear) the fopcode compatibility mode.

If fopcode compatibility mode is enabled, FOP is defined as it had been in previous IA-32 implementations, as the opcode of the last x87 non-control instruction executed (even if that instruction did not incur an unmasked x87 exception).

![Diagram showing the encoding of the first and second instruction bytes into the x87 FPU Opcode Register. The 1st Instruction Byte (bits 7-0) and 2nd Instruction Byte (bits 7-0) are shown. The 1st byte's lower 3 bits (bits 2-0) are mapped to bits 10-8 of the 11-bit x87 FPU Opcode Register. The 2nd byte's bits 7-0 are mapped to bits 7-0 of the register.](63833ebb6af5b7c297ac69a318e96a73_img.jpg)

The diagram illustrates the mapping of instruction bytes to the x87 FPU Opcode Register (FOP). It shows two input bytes: the '1st Instruction Byte' and the '2nd Instruction Byte'. The 1st byte has bits 7, 2, and 0 marked. The 2nd byte has bits 7 and 0 marked. Below these, the 'x87 FPU Opcode Register' is shown as an 11-bit register with bits 10, 8, 7, and 0 marked. Arrows indicate that the lower 3 bits of the 1st byte (bits 2-0) are stored in bits 10-8 of the register, and the entire 8 bits of the 2nd byte (bits 7-0) are stored in bits 7-0 of the register.

Diagram showing the encoding of the first and second instruction bytes into the x87 FPU Opcode Register. The 1st Instruction Byte (bits 7-0) and 2nd Instruction Byte (bits 7-0) are shown. The 1st byte's lower 3 bits (bits 2-0) are mapped to bits 10-8 of the 11-bit x87 FPU Opcode Register. The 2nd byte's bits 7-0 are mapped to bits 7-0 of the register.

Figure 8-8. Contents of x87 FPU Opcode Registers

The fopcode compatibility mode should be enabled only when x87 FPU floating-point exception handlers are designed to use the fopcode to analyze program performance or restart a program after an exception has been handled.

More recent Intel 64 processors do not support fopcode compatibility mode and do not allow software to set bit 2 of the IA32\_MISC\_ENABLE MSR.

### 8.1.10 Saving the x87 FPU State with FSTENV/FNSTENV and FSAVE/FNSAVE

The FSTENV/FNSTENV and FSAVE/FNSAVE instructions store x87 FPU state information in memory for use by exception handlers and other system and application software. The FSTENV/FNSTENV instruction saves the contents of the status, control, tag, x87 FPU instruction pointer, x87 FPU data pointer, and opcode registers. The FSAVE/FNSAVE instruction stores that information plus the contents of the x87 FPU data registers. Note that the FSAVE/FNSAVE instruction also initializes the x87 FPU to default values (just as the FINIT/FNINIT instruction does) after it has saved the original state of the x87 FPU.

The manner in which this information is stored in memory depends on the operating mode of the processor (protected mode or real-address mode) and on the operand-size attribute in effect (32-bit or 16-bit). See Figures 8-9 through 8-12. In virtual-8086 mode or SMM, the real-address mode formats shown in Figure 8-12 is used. See Chapter 34, “System Management Mode,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3C, for information on using the x87 FPU while in SMM.

The FLDENV and FRSTOR instructions allow x87 FPU state information to be loaded from memory into the x87 FPU. Here, the FLDENV instruction loads only the status, control, tag, x87 FPU instruction pointer, x87 FPU data pointer, and opcode registers, and the FRSTOR instruction loads all the x87 FPU registers, including the x87 FPU stack registers.

![](8c407177cdd331f61e4207ce184ff568_img.jpg)

| 32-Bit Protected Mode Format         |                     |    |                                  |                                 |    |
|--------------------------------------|---------------------|----|----------------------------------|---------------------------------|----|
| 31                                   | 16                  | 15 |                                  | 0                               |    |
|                                      |                     |    |                                  | Control Word                    | 0  |
|                                      |                     |    |                                  | Status Word                     | 4  |
|                                      |                     |    |                                  | Tag Word                        | 8  |
| FPU Instruction Pointer Offset (FIP) |                     |    |                                  |                                 | 12 |
| 0 0 0 0 0                            | Bits 10:0 of opcode |    | FPU Instruction Pointer Selector |                                 | 16 |
| FPU Data Pointer Offset (FDP)        |                     |    |                                  |                                 | 20 |
|                                      |                     |    |                                  | FPU Data Pointer Selector (FDS) | 24 |

For instructions that also store x87 FPU data registers, the eight 80-bit registers (R0-R7) follow the above structure in sequence.

**Figure 8-9. Protected Mode x87 FPU State Image in Memory, 32-Bit Format**

![](071401df23f31c4c9dfb897164ac59dc_img.jpg)

**32-Bit Real-Address Mode Format**

|                                 |            |    |    |
|---------------------------------|------------|----|----|
| 31                              | 16         | 15 | 0  |
| Control Word                    |            |    | 0  |
| Status Word                     |            |    | 4  |
| Tag Word                        |            |    | 8  |
| FIP[15:0]                       |            |    | 12 |
| 0 0 0 0                         | FIP[31:16] |    | 16 |
| FDP[15:0]                       |            |    | 20 |
| 0 0 0 0                         | FDP[31:16] |    | 24 |
| 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 |            |    |    |

For instructions that also store x87 FPU data registers, the eight 80-bit registers (R0-R7) follow the above structure in sequence.

Figure 8-10. Real Mode x87 FPU State Image in Memory, 32-Bit Format

![](841943891f19fcd045f406339e8d5655_img.jpg)

**16-Bit Protected Mode Format**

|              |    |
|--------------|----|
| 15           | 0  |
| Control Word | 0  |
| Status Word  | 2  |
| Tag Word     | 4  |
| FIP          | 6  |
| FCS          | 8  |
| FDP          | 10 |
| FDS          | 12 |

Figure 8-11. Protected Mode x87 FPU State Image in Memory, 16-Bit Format

![](33b37422d7968d2d8e7d3c48fe341a77_img.jpg)

**16-Bit Real-Address Mode and Virtual-8086 Mode Format**

|                                 |    |
|---------------------------------|----|
| 15                              | 0  |
| Control Word                    | 0  |
| Status Word                     | 2  |
| Tag Word                        | 4  |
| FIP[15:0]                       | 6  |
| FIP[19:16]   0                  | 8  |
| Bits 10:0 of opcode             |    |
| FDP[15:0]                       | 10 |
| FDP[19:16]   0                  | 12 |
| 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 |    |

Figure 8-12. Real Mode x87 FPU State Image in Memory, 16-Bit Format

8.1.11 Saving the x87 FPU State with FXSAVE

The FXSAVE and FXRSTOR instructions save and restore, respectively, the x87 FPU state along with the state of the XMM registers and the MXCSR register. Using the FXSAVE instruction to save the x87 FPU state has two benefits: (1) FXSAVE executes faster than FSAVE, and (2) FXSAVE saves the entire x87 FPU, MMX, and XMM state in one operation. See Section 10.5, "FXSAVE and FXRSTOR Instructions," for additional information about these instructions.

## 8.2 X87 FPU DATA TYPES

The x87 FPU recognizes and operates on the following seven data types (see Figures 8-13): single precision floating-point, double precision floating-point, double extended precision floating-point, signed word integer, signed doubleword integer, signed quadword integer, and packed BCD decimal integers.

For detailed information about these data types, see Section 4.2.2, "Floating-Point Data Types," Section 4.2.1.2, "Signed Integers," and Section 4.7, "BCD and Packed BCD Integers."

With the exception of the 80-bit double extended precision floating-point format, all of these data types exist in memory only. When they are loaded into x87 FPU data registers, they are converted into double extended precision floating-point format and operated on in that format.

Denormal values are also supported in each of the floating-point types, as required by IEEE Standard 754. When a denormal number in single precision or double precision floating-point format is used as a source operand and the denormal exception is masked, the x87 FPU automatically **normalizes** the number when it is converted to double extended precision format.

When stored in memory, the least significant byte of an x87 FPU data-type value is stored at the initial address specified for the value. Successive bytes from the value are then stored in successively higher addresses in memory. The floating-point instructions load and store memory operands using only the initial address of the operand.

![Figure 8-13: x87 FPU Data Type Formats. This diagram illustrates the bit-level structure of seven x87 FPU data types. 1. Single Precision Floating-Point: A 32-bit format with a 1-bit Sign (bit 31), an 8-bit Exponent (bits 30-23), and a 23-bit Fraction (bits 22-0). An arrow points to the Exponent field with the label 'Implied Integer'. 2. Double Precision Floating-Point: A 64-bit format with a 1-bit Sign (bit 63), a 11-bit Exponent (bits 62-52), and a 52-bit Fraction (bits 51-0). An arrow points to the Exponent field with the label 'Implied Integer'. 3. Double Extended Precision Floating-Point: An 80-bit format with a 1-bit Sign (bit 79), a 15-bit Exponent (bits 78-64), and a 64-bit Fraction (bits 63-0). An arrow points to the Exponent field with the label 'Integer'. 4. Word Integer: A 16-bit signed integer with a 1-bit Sign (bit 15) and 15 data bits (bits 14-0). 5. Doubleword Integer: A 32-bit signed integer with a 1-bit Sign (bit 31) and 31 data bits (bits 30-0). 6. Quadword Integer: A 64-bit signed integer with a 1-bit Sign (bit 63) and 63 data bits (bits 62-0). 7. Packed BCD Integers: A 10-byte (80-bit) format. The first byte (bits 79-72) contains an 'X' (unused) and the next seven bytes (bits 71-0) contain BCD digits D17 through D0. A note indicates '4 Bits = 1 BCD Digit'.](67efa927d9ba6404574fda89b4d48895_img.jpg)

Figure 8-13: x87 FPU Data Type Formats. This diagram illustrates the bit-level structure of seven x87 FPU data types. 1. Single Precision Floating-Point: A 32-bit format with a 1-bit Sign (bit 31), an 8-bit Exponent (bits 30-23), and a 23-bit Fraction (bits 22-0). An arrow points to the Exponent field with the label 'Implied Integer'. 2. Double Precision Floating-Point: A 64-bit format with a 1-bit Sign (bit 63), a 11-bit Exponent (bits 62-52), and a 52-bit Fraction (bits 51-0). An arrow points to the Exponent field with the label 'Implied Integer'. 3. Double Extended Precision Floating-Point: An 80-bit format with a 1-bit Sign (bit 79), a 15-bit Exponent (bits 78-64), and a 64-bit Fraction (bits 63-0). An arrow points to the Exponent field with the label 'Integer'. 4. Word Integer: A 16-bit signed integer with a 1-bit Sign (bit 15) and 15 data bits (bits 14-0). 5. Doubleword Integer: A 32-bit signed integer with a 1-bit Sign (bit 31) and 31 data bits (bits 30-0). 6. Quadword Integer: A 64-bit signed integer with a 1-bit Sign (bit 63) and 63 data bits (bits 62-0). 7. Packed BCD Integers: A 10-byte (80-bit) format. The first byte (bits 79-72) contains an 'X' (unused) and the next seven bytes (bits 71-0) contain BCD digits D17 through D0. A note indicates '4 Bits = 1 BCD Digit'.

Figure 8-13. x87 FPU Data Type Formats

As a general rule, values should be stored in memory in double precision format. This format provides sufficient range and precision to return correct results with a minimum of programmer attention. The single precision format is useful for debugging algorithms, because rounding problems will manifest themselves more quickly in this format. The double extended precision format is normally reserved for holding intermediate results in the x87 FPU registers and constants. Its extra length is designed to shield final results from the effects of rounding and overflow/underflow in intermediate calculations. However, when an application requires the maximum range and precision of the x87 FPU (for data storage, computations, and results), values can be stored in memory in double extended precision format.

8.2.1     Indefinites

For each x87 FPU data type, one unique encoding is reserved for representing the special value **indefinite**. The x87 FPU produces indefinite values as responses to some masked floating-point invalid-operation exceptions. See Tables 4-1, 4-3, and 4-5 for the encoding of the integer indefinite, QNaN floating-point indefinite, and packed BCD integer indefinite, respectively.

The binary integer encoding 100..00B represents either of two things, depending on the circumstances of its use:

- The largest negative number supported by the format ( $-2^{15}$ ,  $-2^{31}$ , or  $-2^{63}$ ).
- The **integer indefinite** value.

If this encoding is used as a source operand (as in an integer load or integer arithmetic instruction), the x87 FPU interprets it as the largest negative number representable in the format being used. If the x87 FPU detects an invalid operation when storing an integer value in memory with an FIST/FISTP instruction and the invalid-operation exception is masked, the x87 FPU stores the integer indefinite encoding in the destination operand as a masked response to the exception. In situations where the origin of a value with this encoding may be ambiguous, the invalid-operation exception flag can be examined to see if the value was produced as a response to an exception.

8.2.2     Unsupported Double Extended Precision Floating-Point Encodings and Pseudo-Denormals

The double extended precision floating-point format permits many encodings that do not fall into any of the categories shown in Table 4-3. Table 8-3 shows these unsupported encodings. Some of these encodings were supported by the Intel 287 math coprocessor; however, most of them are not supported by the Intel 387 math coprocessor and later IA-32 processors. These encodings are no longer supported due to changes made in the final version of IEEE Standard 754 that eliminated these encodings.

Specifically, the categories of encodings formerly known as pseudo-NaNs, pseudo-infinities, and un-normal numbers are not supported and should not be used as operand values. The Intel 387 math coprocessor and later IA-32 processors generate an invalid-operation exception when these encodings are encountered as operands.

Beginning with the Intel 387 math coprocessor, the encodings formerly known as pseudo-denormal numbers are not generated by IA-32 processors. When encountered as operands, however, they are handled correctly, considering the biased exponent as 1 (and the unbiased exponent as -16382); that is, they are treated as denormals and a denormal exception is generated. Pseudo-denormal numbers should not be used as operand values. They are supported by current IA-32 processors (as described here) to support legacy code.

Table 8-3. Unsupported Double Extended Precision Floating-Point Encodings and Pseudo-Denormals

| Class                   |                  | Sign      | Biased Exponent | Significand |                |
|-------------------------|------------------|-----------|-----------------|-------------|----------------|
|                         |                  |           |                 | Integer     | Fraction       |
| Positive Pseudo-NaNs    | Quiet            | 0         | 11..11          | 0           | 11..11         |
|                         |                  | $\dot{0}$ | $\dot{11..11}$  |             | $\dot{10..00}$ |
|                         | Signaling        | 0         | 11..11          | 0           | 01..11         |
|                         |                  | $\dot{0}$ | $\dot{11..11}$  |             | $\dot{00..01}$ |
| Positive Floating-Point | Pseudo-infinity  | 0         | 11..11          | 0           | 00..00         |
|                         | Unnormals        | 0         | 11..10          | 0           | 11..11         |
|                         |                  | $\dot{0}$ | $\dot{00..01}$  |             | $\dot{00..00}$ |
|                         | Pseudo-denormals | 0         | 00..00          | 1           | 11..11         |
|                         |                  | $\dot{0}$ | $\dot{00..00}$  |             | $\dot{00..00}$ |

**Table 8-3. Unsupported Double Extended Precision Floating-Point Encodings and Pseudo-Denormals (Contd.)**

|                         |                  |   |             |   |             |
|-------------------------|------------------|---|-------------|---|-------------|
| Negative Floating-Point | Pseudo-denormals | 1 | 00..00      | 1 | 11..11      |
|                         |                  | . | .           |   | .           |
|                         |                  | 1 | 00..00      |   | 00..00      |
|                         | Unnormals        | 1 | 11..10      | 0 | 11..01      |
|                         |                  | . | .           |   | .           |
|                         |                  | 1 | 00..01      |   | 00..00      |
| Negative Pseudo-NaNs    | Pseudo-infinity  | 1 | 11..11      | 0 | 00..00      |
|                         | Signaling        | 1 | 11..11      | 0 | 01..11      |
|                         |                  | . | .           |   | .           |
|                         | Quiet            | 1 | 11..11      | 0 | 11..11      |
|                         |                  | . | .           |   | .           |
|                         |                  | 1 | 11..11      |   | 10..00      |
|                         |                  |   | ← 15 bits → |   | ← 63 bits → |

## 8.3 X87 FPU INSTRUCTION SET

The floating-point instructions that the x87 FPU supports can be grouped into six functional categories:

- Data transfer instructions.
- Basic arithmetic instructions.
- Comparison instructions.
- Transcendental instructions.
- Load constant instructions.
- x87 FPU control instructions.

See Section 5.2, “x87 FPU Instructions,” for a list of the floating-point instructions by category.

The following section briefly describes the instructions in each category. Detailed descriptions of the floating-point instructions are given in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volumes 2A, 2B, 2C, & 2D.

### 8.3.1 Escape (ESC) Instructions

All of the instructions in the x87 FPU instruction set fall into a class of instructions known as escape (ESC) instructions. All of these instructions have a common opcode format, where the first byte of the opcode is one of the numbers from D8H through DFH.

### 8.3.2 x87 FPU Instruction Operands

Most floating-point instructions require one or two operands, located on the x87 FPU data-register stack or in memory. (None of the floating-point instructions accept immediate operands.)

When an operand is located in a data register, it is referenced relative to the ST(0) register (the register at the top of the register stack), rather than by a physical register number. Often the ST(0) register is an implied operand.

Operands in memory can be referenced using the same operand addressing methods described in Section 3.7, “Operand Addressing.”

### 8.3.3 Data Transfer Instructions

The data transfer instructions (see Table 8-4) perform the following operations:

- Load a floating-point, integer, or packed BCD operand from memory into the ST(0) register.
- Store the value in an ST(0) register to memory in floating-point, integer, or packed BCD format.
- Move values between registers in the x87 FPU register stack.

The FLD (load floating-point) instruction pushes a floating-point operand from memory onto the top of the x87 FPU data-register stack. If the operand is in single precision or double precision floating-point format, it is automatically converted to double extended precision floating-point format. This instruction can also be used to push the value in a selected x87 FPU data register onto the top of the register stack.

The FILD (load integer) instruction converts an integer operand in memory into double extended precision floating-point format and pushes the value onto the top of the register stack. The FBLD (load packed decimal) instruction performs the same load operation for a packed BCD operand in memory.

**Table 8-4. Data Transfer Instructions**

| Floating-Point |                              | Integer |                       | Packed Decimal |                              |
|----------------|------------------------------|---------|-----------------------|----------------|------------------------------|
| FLD            | Load Floating-Point          | FILD    | Load Integer          | FBLD           | Load Packed Decimal          |
| FST            | Store Floating-Point         | FIST    | Store Integer         |                |                              |
| FSTP           | Store Floating-Point and Pop | FISTP   | Store Integer and Pop | FBSTP          | Store Packed Decimal and Pop |
| FXCH           | Exchange Register Contents   |         |                       |                |                              |
| FCMOV $cc$     | Conditional Move             |         |                       |                |                              |

The FST (store floating-point) and FIST (store integer) instructions store the value in register ST(0) in memory in the destination format (floating-point or integer, respectively). Again, the format conversion is carried out automatically.

The FSTP (store floating-point and pop), FISTP (store integer and pop), and FBSTP (store packed decimal and pop) instructions store the value in the ST(0) registers into memory in the destination format (floating-point, integer, or packed BCD), then performs a **pop** operation on the register stack. A pop operation causes the ST(0) register to be marked empty and the stack pointer (TOP) in the x87 FPU control word to be incremented by 1. The FSTP instruction can also be used to copy the value in the ST(0) register to another x87 FPU register [ST(i)].

The FXCH (exchange register contents) instruction exchanges the value in a selected register in the stack [ST(i)] with the value in ST(0).

The FCMOV $cc$  (conditional move) instructions move the value in a selected register in the stack [ST(i)] to register ST(0) if a condition specified with a condition code ( $cc$ ) is satisfied (see Table 8-5). The condition being tested for is represented by the status flags in the EFLAGS register. The condition code mnemonics are appended to the letters "FCMOV" to form the mnemonic for a FCMOV $cc$  instruction.

**Table 8-5. Floating-Point Conditional Move Instructions**

| Instruction Mnemonic | Status Flag States | Condition Description |
|----------------------|--------------------|-----------------------|
| FCMOVB               | CF=1               | Below                 |
| FCMOVNB              | CF=0               | Not below             |
| FCMOVE               | ZF=1               | Equal                 |
| FCMOVNE              | ZF=0               | Not equal             |

**Table 8-5. Floating-Point Conditional Move Instructions (Contd.)**

| Instruction Mnemonic | Status Flag States | Condition Description |
|----------------------|--------------------|-----------------------|
| FCMOVBE              | CF=1 or ZF=1       | Below or equal        |
| FCMOVNBE             | CF=0 or ZF=0       | Not below nor equal   |
| FCMOVU               | PF=1               | Unordered             |
| FCMOVNU              | PF=0               | Not unordered         |

Like the CMOVcc instructions, the FCMOVcc instructions are useful for optimizing small IF constructions. They also help eliminate branching overhead for IF operations and the possibility of branch mispredictions by the processor. Software can check if the FCMOVcc instructions are supported by checking the processor's feature information with the CPUID instruction.

### 8.3.4 Load Constant Instructions

The following instructions push commonly used constants onto the top [ST(0)] of the x87 FPU register stack:

|        |                      |
|--------|----------------------|
| FLDZ   | Load +0.0.           |
| FLD1   | Load +1.0.           |
| FLDPI  | Load $\pi$ .         |
| FLDL2T | Load $\log_2 10$ .   |
| FLDL2E | Load $\log_2 e$ .    |
| FLDLG2 | Load $\log_{10} 2$ . |
| FLDLN2 | Load $\log_e 2$ .    |

The constant values have full double extended precision floating-point precision (64 bits) and are accurate to approximately 19 decimal digits. They are stored internally in a format more precise than double extended precision floating-point. When loading the constant, the x87 FPU rounds the more precise internal constant according to the RC (rounding control) field of the x87 FPU control word. The inexact-result exception (#P) is not generated as a result of this rounding, nor is the C1 flag set in the x87 FPU status word if the value is rounded up. See Section 8.3.8, "Approximation of Pi," for information on the  $\pi$  constant.

### 8.3.5 Basic Arithmetic Instructions

The following floating-point instructions perform basic arithmetic operations on floating-point numbers. Where applicable, these instructions match IEEE Standard 754:

|              |                                               |
|--------------|-----------------------------------------------|
| FADD/FADDP   | Add floating-point.                           |
| FIADD        | Add integer to floating-point.                |
| FSUB/FSUBP   | Subtract floating-point.                      |
| FISUB        | Subtract integer from floating-point.         |
| FSUBR/FSUBRP | Reverse subtract floating-point.              |
| FISUBR       | Reverse subtract floating-point from integer. |
| FMUL/FMULP   | Multiply floating-point.                      |
| FIMUL        | Multiply integer by floating-point.           |
| FDIV/FDIVP   | Divide floating-point.                        |
| FIDIV        | Divide floating-point by integer.             |
| FDIVR/FDIVRP | Reverse divide.                               |
| FIDIVR       | Reverse divide integer by floating-point.     |
| FABS         | Absolute value.                               |
| FCHS         | Change sign.                                  |

|         |                                   |
|---------|-----------------------------------|
| FSQRT   | Square root.                      |
| FPREM   | Partial remainder.                |
| FPREM1  | IEEE partial remainder.           |
| FRNDINT | Round to integral value.          |
| FXTRACT | Extract exponent and significand. |

The add, subtract, multiply, and divide instructions operate on the following types of operands:

- Two x87 FPU data registers.
- An x87 FPU data register and a floating-point or integer value in memory.

See Section 8.1.2, “x87 FPU Data Registers,” for a description of how operands are referenced on the data register stack.

Operands in memory can be in single precision floating-point, double precision floating-point, word-integer, or doubleword-integer format. They are converted to double extended precision floating-point format automatically.

Reverse versions of the subtract (FSUBR) and divide (FDIVR) instructions enable efficient coding. For example, the following options are available with the FSUB and FSUBR instructions for operating on values in a specified x87 FPU data register  $ST(i)$  and the  $ST(0)$  register:

FSUB:

$$ST(0) := ST(0) - ST(i)$$

$$ST(i) := ST(i) - ST(0)$$

FSUBR:

$$ST(0) := ST(i) - ST(0)$$

$$ST(i) := ST(0) - ST(i)$$

These instructions eliminate the need to exchange values between the  $ST(0)$  register and another x87 FPU register to perform a subtraction or division.

The pop versions of the add, subtract, multiply, and divide instructions offer the option of popping the x87 FPU register stack following the arithmetic operation. These instructions operate on values in the  $ST(i)$  and  $ST(0)$  registers, store the result in the  $ST(i)$  register, and pop the  $ST(0)$  register.

The FPREM instruction computes the remainder from the division of two operands in the manner used by the Intel 8087 and Intel 287 math coprocessors; the FPREM1 instruction computes the remainder in the manner specified in IEEE Standard 754.

The FSQRT instruction computes the square root of the source operand.

The FRNDINT instruction returns a floating-point value that is the integral value closest to the source value in the direction of the rounding mode specified in the RC field of the x87 FPU control word.

The FABS, FCHS, and FXTRACT instructions perform convenient arithmetic operations. The FABS instruction produces the absolute value of the source operand. The FCHS instruction changes the sign of the source operand. The FXTRACT instruction separates the source operand into its exponent and fraction and stores each value in a register in floating-point format.

### 8.3.6 Comparison and Classification Instructions

The following instructions compare or classify floating-point values:

|                      |                                                                        |
|----------------------|------------------------------------------------------------------------|
| FCOM/FCOMP/FCOMPP    | Compare floating-point and set x87 FPU condition code flags.           |
| FUCOM/FUCOMP/FUCOMPP | Unordered compare floating-point and set x87 FPU condition code flags. |
| FICOM/FICOMP         | Compare integer and set x87 FPU condition code flags.                  |
| FCOMI/FCOMIP         | Compare floating-point and set EFLAGS status flags.                    |
| FUCOMI/FUCOMIP       | Unordered compare floating-point and set EFLAGS status flags.          |
| FTST                 | Test (compare floating-point with 0.0).                                |

FXAM

Examine.

Comparison of floating-point values differ from comparison of integers because floating-point values have four (rather than three) mutually exclusive relationships: less than, equal, greater than, and unordered.

The unordered relationship is true when at least one of the two values being compared is a NaN or in an unsupported format. This additional relationship is required because, by definition, NaNs are not numbers, so they cannot have less than, equal, or greater than relationships with other floating-point values.

The FCOM, FCOMP, and FCOMPP instructions compare the value in register ST(0) with a floating-point source operand and set the condition code flags (C0, C2, and C3) in the x87 FPU status word according to the results (see Table 8-6).

If an unordered condition is detected (one or both of the values are NaNs or in an undefined format), a floating-point invalid-operation exception is generated.

The pop versions of the instruction pop the x87 FPU register stack once or twice after the comparison operation is complete.

The FUCOM, FUCOMP, and FUCOMPP instructions operate the same as the FCOM, FCOMP, and FCOMPP instructions. The only difference is that with the FUCOM, FUCOMP, and FUCOMPP instructions, if an unordered condition is detected because one or both of the operands are QNaNs, the floating-point invalid-operation exception is not generated.

**Table 8-6. Setting of x87 FPU Condition Code Flags for Floating-Point Number Comparisons**

| Condition              | C3 | C2 | C0 |
|------------------------|----|----|----|
| ST(0) > Source Operand | 0  | 0  | 0  |
| ST(0) < Source Operand | 0  | 0  | 1  |
| ST(0) = Source Operand | 1  | 0  | 0  |
| Unordered              | 1  | 1  | 1  |

The FICOM and FICOMP instructions also operate the same as the FCOM and FCOMP instructions, except that the source operand is an integer value in memory. The integer value is automatically converted into an double extended precision floating-point value prior to making the comparison. The FICOMP instruction pops the x87 FPU register stack following the comparison operation.

The FTST instruction performs the same operation as the FCOM instruction, except that the value in register ST(0) is always compared with the value 0.0.

The FCOMI and FCOMIP instructions were introduced into the IA-32 architecture in the P6 family processors. They perform the same comparison as the FCOM and FCOMP instructions, except that they set the status flags (ZF, PF, and CF) in the EFLAGS register to indicate the results of the comparison (see Table 8-7) instead of the x87 FPU condition code flags. The FCOMI and FCOMIP instructions allow condition branch instructions (Jcc) to be executed directly from the results of their comparison.

**Table 8-7. Setting of EFLAGS Status Flags for Floating-Point Number Comparisons**

| Comparison Results   | ZF | PF | CF |
|----------------------|----|----|----|
| ST0 > ST( <i>i</i> ) | 0  | 0  | 0  |
| ST0 < ST( <i>i</i> ) | 0  | 0  | 1  |
| ST0 = ST( <i>i</i> ) | 1  | 0  | 0  |
| Unordered            | 1  | 1  | 1  |

Software can check if the FCOMI and FCOMIP instructions are supported by checking the processor's feature information with the CPUID instruction.

The FUCOMI and FUCOMIP instructions operate the same as the FCOMI and FCOMIP instructions, except that they do not generate a floating-point invalid-operation exception if the unordered condition is the result of one or both of the operands being a QNaN. The FCOMIP and FUCOMIP instructions pop the x87 FPU register stack following the comparison operation.

The FXAM instruction determines the classification of the floating-point value in the ST(0) register (that is, whether the value is zero, a denormal number, a normal finite number,  $\infty$ , a NaN, or an unsupported format) or that the register is empty. It sets the x87 FPU condition code flags to indicate the classification (see “FXAM—Examine” in Chapter 3, “Instruction Set Reference, A-L,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 2A). It also sets the C1 flag to indicate the sign of the value.

8.3.6.1 Branching on the x87 FPU Condition Codes

The processor does not offer any control-flow instructions that branch on the setting of the condition code flags (C0, C2, and C3) in the x87 FPU status word. To branch on the state of these flags, the x87 FPU status word must first be moved to the AX register in the integer unit. The FSTSW AX (store status word) instruction can be used for this purpose. When these flags are in the AX register, the TEST instruction can be used to control conditional branching as follows:

- 1. Check for an unordered result. Use the TEST instruction to compare the contents of the AX register with the constant 0400H (see Table 8-8). This operation will clear the ZF flag in the EFLAGS register if the condition code flags indicate an unordered result; otherwise, the ZF flag will be set. The JNZ instruction can then be used to transfer control (if necessary) to a procedure for handling unordered operands.

Table 8-8. TEST Instruction Constants for Conditional Branching

| Order                  | Constant | Branch |
|------------------------|----------|--------|
| ST(0) > Source Operand | 4500H    | JZ     |
| ST(0) < Source Operand | 0100H    | JNZ    |
| ST(0) = Source Operand | 4000H    | JNZ    |
| Unordered              | 0400H    | JNZ    |

- 2. Check ordered comparison result. Use the constants given in Table 8-8 in the TEST instruction to test for a less than, equal to, or greater than result, then use the corresponding conditional branch instruction to transfer program control to the appropriate procedure or section of code.

If a program or procedure has been thoroughly tested and it incorporates periodic checks for QNaN results, then it is not necessary to check for the unordered result every time a comparison is made.

See Section 8.1.4, “Branching and Conditional Moves on Condition Codes,” for another technique for branching on x87 FPU condition codes.

Some non-comparison x87 FPU instructions update the condition code flags in the x87 FPU status word. To ensure that the status word is not altered inadvertently, store it immediately following a comparison operation.

8.3.7 Trigonometric Instructions

The following instructions perform four common trigonometric functions:

|         |                  |
|---------|------------------|
| FSIN    | Sine.            |
| FCOS    | Cosine.          |
| FSINCOS | Sine and cosine. |
| FPTAN   | Tangent.         |
| FPATAN  | Arctangent.      |

These instructions operate on the top one or two registers of the x87 FPU register stack and they return their results to the stack. The source operands for the FSIN, FCOS, FSINCOS, and FPTAN instructions must be given in radians; the source operand for the FPATAN instruction is given in rectangular coordinate units.

The FSINCOS instruction returns both the sine and the cosine of a source operand value. It operates faster than executing the FSIN and FCOS instructions in succession.

The FPATAN instruction computes the arctangent of ST(1) divided by ST(0), returning a result in radians. It is useful for converting rectangular coordinates to polar coordinates.

See Section 8.3.8, “Approximation of Pi,” and Section 8.3.10, “Transcendental Instruction Accuracy,” for information regarding the accuracy of these instructions.

### 8.3.8 Approximation of Pi

When the argument (source operand) of a trigonometric function is within the domain of the function, the argument is automatically reduced by the appropriate multiple of  $2\pi$  through the same reduction mechanism used by the FPREM and FPREM1 instructions. The internal value of  $\pi$  (3.1415926...) that the x87 FPU uses for argument reduction and other computations, denoted as Pi in the expression below. The numerical value of Pi can be written as:

$$\text{Pi} = 0.f * 2^2$$

where the fraction f is expressed in binary form as:

$$f = \text{C90FDAA2 2168C234 C}$$

(The spaces in the fraction above indicate 32-bit boundaries.)

The internal approximation Pi of the value  $\pi$  has a 66 significant bits. Since the exact value of  $\pi$  represented in binary has the next 3 bits equal to 0, it means that Pi is the value of  $\pi$  rounded to nearest-even to 68 bits, and also the value of  $\pi$  rounded toward zero (truncated) to 69 bits.

However, accuracy problems may arise because this relatively short finite approximation Pi of the number  $\pi$  is used for calculating the reduced argument of the trigonometric function approximations in the implementations of FSIN, FCOS, FSINCOS, and FPTAN. Alternately, this means that FSIN (x), FCOS (x), and FPTAN (x) are really approximating the mathematical functions  $\sin(x * \pi / \text{Pi})$ ,  $\cos(x * \pi / \text{Pi})$ , and  $\tan(x * \pi / \text{Pi})$ , and not exactly  $\sin(x)$ ,  $\cos(x)$ , and  $\tan(x)$ . (Note that FSINCOS is the equivalent of FSIN and FCOS combined together). The period of  $\sin(x * \pi / \text{Pi})$  for example is  $2 * \text{Pi}$ , and not  $2\pi$ .

See also Section 8.3.10, “Transcendental Instruction Accuracy,” for more information on the accuracy of these functions.

### 8.3.9 Logarithmic, Exponential, and Scale

The following instructions provide two different logarithmic functions, an exponential function and a scale function:

|         |                    |
|---------|--------------------|
| FYL2X   | Logarithm.         |
| FYL2XP1 | Logarithm epsilon. |
| F2XM1   | Exponential.       |
| FSCALE  | Scale.             |

The FYL2X and FYL2XP1 instructions perform two different base 2 logarithmic operations. The FYL2X instruction computes  $(y * \log_2 x)$ . This operation permits the calculation of the log of any base using the following equation:

$$\log_b x = (1 / \log_2 b) * \log_2 x$$

The FYL2XP1 instruction computes  $(y * \log_2(x + 1))$ . This operation provides optimum accuracy for values of x that are close to 0.

The F2XM1 instruction computes  $(2^x - 1)$ . This instruction only operates on source values in the range  $-1.0$  to  $+1.0$ .

The FSCALE instruction multiplies the source operand by a power of 2.

### 8.3.10 Transcendental Instruction Accuracy

New transcendental instruction algorithms were incorporated into the IA-32 architecture beginning with the Pentium processors. These new algorithms (used in transcendental instructions FSIN, FCOS, FSINCOS, FPTAN, FPATAN, F2XM1, FYL2X, and FYL2XP1) allow a higher level of accuracy than was possible in earlier IA-32 proces-

sors and x87 math coprocessors. The accuracy of these instructions is measured in terms of **units in the last place (ulp)**. For a given argument  $x$ , let  $f(x)$  and  $F(x)$  be the correct and computed (approximate) function values, respectively. The error in ulps is defined to be:

$$error = \left| \frac{f(x) - F(x)}{2^{k-63}} \right|$$

where  $k$  is an integer such that:

$$1 \leq 2^{-k} f(x) < 2.$$

With the Pentium processor and later IA-32 processors, the worst case error on transcendental functions is less than 1 ulp when rounding to the nearest (even) and less than 1.5 ulps when rounding in other modes. The functions are guaranteed to be monotonic, with respect to the input operands, throughout the domain supported by the instruction.

However, for FSIN, FCOS, FSINCOS, and FPTAN which approximate periodic trigonometric functions, the previous statement about maximum ulp errors is true only when these instructions are applied to reduced argument (see Section 8.3.8, "Approximation of  $\pi$ "). This is due to the fact that only 66 significant bits are retained in the finite approximation  $\pi$  of the number  $\pi$  (3.1415926...), used internally for calculating the reduced argument in FSIN, FCOS, FSINCOS, and FPTAN. This approximation of  $\pi$  is not always sufficiently accurate for good argument reduction.

For single precision, the argument of FSIN, FCOS, FSINCOS, and FPTAN must exceed 200,000 radians in order for the error of the result to exceed 1 ulp when rounding to the nearest (even), or 1.5 ulps when rounding in other (directed) rounding modes.

For double and double-extended precision, the ulp errors will grow above these thresholds for arguments much smaller in magnitude. The ulp errors increase significantly when the argument approaches the value of  $\pi$  (or  $\pi$ ) for FSIN, and when it approaches  $\pi/2$  (or  $\pi/2$ ) for FCOS, FSINCOS, and FPTAN.

For all three IEEE precisions supported (32-bit single precision, 64-bit double precision, and 80-bit double-extended precision), applying FSIN, FCOS, FSINCOS, or FPTAN to arguments larger than a certain value can lead to reduced arguments (calculated internally) that are inaccurate or even very inaccurate in some cases. This leads to equally inaccurate approximations of the corresponding mathematical functions. In particular, arguments that are close to certain values will lose significance when reduced, leading to increased relative (and ulp) errors in the results of FSIN, FCOS, FSINCOS, and FPTAN. These values are:

- Any non-zero multiple of  $\pi$  for FSIN.
- Any multiple of  $\pi$ , plus  $\pi/2$  for FCOS.
- Any non-zero multiple of  $\pi/2$  for FSINCOS and FPTAN.

If the arguments passed to FSIN, FCOS, FSINCOS, and FPTAN are not close to these values then even the finite approximation  $\pi$  of  $\pi$  used internally for argument reduction will allow for results that have good accuracy.

Therefore, in order to avoid such errors it is recommended to perform accurate argument reduction in software, and to apply FSIN, FCOS, FSINCOS, and FPTAN to reduced arguments only. Regardless of the target precision (single, double, or double-extended), it is safe to reduce the argument to a value smaller in absolute value than about  $3\pi/4$  for FSIN, and smaller than about  $3\pi/8$  for FCOS, FSINCOS, and FPTAN.

The thresholds shown above are not exact. For example, accuracy measurements show that the double-extended precision result of FSIN will not have errors larger than 0.72 ulp for  $|x| < 2.82$  (so  $|x| < 3\pi/4$  will ensure good accuracy, as  $3\pi/4 < 2.82$ ). On the same interval, double precision results from FSIN will have errors at most slightly larger than 0.5 ulp, and single precision results will be correctly rounded in the vast majority of cases.

Likewise, the double-extended precision result of FCOS will not have errors larger than 0.82 ulp for  $|x| < 1.31$  (so  $|x| < 3\pi/8$  will ensure good accuracy, as  $3\pi/8 < 1.31$ ). On the same interval, double precision results from FCOS will have errors at most slightly larger than 0.5 ulp, and single precision results will be correctly rounded in the vast majority of cases.

FSINCOS behaves similarly to FSIN and FCOS, combined as a pair.

Finally, the double-extended precision result of FPTAN will not have errors larger than 0.78 ulp for  $|x| < 1.25$  (so  $|x| < 3\pi/8$  will ensure good accuracy, as  $3\pi/8 < 1.25$ ). On the same interval, double precision results from FPTAN will have errors at most slightly larger than 0.5 ulp, and single precision results will be correctly rounded in the vast majority of cases.

A recommended alternative in order to avoid the accuracy issues that might be caused by FSIN, FCOS, FSINCOS, and FPTAN, is to use good quality mathematical library implementations of the sin, cos, sincos, and tan functions, for example those from the Intel<sup>®</sup> Math Library available in the Intel<sup>®</sup> Compiler.

The instructions FYL2X and FYL2XP1 are two operand instructions and are guaranteed to be within 1 ulp only when y equals 1. When y is not equal to 1, the maximum ulp error is always within 1.35 ulps in round to nearest mode. (For the two operand functions, monotonicity was proved by holding one of the operands constant.)

### 8.3.11 x87 FPU Control Instructions

The following instructions control the state and modes of operation of the x87 FPU. They also allow the status of the x87 FPU to be examined:

|                |                                                           |
|----------------|-----------------------------------------------------------|
| FINIT/FNINIT   | Initialize x87 FPU.                                       |
| FLDCW          | Load x87 FPU control word.                                |
| FSTCW/FNSTCW   | Store x87 FPU control word.                               |
| FSTSW/FNSTSW   | Store x87 FPU status word.                                |
| FCLEX/FNCLEX   | Clear x87 FPU exception flags.                            |
| FLDENV         | Load x87 FPU environment.                                 |
| FSTENV/FNSTENV | Store x87 FPU environment.                                |
| FRSTOR         | Restore x87 FPU state.                                    |
| FSAVE/FNSAVE   | Save x87 FPU state.                                       |
| FINCSTP        | Increment x87 FPU register stack pointer.                 |
| FDECSTP        | Decrement x87 FPU register stack pointer.                 |
| FFREE          | Free x87 FPU register.                                    |
| FNOP           | No operation.                                             |
| WAIT/FWAIT     | Check for and handle pending unmasked x87 FPU exceptions. |

The FINIT/FNINIT instructions initialize the x87 FPU and its internal registers to default values.

The FLDCW instructions loads the x87 FPU control word register with a value from memory. The FSTCW/FNSTCW and FSTSW/FNSTSW instructions store the x87 FPU control and status words, respectively, in memory (or for an FSTSW/FNSTSW instruction in a general-purpose register).

The FSTENV/FNSTENV and FSAVE/FNSAVE instructions save the x87 FPU environment and state, respectively, in memory. The x87 FPU environment includes all the x87 FPU's control and status registers; the x87 FPU state includes the x87 FPU environment and the data registers in the x87 FPU register stack. (The FSAVE/FNSAVE instruction also initializes the x87 FPU to default values, like the FINIT/FNINIT instruction, after it saves the original state of the x87 FPU.)

The FLDENV and FRSTOR instructions load the x87 FPU environment and state, respectively, from memory into the x87 FPU. These instructions are commonly used when switching tasks or contexts.

The WAIT/FWAIT instructions are synchronization instructions. (They are actually mnemonics for the same opcode.) These instructions check the x87 FPU status word for pending unmasked x87 FPU exceptions. If any pending unmasked x87 FPU exceptions are found, they are handled before the processor resumes execution of the instructions (integer, floating-point, or system instruction) in the instruction stream. The WAIT/FWAIT instructions are provided to allow synchronization of instruction execution between the x87 FPU and the processor's integer unit. See Section 8.6, "x87 FPU Exception Synchronization," for more information on the use of the WAIT/FWAIT instructions.

### 8.3.12 Waiting vs. Non-waiting Instructions

All of the x87 FPU instructions except a few special control instructions perform a wait operation (similar to the WAIT/FWAIT instructions), to check for and handle pending unmasked x87 FPU floating-point exceptions, before they perform their primary operation (such as adding two floating-point numbers). These instructions are called **waiting** instructions. Some of the x87 FPU control instructions, such as FSTSW/FNSTSW, have both a waiting and a non-waiting version. The waiting version (with the "F" prefix) executes a wait operation before it performs its primary operation; whereas, the non-waiting version (with the "FN" prefix) ignores pending unmasked exceptions.

Non-waiting instructions allow software to save the current x87 FPU state without first handling pending exceptions or to reset or reinitialize the x87 FPU without regard for pending exceptions.

#### NOTES

When operating a Pentium or Intel486 processor in MS-DOS compatibility mode, it is possible (under unusual circumstances) for a non-waiting instruction to be interrupted prior to being executed to handle a pending x87 FPU exception.

When operating a P6 family, Pentium 4, or Intel Xeon processor in MS-DOS compatibility mode, non-waiting instructions cannot be interrupted in this way.

### 8.3.13 Unsupported x87 FPU Instructions

The Intel 8087 instructions FENI and FDISI and the Intel 287 math coprocessor instruction FSETPM perform no function in the Intel 387 math coprocessor and later IA-32 processors. If these opcodes are detected in the instruction stream, the x87 FPU performs no specific operation and no internal x87 FPU states are affected.

## 8.4 X87 FPU FLOATING-POINT EXCEPTION HANDLING

The x87 FPU detects the six classes of exception conditions described in Section 4.9, "Overview of Floating-Point Exceptions":

- Invalid operation (#I), with two subclasses:
  - Stack overflow or underflow (#IS).
  - Invalid arithmetic operation (#IA).
- Denormalized operand (#D).
- Divide-by-zero (#Z).
- Numeric overflow (#O).
- Numeric underflow (#U).
- Inexact result (precision) (#P).

Each of the six exception classes has a corresponding flag bit in the x87 FPU status word and a mask bit in the x87 FPU control word (see Section 8.1.3, "x87 FPU Status Register," and Section 8.1.5, "x87 FPU Control Word," respectively). In addition, the exception summary (ES) flag in the status word indicates when one or more unmasked exceptions has been detected. The stack fault (SF) flag (also in the status word) distinguishes between the two types of invalid-operation exceptions.

The mask bits can be set with FLDCW, FRSTOR, or FXRSTOR; they can be read with either FSTCW/FNSTCW, FSAVE/FNSAVE, or FXSAVE. The flag bits can be read with the FSTSW/FNSTSW, FSAVE/FNSAVE, or FXSAVE instruction.

#### NOTE

Section 4.9.1, "Floating-Point Exception Conditions," provides a general overview of how the IA-32 processor detects and handles the various classes of floating-point exceptions. This information pertains to the x87 FPU as well as the Intel SSE, SSE2, and SSE3 instructions.

The following sections give specific information about how the x87 FPU handles floating-point exceptions that are unique to the x87 FPU.

### 8.4.1 Arithmetic vs. Non-arithmetic Instructions

When dealing with floating-point exceptions, it is useful to distinguish between **arithmetic instructions** and **non-arithmetic instructions**. Non-arithmetic instructions have no operands or do not make substantial changes to their operands. Arithmetic instructions do make significant changes to their operands; in particular, they make changes that could result in floating-point exceptions being signaled. Table 8-9 lists the non-arithmetic and arithmetic instructions. It should be noted that some non-arithmetic instructions can signal a floating-point stack (fault) exception, but this exception is not the result of an operation on an operand.

**Table 8-9. Arithmetic and Non-arithmetic Instructions**

| Non-arithmetic Instructions       | Arithmetic Instructions      |
|-----------------------------------|------------------------------|
| FABS                              | F2XM1                        |
| FCHS                              | FADD/FADDP                   |
| FCLEX                             | FBLD                         |
| FDECSTP                           | FBSTP                        |
| FFREE                             | FCOM/FCOMP/FCOMPP            |
| FINCSTP                           | FCOS                         |
| FINIT/FNINIT                      | FDIV/FDIVP/FDIVR/FDIVRP      |
| FLD (register-to-register)        | FIADD                        |
| FLD (extended format from memory) | FICOM/FICOMP                 |
| FLD constant                      | FIDIV/FIDIVR                 |
| FLDCW                             | FILD                         |
| FLDENV                            | FIMUL                        |
| FNOP                              | FIST/FISTP <sup>1</sup>      |
| FRSTOR                            | FISUB/FISUBR                 |
| FSAVE/FNSAVE                      | FLD (single and double)      |
| FST/FSTP (register-to-register)   | FMUL/FMULP                   |
| FSTP (extended format to memory)  | FPATAN                       |
| FSTCW/FNSTCW                      | FPREM/FPREM1                 |
| FSTENV/FNSTENV                    | FPTAN                        |
| FSTSW/FNSTSW                      | FRNDINT                      |
| WAIT/FWAIT                        | FSCALE                       |
| FXAM                              | FSIN                         |
| FXCH                              | FSINCOS                      |
|                                   | FSQRT                        |
|                                   | FST/FSTP (single and double) |
|                                   | FSUB/FSUBP/FSUBR/FSUBRP      |
|                                   | FTST                         |
|                                   | FUCOM/FUCOMP/FUCOMPP         |
|                                   | FXTRACT                      |
|                                   | FYL2X/FYL2XP1                |

Table 8-9. Arithmetic and Non-arithmetic Instructions (Contd.)

| Non-arithmetic Instructions                                                             | Arithmetic Instructions |
|-----------------------------------------------------------------------------------------|-------------------------|
| <b>NOTE:</b><br>1. The FISTTP instruction in SSE3 is an arithmetic x87 FPU instruction. |                         |

8.5 X87 FPU FLOATING-POINT EXCEPTION CONDITIONS

The following sections describe the various conditions that cause a floating-point exception to be generated by the x87 FPU and the masked response of the x87 FPU when these conditions are detected. The Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volumes 2A, 2B, 2C, & 2D, lists the floating-point exceptions that can be signaled for each floating-point instruction.

See Section 4.9.2, “Floating-Point Exception Priority,” for a description of the rules for exception precedence when more than one floating-point exception condition is detected for an instruction.

8.5.1 Invalid Operation Exception

The floating-point invalid-operation exception occurs in response to two sub-classes of operations:

- Stack overflow or underflow (#IS).
- Invalid arithmetic operand (#IA).

The flag for this exception (IE) is bit 0 of the x87 FPU status word, and the mask bit (IM) is bit 0 of the x87 FPU control word. The stack fault flag (SF) of the x87 FPU status word indicates the type of operation that caused the exception. When the SF flag is set to 1, a stack operation has resulted in stack overflow or underflow; when the flag is cleared to 0, an arithmetic instruction has encountered an invalid operand. Note that the x87 FPU explicitly sets the SF flag when it detects a stack overflow or underflow condition, but it does not explicitly clear the flag when it detects an invalid-arithmetic-operand condition. As a result, the state of the SF flag can be 1 following an invalid-arithmetic-operation exception, if it was not cleared from the last time a stack overflow or underflow condition occurred. See Section 8.1.3.4, “Stack Fault Flag,” for more information about the SF flag.

8.5.1.1 Stack Overflow or Underflow Exception (#IS)

The x87 FPU tag word keeps track of the contents of the registers in the x87 FPU register stack (see Section 8.1.7, “x87 FPU Tag Word”). It then uses this information to detect two different types of stack faults:

- Stack overflow** — An instruction attempts to load a non-empty x87 FPU register from memory. A non-empty register is defined as a register containing a zero (tag value of 01), a valid value (tag value of 00), or a special value (tag value of 10).
- Stack underflow** — An instruction references an empty x87 FPU register as a source operand, including attempting to write the contents of an empty register to memory. An empty register has a tag value of 11.

NOTES

The term stack overflow originates from the situation where the program has loaded (pushed) eight values from memory onto the x87 FPU register stack and the next value pushed on the stack causes a stack wraparound to a register that already contains a value.

The term stack underflow originates from the opposite situation. Here, a program has stored (popped) eight values from the x87 FPU register stack to memory and the next value popped from the stack causes stack wraparound to an empty register.

When the x87 FPU detects stack overflow or underflow, it sets the IE flag (bit 0) and the SF flag (bit 6) in the x87 FPU status word to 1. It then sets condition-code flag C1 (bit 9) in the x87 FPU status word to 1 if stack overflow occurred or to 0 if stack underflow occurred.

If the invalid-operation exception is masked, the x87 FPU returns the floating-point, integer, or packed decimal integer indefinite value to the destination operand, depending on the instruction being executed. This value overwrites the destination register or memory location specified by the instruction.

If the invalid-operation exception is not masked, a software exception handler is invoked (see Section 8.7, “Handling x87 FPU Exceptions in Software”) and the top-of-stack pointer (TOP) and source operands remain unchanged.

### 8.5.1.2 Invalid Arithmetic Operand Exception (#IA)

The x87 FPU is able to detect a variety of invalid arithmetic operations that can be coded in a program. These operations are listed in Table 8-10. (This list includes the invalid operations defined in IEEE Standard 754.)

When the x87 FPU detects an invalid arithmetic operand, it sets the IE flag (bit 0) in the x87 FPU status word to 1. If the invalid-operation exception is masked, the x87 FPU then returns an indefinite value or QNaN to the destination operand and/or sets the floating-point condition codes as shown in Table 8-10. If the invalid-operation exception is not masked, a software exception handler is invoked (see Section 8.7, “Handling x87 FPU Exceptions in Software”) and the top-of-stack pointer (TOP) and source operands remain unchanged.

**Table 8-10. Invalid Arithmetic Operations and the Masked Responses to Them**

| Condition                                                                                                                                                                | Masked Response                                                                                                                                       |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Any arithmetic operation on an operand that is in an unsupported format.                                                                                                 | Return the QNaN floating-point indefinite value to the destination operand.                                                                           |
| Any arithmetic operation on a SNaN.                                                                                                                                      | Return a QNaN to the destination operand (see Table 4-8).                                                                                             |
| Ordered compare and test operations: one or both operands are NaNs.                                                                                                      | Set the condition code flags (C0, C2, and C3) in the x87 FPU status word or the CF, PF, and ZF flags in the EFLAGS register to 111B (not comparable). |
| Addition: operands are opposite-signed infinities.<br>Subtraction: operands are like-signed infinities.                                                                  | Return the QNaN floating-point indefinite value to the destination operand.                                                                           |
| Multiplication: $\infty$ by 0; 0 by $\infty$ .                                                                                                                           | Return the QNaN floating-point indefinite value to the destination operand.                                                                           |
| Division: $\infty$ by $\infty$ ; 0 by 0.                                                                                                                                 | Return the QNaN floating-point indefinite value to the destination operand.                                                                           |
| Remainder instructions FPREM, FPREM1: modulus (divisor) is 0 or dividend is $\infty$ .                                                                                   | Return the QNaN floating-point indefinite; clear condition code flag C2 to 0.                                                                         |
| Trigonometric instructions FCOS, FPTAN, FSIN, FSINCOS: source operand is $\infty$ .                                                                                      | Return the QNaN floating-point indefinite; clear condition code flag C2 to 0.                                                                         |
| FSQRT: negative operand (except FSQRT (–0) = –0); FYL2X: negative operand (except FYL2X (–0) = – $\infty$ ); FYL2XP1: operand more negative than –1.                     | Return the QNaN floating-point indefinite value to the destination operand.                                                                           |
| FBSTP: Converted value cannot be represented in 18 decimal digits, or source value is an SNaN, QNaN, $\pm\infty$ , or in an unsupported format.                          | Store packed BCD integer indefinite value in the destination operand.                                                                                 |
| FIST/FISTP: Converted value exceeds representable integer range of the destination operand, or source value is an SNaN, QNaN, $\pm\infty$ , or in an unsupported format. | Store integer indefinite value in the destination operand.                                                                                            |
| FXCH: one or both registers are tagged empty.                                                                                                                            | Load empty registers with the QNaN floating-point indefinite value, then perform the exchange.                                                        |

Normally, when one or both of the source operands is a QNaN (and neither is an SNaN or in an unsupported format), an invalid-operand exception is not generated. An exception to this rule is most of the compare instructions (such as the FCOM and FCOMI instructions) and the floating-point to integer conversion instructions

(FIST/FISTP and FBSTP). With these instructions, a QNaN source operand will generate an invalid-operand exception.

### 8.5.2 Denormal Operand Exception (#D)

The x87 FPU signals the denormal-operand exception under the following conditions:

- If an arithmetic instruction attempts to operate on a denormal operand (see Section 4.8.3.2, “Normalized and Denormalized Finite Numbers”).
- If an attempt is made to load a denormal single precision or double precision floating-point value into an x87 FPU register. (If the denormal value being loaded is a double extended precision floating-point value, the denormal-operand exception is not reported.)

The flag (DE) for this exception is bit 1 of the x87 FPU status word, and the mask bit (DM) is bit 1 of the x87 FPU control word.

When a denormal-operand exception occurs and the exception is masked, the x87 FPU sets the DE flag, then proceeds with the instruction. The denormal operand in single- or double precision floating-point format is automatically normalized when converted to the double extended precision floating-point format. Subsequent operations will benefit from the additional precision of the internal double extended precision floating-point format.

When a denormal-operand exception occurs and the exception is not masked, the DE flag is set and a software exception handler is invoked (see Section 8.7, “Handling x87 FPU Exceptions in Software”). The top-of-stack pointer (TOP) and source operands remain unchanged.

For additional information about the denormal-operation exception, see Section 4.9.1.2, “Denormal Operand Exception (#D).”

### 8.5.3 Divide-By-Zero Exception (#Z)

The x87 FPU reports a floating-point divide-by-zero exception whenever an instruction attempts to divide a finite non-zero operand by 0. The flag (ZE) for this exception is bit 2 of the x87 FPU status word, and the mask bit (ZM) is bit 2 of the x87 FPU control word. The *FDIV*, *FDIVP*, *FDIVR*, *FDIVRP*, *FIDIV*, and *FIDIVR* instructions and the other instructions that perform division internally (*FYL2X* and *FXTRACT*) can report the divide-by-zero exception.

When a divide-by-zero exception occurs and the exception is masked, the x87 FPU sets the ZE flag and returns the values shown in Table 8-11. If the divide-by-zero exception is not masked, the ZE flag is set, a software exception handler is invoked (see Section 8.7, “Handling x87 FPU Exceptions in Software”), and the top-of-stack pointer (TOP) and source operands remain unchanged.

**Table 8-11. Divide-By-Zero Conditions and the Masked Responses to Them**

| Condition                                            | Masked Response                                                                                              |
|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Divide or reverse divide operation with a 0 divisor. | Returns an $\infty$ signed with the exclusive OR of the sign of the two operands to the destination operand. |
| <i>FYL2X</i> instruction.                            | Returns an $\infty$ signed with the opposite sign of the non-zero operand to the destination operand.        |
| <i>FXTRACT</i> instruction.                          | ST(1) is set to $-\infty$ ; ST(0) is set to 0 with the same sign as the source operand.                      |

### 8.5.4 Numeric Overflow Exception (#O)

The x87 FPU reports a floating-point numeric overflow exception (#O) whenever the rounded result of an arithmetic instruction exceeds the largest allowable finite value that will fit into the floating-point format of the destination operand. (See Section 4.9.1.4, “Numeric Overflow Exception (#O),” for additional information about the numeric overflow exception.)

When using the x87 FPU, numeric overflow can occur on arithmetic operations where the result is stored in an x87 FPU data register. It can also occur on store floating-point operations (using the *FST* and *FSTP* instructions), where a within-range value in a data register is stored in memory in a single precision or double precision floating-point

format. The numeric overflow exception cannot occur when storing values in an integer or BCD integer format. Instead, the invalid-arithmetic-operand exception is signaled.

The flag (OE) for the numeric-overflow exception is bit 3 of the x87 FPU status word, and the mask bit (OM) is bit 3 of the x87 FPU control word.

When a numeric-overflow exception occurs and the exception is masked, the x87 FPU sets the OE flag and returns one of the values shown in Table 4-11. The value returned depends on the current rounding mode of the x87 FPU (see Section 8.1.5.3, "Rounding Control Field").

The action that the x87 FPU takes when numeric overflow occurs and the numeric-overflow exception is not masked, depends on whether the instruction is supposed to store the result in memory or on the register stack.

- **Destination is a memory location** — The OE flag is set and a software exception handler is invoked (see Section 8.7, "Handling x87 FPU Exceptions in Software"). The top-of-stack pointer (TOP) and source and destination operands remain unchanged. Because the data in the stack is in double extended precision format, the exception handler has the option either of re-executing the store instruction after proper adjustment of the operand or of rounding the significand on the stack to the destination's precision as the standard requires. The exception handler should ultimately store a value into the destination location in memory if the program is to continue.
- **Destination is the register stack** — The significand of the result is rounded according to current settings of the precision and rounding control bits in the x87 FPU control word and the exponent of the result is adjusted by dividing it by  $2^{24576}$ . (For instructions not affected by the precision field, the significand is rounded to double-extended precision.) The resulting value is stored in the destination operand. Condition code bit C1 in the x87 FPU status word (called in this situation the "round-up bit") is set if the significand was rounded upward and cleared if the result was rounded toward 0. After the result is stored, the OE flag is set and a software exception handler is invoked. The scaling bias value 24,576 is equal to  $3 * 2^{13}$ . Biasing the exponent by 24,576 normally translates the number as nearly as possible to the middle of the double extended precision floating-point exponent range so that, if desired, it can be used in subsequent scaled operations with less risk of causing further exceptions.

When using the FSCALE instruction, massive overflow can occur, where the result is too large to be represented, even with a bias-adjusted exponent. Here, if overflow occurs again, after the result has been biased, a properly signed  $\infty$  is stored in the destination operand.

## 8.5.5 Numeric Underflow Exception (#U)

The x87 FPU detects a potential floating-point numeric underflow condition whenever the result of an arithmetic instruction is non-zero and tiny; that is, the magnitude of the rounded result with unbounded exponent is non-zero and less than the smallest possible normalized, finite value that will fit into the floating-point format of the destination operand. See Section 4.9.1.5, "Numeric Underflow Exception (#U)," for additional information about the numeric underflow exception.

Like numeric overflow, numeric underflow can occur on arithmetic operations where the result is stored in an x87 FPU data register. It can also occur on store floating-point operations (with the FST and FSTP instructions), where a within-range value in a data register is stored in memory in the smaller single precision or double precision floating-point formats. A numeric underflow exception cannot occur when storing values in an integer or BCD integer format, because a value with magnitude less than 1 is always rounded to an integral value of 0 or 1, depending on the rounding mode in effect.

The flag (UE) for the numeric-underflow exception is bit 4 of the x87 FPU status word, and the mask bit (UM) is bit 4 of the x87 FPU control word.

When a numeric-underflow condition occurs and the exception is masked, the x87 FPU performs the operation described in Section 4.9.1.5, "Numeric Underflow Exception (#U)."

When the exception is not masked, the action of the x87 FPU depends on whether the instruction is supposed to store the result in a memory location or on the x87 FPU register stack.

- **Destination is a memory location** — (Can occur only with a store instruction.) The UE flag is set and a software exception handler is invoked; see Section 8.2, “x87 FPU Data Types.” The top-of-stack pointer (TOP) and source and destination operands remain unchanged, and no result is stored in memory. Because the data in the stack is in double extended precision format, the exception handler has the option either of re-executing the store instruction after proper adjustment of the operand or of rounding the significand on the stack to the destination's precision as the standard requires. The exception handler should ultimately store a value into the destination location in memory if the program is to continue.
- **Destination is the register stack** — The significand of the result is rounded according to current settings of the precision and rounding control bits in the x87 FPU control word and the exponent of the result is adjusted by multiplying it by  $2^{24576}$ . (For instructions not affected by the precision field, the significand is rounded to double extended precision.) The resulting value is stored in the destination operand. Condition code bit C1 in the x87 FPU status register (acting here as a “round-up bit”) is set if the significand was rounded upward and cleared if the result was rounded toward 0. After the result is stored, the UE flag is set and a software exception handler is invoked. The scaling bias value 24,576 is the same as is used for the overflow exception and has the same effect, which is to translate the result as nearly as possible to the middle of the double extended precision floating-point exponent range.

When using the FSCALE instruction, massive underflow can occur, where the magnitude of the result is too small to be represented, even with a bias-adjusted exponent. Here, if underflow occurs again after the result has been biased, a properly signed 0 is stored in the destination operand.

## 8.5.6 Inexact-Result (Precision) Exception (#P)

The inexact-result exception (also called the precision exception) occurs if the result of an operation is not exactly representable in the destination format. (See Section 4.9.1.6, “Inexact-Result (Precision) Exception (#P),” for additional information about the numeric overflow exception.) Note that the transcendental instructions (FSIN, FCOS, FSINCOS, FPTAN, FPATAN, F2XM1, FYL2X, and FYL2XP1) by nature produce inexact results.

The inexact-result exception flag (PE) is bit 5 of the x87 FPU status word, and the mask bit (PM) is bit 5 of the x87 FPU control word.

If the inexact-result exception is masked when an inexact-result condition occurs and a numeric overflow or underflow condition has not occurred, the x87 FPU handles the exception as described in Section 4.9.1.6, “Inexact-Result (Precision) Exception (#P),” with one additional action. The C1 (round-up) bit in the x87 FPU status word is set to indicate whether the inexact result was rounded up (C1 is set) or “not rounded up” (C1 is cleared). In the “not rounded up” case, the least-significant bits of the inexact result are truncated so that the result fits in the destination format.

If the inexact-result exception is not masked when an inexact result occurs and numeric overflow or underflow has not occurred, the x87 FPU handles the exception as described in the previous paragraph and, in addition, invokes a software exception handler.

If an inexact result occurs in conjunction with numeric overflow or underflow, the x87 FPU carries out one of the following operations:

- If an inexact result occurs in conjunction with masked overflow or underflow, the OE or UE flag and the PE flag are set and the result is stored as described for the overflow or underflow exceptions (see Section 8.5.4, “Numeric Overflow Exception (#O),” or Section 8.5.5, “Numeric Underflow Exception (#U)”). If the inexact result exception is unmasked, the x87 FPU also invokes a software exception handler.
- If an inexact result occurs in conjunction with unmasked overflow or underflow and the destination operand is a register, the OE or UE flag and the PE flag are set, the result is stored as described for the overflow or underflow exceptions (see Section 8.5.4, “Numeric Overflow Exception (#O),” or Section 8.5.5, “Numeric Underflow Exception (#U)”) and a software exception handler is invoked.

If an unmasked numeric overflow or underflow exception occurs and the destination operand is a memory location (which can happen only for a floating-point store), the inexact-result condition is not reported and the C1 flag is cleared.

## 8.6 X87 FPU EXCEPTION SYNCHRONIZATION

Because the integer unit and x87 FPU are separate execution units, it is possible for the processor to execute floating-point, integer, and system instructions concurrently. No special programming techniques are required to gain the advantages of concurrent execution. (Floating-point instructions are placed in the instruction stream along with the integer and system instructions.) However, concurrent execution can cause problems for floating-point exception handlers.

This problem is related to the way the x87 FPU signals the existence of unmasked floating-point exceptions. (Special exception synchronization is not required for masked floating-point exceptions, because the x87 FPU always returns a masked result to the destination operand.)

When a floating-point exception is unmasked and the exception condition occurs, the x87 FPU stops further execution of the floating-point instruction and signals the exception event. On the next occurrence of a floating-point instruction or a WAIT/FWAIT instruction in the instruction stream, the processor checks the ES flag in the x87 FPU status word for pending floating-point exceptions. If floating-point exceptions are pending, the x87 FPU makes an implicit call (traps) to the floating-point software exception handler. The exception handler can then execute recovery procedures for selected or all floating-point exceptions.

Synchronization problems occur in the time between the moment when the exception is signaled and when it is actually handled. Because of concurrent execution, integer or system instructions can be executed during this time. It is thus possible for the source or destination operands for a floating-point instruction that faulted to be overwritten in memory, making it impossible for the exception handler to analyze or recover from the exception.

To solve this problem, an exception synchronizing instruction (either a floating-point instruction or a WAIT/FWAIT instruction) can be placed immediately after any floating-point instruction that might present a situation where state information pertaining to a floating-point exception might be lost or corrupted. Floating-point instructions that store data in memory are prime candidates for synchronization. For example, the following three lines of code have the potential for exception synchronization problems:

```
FILD COUNT      ;Floating-point instruction
INC COUNT       ;Integer instruction
FSQRT           ;Subsequent floating-point instruction
```

In this example, the INC instruction modifies the source operand of the floating-point instruction, FILD. If an exception is signaled during the execution of the FILD instruction, the INC instruction would be allowed to overwrite the value stored in the COUNT memory location before the floating-point exception handler is called. With the COUNT variable modified, the floating-point exception handler would not be able to recover from the error.

Rearranging the instructions, as follows, so that the FSQRT instruction follows the FILD instruction, synchronizes floating-point exception handling and eliminates the possibility of the COUNT variable being overwritten before the floating-point exception handler is invoked.

```
FILD COUNT      ;Floating-point instruction
FSQRT           ;Subsequent floating-point instruction synchronizes
                ;any exceptions generated by the FILD instruction.
INC COUNT       ;Integer instruction
```

The FSQRT instruction does not require any synchronization, because the results of this instruction are stored in the x87 FPU data registers and will remain there, undisturbed, until the next floating-point or WAIT/FWAIT instruction is executed. To absolutely ensure that any exceptions emanating from the FSQRT instruction are handled (for example, prior to a procedure call), a WAIT instruction can be placed directly after the FSQRT instruction.

Note that some floating-point instructions (non-waiting instructions) do not check for pending unmasked exceptions (see Section 8.3.11, “x87 FPU Control Instructions”). They include the FNINIT, FNSTENV, FNSAVE, FNSTSW, FNSTCW, and FNCLEX instructions. When an FNINIT, FNSTENV, FNSAVE, or FNCLEX instruction is executed, all pending exceptions are essentially lost (either the x87 FPU status register is cleared or all exceptions are masked). The FNSTSW and FNSTCW instructions do not check for pending interrupts, but they do not modify the x87 FPU status and control registers. A subsequent “waiting” floating-point instruction can then handle any pending exceptions.

## 8.7 HANDLING X87 FPU EXCEPTIONS IN SOFTWARE

The x87 FPU in Pentium and later IA-32 processors provides two different modes of operation for invoking a software exception handler for floating-point exceptions: native mode and MS-DOS compatibility mode. The mode of operation is selected by CR0.NE[bit 5]. See Chapter 2, “System Architecture Overview,” in the Intel<sup>®</sup> 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A, for more information about the NE flag.

### 8.7.1 Native Mode

The native mode for handling floating-point exceptions is selected by setting CR0.NE[bit 5] to 1. In this mode, if the x87 FPU detects an exception condition while executing a floating-point instruction and the exception is unmasked (the mask bit for the exception is cleared), the x87 FPU sets the flag for the exception and the ES flag in the x87 FPU status word. It then invokes the software exception handler through the floating-point-error exception (#MF, exception vector 16), immediately before execution of any of the following instructions in the processor’s instruction stream:

- The next floating-point instruction, unless it is one of the non-waiting instructions (FNINIT, FNCLEX, FNSTSW, FNSTCW, FNSTENV, and FNSAVE).
- The next WAIT/FWAIT instruction.
- The next MMX instruction.

If the next floating-point instruction in the instruction stream is a non-waiting instruction, the x87 FPU executes the instruction without invoking the software exception handler.

### 8.7.2 MS-DOS\* Compatibility Sub-mode

If CR0.NE[bit 5] is 0, the MS-DOS compatibility mode for handling floating-point exceptions is selected. In this mode, the software exception handler for floating-point exceptions is invoked externally using the processor’s FERR#, INTR, and IGNNE# pins. This method of reporting floating-point errors and invoking an exception handler is provided to support the floating-point exception handling mechanism used in PC systems that are running the MS-DOS or Windows\* 95 operating system.

Using FERR# and IGNNE# to handle floating-point exception is deprecated by modern operating systems, this approach also limits newer processors to operate with one logical processor active.

The MS-DOS compatibility mode is typically used as follows to invoke the floating-point exception handler:

1. If the x87 FPU detects an unmasked floating-point exception, it sets the flag for the exception and the ES flag in the x87 FPU status word.
2. If the IGNNE# pin is deasserted, the x87 FPU then asserts the FERR# pin either immediately, or else delayed (deferred) until just before the execution of the next waiting floating-point instruction or MMX instruction. Whether the FERR# pin is asserted immediately or delayed depends on the type of processor, the instruction, and the type of exception.
3. If a preceding floating-point instruction has set the exception flag for an unmasked x87 FPU exception, the processor freezes just before executing the **next** WAIT instruction, waiting floating-point instruction, or MMX instruction. Whether the FERR# pin was asserted at the preceding floating-point instruction or is just now being asserted, the freezing of the processor assures that the x87 FPU exception handler will be invoked before the new floating-point (or MMX) instruction gets executed.
4. The FERR# pin is connected through external hardware to IRQ13 of a cascaded, programmable interrupt controller (PIC). When the FERR# pin is asserted, the PIC is programmed to generate an interrupt 75H.
5. The PIC asserts the INTR pin on the processor to signal the interrupt 75H.
6. The BIOS for the PC system handles the interrupt 75H by branching to the interrupt 02H (NMI) interrupt handler.
7. The interrupt 02H handler determines if the interrupt is the result of an NMI interrupt or a floating-point exception.

8. If a floating-point exception is detected, the interrupt 02H handler branches to the floating-point exception handler.

If the IGNNE# pin is asserted, the processor ignores floating-point error conditions. This pin is provided to inhibit floating-point exceptions from being generated while the floating-point exception handler is servicing a previously signaled floating-point exception.

Appendix D, "Guidelines for Writing SIMD Floating-Point Exception Handlers," describes the MS-DOS compatibility mode in much greater detail. This mode is somewhat more complicated in the Intel486 and Pentium processor implementations, as described in Appendix D.

### 8.7.3 Handling x87 FPU Exceptions in Software

Section 4.9.3, "Typical Actions of a Floating-Point Exception Handler," shows actions that may be carried out by a floating-point exception handler. The state of the x87 FPU can be saved with the FSTENV/FNSTENV or FSAVE/FNSAVE instructions; see Section 8.1.10, "Saving the x87 FPU State with FSTENV/FNSTENV and FSAVE/FNSAVE."

If the faulting floating-point instruction is followed by one or more non-floating-point instructions, it may not be useful to re-execute the faulting instruction. See Section 8.6, "x87 FPU Exception Synchronization," for more information on synchronizing floating-point exceptions.

In cases where the handler needs to restart program execution with the faulting instruction, the IRET instruction cannot be used directly. The reason for this is that because the exception is not generated until the next floating-point or WAIT/FWAIT instruction following the faulting floating-point instruction, the return instruction pointer on the stack may not point to the faulting instruction. To restart program execution at the faulting instruction, the exception handler must obtain a pointer to the instruction from the saved x87 FPU state information, load it into the return instruction pointer location on the stack, and then execute the IRET instruction.



The Intel MMX technology was introduced into the IA-32 architecture in the Pentium II processor family and Pentium processor with MMX technology. The extensions introduced in MMX technology support a single-instruction, multiple-data (SIMD) execution model that is designed to accelerate the performance of advanced media and communications applications.

This chapter describes MMX technology.