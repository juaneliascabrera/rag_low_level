---
architecture: x86_32
component: sse3_sse4_aesni
mode: protected
tags: ['sse3', 'ssse3', 'sse4', 'aesni']
source: intel_sdm_vol1_chapter_12.md
---

# Intel SDM Volume 1 - Chapter 12

# CHAPTER 12

## PROGRAMMING WITH INTEL® SSE3, SSSE3, INTEL® SSE4, AND INTEL® AES-NI

---

This chapter describes the Intel SSE3, SSSE3, and Intel SSE4 instructions, and provides information to assist in writing application programs that use these extensions.

Intel AES-NI and PCLMLQDQ are instruction extensions targeted to accelerate high-speed block encryption and cryptographic processing. Section 12.13 covers these instructions and their relationship to the Advanced Encryption Standard (AES).

### 12.1 PROGRAMMING ENVIRONMENT AND DATA TYPES

The programming environment for using Intel SSE3, SSSE3, and Intel SSE4 is unchanged from those shown in Figure 3-1 and Figure 3-2. These extensions do not introduce new data types. XMM registers are used to operate on packed integer data, single precision floating-point data, or double precision floating-point data.

One Intel SSE3 instruction uses the x87 FPU for x87-style programming. There are two Intel SSE3 instructions that use the general registers for thread synchronization. The MXCSR register governs SIMD floating-point operations. Note, however, that the x87 FPU control word does not affect the Intel SSE3 instruction that is executed by the x87 FPU (FISTTP), other than by unmasking an invalid operand or inexact result exception.

Intel SSE4 instructions do not use MMX registers. The majority of Intel SSE4.2<sup>1</sup> and SSE4.1 instructions operate on XMM registers.

#### 12.1.1 Intel® SSE3, SSSE3, and Intel® SSE4 in 64-Bit Mode and Compatibility Mode

In compatibility mode, Intel SSE3, SSSE3, and Intel SSE4 function like they do in protected mode. In 64-bit mode, eight additional XMM registers are accessible. Registers XMM8-XMM15 are accessed by using REX prefixes.

Memory operands are specified using the ModR/M, SIB encoding described in Section 3.7.5.

Some Intel SSE3, SSSE3, and Intel SSE4 instructions may be used to operate on general-purpose registers. Use the REX.W prefix to access 64-bit general-purpose registers. Note that if a REX prefix is used when it has no meaning, the prefix is ignored.

#### 12.1.2 Compatibility of Intel® SSE3 and SSSE3 with MMX Technology, the x87 FPU Environment, and Intel® SSE and SSE2

Intel SSE3, SSSE3, and Intel SSE4 do not introduce any new state to the Intel 64 and IA-32 execution environments.

For SIMD and x87 programming, the FXSAVE and FXRSTOR instructions save and restore the architectural states of XMM, MXCSR, x87 FPU, and MMX registers. The MONITOR and MWAIT instructions use general purpose registers on input, they do not modify the content of those registers.

#### 12.1.3 Horizontal and Asymmetric Processing

Many of the Intel SSE/SSE2/SSE3 and SSSE3 instructions accelerate SIMD data processing using a model referred to as vertical computation. Using this model, data flow is vertical between the data elements of the inputs and the output.

---

1. Although the presence of CRC32 support is enumerated by CPUID.01H:ECX.SSE4\_2 = 1, CRC32 operates on general purpose registers.

Figure 12-1 illustrates the asymmetric processing of the Intel SSE3 instruction ADDSUBPD. Figure 12-2 illustrates the horizontal data movement of the Intel SSE3 instruction HADDPD.

![Figure 12-1: Asymmetric Processing in ADDSUBPD. This diagram shows a two-stage processing flow. In the first stage, two 128-bit registers, X1 and X0, are shown. X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. In the second stage, Y1 is processed by an ADD operation, and Y0 is processed by a SUB operation. The final results are X1 + Y1 and X0 - Y0.](1c827187f19ff1a7e70507f13be516d4_img.jpg)

The diagram illustrates the asymmetric processing of the ADDSUBPD instruction. It shows two 128-bit registers, X1 and X0, at the top. Arrows indicate that X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. Below Y1, an ADD operation is performed, resulting in X1 + Y1. Below Y0, a SUB operation is performed, resulting in X0 - Y0.

Figure 12-1: Asymmetric Processing in ADDSUBPD. This diagram shows a two-stage processing flow. In the first stage, two 128-bit registers, X1 and X0, are shown. X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. In the second stage, Y1 is processed by an ADD operation, and Y0 is processed by a SUB operation. The final results are X1 + Y1 and X0 - Y0.

**Figure 12-1. Asymmetric Processing in ADDSUBPD**

![Figure 12-2: Horizontal Data Movement in HADDPD. This diagram shows a two-stage processing flow. In the first stage, two 128-bit registers, X1 and X0, are shown. X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. In the second stage, Y1 is processed by an ADD operation, and Y0 is processed by an ADD operation. The final results are Y0 + Y1 and X0 + X1.](e0304e6389e07d2620a7aac6efa6c940_img.jpg)

The diagram illustrates the horizontal data movement of the HADDPD instruction. It shows two 128-bit registers, X1 and X0, at the top. Arrows indicate that X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. Below Y1, an ADD operation is performed, resulting in Y0 + Y1. Below Y0, an ADD operation is performed, resulting in X0 + X1.

Figure 12-2: Horizontal Data Movement in HADDPD. This diagram shows a two-stage processing flow. In the first stage, two 128-bit registers, X1 and X0, are shown. X1 is connected to a 128-bit register Y1, and X0 is connected to a 128-bit register Y0. In the second stage, Y1 is processed by an ADD operation, and Y0 is processed by an ADD operation. The final results are Y0 + Y1 and X0 + X1.

**Figure 12-2. Horizontal Data Movement in HADDPD**

## 12.2 OVERVIEW OF INTEL® SSE3 INSTRUCTIONS

Intel SSE3 extensions include 13 instructions. See:

- Section 12.3, “Intel® SSE3 Instructions,” provides an introduction to individual Intel SSE3 instructions.
- The Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volumes 2A, 2B, 2C, & 2D, provides detailed information on individual instructions.
- Chapter 16, “System Programming for Instruction Set Extensions and Processor Extended States,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A, gives guidelines for integrating Intel SSE/SSE2/SSE3 extensions into an operating-system environment.

## 12.3 INTEL® SSE3 INSTRUCTIONS

Intel SSE3 instructions are grouped as follows:

- x87 FPU instruction:
  - One instruction that improves x87 FPU floating-point to integer conversion.

- SIMD integer instruction:
  - One instruction that provides a specialized 128-bit unaligned data load.
- SIMD floating-point instructions:
  - Three instructions that enhance LOAD/MOVE/DUPLICATE performance.
  - Two instructions that provide packed addition/subtraction.
  - Four instructions that provide horizontal addition/subtraction.
- Thread synchronization instructions:
  - Two instructions that improve synchronization between multi-threaded agents.

The instructions are discussed in more detail in the following paragraphs.

### 12.3.1 **x87 FPU Instruction for Integer Conversion**

The **FISTTP** instruction (x87 FPU Store Integer and Pop with Truncation) behaves like FISTP, but uses truncation regardless of what rounding mode is specified in the x87 FPU control word. The instruction converts the top of stack (ST0) to integer with rounding to and pops the stack.

The **FISTTP** instruction is available in three precisions: short integer (word or 16-bit), integer (double word or 32-bit), and long integer (64-bit). With FISTTP, applications no longer need to change the FCW when truncation is required.

### 12.3.2 **SIMD Integer Instruction for Specialized 128-Bit Unaligned Data Load**

The **LDDQU** instruction is a special 128-bit unaligned load designed to avoid cache line splits. If the address of a 16-byte load is on a 16-byte boundary, LDQQU loads the bytes requested. If the address of the load is not aligned on a 16-byte boundary, LDDQU loads a 32-byte block starting at the 16-byte aligned address immediately below the load request. It then extracts the requested 16 bytes.

The instruction provides significant performance improvement on 128-bit unaligned memory accesses at the cost of some usage model restrictions.

### 12.3.3 **SIMD Floating-Point Instructions That Enhance LOAD/MOVE/DUPLICATE Performance**

The **MOVSHDUP** instruction loads/moves 128-bits, duplicating the second and fourth 32-bit data elements.

- **MOVSHDUP** OperandA, OperandB
  - OperandA (128 bits, four data elements):  $3_a, 2_a, 1_a, 0_a$
  - OperandB (128 bits, four data elements):  $3_b, 2_b, 1_b, 0_b$
  - Result (stored in OperandA):  $3_b, 3_b, 1_b, 1_b$

The **MOVSLDUP** instruction loads/moves 128-bits, duplicating the first and third 32-bit data elements.

- **MOVSLDUP** OperandA, OperandB
  - OperandA (128 bits, four data elements):  $3_a, 2_a, 1_a, 0_a$
  - OperandB (128 bits, four data elements):  $3_b, 2_b, 1_b, 0_b$
  - Result (stored in OperandA):  $2_b, 2_b, 0_b, 0_b$

The **MOVDDUP** instruction loads/moves 64-bits; duplicating the 64 bits from the source.

- **MOVDDUP** OperandA, OperandB
  - OperandA (128 bits, two data elements):  $1_a, 0_a$
  - OperandB (64 bits, one data element):  $0_b$
  - Result (stored in OperandA):  $0_b, 0_b$

### 12.3.4 SIMD Floating-Point Instructions Provide Packed Addition/Subtraction

The ADDSUBPS instruction has two 128-bit operands. The instruction performs single precision addition on the second and fourth pairs of 32-bit data elements within the operands; and single precision subtraction on the first and third pairs.

- ADDSUBPS OperandA, OperandB
  - OperandA (128 bits, four data elements):  $3_a, 2_a, 1_a, 0_a$
  - OperandB (128 bits, four data elements):  $3_b, 2_b, 1_b, 0_b$
  - Result (stored in OperandA):  $3_a+3_b, 2_a-2_b, 1_a+1_b, 0_a-0_b$

The ADDSUBPD instruction has two 128-bit operands. The instruction performs double precision addition on the second pair of quadwords, and double precision subtraction on the first pair.

- ADDSUBPD OperandA, OperandB
  - OperandA (128 bits, two data elements):  $1_a, 0_a$
  - OperandB (128 bits, two data elements):  $1_b, 0_b$
  - Result (stored in OperandA):  $1_a+1_b, 0_a-0_b$

### 12.3.5 SIMD Floating-Point Instructions Provide Horizontal Addition/Subtraction

Most SIMD instructions operate vertically. This means that the result in position  $i$  is a function of the elements in position  $i$  of both operands. Horizontal addition/subtraction operates horizontally. This means that contiguous data elements in the same source operand are used to produce a result.

The HADDPS instruction performs a single precision addition on contiguous data elements. The first data element of the result is obtained by adding the first and second elements of the first operand; the second element by adding the third and fourth elements of the first operand; the third by adding the first and second elements of the second operand; and the fourth by adding the third and fourth elements of the second operand.

- HADDPS OperandA, OperandB
  - OperandA (128 bits, four data elements):  $3_a, 2_a, 1_a, 0_a$
  - OperandB (128 bits, four data elements):  $3_b, 2_b, 1_b, 0_b$
  - Result (Stored in OperandA):  $3_b+2_b, 1_b+0_b, 3_a+2_a, 1_a+0_a$

The HSUBPS instruction performs a single precision subtraction on contiguous data elements. The first data element of the result is obtained by subtracting the second element of the first operand from the first element of the first operand; the second element by subtracting the fourth element of the first operand from the third element of the first operand; the third by subtracting the second element of the second operand from the first element of the second operand; and the fourth by subtracting the fourth element of the second operand from the third element of the second operand.

- HSUBPS OperandA, OperandB
  - OperandA (128 bits, four data elements):  $3_a, 2_a, 1_a, 0_a$
  - OperandB (128 bits, four data elements):  $3_b, 2_b, 1_b, 0_b$
  - Result (Stored in OperandA):  $2_b-3_b, 0_b-1_b, 2_a-3_a, 0_a-1_a$

The HADDPD instruction performs a double precision addition on contiguous data elements. The first data element of the result is obtained by adding the first and second elements of the first operand; the second element by adding the first and second elements of the second operand.

- HADDPD OperandA, OperandB
  - OperandA (128 bits, two data elements):  $1_a, 0_a$
  - OperandB (128 bits, two data elements):  $1_b, 0_b$
  - Result (Stored in OperandA):  $1_b+0_b, 1_a+0_a$

The HSUBPD instruction performs a double precision subtraction on contiguous data elements. The first data element of the result is obtained by subtracting the second element of the first operand from the first element of the first operand; the second element by subtracting the second element of the second operand from the first element of the second operand.

- HSUBPD OperandA OperandB
  - OperandA (128 bits, two data elements):  $1_a, 0_a$
  - OperandB (128 bits, two data elements):  $1_b, 0_b$
  - Result (Stored in OperandA):  $0_b-1_b, 0_a-1_a$

### 12.3.6 Two Thread Synchronization Instructions

The MONITOR instruction sets up an address range that is used to monitor write-back-stores.

MWAIT enables a logical processor to enter into an optimized state while waiting for a write-back-store to the address range set up by MONITOR. MONITOR and MWAIT require the use of general purpose registers for its input. The registers used by MONITOR and MWAIT must be initialized properly; register content is not modified by these instructions.

## 12.4 WRITING APPLICATIONS WITH INTEL® SSE3

The following sections give guidelines for writing application programs and operating-system code that use Intel SSE3 instructions.

### 12.4.1 Guidelines for Using Intel® SSE3

The following guidelines describe how to maximize the benefits of using Intel SSE3:

- Check that the processor supports Intel SSE3.
  - Applications may need to ensure that the target operating system supports Intel SSE3. (Operating system support for the Intel SSE implies sufficient support for Intel SSE2 and SSE3.)
- Ensure your operating system supports MONITOR and MWAIT.
- Employ the optimization and scheduling techniques described in the Intel® 64 and IA-32 Architectures Optimization Reference Manual (see Section 1.4, “Related Literature”).

### 12.4.2 Checking for Intel® SSE3 Support

Before an application attempts to use the SIMD subset of Intel SSE3 instructions, the application should follow the steps illustrated in Section 11.6.2, “Checking for Intel® SSE and SSE2 Support.” Next, use the additional step provided below:

- Check that the processor supports the SIMD and x87 Intel SSE3 extensions (if CPUID.01H:ECX.SSE3[0] = 1).

An operating system that provides application support for Intel SSE and SSE2 also provides sufficient application support for Intel SSE3. To use FISTTP, software only needs to check support for Intel SSE3.

In the initial implementation of MONITOR and MWAIT, these two instructions are available to ring 0 and conditionally available at ring level greater than 0. Before an application attempts to use the MONITOR and MWAIT instructions, the application should use the following steps:

1. Check that the processor supports MONITOR and MWAIT. If CPUID.01H:ECX.MONITOR[3] = 1, MONITOR and MWAIT are available at ring 0.
2. Query the smallest and largest line size that MONITOR uses. Use CPUID.05H:EAX.SMALLEST[15:0];EBX.LARGEST[15:0]. Values are returned in bytes in EAX and EBX.
3. Ensure the memory address range(s) that will be supplied to MONITOR meets memory type requirements.

MONITOR and MWAIT are targeted for system software that supports efficient thread synchronization, see Chapter 16 in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A for details.

### 12.4.3 Enable FTZ and DAZ for SIMD Floating-Point Computation

Enabling the FTZ and DAZ flags in the MXCSR register is likely to accelerate SIMD floating-point computation where strict compliance to the IEEE standard 754-1985 is not required. The FTZ flag is available to Intel 64 and IA-32 processors that support Intel SSE; DAZ is available to Intel 64 processors and to most IA-32 processors that support Intel SSE, SSE2, and SSE3.

Software can detect the presence of DAZ, modify the MXCSR register, and save and restore state information by following the techniques discussed in Section 11.6.3 through Section 11.6.6.

### 12.4.4 Programming Intel® SSE3 with Intel® SSE and SSE2

SIMD instructions in Intel SSE3 are intended to complement the use of Intel SSE and SSE2 in programming SIMD applications. Application software that intends to use Intel SSE3 instructions should also check for the availability of Intel SSE and SSE2 instructions.

The FISTTP instruction in Intel SSE3 is intended to accelerate x87 style programming where performance is limited by frequent floating-point conversion to integers; this happens when the x87 FPU control word is modified frequently. Use of the FISTTP instruction can eliminate the need to access the x87 FPU control word.

## 12.5 OVERVIEW OF SSSE3 INSTRUCTIONS

SSSE3 provides 32 instructions to accelerate a variety of multimedia and signal processing applications employing SIMD integer data. See:

- Section 12.6, "SSSE3 Instructions," provides an introduction to individual SSSE3 instructions.
- The Intel® 64 and IA-32 Architectures Software Developer's Manual, Volumes 2A, 2B, 2C, & 2D, provides detailed information on individual instructions.
- Chapter 16, "System Programming for Instruction Set Extensions and Processor Extended States," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, gives guidelines for integrating SSSE3 and Intel SSE, SSE2, and SSE3 into an operating-system environment.

## 12.6 SSSE3 INSTRUCTIONS

SSSE3 instructions include:

- Twelve instructions that perform horizontal addition or subtraction operations.
- Six instructions that evaluate the absolute values.
- Two instructions that perform multiply and add operations and speed up the evaluation of dot products.
- Two instructions that accelerate packed-integer multiply operations and produce integer values with scaling.
- Two instructions that perform a byte-wise, in-place shuffle according to the second shuffle control operand.
- Six instructions that negate packed integers in the destination operand if the signs of the corresponding element in the source operand is less than zero.
- Two instructions that align data from the composite of two operands.

The operands of these instructions are packed integers of byte, word, or double word sizes. The operands are stored as 64 or 128 bit data in MMX registers, XMM registers, or memory.

The instructions are discussed in more detail in the following paragraphs.

## 12.6.1 Horizontal Addition/Subtraction

In analogy to the packed, floating-point horizontal add and subtract instructions in Intel SSE3, SSSE3 offers similar capabilities on packed integer data. Data elements of signed words, doublewords are supported. Saturated version for horizontal add and subtract on signed words are also supported. The horizontal data movement of PHADD is shown in Figure 12-3.

![Figure 12-3: Horizontal Data Movement in PHADD. The diagram illustrates the data flow for the PHADD instruction. It shows two 128-bit source registers, X and Y, each divided into four 32-bit elements (X3, X2, X1, X0 and Y3, Y2, Y1, Y0). These are connected to four 32-bit adders (ADD). The adders perform horizontal additions: Y2 + Y3, Y0 + Y1, X2 + X3, and X0 + X1. The results are then packed into a 128-bit destination register, which is also divided into four 32-bit elements.](81e0bc85cbb6bdb4779d4af6d86e80cd_img.jpg)

Figure 12-3: Horizontal Data Movement in PHADD. The diagram illustrates the data flow for the PHADD instruction. It shows two 128-bit source registers, X and Y, each divided into four 32-bit elements (X3, X2, X1, X0 and Y3, Y2, Y1, Y0). These are connected to four 32-bit adders (ADD). The adders perform horizontal additions: Y2 + Y3, Y0 + Y1, X2 + X3, and X0 + X1. The results are then packed into a 128-bit destination register, which is also divided into four 32-bit elements.

**Figure 12-3. Horizontal Data Movement in PHADD**

There are six horizontal add instructions (represented by three mnemonics); three operate on 128-bit operands and three operate on 64-bit operands. The width of each data element is either 16 bits or 32 bits. The mnemonics are listed below.

- PHADDW adds two adjacent, signed 16-bit integers horizontally from the source and destination operands and packs the signed 16-bit results to the destination operand.
- PHADDSW adds two adjacent, signed 16-bit integers horizontally from the source and destination operands and packs the signed, saturated 16-bit results to the destination operand.
- PHADDQ adds two adjacent, signed 32-bit integers horizontally from the source and destination operands and packs the signed 32-bit results to the destination operand.

There are six horizontal subtract instructions (represented by three mnemonics); three operate on 128-bit operands and three operate on 64-bit operands. The width of each data element is either 16 bits or 32 bits. These are listed below.

- PHSUBW performs horizontal subtraction on each adjacent pair of 16-bit signed integers by subtracting the most significant word from the least significant word of each pair in the source and destination operands. The signed 16-bit results are packed and written to the destination operand.
- PHSUBSW performs horizontal subtraction on each adjacent pair of 16-bit signed integers by subtracting the most significant word from the least significant word of each pair in the source and destination operands. The signed, saturated 16-bit results are packed and written to the destination operand.
- PHSUBQ performs horizontal subtraction on each adjacent pair of 32-bit signed integers by subtracting the most significant doubleword from the least significant double word of each pair in the source and destination operands. The signed 32-bit results are packed and written to the destination operand.

## 12.6.2 Packed Absolute Values

There are six packed-absolute-value instructions (represented by three mnemonics). Three operate on 128-bit operands and three operate on 64-bit operands. The widths of data elements are 8 bits, 16 bits or 32 bits. The absolute value of each data element of the source operand is stored as an UNSIGNED result in the destination operand.

- PABSQB computes the absolute value of each signed byte data element.

- PABSW computes the absolute value of each signed 16-bit data element.
- PABSD computes the absolute value of each signed 32-bit data element.

### 12.6.3 Multiply and Add Packed Signed and Unsigned Bytes

There are two multiply-and-add-packed-signed-unsigned-byte instructions (represented by one mnemonic). One operates on 128-bit operands and the other operates on 64-bit operands. Multiplications are performed on each vertical pair of data elements. The data elements in the source operand are signed byte values, the input data elements of the destination operand are unsigned byte values.

- PMADDUBSW multiplies each unsigned byte value with the corresponding signed byte value to produce an intermediate, 16-bit signed integer. Each adjacent pair of 16-bit signed values are added horizontally. The signed, saturated 16-bit results are packed to the destination operand.

### 12.6.4 Packed Multiply High with Round and Scale

There are two packed-multiply-high-with-round-and-scale instructions (represented by one mnemonic). One operates on 128-bit operands and the other operates on 64-bit operands.

- PMULHRWS multiplies vertically each signed 16-bit integer from the destination operand with the corresponding signed 16-bit integer of the source operand, producing intermediate, signed 32-bit integers. Each intermediate 32-bit integer is truncated to the 18 most significant bits. Rounding is always performed by adding 1 to the least significant bit of the 18-bit intermediate result. The final result is obtained by selecting the 16 bits immediately to the right of the most significant bit of each 18-bit intermediate result and packed to the destination operand.

### 12.6.5 Packed Shuffle Bytes

There are two packed-shuffle-bytes instructions (represented by one mnemonic). One operates on 128-bit operands and the other operates on 64-bit operands. The shuffle operations are performed bitwise on the destination operand using the source operand as a control mask.

- PSHUFB permutes each byte in place, according to a shuffle control mask. The least significant three or four bits of each shuffle control byte of the control mask form the shuffle index. The shuffle mask is unaffected. If the most significant bit (bit 7) of a shuffle control byte is set, the constant zero is written in the result byte.

### 12.6.6 Packed Sign

There are six packed-sign instructions (represented by three mnemonics). Three operate on 128-bit operands and three operate on 64-bit operands. The widths of each data element for these instructions are 8 bit, 16 bit or 32 bit signed integers.

- PSIGNB/W/D negates each signed integer element of the destination operand if the sign of the corresponding data element in the source operand is less than zero.

### 12.6.7 Packed Align Right

There are two packed-align-right instructions (represented by one mnemonic). One operates on 128-bit operands and the other operates on 64-bit operands. These instructions concatenate the destination and source operand into a composite, and extract the result from the composite according to an immediate constant.

- PALIGNR's source operand is appended after the destination operand forming an intermediate value of twice the width of an operand. The result is extracted from the intermediate value into the destination operand by selecting the 128-bit or 64-bit value that are right-aligned to the byte offset specified by the immediate value.

## 12.7 WRITING APPLICATIONS WITH SSSE3 EXTENSIONS

The following sections give guidelines for writing application programs and operating-system code that use SSSE3 instructions.

### 12.7.1 Guidelines for Using SSSE3

The following guidelines describe how to maximize the benefits of using SSSE3:

- Check that the processor supports SSSE3.
- Ensure that your operating system supports SSSE3 and Intel SSE, SSE2, and SSE3. (Operating system support for Intel SSE implies sufficient support for SSSE3 and Intel SSE2 and SSE3.)
- Employ the optimization and scheduling techniques described in the Intel® 64 and IA-32 Architectures Optimization Reference Manual (see Section 1.4, “Related Literature”).

### 12.7.2 Checking for SSSE3 Support

Before an application attempts to use SSSE3, the application should follow the steps illustrated in Section 11.6.2, “Checking for Intel® SSE and SSE2 Support.” Next, use the additional step provided below:

- Check that the processor supports SSSE3 (if CPUID.01H:ECX.SSSE3[9] = 1).

## 12.8 INTEL® SSE3, SSSE3, AND INTEL® SSE4 EXCEPTIONS

Intel SSE3, SSSE3, and Intel SSE4 instructions can generate the same type of memory-access and non-numeric exceptions as other Intel 64 or IA-32 instructions. Existing exception handlers generally handle these exceptions without code modification.

FISTTP can generate floating-point exceptions. Some Intel SSE3 instructions can also generate SIMD floating-point exceptions.

Intel SSE3 additions and changes are noted in the following sections. See also: Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions”.

### 12.8.1 Device Not Available (DNA) Exceptions

Intel SSE3, SSSE3, and Intel SSE4 will cause a DNA Exception (#NM) if the processor attempts to execute an Intel SSE3 instruction while CR0.TS[bit 3] = 1. If CPUID.01H:ECX.SSE3[0] = 0, execution of an Intel SSE3 instruction will cause an invalid opcode fault regardless of the state of CR0.TS[bit 3].

Similarly, an attempt to execute an SSSE3 instruction on a processor that reports CPUID.01H:ECX.SSSE3[9] = 0 will cause an invalid opcode fault regardless of the state of CR0.TS[bit 3]. An attempt to execute an Intel SSE4.1 instruction on a processor that reports CPUID.01H:ECX.SSE4\_1[19] = 0 will cause an invalid opcode fault regardless of the state of CR0.TS[bit 3].

An attempt to execute PCMPGTQ or any one of the four string processing instructions in Intel SSE4.2 on a processor that reports CPUID.01H:ECX.SSE4\_2[20] = 0 will cause an invalid opcode fault regardless of the state of CR0.TS[bit 3]. CRC32 and POPCNT do not cause #NM.

### 12.8.2 Numeric Error Flag and IGNNE#

Most Intel SSE3 instructions ignore CR0.NE[bit 5] (treats it as if it were always set) and the IGNNE# pin. With one exception, all use the exception 19 (#XM) software exception for error reporting. The exception is FISTTP; it behaves like other x87-FP instructions.

SSSE3 instructions ignore CR0.NE[bit 5] (treats it as if it were always set) and the IGNNE# pin.

SSSE3 instructions do not cause floating-point errors. Floating-point numeric errors for Intel SSE4.1 are described in Section 12.8.4. Intel SSE4.2 instructions do not cause floating-point errors.

### 12.8.3 Emulation

CR0.EM is used by some software to emulate x87 floating-point instructions. CR0.EM[bit 2] cannot be used for emulation of SSSE3 and Intel SSE, SSE2, SSE3, and SSE4. If an Intel SSE3, SSSE3, or Intel SSE4 instruction execute with CR0.EM[bit 2] set, an invalid opcode exception (INT 6) is generated instead of a device not available exception (INT 7).

### 12.8.4 IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions

The six Intel SSE4.1 instructions that perform floating-point arithmetic are:

- DPPS
- DPPD
- ROUNDPS
- ROUNDPD
- ROUNDSS
- ROUNDSD

Dot Product operations are not specified in IEEE-754. When neither FTZ nor DAZ are enabled, the dot product instructions resemble sequences of IEEE-754 multiplies and adds (with rounding at each stage), except that the treatment of input NaN's is implementation specific (there will be at least one NaN in the output). The input select fields (bits imm8[4:7]) force input elements to +0.0f prior to the first multiply and will suppress input exceptions that would otherwise have been generated.

As a convenience to the exception handler, any exceptions signaled from DPPS or DPPD leave the destination unmodified.

Round operations signal invalid and precision only.

**Table 12-1. SIMD Numeric Exceptions Signaled by SSE4.1**

|                   | DPPS | DPPD | ROUNDPS<br>ROUNDSS | ROUNDPD<br>ROUNDSD |
|-------------------|------|------|--------------------|--------------------|
| Overflow          | X    | X    |                    |                    |
| Underflow         | X    | X    |                    |                    |
| Invalid           | X    | X    | X <sup>(1)</sup>   | X <sup>(1)</sup>   |
| Inexact Precision | X    | X    | X <sup>(2)</sup>   | X <sup>(2)</sup>   |
| Denormal          | X    | X    |                    |                    |

**NOTE:**

1. Invalid is signaled only if Src = SNaN.
2. Precision is ignored (regardless of the MXCSR precision mask) if imm8[3] = '1'.

The other Intel SSE4.1 instructions with floating-point arguments (BLENDPS, BLENDPD, BLENDVPS, BLENDVPD, INSERTPS, EXTRACTPS) do not signal any SIMD numeric exceptions.

## 12.9 INTEL® SSE4 OVERVIEW

Intel SSE4 comprises two sets of extensions: Intel SSE4.1 and SSE4.2. Intel SSE4.1 is targeted to improve the performance of media, imaging, and 3D workloads. Intel SSE4.1 adds instructions that improve compiler vectoriza-

tion and significantly increase support for packed dword computation. The technology also provides a hint that can improve memory throughput when reading from uncachable WC memory type.

The 47 Intel SSE4.1 instructions include:

- Two instructions perform packed dword multiplies.
- Two instructions perform floating-point dot products with input/output selects.
- One instruction performs a load with a streaming hint.
- Six instructions simplify packed blending.
- Eight instructions expand support for packed integer MIN/MAX.
- Four instructions support floating-point round with selectable rounding mode and precision exception override.
- Seven instructions improve data insertion and extractions from XMM registers
- Twelve instructions improve packed integer format conversions (sign and zero extensions).
- One instruction improves SAD (sum absolute difference) generation for small block sizes.
- One instruction aids horizontal searching operations.
- One instruction improves masked comparisons.
- One instruction adds qword packed equality comparisons.
- One instruction adds dword packing with unsigned saturation.

The Intel SSE4.2 instructions operating on XMM registers improve performance in the following areas:

- String and text processing that can take advantage of single-instruction multiple-data programming techniques.
- A SIMD integer instruction that enhances the capability of the 128-bit integer SIMD capability in Intel SSE4.1.

## 12.10 INTEL® SSE4.1 INSTRUCTION SET

### 12.10.1 Dword Multiply Instructions

Intel SSE4.1 adds two dword multiply instructions that aid vectorization. They allow four simultaneous 32 bit by 32 bit multiplies. PMULLD returns a low 32-bits of the result and PMULDQ returns a 64-bit signed result. These represent the most common integer multiply operation. See Table 12-2.

**Table 12-2. Enhanced 32-Bit SIMD Multiply Supported by Intel® SSE4.1**

|        |             | 32-Bit Integer Operation |                 |
|--------|-------------|--------------------------|-----------------|
|        |             | Unsigned x Unsigned      | Signed x Signed |
| Result | Low 32-bit  | (not available)          | PMULLD          |
|        | High 32-bit | (not available)          | (not available) |
|        | 64-bit      | PMULUDQ*                 | PMULDQ          |

**NOTE:**

\* Available prior to Intel SSE4.1.

### 12.10.2 Floating-Point Dot Product Instructions

Intel SSE4.1 adds two instructions for double precision (for up to 2 elements; DPPD) and single precision dot products (for up to 4 elements; DPPS).

These dot-product instructions include source select and destination broadcast which generally improves the flexibility. For example, a single DPPS instruction can be used for a 2, 3, or 4 element dot product.

### 12.10.3 Streaming Load Hint Instruction

Historically, CPU read accesses of WC memory type regions have significantly lower throughput than accesses to cacheable memory.

The streaming load instruction in SSE4.1, MOVNTDQA, provides a non-temporal hint that can cause adjacent 16-byte items within an aligned 64-byte region of WC memory type (a streaming line) to be fetched and held in a small set of temporary buffers ("streaming load buffers"). Subsequent streaming loads to other aligned 16-byte items in the same streaming line may be satisfied from the streaming load buffer and can improve throughput.

Programmers are advised to use the following practices to improve the efficiency of MOVNTDQA streaming loads from WC memory:

- Streaming loads must be 16-byte aligned.
- Temporally group streaming loads of the same streaming cache line for effective use of the small number of streaming load buffers. If loads to the same streaming line are excessively spaced apart, it may cause the streaming line to be re-fetched from memory.
- Temporally group streaming loads from at most a few streaming lines together. The number of streaming load buffers is small; grouping a modest number of streams will avoid running out of streaming load buffers and the resultant re-fetching of streaming lines from memory.
- Avoid writing to a streaming line until all 16-byte-aligned reads from the streaming line have occurred. Reading a 16-byte item from a streaming line that has been written, may cause the streaming line to be re-fetched.
- Avoid reading a given 16-byte item within a streaming line more than once; repeated loads of a particular 16-byte item are likely to cause the streaming line to be re-fetched.
- The streaming load buffers, reflecting the WC memory type characteristics, are not required to be snooped by operations from other agents. Software should not rely upon such coherency actions to provide any data coherency with respect to other logical processors or bus agents. Rather, software must ensure the consistency of WC memory accesses between producers and consumers.
- Streaming loads may be weakly ordered and may appear to software to execute out of order with respect to other memory operations. Software must explicitly use MFENCE if it needs to preserve order among streaming loads or between streaming loads and other memory operations.
- Streaming loads must not be used to reference memory addresses that are mapped to I/O devices having side effects or when reads to these devices are destructive. This is because MOVNTDQA is speculative in nature.

Example 12-1 provides a sketch of the basic assembly sequences that illustrate the principles of using MOVNTDQA in a situation with a producer-consumer accessing a WC memory region.

**Example 12-1. Sketch of MOVNTDQA Usage of a Consumer and a PCI Producer**

```

// P0: producer is a PCI device writing into the WC space
# the PCI device updates status through a UC flag, "u_dev_status" .
# the protocol for "u_dev_status" : 0: produce; 1: consume; 2: all done

    mov eax, $0
    mov [u_dev_status], eax
producerStart:
    mov eax, [u_dev_status] # poll status flag to see if consumer is requestion data
    cmp eax, $0             #
    jne done                # I no longer need to produce
    commence PCI writes to WC region..

    mov eax, $1 # producer ready to notify the consumer via status flag
    mov [u_dev_status], eax
# now wait for consumer to signal its status
spinloop:
    cmp [u_dev_status], $1 # did I get a signal from the consumer ?
    jne producerStart      # yes I did
    jmp spinloop           # check again
done:
// producer is finished at this point

```

---

```

// P1: consumer check PCI status flag to consume WC data
    mov eax, $0 # request to the producer
    mov [u_dev_status], eax
consumerStart:
    mov; eax, [u_dev_status] # reads the value of the PCI status
    cmp eax, $1             # has producer written
    jne consumerStart       # tight loop; make it more efficient with pause, etc.
    mfence # producer finished device writes to WC, ensure WC region is coherent
ntread:
    movntdqa xmm0, [addr]
    movntdqa xmm1, [addr + 16]
    movntdqa xmm2, [addr + 32]
    movntdqa xmm3, [addr + 48]
    ... # do any more NT reads as needed
    mfence # ensure PCI device reads the correct value of [u_dev_status]
# now decide whether we are done or we need the producer to produce more data
# if we are done write a 2 into the variable, otherwise write a 0 into the variable
    mov eax, $0/$2 # end or continue producing
    mov [u_dev_status], eax
# if I want to consume again I will jump back to consumerStart after storing a 0 into eax
# otherwise I am done

```

## 12.10.4 Packed Blending Instructions

Intel SSE4.1 adds 6 instructions used for blending (BLENDPS, BLENDPD, BLENDVPS, BLENDVPD, PBLENDVB, PBLENDW).

Blending conditionally copies a data element in a source operand to the same element in the destination. Intel SSE4.1 instructions improve blending operations for most field sizes. A single new Intel SSE4.1 instruction can generally replace a sequence of 2 to 4 operations using previous architectures.

The variable blend instructions (BLENDVPS, BLENDVPD, PBLENDW) introduce the use of control bits stored in an implicit XMM register (XMM0). The most significant bit in each field (the sign bit, for 2's complement integer or floating-point) is used as a selector. See Table 12-3.

**Table 12-3. Blend Field Size and Control Modes Supported by Intel® SSE4.1**

| Instructions | Packed Double FP | Packed Single FP | Packed QWord     | Packed DWord     | Packed Word    | Packed Byte | Blend Control |
|--------------|------------------|------------------|------------------|------------------|----------------|-------------|---------------|
| BLENDPS      |                  | X                |                  |                  |                |             | Imm8          |
| BLENDPD      | X                |                  |                  |                  |                |             | Imm8          |
| BLENDVPS     |                  | X                |                  | X <sup>(1)</sup> |                |             | XMM0          |
| BLENDVPD     | X                |                  | X <sup>(1)</sup> |                  |                |             | XMM0          |
| PBLENDVB     |                  |                  | <sup>(2)</sup>   | <sup>(2)</sup>   | <sup>(2)</sup> | X           | XMM0          |
| PBLENDW      |                  |                  | X                | X                | X              |             | Imm8          |

**NOTE:**

1. Use of floating-point SIMD instructions on integer data types may incur performance penalties.
2. Byte variable blend can be used for larger sized fields by reformatting (or shuffling) the blend control.

## 12.10.5 Packed Integer MIN/MAX Instructions

Intel SSE4.1 adds 8 packed integer MIN and MAX instructions: PMINUW, PMINUD, PMINSB, PMINSD; PMAUW, PMAUD, PMAUSB, and PMAUSD.

Four 32-bit integer packed MIN and MAX instructions operate on unsigned and signed dwords. Two instructions operate on signed bytes. Two instructions operate on unsigned words. See Table 12-4.

**Table 12-4. Enhanced SIMD Integer MIN/MAX Instructions Supported by Intel® SSE4.1**

|                |          | Integer Width      |                    |                  |
|----------------|----------|--------------------|--------------------|------------------|
|                |          | Byte               | Word               | DWord            |
| Integer Format | Unsigned | PMINUB*<br>PMAUSB* | PMINUW<br>PMAUW    | PMINUD<br>PMAUD  |
|                | Signed   | PMINSB<br>PMAUSB   | PMINSW*<br>PMAWSW* | PMINSD<br>PMAUSD |

**NOTE:**

\* Available prior to Intel SSE4.1.

## 12.10.6 Floating-Point Round Instructions with Selectable Rounding Mode

High level languages and libraries often expose rounding operations having a variety of numeric rounding and exception behaviors. Using Intel SSE, SSE2, and SSE3 instructions to mitigate the rounding-mode-related problem is sometimes not straight forward.

Intel SSE4.1 introduces four rounding instructions (ROUNDPS, ROUNDPD, ROUNDSS, and ROUNDDSD) that cover scalar and packed single- and double precision floating-point operands. The rounding mode can be selected using an immediate from one of the IEEE-754 modes (Nearest, -Inf, +Inf, and Truncate) without changing the current

rounding mode; or the instruction can be forced to use the current rounding mode. Another bit in the immediate is used to suppress inexact precision exceptions.

Rounding instructions in Intel SSE4.1 generally permit single-instruction solutions to C99 functions `ceil()`, `floor()`, `trunc()`, `rint()`, `nearbyint()`. These instructions simplify the implementations of half-way-away-from-zero rounding modes as used by C99 `round()` and F90's `nint()`.

## 12.10.7 Insertion and Extractions from XMM Registers

Intel SSE4.1 adds 7 instructions (corresponding to 9 assembly instruction mnemonics) that simplify data insertion and extraction between general-purpose register (GPR) and XMM registers: `EXTRACTPS`, `INSERTPS`, `PINSRB`, `PINSRD`, `PINSRQ`, `PEXTRB`, `PEXTRW`, `PEXTRD`, and `PEXTRQ`. When accessing memory, no alignment is required for any of these instructions (unless alignment checking is enabled).

`EXTRACTPS` extracts a single precision floating-point value from any dword offset in an XMM register and stores the result to memory or a general-purpose register. `INSERTPS` inserts a single floating-point value from either a 32-bit memory location or from specified element in an XMM register to a selected element in the destination XMM register. In addition, `INSERTPS` allows the insertion of `+0.0f` into any destination elements using a mask.

`PINSRB`, `PINSRD`, and `PINSRQ` insert byte, dword, or qword integer values from a register or memory into an XMM register. Insertion of integer word values were already supported by Intel SSE2 (`PINSRW`).

`PEXTRB`, `PEXTRW`, `PEXTRD`, and `PEXTRQ` extract byte, word, dword, and qword from an XMM register and insert the values into a general-purpose register or memory.

## 12.10.8 Packed Integer Format Conversions

A common type of operation on packed integers is the conversion by zero- or sign-extension of packed integers into wider data types. Intel SSE4.1 adds 12 instructions that convert from a smaller packed integer type to a larger integer type: `PMOVSXBW`, `PMOVZXBW`, `PMOVXBD`, `PMOVZxbd`, `PMOVXWD`, `PMOVZXWD`, `PMOVXBQ`, `PMOVXWQ`, `PMOVZXWQ`, `PMOVXDQ`, and `PMOVZXDQ`.

The source operand is from either an XMM register or memory; the destination is an XMM register. See Table 12-5.

When accessing memory, no alignment is required for any of the instructions unless alignment checking is enabled. In which case, all conversions must be aligned to the width of the memory reference. The number of elements converted (and width of memory reference) is illustrated in Table 12-6. The alignment requirement is shown in parenthesis.

**Table 12-5. New SIMD Integer Conversions Supported by Intel® SSE4.1**

|                  |                | Source Type           |                       |                       |
|------------------|----------------|-----------------------|-----------------------|-----------------------|
|                  |                | Byte                  | Word                  | Dword                 |
| Destination Type | Signed Word    | <code>PMOVSXBW</code> |                       |                       |
|                  | Unsigned Word  | <code>PMOVZXBW</code> |                       |                       |
|                  | Signed Dword   | <code>PMOVXBD</code>  | <code>PMOVXWD</code>  |                       |
|                  | Unsigned Dword | <code>PMOVZxbd</code> | <code>PMOVZXWD</code> |                       |
|                  | Signed Qword   | <code>PMOVXBQ</code>  | <code>PMOVXWQ</code>  | <code>PMOVXDQ</code>  |
|                  | Unsigned Qword | <code>PMOVZXBQ</code> | <code>PMOVZXWQ</code> | <code>PMOVZXDQ</code> |

Table 12-6. New SIMD Integer Conversions Supported by Intel® SSE4.1

|                  |       | Source Type |             |             |
|------------------|-------|-------------|-------------|-------------|
|                  |       | Byte        | Word        | Dword       |
| Destination Type | Word  | 8 (64 bits) |             |             |
|                  | Dword | 4 (32 bits) | 4 (64 bits) |             |
|                  | Qword | 2 (16 bits) | 2 (32 bits) | 2 (64 bits) |

**12.10.9 Improved Sums of Absolute Differences (SAD) for 4-Byte Blocks**

Intel SSE4.1 adds an instruction (MPSADBW) that performs eight 4-byte wide SAD operations per instruction to produce eight results. Compared to PSADBW, MPSADBW operates on smaller chunks (4-byte instead of 8-byte chunks); this makes the instruction better suited to video coding standards such as VC.1 and H.264. MPSADBW performs four times the number of absolute difference operations than that of PSADBW (per instruction). This can improve performance for dense motion searches.

MPSADBW uses a 4-byte wide field from a source operand; the offset of the 4-byte field within the 128-bit source operand is specified by two immediate control bits. MPSADBW produces eight 16-bit SAD results. Each 16-bit SAD result is formed from overlapping pairs of 4 bytes in the destination with the 4-byte field from the source operand. MPSADBW uses eleven consecutive bytes in the destination operand, its offset is specified by a control bit in the immediate byte (i.e., the offset can be from byte 0 or from byte 4). Figure 12-4 illustrates the operation of MPSADBW. MPSADBW can simplify coding of dense motion estimation by providing source and destination offset control, higher throughput of SAD operations, and the smaller chunk size.

![Diagram of MPSADBW operation showing a 128-bit Source register where a 4-byte block is selected via Imm[1:0]*32. This block is compared against eight overlapping 4-byte blocks in a 128-bit Destination register (offset by Imm[2]*32). Each comparison undergoes an Absolute Difference (Abs. Diff.) and Sum operation to produce eight 16-bit results stored in the Destination register.](6d1910bc8db5fd0b035d17f7d15eed1a_img.jpg)

The diagram illustrates the MPSADBW operation. At the top, a 128-bit 'Source' register is shown with bit positions 127 down to 0. A 4-byte field is selected from it, controlled by 'Imm[1:0]\*32'. Below this, an 'Abs. Diff.' calculation is shown between the selected 4-byte field and overlapping 4-byte fields from an 11-byte 'Destination' register. The 'Destination' register is also shown with bit positions 127 down to 0, and its 11-byte field is controlled by 'Imm[2]\*32'. The result of the absolute difference calculation is a 'Sum' of 16 bits, which is then stored in the Destination register. The diagram shows that eight such 16-bit results are produced from the 11-byte destination field.

Diagram of MPSADBW operation showing a 128-bit Source register where a 4-byte block is selected via Imm[1:0]\*32. This block is compared against eight overlapping 4-byte blocks in a 128-bit Destination register (offset by Imm[2]\*32). Each comparison undergoes an Absolute Difference (Abs. Diff.) and Sum operation to produce eight 16-bit results stored in the Destination register.

Figure 12-4. MPSADBW Operation

**12.10.10 Horizontal Search**

Intel SSE4.1 adds a search instruction (PHMINPOSUW) that finds the value and location of the minimum unsigned word from one of 8 horizontally packed unsigned words. The resulting value and location (offset within the source) are packed into the low dword of the destination XMM register.

Rapid search is often a significant component of motion estimation. MPSADBW and PHMINPOSUW can be used together to improve video encode.

### 12.10.11 Packed Test

The packed test instruction PTEST is similar to a 128-bit equivalent to the legacy instruction TEST. With PTEST, the source argument is typically used like a bit mask.

PTEST performs a logical AND between the destination with this mask and sets the ZF flag if the result is zero. The CF flag (zero for TEST) is set if the inverted mask AND'd with the destination is all zero. Because the destination is not modified, PTEST simplifies branching operations (such as branching on signs of packed floating-point numbers, or branching on zero fields).

### 12.10.12 Packed Qword Equality Comparisons

Intel SSE4.1 adds a 128-bit packed qword equality test. The new instruction (PCMPEQQ) is identical to PCMPEQD, but has qword granularity.

### 12.10.13 Dword Packing With Unsigned Saturation

Intel SSE4.1 adds a new instruction PACKUSDW to complete the set of small integer pack instructions in the family of SIMD instruction extensions. PACKUSDW packs dword to word with unsigned saturation. See Table 12-7 for the complete set of packing instructions for small integers.

**Table 12-7. Enhanced SIMD Pack Support by Intel® SSE4.1**

|                 |          | Pack Type       |              |
|-----------------|----------|-----------------|--------------|
|                 |          | DWord -> Word   | Word -> Byte |
| Saturation Type | Unsigned | PACKUSDW (new!) | PACKUSWB     |
|                 | Signed   | PACKSSDW        | PACKSSWB     |

## 12.11 INTEL® SSE4.2 INSTRUCTION SET

Five of the seven Intel SSE4.2 instructions can use an XMM register as a source or destination. These include four text/string processing instructions and one packed quadword compare SIMD instruction. Programming these five Intel SSE4.2 instructions is similar to programming 128-bit Integer SIMD in Intel SSE2 or SSSE3. Intel SSE4.2 does not provide any 64-bit integer SIMD instructions.

### 12.11.1 String and Text Processing Instructions

String and text processing instructions in Intel SSE4.2 allocates four opcodes to provide a rich set of string and text processing capabilities that traditionally required many more opcodes. These four instructions use XMM registers to process string or text elements of up to 128-bits (16 bytes or 8 words). Each instruction uses an immediate byte to support a rich set of programmable controls. A string-processing Intel SSE4.2 instruction returns the result of processing each pair of string elements using either an index or a mask.

The capabilities of the string/text processing instructions include:

- Handling string/text fragments consisting of bytes or words, either signed or unsigned.
- Support for partial string or fragments less than 16 bytes in length, using either explicit length or implicit null-termination.
- Four types of string compare operations on word/byte elements.
- Up to 256 compare operations performed in a single instruction on all string/text element pairs.
- Built-in aggregation of intermediate results from comparisons.

- Programmable control of processing on intermediate results.
- Programmable control of output formats in terms of an index or mask.
- Bi-directional support for the index format.
- Support for two mask formats: bit or natural element width.
- Not requiring 16-byte alignment for memory operand.

The four Intel SSE4.2 instructions that process text/string fragments are:

- PCMPSTR — Packed compare explicit-length strings, return index in ECX/RCX.
- PCMPSTRM — Packed compare explicit-length strings, return mask in XMM0.
- PCMPISTR — Packed compare implicit-length strings, return index in ECX/RCX.
- PCMPISTRM — Packed compare implicit-length strings, return mask in XMM0.

All four of these instructions require the use of an immediate byte to control operation. The two source operands can be XMM registers or a combination of XMM register and memory address. The immediate byte provides programmable control with the following attributes:

- Input data format.
- Compare operation mode.
- Intermediate result processing.
- Output selection.

Depending on the output format associated with the instruction, the text/string processing instructions implicitly uses either a general-purpose register (ECX/RCX) or an XMM register (XMM0) to return the final result.

Two of the four text-string processing instructions specify string length explicitly. They use two general-purpose registers (EDX, EAX) to specify the number of valid data elements (either word or byte) in the source operands. The other two instructions specify valid string elements using null termination. A data element is considered valid only if it has a lower index than the least significant null data element.

### 12.11.1.1 Memory Operand Alignment

The text and string processing instructions in Intel SSE4.2 do not perform alignment checking on memory operands. This is different from most other 128-bit SIMD instructions accessing the XMM registers. The absence of an alignment check for these four instructions does not imply any modification to the existing definitions of other instructions.

### 12.11.2 Packed Comparison SIMD Integer Instruction

Intel SSE4.2 also provides a 128-bit integer SIMD instruction PCMPGTQ that performs logical compare of greater-than on packed integer quadwords.

## 12.12 WRITING APPLICATIONS WITH INTEL® SSE4 EXTENSIONS

### 12.12.1 Guidelines for Using Intel® SSE4 Extensions

The following guidelines describe how to maximize the benefits of using Intel SSE4 extensions:

- Check that the processor supports Intel SSE4 extensions.
- Ensure that the operating system supports SSSE3 and Intel SSE, SSE2, and SSE3. (Operating system support for Intel SSE implies sufficient support for SSSE3 and Intel SSE2, SSE3, and SSE4.)
- Employ the optimization and scheduling techniques described in the Intel® 64 and IA-32 Architectures Optimization Reference Manual (see Section 1.4, “Related Literature”).

### 12.12.2 Checking for Intel® SSE4.1 Support

Before an application attempts to use Intel SSE4.1 instructions, the application should follow the steps illustrated in Section 11.6.2, “Checking for Intel® SSE and SSE2 Support.” Next, use the additional step provided below:

Check that the processor supports Intel SSE4.1 (if CPUID.01H:ECX.SSE4\_1[19] = 1), Intel SSE3 (if CPUID.01H:ECX.SSE3[0] = 1), and SSSE3 (if CPUID.01H:ECX.SSSE3[9] = 1).

### 12.12.3 Checking for Intel® SSE4.2 Support

Before an application attempts to use the following Intel SSE4.2 instructions: PCMPSTRI/PCMPSTRM/PCMP-ISTRI/PCMPISTRM, PCMPGTQ; the application should follow the steps illustrated in Section 11.6.2, “Checking for Intel® SSE and SSE2 Support.” Next, use the additional steps provided below:

- Check that the processor supports Intel SSE4.2 (if CPUID.01H:ECX.SSE4\_2[20] = 1), Intel SSE4.1 (if CPUID.01H:ECX.SSE4\_1[19] = 1), and SSSE3 (if CPUID.01H:ECX.SSSE3[9] = 1).
- Before an application attempts to use the CRC32 instruction, it must check that the processor supports Intel SSE4.2 (if CPUID.01H:ECX.SSE4\_2[20] = 1).
- Before an application attempts to use the POPCNT instruction, it must check that the processor supports Intel SSE4.2 (if CPUID.01H:ECX.SSE4\_2[20] = 1) and POPCNT (if CPUID.01H:ECX.POPCNT[23] = 1).

## 12.13 INTEL® AES-NI OVERVIEW

Intel AES-NI provides six instructions to accelerate symmetric block encryption/decryption of 128-bit data blocks using the Advanced Encryption Standard (AES) specified by the NIST publication FIPS 197. Specifically, two instructions (AESENC and AESENCST) target the AES encryption rounds; and two instructions (AESDEC and AESDECLAST) target AES decryption rounds using the Equivalent Inverse Cipher. One instruction (AESIMC) targets the Inverse MixColumn transformation primitive, and one instruction (AESKEYGEN) targets generation of round keys from the cipher key for the AES encryption/decryption rounds.

AES supports encryption/decryption using cipher key lengths of 128, 192, and 256 bits by processing the data block in 10, 12, and 14 rounds of predefined transformations. Figure 12-5 depicts the cryptographic processing of a block of 128-bit plain text into cipher text.

![Figure 12-5: AES State Flow diagram showing the transformation of plain text into cipher text through multiple rounds of AES processing.](27786744857e3e5e522ae1cff7be1f97_img.jpg)

The diagram illustrates the AES state flow. It begins with a 4x4 grid representing 'Plain text'. An arrow labeled 'RK(0)' points to a triangle labeled 'XOR', which then points to another 4x4 grid labeled 'AES State'. From this state, an arrow labeled 'Round 1' points to a second 4x4 grid labeled 'AES State'. This is followed by an ellipsis 'Rounds 2.. n-2'. Then, an arrow labeled 'RK(n-1)' points to a triangle, which points to a final 4x4 grid labeled 'Cipher text'. Below the diagram, the number of rounds (n) for different key sizes is specified: AES-128: n = 10, AES-192: n = 12, and AES-256: n = 14.

Figure 12-5: AES State Flow diagram showing the transformation of plain text into cipher text through multiple rounds of AES processing.

Figure 12-5. AES State Flow

The predefined AES transformation primitives are described in the next few sections, they are also referenced in the operation flow of instruction reference page of these instructions.

### 12.13.1 Little-Endian Architecture and Big-Endian Specification (FIPS 197)

FIPS 197 document defines the Advanced Encryption Standard (AES) and includes a set of test vectors for testing all of the steps in the algorithm, and can be used for testing and debugging.

The following observation is important for using the AES instructions offered in Intel 64 Architecture: FIPS 197 text convention is to write hex strings with the low-memory byte on the left and the high-memory byte on the right. Intel’s convention is the reverse. It is similar to the difference between Big Endian and Little Endian notations.

In other words, a 128 bits vector in the FIPS document, when read from left to right, is encoded as [7:0, 15:8, 23:16, 31:24, ...127:120]. Note that inside the byte, the encoding is [7:0], so the first bit from the left is the most significant bit. In practice, the test vectors are written in hexadecimal notation, where pairs of hexadecimal digits define the different bytes. To translate the FIPS 197 notation to an Intel 64 architecture compatible (“Little Endian”) format, each test vector needs to be byte-reflected to [127:120,... 31:24, 23:16, 15:8, 7:0].

Example A:  
FIPS Test vector: 000102030405060708090a0b0c0d0e0fH  
Intel AES Hardware: 0f0e0d0c0b0a09080706050403020100H

It should be pointed out that the only thing at issue is a textual convention, and programmers do not need to perform byte-reversal in their code, when using the AES instructions.

12.13.1.1 AES Data Structure in Intel® 64 Architecture

The AES instructions that are defined in this document operate on one or on two 128 bits source operands: State and Round Key. From the architectural point of view, the state is input in an xmm register and the Round key is input either in an xmm register or a 128-bit memory location.

In AES algorithm, the state (128 bits) can be viewed as four 32-bit doublewords (“Words” in AES terminology): X3, X2, X1, and X0.

The state may also be viewed as a set of 16 bytes. The 16 bytes can also be viewed as a 4x4 matrix of bytes where S(i, j) with i, j = 0, 1, 2, 3 compose the 32-bit “words” as follows:

- X0 = S (3, 0) S (2, 0) S (1, 0) S (0, 0)
- X1 = S (3, 1) S (2, 1) S (1, 1) S (0, 1)
- X2 = S (3, 2) S (2, 2) S (1, 2) S (0, 2)
- X3 = S (3, 3) S (2, 3) S (1, 3) S (0, 3)

The following tables, Table 12-8 through Table 12-11, illustrate various representations of a 128-bit state.

Table 12-8. Byte and 32-Bit Word Representation of a 128-Bit State

| Byte #       | 15       | 14      | 13      | 12     | 11      | 10    | 9     | 8     | 7       | 6     | 5     | 4     | 3      | 2     | 1    | 0   |
|--------------|----------|---------|---------|--------|---------|-------|-------|-------|---------|-------|-------|-------|--------|-------|------|-----|
| Bit Position | 127-120  | 119-112 | 111-103 | 103-96 | 95-88   | 87-80 | 79-72 | 71-64 | 63-56   | 55-48 | 47-40 | 39-32 | 31-24  | 23-16 | 15-8 | 7-0 |
|              | 127 - 96 |         |         |        | 95 - 64 |       |       |       | 64 - 32 |       |       |       | 31 - 0 |       |      |     |
| State Word   | X3       |         |         |        | X2      |       |       |       | X1      |       |       |       | X0     |       |      |     |
| State Byte   | P        | O       | N       | M      | L       | K     | J     | I     | H       | G     | F     | E     | D      | C     | B    | A   |

Table 12-9. Matrix Representation of a 128-Bit State

|   |   |   |   |         |         |         |         |
|---|---|---|---|---------|---------|---------|---------|
| A | E | I | M | S(0, 0) | S(0, 1) | S(0, 2) | S(0, 3) |
| B | F | J | N | S(1, 0) | S(1, 1) | S(1, 2) | S(1, 3) |
| C | G | K | O | S(2, 0) | S(2, 1) | S(2, 2) | S(2, 3) |
| D | H | L | P | S(3, 0) | S(3, 1) | S(3, 2) | S(3, 3) |

Example:  
FIPS vector: d4 bf 5d 30 e0 b4 52 ae b8 41 11 f1 1e 27 98 e5

This vector has the “least significant” byte d4 and the significant byte e5 (written in Big Endian format in the FIPS document). When it is translated to IA notations, the encoding is:

**Table 12-10. Little Endian Representation of a 128-Bit State**

| Byte #      | 15 | 14 | 13 | 12 | 11 | 10 | 9  | 8  | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
|-------------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| State Byte  | P  | O  | N  | M  | L  | K  | J  | I  | H  | G  | F  | E  | D  | C  | B  | A  |
| State Value | e5 | 98 | 27 | 1e | f1 | 11 | 41 | b8 | ae | 52 | b4 | e0 | 30 | 5d | bf | d4 |

**Table 12-11. Little Endian Representation of a 4x4 Byte Matrix**

|   |   |   |   |  |    |    |    |    |
|---|---|---|---|--|----|----|----|----|
| A | E | I | M |  | d4 | e0 | b8 | 1e |
| B | F | J | N |  | bf | b4 | 41 | 27 |
| C | G | K | O |  | 5d | 52 | 11 | 98 |
| D | H | L | P |  | 30 | ae | f1 | e5 |

### 12.13.2 AES Transformations and Functions

The following functions and transformations are used in the algorithmic descriptions of AES instruction extensions AESDEC, AESDECLAST, AESENC, AESENCCLAST, AESIMC, and AESKEYGENASSIST.

Note that these transformations are expressed here in a Little Endian format (and not as in the FIPS 197 document).

- **MixColumns():** A byte-oriented 4x4 matrix transformation on the matrix representation of a 128-bit AES state. A FIPS-197 defined 4x4 matrix is multiplied to each 4x1 column vector of the AES state. The columns are considered polynomials with coefficients in the Finite Field that is used in the definition of FIPS 197, the operations (“multiplication” and “addition”) are in that Finite Field, and the polynomials are reduced modulo  $x^4+1$ .

The MixColumns() transformation defines the relationship between each byte of the result state, represented as  $S'(i, j)$  of a 4x4 matrix (see Section 12.13.1), as a function of input state bytes,  $S(i, j)$ , as follows

$$S'(0, j) := \text{FF\_MUL}(02\text{H}, S(0, j)) \text{ XOR } \text{FF\_MUL}(03\text{H}, S(1, j)) \text{ XOR } S(2, j) \text{ XOR } S(3, j)$$

$$S'(1, j) := S(0, j) \text{ XOR } \text{FF\_MUL}(02\text{H}, S(1, j)) \text{ XOR } \text{FF\_MUL}(03\text{H}, S(2, j)) \text{ XOR } S(3, j)$$

$$S'(2, j) := S(0, j) \text{ XOR } S(1, j) \text{ XOR } \text{FF\_MUL}(02\text{H}, S(2, j)) \text{ XOR } \text{FF\_MUL}(03\text{H}, S(3, j))$$

$$S'(3, j) := \text{FF\_MUL}(03\text{H}, S(0, j)) \text{ XOR } S(1, j) \text{ XOR } S(2, j) \text{ XOR } \text{FF\_MUL}(02\text{H}, S(3, j))$$

where  $j = 0, 1, 2, 3$ . **FF\_MUL(Byte1, Byte2)** denotes the result of multiplying two elements (represented by Byte1 and byte2) in the Finite Field representation that defines AES. The result of produced by **FF\_MUL(Byte1, Byte2)** is an element in the Finite Field (represented as a byte). A Finite Field is a field with a finite number of elements, and when this number can be represented as a power of 2 ( $2^n$ ), its elements can be represented as the set of  $2^n$  binary strings of length  $n$ . AES uses a finite field with  $n=8$  (having 256 elements). With this representation, “addition” of two elements in that field is a bit-wise XOR of their binary-string representation, producing another element in the field. Multiplication of two elements in that field is defined using an irreducible polynomial (for AES, this polynomial is  $m(x) = x^8 + x^4 + x^3 + x + 1$ ). In this Finite Field representation, the bit value of bit position  $k$  of a byte represents the coefficient of a polynomial of order  $k$ , e.g., 1010\_1101B (ADH) is represented by the polynomial  $(x^7 + x^5 + x^3 + x^2 + 1)$ . The byte value result of multiplication of two elements is obtained by a carry-less multiplication of the two corresponding polynomials, followed by reduction modulo the polynomial, where the remainder is calculated using operations defined in the field. For example, **FF\_MUL(57H, 83H) = C1H**, because the carry-less polynomial multiplication of the polynomials represented by 57H and 83H produces  $(x^{13} + x^{11} + x^9 + x^8 + x^6 + x^5 + x^4 + x^3 + 1)$ , and the remainder modulo  $m(x)$  is  $(x^7 + x^6 + 1)$ .

- **RotWord():** performs a byte-wise cyclic permutation (rotate right in little-endian byte order) on a 32-bit AES word.

- The output word  $X'[j]$  of  $\text{RotWord}(X[j])$  where  $X[j]$  represent the four bytes of column  $j$ ,  $S(i, j)$ , in descending order  $X[j] = ( S(3, j), S(2, j), S(1, j), S(0, j) )$ ;  $X'[j] = ( S'(3, j), S'(2, j), S'(1, j), S'(0, j) ) := ( S(0, j), S(3, j), S(2, j), S(1, j) )$
- ShiftRows(): A byte-oriented matrix transformation that processes the matrix representation of a 16-byte AES state by cyclically shifting the last three rows of the state by different offset to the left, see Table 12-12.

Table 12-12. The ShiftRows Transformation

| Matrix Representation of Input State |   |   |   | Output of ShiftRows |   |   |   |
|--------------------------------------|---|---|---|---------------------|---|---|---|
| A                                    | E | I | M | A                   | E | I | M |
| B                                    | F | J | N | F                   | J | N | B |
| C                                    | G | K | O | K                   | O | C | G |
| D                                    | H | L | P | P                   | D | H | L |

- SubBytes(): A byte-oriented transformation that processes the 128-bit AES state by applying a non-linear substitution table (S-BOX) on each byte of the state.
- The SubBytes() function defines the relationship between each byte of the result state  $S'(i, j)$  as a function of input state byte  $S(i, j)$ , by
- $$S'(i, j) := \text{S-Box} (S(i, j)[7:4], S(i, j)[3:0])$$
- where S-BOX ( $S[7:4], S[3:0]$ ) represents a look-up operation on a 16x16 table to return a byte value, see Table 12-13.

Table 12-13. Look-up Table Associated with S-Box Transformation

|        |   | S[3:0] |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|--------|---|--------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|        |   | 0      | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | a  | b  | c  | d  | e  | f  |
| S[7:4] | 0 | 63     | 7c | 77 | 7b | f2 | 6b | 6f | c5 | 30 | 01 | 67 | 2b | fe | d7 | ab | 76 |
|        | 1 | ca     | 82 | c9 | 7d | fa | 59 | 47 | f0 | ad | d4 | a2 | af | 9c | a4 | 72 | c0 |
|        | 2 | b7     | fd | 93 | 26 | 36 | 3f | f7 | cc | 34 | a5 | e5 | f1 | 71 | d8 | 31 | 15 |
|        | 3 | 04     | c7 | 23 | c3 | 18 | 96 | 05 | 9a | 07 | 12 | 80 | e2 | eb | 27 | b2 | 75 |
|        | 4 | 09     | 83 | 2c | 1a | 1b | 6e | 5a | a0 | 52 | 3b | d6 | b3 | 29 | e3 | 2f | 84 |
|        | 5 | 53     | d1 | 00 | ed | 20 | fc | b1 | 5b | 6a | cb | be | 39 | 4a | 4c | 58 | cf |
|        | 6 | d0     | ef | aa | fb | 43 | 4d | 33 | 85 | 45 | f9 | 02 | 7f | 50 | 3c | 9f | a8 |
|        | 7 | 51     | a3 | 40 | 8f | 92 | 9d | 38 | f5 | bc | b6 | da | 21 | 10 | ff | f3 | d2 |
|        | 8 | cd     | 0c | 13 | ec | 5f | 97 | 44 | 17 | c4 | a7 | 7e | 3d | 64 | 5d | 19 | 73 |
|        | 9 | 60     | 81 | 4f | dc | 22 | 2a | 90 | 88 | 46 | ee | b8 | 14 | de | 5e | 0b | db |
|        | a | e0     | 32 | 3a | 0a | 49 | 06 | 24 | 5c | c2 | d3 | ac | 62 | 91 | 95 | e4 | 79 |
|        | b | e7     | c8 | 37 | 6d | 8d | d5 | 4e | a9 | 6c | 56 | f4 | ea | 65 | 7a | ae | 08 |
|        | c | ba     | 78 | 25 | 2e | 1c | a6 | b4 | c6 | e8 | dd | 74 | 1f | 4b | bd | 8b | 8a |
|        | d | 70     | 3e | b5 | 66 | 48 | 03 | f6 | 0e | 61 | 35 | 57 | b9 | 86 | c1 | 1d | 9e |
|        | e | e1     | f8 | 98 | 11 | 69 | d9 | 8e | 94 | 9b | 1e | 87 | e9 | ce | 55 | 28 | df |
|        | f | 8c     | a1 | 89 | 0d | bf | e6 | 42 | 68 | 41 | 99 | 2d | 0f | b0 | 54 | bb | 16 |

- SubWord(): produces an output AES word (four bytes) from the four bytes of an input word using a non-linear substitution table (S-BOX).

$X'[j] = ( S'(3, j), S'(2, j), S'(1, j), S'(0, j) ) := ( \text{S-Box}( S(3, j) ), \text{S-Box}( S(2, j) ), \text{S-Box}( S(1, j) ), \text{S-Box}( S(0, j) ) )$

- **InvMixColumns():** The inverse transformation of MixColumns().

The InvMixColumns() transformation defines the relationship between each byte of the result state  $S'(i, j)$  as a function of input state bytes,  $S(i, j)$ , by

$S'(0, j) := \text{FF\_MUL}( 0eH, S(0, j) ) \text{ XOR } \text{FF\_MUL}(0bH, S(1, j) ) \text{ XOR } \text{FF\_MUL}(0dH, S(2, j) ) \text{ XOR } \text{FF\_MUL}( 09H, S(3, j) )$

$S'(1, j) := \text{FF\_MUL}(09H, S(0, j) ) \text{ XOR } \text{FF\_MUL}( 0eH, S(1, j) ) \text{ XOR } \text{FF\_MUL}(0bH, S(2, j) ) \text{ XOR } \text{FF\_MUL}( 0dH, S(3, j) )$

$S'(2, j) := \text{FF\_MUL}(0dH, S(0, j) ) \text{ XOR } \text{FF\_MUL}( 09H, S(1, j) ) \text{ XOR } \text{FF\_MUL}( 0eH, S(2, j) ) \text{ XOR } \text{FF\_MUL}(0bH, S(3, j) )$

$S'(3, j) := \text{FF\_MUL}(0bH, S(0, j) ) \text{ XOR } \text{FF\_MUL}(0dH, S(1, j) ) \text{ XOR } \text{FF\_MUL}( 09H, S(2, j) ) \text{ XOR } \text{FF\_MUL}( 0eH, S(3, j) )$ , where  $j = 0, 1, 2, 3$ .

- **InvShiftRows():** The inverse transformation of InvShiftRows(). The InvShiftRows() transforms the matrix representation of a 16-byte AES state by cyclically shifting the last three rows of the state by different offset to the right, see Table 12-14.

**Table 12-14. The InvShiftRows Transformation**

| Matrix Representation of Input State |   |   |   | Output of ShiftRows |   |   |   |
|--------------------------------------|---|---|---|---------------------|---|---|---|
| A                                    | E | I | M | A                   | E | I | M |
| B                                    | F | J | N | N                   | B | F | J |
| C                                    | G | K | O | K                   | O | C | G |
| D                                    | H | L | P | H                   | L | P | D |

- **InvSubBytes():** The inverse transformation of SubBytes().

The InvSubBytes() transformation defines the relationship between each byte of the result state  $S'(i, j)$  as a function of input state byte  $S(i, j)$ , by

$S'(i, j) := \text{InvS-Box}( S(i, j)[7:4], S(i, j)[3:0] )$

where InvS-BOX ( $S[7:4], S[3:0]$ ) represents a look-up operation on a 16x16 table to return a byte value, see Table 12-15.

**Table 12-15. Look-up Table Associated with InvS-Box Transformation**

|        |   | S[3:0] |    |    |    |    |    |    |    |    |    |    |    |    |    |    |    |
|--------|---|--------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
|        |   | 0      | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | a  | b  | c  | d  | e  | f  |
| S[7:4] | 0 | 52     | 09 | 6a | d5 | 30 | 36 | a5 | 38 | bf | 40 | a3 | 9e | 81 | f3 | d7 | fb |
|        | 1 | 7c     | e3 | 39 | 82 | 9b | 2f | ff | 87 | 34 | 8e | 43 | 44 | c4 | de | e9 | cb |
|        | 2 | 54     | 7b | 94 | 32 | a6 | c2 | 23 | 3d | ee | 4c | 95 | 0b | 42 | fa | c3 | 4e |
|        | 3 | 08     | 2e | a1 | 66 | 28 | d9 | 24 | b2 | 76 | 5b | a2 | 49 | 6d | 8b | d1 | 25 |
|        | 4 | 72     | f8 | f6 | 64 | 86 | 68 | 98 | 16 | d4 | a4 | 5c | cc | 5d | 65 | b6 | 92 |
|        | 5 | 6c     | 70 | 48 | 50 | fd | ed | b9 | da | 5e | 15 | 46 | 57 | a7 | 8d | 9d | 84 |
|        | 6 | 90     | d8 | ab | 00 | 8c | bc | d3 | 0a | f7 | e4 | 58 | 05 | b8 | b3 | 45 | 06 |
|        | 7 | d0     | 2c | 1e | 8f | ca | 3f | 0f | 02 | c1 | af | bd | 03 | 01 | 13 | 8a | 6b |
|        | 8 | 3a     | 91 | 11 | 41 | 4f | 67 | dc | ea | 97 | f2 | cf | ce | f0 | b4 | e6 | 73 |
|        | 9 | 96     | ac | 74 | 22 | e7 | ad | 35 | 85 | e2 | f9 | 37 | e8 | 1c | 75 | df | 6e |
|        | a | 47     | f1 | 1a | 71 | 1d | 29 | c5 | 89 | 6f | b7 | 62 | 0e | aa | 18 | be | 1b |
|        | b | fc     | 56 | 3e | 4b | c6 | d2 | 79 | 20 | 9a | db | c0 | fe | 78 | cd | 5a | f4 |
|        | c | 1f     | dd | a8 | 33 | 88 | 07 | c7 | 31 | b1 | 12 | 10 | 59 | 27 | 80 | ec | 5f |
|        | d | 60     | 51 | 7f | a9 | 19 | b5 | 4a | 0d | 2d | e5 | 7a | 9f | 93 | c9 | 9c | ef |
|        | e | a0     | e0 | 3b | 4d | ae | 2a | f5 | b0 | c8 | eb | bb | 3c | 83 | 53 | 99 | 61 |
|        | f | 17     | 2b | 04 | 7e | ba | 77 | d6 | 26 | e1 | 69 | 14 | 63 | 55 | 21 | 0c | 7d |

### 12.13.3 PCLMULQDQ

The PCLMULQDQ instruction performs carry-less multiplication of two 64-bit data into a 128-bit result. Carry-less multiplication of two 128-bit data into a 256-bit result can use PCLMULQDQ as building blocks.

Carry-less multiplication is a component of many cryptographic systems. It is an important piece of implementing Galois Counter Mode (GCM) operation of block ciphers. GCM operation can be used in conjunction with AES algorithms to add authentication capability. GCM usage models also include IPsec, storage standard, and security protocols over fiber channel. Additionally, PCLMULQDQ can be used in calculations of hash functions and CRC using arbitrary polynomials.

### 12.13.4 Checking for Intel® AES-NI Support

Before an application attempts to use AESNI instructions or PCLMULQDQ, the application should follow the steps illustrated in Section 11.6.2, “Checking for Intel® SSE and SSE2 Support.” Next, use the additional step provided below:

Check that the processor supports Intel AES-NI (if CPUID.01H:ECX.AESNI[25] = 1); check that the processor supports PCLMULQDQ (if CPUID.01H:ECX.PCLMULQDQ[1] = 1).

## CHAPTER 13
