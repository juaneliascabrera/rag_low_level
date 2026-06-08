---
architecture: x86_32
component: sse
mode: protected
tags: ['sse', 'xmm', 'simd', 'floating_point']
source: intel_sdm_vol1_chapter_10.md
---

# Intel SDM Volume 1 - Chapter 10

# CHAPTER 10

## PROGRAMMING WITH INTEL® STREAMING SIMD EXTENSIONS (INTEL® SSE)

---

The Intel® Streaming SIMD Extensions (Intel® SSE) were introduced into the IA-32 architecture in the Pentium III processor family. These extensions enhance the performance of IA-32 processors for advanced 2-D and 3-D graphics, motion video, image processing, speech recognition, audio synthesis, telephony, and video conferencing. This chapter describes SSE. Chapter 11, “Programming with Intel® Streaming SIMD Extensions 2 (Intel® SSE2),” provides information to assist in writing application programs that use Intel SSE2. Chapter 12, “Programming with Intel® SSE3, SSSE3, Intel® SSE4, and Intel® AES-NI,” provides this information for Intel SSE3.

### 10.1 OVERVIEW OF INTEL® SSE

Intel MMX technology introduced single-instruction multiple-data (SIMD) capability into the IA-32 architecture, with the 64-bit MMX registers, 64-bit packed integer data types, and instructions that allowed SIMD operations to be performed on packed integers. Intel SSE expanded the SIMD execution model by adding facilities for handling packed and scalar single precision floating-point values contained in 128-bit registers.

If `CPUID.01H:EDX.SSE[25] = 1`, Intel SSE is available.

Intel SSE adds the following features to the IA-32 architecture, while maintaining backward compatibility with all existing IA-32 processors, applications, and operating systems:

- Eight 128-bit data registers (called XMM registers) in non-64-bit modes; 16 XMM registers are available in 64-bit mode.
- The 32-bit MXCSR register, which provides control and status bits for operations performed on XMM registers.
- The 128-bit packed single precision floating-point data type (four IEEE single precision floating-point values packed into a double quadword).
- Instructions that perform SIMD operations on single precision floating-point values and that extend SIMD operations that can be performed on integers:
  - 128-bit Packed and scalar single precision floating-point instructions that operate on data located in MMX registers.
  - 64-bit SIMD integer instructions that support additional operations on packed integer operands located in MMX registers.
- Instructions that save and restore the state of the MXCSR register.
- Instructions that support explicit prefetching of data, control of the cacheability of data, and control the ordering of store operations.
- Extensions to the CPUID instruction.

These features extend the IA-32 architecture’s SIMD programming model in four important ways:

- The ability to perform SIMD operations on four packed single precision floating-point values enhances the performance of IA-32 processors for advanced media and communications applications that use computation-intensive algorithms to perform repetitive operations on large arrays of simple, native data elements.
- The ability to perform SIMD single precision floating-point operations in XMM registers and SIMD integer operations in MMX registers provides greater flexibility and throughput for executing applications that operate on large arrays of floating-point and integer data.
- Cache control instructions provide the ability to stream data in and out of XMM registers without polluting the caches and the ability to prefetch data to selected cache levels before it is actually used. Applications that require regular access to large amounts of data benefit from these prefetching and streaming store capabilities.
- The SFENCE (store fence) instruction provides greater control over the ordering of store operations when using weakly-ordered memory types.

Intel SSE is fully compatible with all software written for IA-32 processors. All existing software continues to run correctly, without modification, on processors that incorporate Intel SSE. Enhancements to CPUID permit detection of Intel SSE. Intel SSE is accessible from all IA-32 execution modes: protected mode, real address mode, and virtual-8086 mode.

The following sections of this chapter describe the programming environment for Intel SSE, including: XMM registers, the packed single precision floating-point data type, and Intel SSE instructions. For additional information, see:

- Section 11.6, “Writing Applications with Intel® SSE and SSE2.”
- Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions,” describes the exceptions that can be generated with Intel SSE/SSE2/SSE3 instructions.
- The Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volumes 2A, 2B, 2C, & 2D, provides a detailed description of these instructions.
- Chapter 16, “System Programming for Instruction Set Extensions and Processor Extended States,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A, gives guidelines for integrating these extensions into an operating-system environment.

## 10.2 INTEL® SSE PROGRAMMING ENVIRONMENT

Figure 10-1 shows the execution environment for Intel SSE. All Intel SSE instructions operate on the XMM registers, MMX registers, and/or memory as follows:

- **XMM registers** — These eight registers (see Figure 10-2 and Section 10.2.2, “XMM Registers”) are used to operate on packed or scalar single precision floating-point data. Scalar operations are operations performed on individual (unpacked) single precision floating-point values stored in the low doubleword of an XMM register. XMM registers are referenced by the names XMM0 through XMM7.

![Diagram of the Intel SSE Execution Environment showing the hierarchy of registers and memory address space.](7f8e2d136e7ac49a7d427e57321e47b9_img.jpg)

The diagram illustrates the execution environment for Intel SSE. It shows a hierarchy of registers and the memory address space. On the left, a large box contains the following components from top to bottom:
 

- XMM Registers**: Eight 128-Bit registers.
- MXCSR Register**: A 32-Bit register.
- MMX Registers**: Eight 64-Bit registers.
- General-Purpose Registers**: Eight 32-Bit registers.
- EFLAGS Register**: A 32-Bit register.

 To the right of these registers is the **Address Space**, represented by a vertical bar. The address space ranges from  $2^{32}-1$  at the top to  $0$  at the bottom.

Diagram of the Intel SSE Execution Environment showing the hierarchy of registers and memory address space.

**Figure 10-1. Intel® SSE Execution Environment**

- **MXCSR register** — This 32-bit register (see Figure 10-3 and Section 10.2.3, “MXCSR Control and Status Register”) provides status and control bits used in SIMD floating-point operations.
- **MMX registers** — These eight registers (see Figure 9-2) are used to perform operations on 64-bit packed integer data. They are also used to hold operands for some operations performed between the MMX and XMM registers. MMX registers are referenced by the names MM0 through MM7.
- **General-purpose registers** — The eight general-purpose registers (see Figure 3-5) are used along with the existing IA-32 addressing modes to address operands in memory. (MMX and XMM registers cannot be used to

address memory). The general-purpose registers are also used to hold operands for some SSE instructions and are referenced as EAX, EBX, ECX, EDX, EBP, ESI, EDI, and ESP.

- **EFLAGS register** — This 32-bit register (see Figure 3-8) is used to record result of some compare operations.

## 10.2.1 Intel® SSE in 64-Bit Mode and Compatibility Mode

In compatibility mode, Intel SSE functions like it does in protected mode. In 64-bit mode, eight additional XMM registers are accessible. Registers XMM8-XMM15 are accessed by using REX prefixes. Memory operands are specified using the ModR/M, SIB encoding described in Section 3.7.5.

Some Intel SSE instructions may be used to operate on general-purpose registers. Use the REX.W prefix to access 64-bit general-purpose registers. Note that if a REX prefix is used when it has no meaning, the prefix is ignored.

## 10.2.2 XMM Registers

Eight 128-bit XMM data registers were introduced into the IA-32 architecture with Intel SSE (see Figure 10-2). These registers can be accessed directly using the names XMM0 to XMM7; and they can be accessed independently from the x87 FPU and MMX registers and the general-purpose registers (that is, they are not aliased to any other of the processor's registers).

![Diagram of XMM Registers showing eight 128-bit registers labeled XMM0 through XMM7, with bit positions 127 and 0 indicated.](02a799c1f5281fea2b73bdf67f128cff_img.jpg)

The diagram illustrates the XMM registers as a vertical stack of eight horizontal bars, each representing a 128-bit register. The registers are labeled XMM7 at the top and XMM0 at the bottom. Above the stack, the bit position 127 is marked on the left and 0 on the right, indicating the 128-bit width of each register.

| 127 |      | 0 |
|-----|------|---|
|     | XMM7 |   |
|     | XMM6 |   |
|     | XMM5 |   |
|     | XMM4 |   |
|     | XMM3 |   |
|     | XMM2 |   |
|     | XMM1 |   |
|     | XMM0 |   |

Diagram of XMM Registers showing eight 128-bit registers labeled XMM0 through XMM7, with bit positions 127 and 0 indicated.

Figure 10-2. XMM Registers

Intel SSE instructions use the XMM registers only to operate on packed single precision floating-point operands. SSE2 extensions expand the functions of the XMM registers to operand on packed or scalar double precision floating-point operands and packed integer operands; see Section 11.2, "Intel® SSE2 Programming Environment," and Section 12.1, "Programming Environment and Data types."

XMM registers can only be used to perform calculations on data; they cannot be used to address memory. Addressing memory is accomplished by using the general-purpose registers.

Data can be loaded into XMM registers or written from the registers to memory in 32-bit, 64-bit, and 128-bit increments. When storing the entire contents of an XMM register in memory (128-bit store), the data is stored in 16 consecutive bytes, with the low-order byte of the register being stored in the first byte in memory.

## 10.2.3 MXCSR Control and Status Register

The 32-bit MXCSR register (see Figure 10-3) contains control and status information for Intel SSE, SSE2, and SSE3 SIMD floating-point operations. This register contains:

- Flag and mask bits for SIMD floating-point exceptions.
- Rounding control field for SIMD floating-point operations.

- Flush-to-zero flag that provides a means of controlling underflow conditions on SIMD floating-point operations.
- Denormals-are-zeros flag that controls how SIMD floating-point instructions handle denormal source operands.

The contents of this register can be loaded from memory with the LDMXCSR and FXRSTOR instructions and stored in memory with STMXCSR and FXSAVE.

Bits 16 through 31 of the MXCSR register are reserved and are cleared on a power-up or reset of the processor; attempting to write a non-zero value to these bits, using either the FXRSTOR or LDMXCSR instructions, will result in a general-protection exception (#GP) being generated.

![Diagram of the MXCSR Control/Status Register showing bit fields and their functions.](9806e5b1f8174a20562453d813424803_img.jpg)

The diagram illustrates the MXCSR Control/Status Register, a 32-bit register. The bit positions are labeled at the top: 31, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0. The register is divided into two main sections. Bits 16 through 31 are labeled 'Reserved'. Bits 0 through 15 are divided into two groups. Bits 15, 14, and 13 form the Rounding Control (RC) field. Bits 12 through 7 are individual mask bits for various exceptions: Precision Mask (PM), Underflow Mask (UM), Overflow Mask (OM), Divide-by-Zero Mask (DM), Denormal Operation Mask (DMM), and Invalid Operation Mask (IM). Bits 6 through 0 are individual flag bits for the same exceptions: Precision Flag (PF), Underflow Flag (UF), Overflow Flag (OF), Divide-by-Zero Flag (DF), Denormal Flag (DMMF), and Invalid Operation Flag (IMF). A note at the bottom states: '\* The denormals-are-zeros flag was introduced in the Pentium 4 and Intel Xeon processor.'

Diagram of the MXCSR Control/Status Register showing bit fields and their functions.

Figure 10-3. MXCSR Control/Status Register

### 10.2.3.1 SIMD Floating-Point Mask and Flag Bits

Bits 0 through 5 of the MXCSR register indicate whether a SIMD floating-point exception has been detected. They are “sticky” flags. That is, after a flag is set, it remains set until explicitly cleared. To clear these flags, use the LDMXCSR or the FXRSTOR instruction to write zeroes to them.

Bits 7 through 12 provide individual mask bits for the SIMD floating-point exceptions. An exception type is masked if the corresponding mask bit is set, and it is unmasked if the bit is clear. These mask bits are set upon a power-up or reset. This causes all SIMD floating-point exceptions to be initially masked.

If LDMXCSR or FXRSTOR clears a mask bit and sets the corresponding exception flag bit, a SIMD floating-point exception will not be generated as a result of this change. The unmasked exception will be generated only upon the execution of the next SSE/SSE2/SSE3 instruction that detects the unmasked exception condition.

For more information about the use of the SIMD floating-point exception mask and flag bits, see Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions,” and Section 12.8, “Intel® SSE3, SSSE3, And Intel® SSE4 Exceptions.”

### 10.2.3.2 SIMD Floating-Point Rounding Control Field

Bits 13 and 14 of the MXCSR register (the rounding control [RC] field) control how the results of SIMD floating-point instructions are rounded. See Section 4.8.4, “Rounding,” for a description of the function and encoding of the rounding control bits.

### 10.2.3.3 Flush-To-Zero

Bit 15 (FTZ) of the MXCSR register enables the flush-to-zero mode, which controls the masked response to a SIMD floating-point underflow condition. When the underflow exception is masked and the flush-to-zero mode is enabled, the processor performs the following operations when it detects a floating-point underflow condition.

- Returns a zero result with the sign of the true result.
- Sets the precision and underflow exception flags.

If the underflow exception is not masked, the flush-to-zero bit is ignored.

The flush-to-zero mode is not compatible with IEEE Standard 754. The IEEE-mandated masked response to underflow is to deliver the denormalized result (see Section 4.8.3.2, “Normalized and Denormalized Finite Numbers”). The flush-to-zero mode is provided primarily for performance reasons. At the cost of a slight precision loss, faster execution can be achieved for applications where underflows are common and rounding the underflow result to zero can be tolerated.

The flush-to-zero bit is cleared upon a power-up or reset of the processor, disabling the flush-to-zero mode.

#### 10.2.3.4 Denormals-Are-Zeros

Bit 6 (DAZ) of the MXCSR register enables the denormals-are-zeros mode, which controls the processor’s response to a SIMD floating-point denormal operand condition. When the denormals-are-zeros flag is set, the processor converts all denormal source operands to a zero with the sign of the original operand before performing any computations on them. The processor does not set the denormal-operand exception flag (DE), regardless of the setting of the denormal-operand exception mask bit (DM); and it does not generate a denormal-operand exception if the exception is unmasked.

The denormals-are-zeros mode is not compatible with IEEE Standard 754 (see Section 4.8.3.2, “Normalized and Denormalized Finite Numbers”). The denormals-are-zeros mode is provided to improve processor performance for applications such as streaming media processing, where rounding a denormal operand to zero does not appreciably affect the quality of the processed data.

The denormals-are-zeros flag is cleared upon a power-up or reset of the processor, disabling the denormals-are-zeros mode.

The denormals-are-zeros mode was introduced in the Pentium 4 and Intel Xeon processor with the SSE2 extensions; however, it is fully compatible with the SSE SIMD floating-point instructions (that is, the denormals-are-zeros flag affects the operation of the SSE SIMD floating-point instructions). In earlier IA-32 processors and in some models of the Pentium 4 processor, this flag (bit 6) is reserved. See Section 11.6.3, “Checking for the DAZ Flag in the MXCSR Register,” for instructions for detecting the availability of this feature.

Attempting to set bit 6 of the MXCSR register on processors that do not support the DAZ flag will cause a general-protection exception (#GP). See Section 11.6.6, “Guidelines for Writing to the MXCSR Register,” for instructions for preventing such general-protection exceptions by using the MXCSR\_MASK value returned by the FXSAVE instruction.

#### 10.2.4 Compatibility of Intel® SSE with Intel® SSE2 and SSE3, MMX, and the x87 FPU

The state (XMM registers and MXCSR register) introduced into the IA-32 execution environment with Intel SSE is shared with Intel SSE2 and SSE3. Intel SSE, SSE2, and SSE3 instructions are fully compatible; they can be executed together in the same instruction stream with no need to save state when switching between instruction sets.

XMM registers are independent of the x87 FPU and MMX registers, so Intel SSE, SSE2, and SSE3 operations performed on the XMM registers can be performed in parallel with operations on the x87 FPU and MMX registers; see Section 11.6.7, “Interaction of Intel® SSE and SSE2 Instructions with x87 FPU and MMX Instructions.”

The FXSAVE and FXRSTOR instructions save and restore the SSE/SSE2/SSE3 states along with the x87 FPU and MMX state.

### 10.3 INTEL® SSE DATA TYPES

Intel SSE introduced one data type, the 128-bit packed single precision floating-point data type, to the IA-32 architecture (see Figure 10-4). This data type consists of four IEEE 32-bit single precision floating-point values packed

into a double quadword. See Figure 4-3 for the layout of a single precision floating-point value; refer to Section 4.2.2, “Floating-Point Data Types,” for a detailed description of the single precision floating-point format.

![Diagram of a 128-bit packed single precision floating-point data type. It shows a horizontal bar divided into four equal segments. Below the bar, bit positions are marked: 127 at the left end of the first segment, 96 at the boundary between the first and second segments, 64 at the boundary between the second and third segments, 32 at the boundary between the third and fourth segments, and 0 at the right end of the fourth segment. To the right of the bar, text reads 'Contains 4 Single Precision Floating-Point Values'.](6c9bacdac80f16c0a957572b9269e9c0_img.jpg)

Diagram of a 128-bit packed single precision floating-point data type. It shows a horizontal bar divided into four equal segments. Below the bar, bit positions are marked: 127 at the left end of the first segment, 96 at the boundary between the first and second segments, 64 at the boundary between the second and third segments, 32 at the boundary between the third and fourth segments, and 0 at the right end of the fourth segment. To the right of the bar, text reads 'Contains 4 Single Precision Floating-Point Values'.

**Figure 10-4. 128-Bit Packed Single Precision Floating-Point Data Type**

This 128-bit packed single precision floating-point data type is operated on in the XMM registers or in memory. Conversion instructions are provided to convert two packed single precision floating-point values into two packed doubleword integers or a scalar single precision floating-point value into a doubleword integer (see Figure 11-8).

Intel SSE provides conversion instructions between XMM registers and MMX registers, and between XMM registers and general-purpose bit registers. See Figure 11-8.

The address of a 128-bit packed memory operand must be aligned on a 16-byte boundary, except in the following cases:

- The MOVUPS instruction supports unaligned accesses.
- Scalar instructions that use a 4-byte memory operand that is not subject to alignment requirements.

Figure 4-2 shows the byte order of 128-bit (double quadword) data types in memory.

## 10.4 INTEL® SSE INSTRUCTION SET

Intel SSE instructions are divided into four functional groups:

- Packed and scalar single precision floating-point instructions.
- 64-bit SIMD integer instructions.
- State management instructions.
- Cacheability control, prefetch, and memory ordering instructions.

The following sections give an overview of each of the instructions in these groups.

### 10.4.1 Intel® SSE Packed and Scalar Floating-Point Instructions

The packed and scalar single precision floating-point instructions are divided into the following subgroups:

- Data movement instructions.
- Arithmetic instructions.
- Logical instructions.
- Comparison instructions.
- Shuffle instructions.
- Conversion instructions.

The packed single precision floating-point instructions perform SIMD operations on packed single precision floating-point operands (see Figure 10-5). Each source operand contains four single precision floating-point values, and the destination operand contains the results of the operation (OP) performed in parallel on the corresponding values (X0 and Y0, X1 and Y1, X2 and Y2, and X3 and Y3) in each operand.

![Figure 10-5: Packed Single Precision Floating-Point Operation. This diagram illustrates a SIMD (Single Instruction, Multiple Data) operation where two 128-bit registers, each containing four 32-bit single-precision floating-point values (X3, X2, X1, X0 and Y3, Y2, Y1, Y0), are processed. Each corresponding pair (e.g., X3 and Y3) is fed into an operator (OP), resulting in four separate results (X3 OP Y3, X2 OP Y2, X1 OP Y1, X0 OP Y0) stored in a destination register.](163c1efdd9ff6e8c339e8912b23e22f3_img.jpg)

```

graph TD
    subgraph X [Source 1]
        X3
        X2
        X1
        X0
    end
    subgraph Y [Source 2]
        Y3
        Y2
        Y1
        Y0
    end
    OP3((OP))
    OP2((OP))
    OP1((OP))
    OP0((OP))
    subgraph D [Destination]
        D3["X3 OP Y3"]
        D2["X2 OP Y2"]
        D1["X1 OP Y1"]
        D0["X0 OP Y0"]
    end
    X3 --> OP3
    Y3 --> OP3
    OP3 --> D3
    X2 --> OP2
    Y2 --> OP2
    OP2 --> D2
    X1 --> OP1
    Y1 --> OP1
    OP1 --> D1
    X0 --> OP0
    Y0 --> OP0
    OP0 --> D0

```

Figure 10-5: Packed Single Precision Floating-Point Operation. This diagram illustrates a SIMD (Single Instruction, Multiple Data) operation where two 128-bit registers, each containing four 32-bit single-precision floating-point values (X3, X2, X1, X0 and Y3, Y2, Y1, Y0), are processed. Each corresponding pair (e.g., X3 and Y3) is fed into an operator (OP), resulting in four separate results (X3 OP Y3, X2 OP Y2, X1 OP Y1, X0 OP Y0) stored in a destination register.

**Figure 10-5. Packed Single Precision Floating-Point Operation**

The scalar single precision floating-point instructions operate on the low (least significant) doublewords of the two source operands (X0 and Y0); see Figure 10-6. The three most significant doublewords (X1, X2, and X3) of the first source operand are passed through to the destination. The scalar operations are similar to the floating-point operations performed in the x87 FPU data registers with the precision control field in the x87 FPU control word set for single precision (24-bit significand), except that x87 stack operations use a 15-bit exponent range for the result, while SSE operations use an 8-bit exponent range.

![Figure 10-6: Scalar Single Precision Floating-Point Operation. This diagram shows a scalar operation where only the lowest 32-bit doublewords (X0 and Y0) of two 128-bit registers are operated upon by an operator (OP). The result (X0 OP Y0) is placed in the lowest doubleword of the destination. The upper three doublewords of the first source operand (X3, X2, X1) are passed directly to the destination register unchanged.](a846cf46c3f742327ce6eebbfbb5ce12_img.jpg)

```

graph TD
    subgraph X [Source 1]
        X3
        X2
        X1
        X0
    end
    subgraph Y [Source 2]
        Y3
        Y2
        Y1
        Y0
    end
    OP0((OP))
    subgraph D [Destination]
        D3["X3"]
        D2["X2"]
        D1["X1"]
        D0["X0 OP Y0"]
    end
    X3 --> D3
    X2 --> D2
    X1 --> D1
    X0 --> OP0
    Y0 --> OP0
    OP0 --> D0

```

Figure 10-6: Scalar Single Precision Floating-Point Operation. This diagram shows a scalar operation where only the lowest 32-bit doublewords (X0 and Y0) of two 128-bit registers are operated upon by an operator (OP). The result (X0 OP Y0) is placed in the lowest doubleword of the destination. The upper three doublewords of the first source operand (X3, X2, X1) are passed directly to the destination register unchanged.

**Figure 10-6. Scalar Single Precision Floating-Point Operation**

### 10.4.1.1 Intel® SSE Data Movement Instructions

Intel SSE data movement instructions move single precision floating-point data between XMM registers and between an XMM register and memory.

The **MOVAPS** (move aligned packed single precision floating-point values) instruction transfers a double quadword operand containing four packed single precision floating-point values from memory to an XMM register and vice versa, or between XMM registers. The memory address must be aligned to a 16-byte boundary; otherwise, a general-protection exception (#GP) is generated.

The **MOVUPS** (move unaligned packed single precision, floating-point) instruction performs the same operations as the **MOVAPS** instruction, except that 16-byte alignment of a memory address is not required.

The **MOVSS** (move scalar single precision floating-point) instruction transfers a 32-bit single precision floating-point operand from memory to the low doubleword of an XMM register and vice versa, or between XMM registers.

The **MOVLPS** (move low packed single precision floating-point) instruction moves two packed single precision floating-point values from memory to the low quadword of an XMM register and vice versa. The high quadword of the register is left unchanged.

The MOVHPS (move high packed single precision floating-point) instruction moves two packed single precision floating-point values from memory to the high quadword of an XMM register and vice versa. The low quadword of the register is left unchanged.

The MOVLHPS (move packed single precision floating-point low to high) instruction moves two packed single precision floating-point values from the low quadword of the source XMM register into the high quadword of the destination XMM register. The low quadword of the destination register is left unchanged.

The MOVHLPS (move packed single precision floating-point high to low) instruction moves two packed single precision floating-point values from the high quadword of the source XMM register into the low quadword of the destination XMM register. The high quadword of the destination register is left unchanged.

The MOVMSKPS (move packed single precision floating-point mask) instruction transfers the most significant bit of each of the four packed single precision floating-point numbers in an XMM register to a general-purpose register. This 4-bit value can then be used as a condition to perform branching.

### 10.4.1.2 Intel® SSE Arithmetic Instructions

Intel SSE arithmetic instructions perform addition, subtraction, multiply, divide, reciprocal, square root, reciprocal of square root, and maximum/minimum operations on packed and scalar single precision floating-point values.

The ADDPS (add packed single precision floating-point values) and SUBPS (subtract packed single precision floating-point values) instructions add and subtract, respectively, two packed single precision floating-point operands.

The ADDSS (add scalar single precision floating-point values) and SUBSS (subtract scalar single precision floating-point values) instructions add and subtract, respectively, the low single precision floating-point values of two operands and store the result in the low doubleword of the destination operand.

The MULPS (multiply packed single precision floating-point values) instruction multiplies two packed single precision floating-point operands.

The MULSS (multiply scalar single precision floating-point values) instruction multiplies the low single precision floating-point values of two operands and stores the result in the low doubleword of the destination operand.

The DIVPS (divide packed, single precision floating-point values) instruction divides two packed single precision floating-point operands.

The DIVSS (divide scalar single precision floating-point values) instruction divides the low single precision floating-point values of two operands and stores the result in the low doubleword of the destination operand.

The RCPPS (compute reciprocals of packed single precision floating-point values) instruction computes the approximate reciprocals of values in a packed single precision floating-point operand.

The RCPSS (compute reciprocal of scalar single precision floating-point values) instruction computes the approximate reciprocal of the low single precision floating-point value in the source operand and stores the result in the low doubleword of the destination operand.

The SQRTPS (compute square roots of packed single precision floating-point values) instruction computes the square roots of the values in a packed single precision floating-point operand.

The SQRTSS (compute square root of scalar single precision floating-point values) instruction computes the square root of the low single precision floating-point value in the source operand and stores the result in the low doubleword of the destination operand.

The RSQRTPS (compute reciprocals of square roots of packed single precision floating-point values) instruction computes the approximate reciprocals of the square roots of the values in a packed single precision floating-point operand.

The RSQRTSS (reciprocal of square root of scalar single precision floating-point value) instruction computes the approximate reciprocal of the square root of the low single precision floating-point value in the source operand and stores the result in the low doubleword of the destination operand.

The MAXPS (return maximum of packed single precision floating-point values) instruction compares the corresponding values from two packed single precision floating-point operands and returns the numerically greater value from each comparison to the destination operand.

The MAXSS (return maximum of scalar single precision floating-point values) instruction compares the low values from two packed single precision floating-point operands and returns the numerically greater value from the comparison to the low doubleword of the destination operand.

The MINPS (return minimum of packed single precision floating-point values) instruction compares the corresponding values from two packed single precision floating-point operands and returns the numerically lesser value from each comparison to the destination operand.

The MINSS (return minimum of scalar single precision floating-point values) instruction compares the low values from two packed single precision floating-point operands and returns the numerically lesser value from the comparison to the low doubleword of the destination operand.

## 10.4.2 Intel® SSE Logical Instructions

Intel SSE logical instructions perform AND, AND NOT, OR, and XOR operations on packed single precision floating-point values.

The ANDPS (bitwise logical AND of packed single precision floating-point values) instruction returns the logical AND of two packed single precision floating-point operands.

The ANDNPS (bitwise logical AND NOT of packed single precision, floating-point values) instruction returns the logical AND NOT of two packed single precision floating-point operands.

The ORPS (bitwise logical OR of packed single precision, floating-point values) instruction returns the logical OR of two packed single precision floating-point operands.

The XORPS (bitwise logical XOR of packed single precision, floating-point values) instruction returns the logical XOR of two packed single precision floating-point operands.

### 10.4.2.1 Intel® SSE Comparison Instructions

The compare instructions compare packed and scalar single precision floating-point values and return the results of the comparison either to the destination operand or to the EFLAGS register.

The CMPPS (compare packed single precision floating-point values) instruction compares the corresponding values from two packed single precision floating-point operands, using an immediate operand as a predicate, and returns a 32-bit mask result of all 1s or all 0s for each comparison to the destination operand. The value of the immediate operand allows the selection of any of 8 compare conditions: equal, less than, less than equal, unordered, not equal, not less than, not less than or equal, or ordered.

The CMPSS (compare scalar single precision, floating-point values) instruction compares the low values from two packed single precision floating-point operands, using an immediate operand as a predicate, and returns a 32-bit mask result of all 1s or all 0s for the comparison to the low doubleword of the destination operand. The immediate operand selects the compare conditions as with the CMPPS instruction.

The COMISS (compare scalar single precision floating-point values and set EFLAGS) and UCOMISS (unordered compare scalar single precision floating-point values and set EFLAGS) instructions compare the low values of two packed single precision floating-point operands and set the ZF, PF, and CF flags in the EFLAGS register to show the result (greater than, less than, equal, or unordered). These two instructions differ as follows: the COMISS instruction signals a floating-point invalid-operation (#1) exception when a source operand is either a QNaN or an SNaN; the UCOMISS instruction only signals an invalid-operation exception when a source operand is an SNaN.

### 10.4.2.2 Intel® SSE Shuffle and Unpack Instructions

Intel SSE shuffle and unpack instructions shuffle or interleave the contents of two packed single precision floating-point values and store the results in the destination operand.

The SHUFPS (shuffle packed single precision floating-point values) instruction places any two of the four packed single precision floating-point values from the destination operand into the two low-order doublewords of the destination operand, and places any two of the four packed single precision floating-point values from the source operand in the two high-order doublewords of the destination operand (see Figure 10-7). By using the same register for the source and destination operands, the SHUFPS instruction can shuffle four single precision floating-point values into any order.

![Diagram of SHUFPS instruction showing a packed shuffle operation.](3f5d468bbb8699481bd414901aacea4f_img.jpg)

The diagram illustrates the SHUFPS instruction's packed shuffle operation. It shows three rows of 4-element registers. The top row, labeled 'DEST', contains elements X3, X2, X1, and X0. The middle row, labeled 'SRC', contains elements Y3, Y2, Y1, and Y0. The bottom row, also labeled 'DEST', shows the result: the first two elements are 'Y3 ... Y0' and the last two are 'X3 ... X0'. Arrows indicate the mapping: X1 from the top DEST maps to the first 'Y3 ... Y0' in the bottom DEST; X2 from the top DEST maps to the second 'Y3 ... Y0'; Y1 from the SRC maps to the first 'X3 ... X0'; and Y0 from the SRC maps to the second 'X3 ... X0'.

Diagram of SHUFPS instruction showing a packed shuffle operation.

Figure 10-7. SHUFPS Instruction, Packed Shuffle Operation

The UNPCKHPS (unpack and interleave high packed single precision floating-point values) instruction performs an interleaved unpack of the high-order single precision floating-point values from the source and destination operands and stores the result in the destination operand (see Figure 10-8).

![Diagram of UNPCKHPS instruction showing high unpack and interleave operation.](e8548116529ee9e05c70ce229d67d749_img.jpg)

The diagram illustrates the UNPCKHPS instruction's high unpack and interleave operation. It shows three rows of 4-element registers. The top row, labeled 'DEST', contains X3, X2, X1, and X0. The middle row, labeled 'SRC', contains Y3, Y2, Y1, and Y0. The bottom row, labeled 'DEST', shows the result: Y3, X3, Y2, and X2. Arrows show the mapping: X3 from the top DEST maps to X3 in the bottom DEST; X2 from the top DEST maps to X2; Y3 from the SRC maps to Y3; and Y2 from the SRC maps to Y2.

Diagram of UNPCKHPS instruction showing high unpack and interleave operation.

Figure 10-8. UNPCKHPS Instruction, High Unpack and Interleave Operation

The UNPCKLPS (unpack and interleave low packed single precision floating-point values) instruction performs an interleaved unpack of the low-order single precision floating-point values from the source and destination operands and stores the result in the destination operand (see Figure 10-9).

![Diagram of UNPCKLPS instruction showing low unpack and interleave operation.](2835c2dd5ab71883db91a57d891f299a_img.jpg)

The diagram illustrates the UNPCKLPS instruction's low unpack and interleave operation. It shows three rows of 4-element registers. The top row, labeled 'DEST', contains X3, X2, X1, and X0. The middle row, labeled 'SRC', contains Y3, Y2, Y1, and Y0. The bottom row, labeled 'DEST', shows the result: Y1, X1, Y0, and X0. Arrows show the mapping: X1 from the top DEST maps to X1; X0 from the top DEST maps to X0; Y1 from the SRC maps to Y1; and Y0 from the SRC maps to Y0.

Diagram of UNPCKLPS instruction showing low unpack and interleave operation.

Figure 10-9. UNPCKLPS Instruction, Low Unpack and Interleave Operation

### 10.4.3 Intel® SSE Conversion Instructions

Intel SSE conversion instructions (see Figure 11-8) support packed and scalar conversions between single precision floating-point and doubleword integer formats.

The CVTPI2PS (convert packed doubleword integers to packed single precision floating-point values) instruction converts two packed signed doubleword integers into two packed single precision floating-point values. When the conversion is inexact, the result is rounded according to the rounding mode selected in the MXCSR register.

The CVTSI2SS (convert signed integer to scalar single precision floating-point value) instruction converts a signed doubleword or quadword integer into a single precision floating-point value. When the conversion is inexact, the result is rounded according to the rounding mode selected in the MXCSR register.

The CVTSP2PI (convert packed single precision floating-point values to packed doubleword integers) instruction converts two packed single precision floating-point values into two packed signed doubleword integers. When the conversion is inexact, the result is rounded according to the rounding mode selected in the MXCSR register. The CVTTPS2PI (convert with truncation packed single precision floating-point values to packed doubleword integers) instruction is similar to the CVTSP2PI instruction, except that truncation is used to round a source value to an integer value; see Section 4.8.4.2, “Truncation with Intel® SSE, SSE2, and AVX Conversion Instructions.”

The CVTSS2SI (convert scalar single precision floating-point value to signed integer) instruction converts a single precision floating-point value into a signed integer. When the conversion is inexact, the result is rounded according to the rounding mode selected in the MXCSR register. The CVTTSS2SI (convert with truncation scalar single precision floating-point value to signed integer) instruction is similar to the CVTSS2SI instruction, except that truncation is used to round the source value to an integer value; see Section 4.8.4.2, “Truncation with Intel® SSE, SSE2, and AVX Conversion Instructions.”

### 10.4.4 Intel® SSE 64-Bit SIMD Integer Instructions

Intel SSE adds the following 64-bit packed integer instructions to the IA-32 architecture. These instructions operate on data in MMX registers and 64-bit memory locations.

#### NOTE

When Intel SSE2 is present in an IA-32 processor, these instructions are extended to operate on 128-bit operands in XMM registers and 128-bit memory locations.

The PAVGB (compute average of packed unsigned byte integers) and PAVGW (compute average of packed unsigned word integers) instructions compute a SIMD average of two packed unsigned byte or word integer operands, respectively. For each corresponding pair of data elements in the packed source operands, the elements are added together, a 1 is added to the temporary sum, and that result is shifted right one bit position.

The PEXTRW (extract word) instruction copies a selected word from an MMX register into a general-purpose register.

The PINSRW (insert word) instruction copies a word from a general-purpose register or from memory into a selected word location in an MMX register.

The PMAUB (maximum of packed unsigned byte integers) instruction compares the corresponding unsigned byte integers in two packed operands and returns the greater of each comparison to the destination operand.

The PMINUB (minimum of packed unsigned byte integers) instruction compares the corresponding unsigned byte integers in two packed operands and returns the lesser of each comparison to the destination operand.

The PMAWSW (maximum of packed signed word integers) instruction compares the corresponding signed word integers in two packed operands and returns the greater of each comparison to the destination operand.

The PMINSW (minimum of packed signed word integers) instruction compares the corresponding signed word integers in two packed operands and returns the lesser of each comparison to the destination operand.

The PMOVMASKB (move byte mask) instruction creates an 8-bit mask from the packed byte integers in an MMX register and stores the result in the low byte of a general-purpose register. The mask contains the most significant bit of each byte in the MMX register. (When operating on 128-bit operands, a 16-bit mask is created.)

The PMULHUW (multiply packed unsigned word integers and store high result) instruction performs a SIMD unsigned multiply of the words in the two source operands and returns the high word of each result to an MMX register.

The PSADBW (compute sum of absolute differences) instruction computes the SIMD absolute differences of the corresponding unsigned byte integers in two source operands, sums the differences, and stores the sum in the low word of the destination operand.

The PSHUFW (shuffle packed word integers) instruction shuffles the words in the source operand according to the order specified by an 8-bit immediate operand and returns the result to the destination operand.

## 10.4.5 MXCSR State Management Instructions

The MXCSR state management instructions (LDMXCSR and STMXCSR) load and save the state of the MXCSR register, respectively. The LDMXCSR instruction loads the MXCSR register from memory, while the STMXCSR instruction stores the contents of the register to memory.

## 10.4.6 Cacheability Control, Prefetch, and Memory Ordering Instructions

Intel SSE introduced several new instructions to give programs more control over the caching of data. They also introduces the PREFETCH $h$  instructions, which provide the ability to prefetch data to a specified cache level, and the SFENCE instruction, which enforces program ordering on stores. These instructions are described in the following sections.

### 10.4.6.1 Cacheability Control Instructions

The following three instructions enable data from the MMX and XMM registers to be stored to memory using a non-temporal hint. The non-temporal hint directs the processor to store the data to memory without writing the data into the cache hierarchy. See Section 10.4.6.2, “Caching of Temporal vs. Non-Temporal Data,” for information about non-temporal stores and hints.

The MOVNTQ (store quadword using non-temporal hint) instruction stores packed integer data from an MMX register to memory, using a non-temporal hint.

The MOVNTPS (store packed single precision floating-point values using non-temporal hint) instruction stores packed floating-point data from an XMM register to memory, using a non-temporal hint.

The MASKMOVQ (store selected bytes of quadword) instruction stores selected byte integers from an MMX register to memory, using a byte mask to selectively write the individual bytes. This instruction also uses a non-temporal hint.

### 10.4.6.2 Caching of Temporal vs. Non-Temporal Data

Data referenced by a program can be temporal (data will be used again) or non-temporal (data will be referenced once and not reused in the immediate future). For example, program code is generally temporal, whereas, multi-media data, such as the display list in a 3-D graphics application, is often non-temporal. To make efficient use of the processor’s caches, it is generally desirable to cache temporal data and not cache non-temporal data. Overloading the processor’s caches with non-temporal data is sometimes referred to as “polluting the caches.” The Intel SSE and SSE2 cacheability control instructions enable a program to write non-temporal data to memory in a manner that minimizes pollution of caches.

These Intel SSE and SSE2 non-temporal store instructions minimize cache pollutions by treating the memory being accessed as the write combining (WC) type. If a program specifies a non-temporal store with one of these instructions and the memory type of the destination region is write back (WB), write through (WT), or write combining (WC), the processor will do the following:

- If the memory location being written to is present in the cache hierarchy, the data in the caches is evicted.<sup>1</sup>

1. Some older CPU implementations (e.g., Pentium M) allowed addresses being written with a non-temporal store instruction to be updated in-place if the memory type was not WC and line was already in the cache.

- The non-temporal data is written to memory with WC semantics.

See also: Chapter 14, “Memory Cache Control,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A.

Using the WC semantics, the store transaction will be weakly ordered, meaning that the data may not be written to memory in program order, and the store will not write allocate (that is, the processor will not fetch the corresponding cache line into the cache hierarchy, prior to performing the store). Also, different processor implementations may choose to collapse and combine these stores.

The memory type of the region being written to can override the non-temporal hint, if the memory address specified for the non-temporal store is in uncacheable memory. Uncacheable as referred to here means that the region being written to has been mapped with either an uncacheable (UC) or write protected (WP) memory type.

In general, WC semantics require software to ensure coherence, with respect to other processors and other system agents (such as graphics cards). Appropriate use of synchronization and fencing must be performed for producer-consumer usage models. Fencing ensures that all system agents have global visibility of the stored data; for instance, failure to fence may result in a written cache line staying within a processor and not being visible to other agents.

The memory type visible on the bus in the presence of memory type aliasing is implementation specific. As one possible example, the memory type written to the bus may reflect the memory type for the first store to this line, as seen in program order; other alternatives are possible. This behavior should be considered reserved, and dependence on the behavior of any particular implementation risks future incompatibility.

### NOTE

Some older CPU implementations (e.g., Pentium M) may implement non-temporal stores by updating in place data that already reside in the cache hierarchy. For such processors, the destination region should also be mapped as WC. If mapped as WB or WT, there is the potential for speculative processor reads to bring the data into the caches; in this case, non-temporal stores would then update in place, and data would not be flushed from the processor by a subsequent fencing operation.

### 10.4.6.3 PREFETCHh Instructions

The **PREFETCHh** instructions permit programs to load data into the processor at a suggested cache level, so that the data is closer to the processor’s load and store unit when it is needed. These instructions fetch 32 aligned bytes (or more, depending on the implementation) containing the addressed byte to a location in the cache hierarchy specified by the temporal locality hint (see Table 10-1). In this table, the first-level cache is closest to the processor and second-level cache is farther away from the processor than the first-level cache. The hints specify a prefetch of either temporal or non-temporal data (see Section 10.4.6.2, “Caching of Temporal vs. Non-Temporal Data”). Subsequent accesses to temporal data are treated like normal accesses, while those to non-temporal data will continue to minimize cache pollution. If the data is already present at a level of the cache hierarchy that is closer to the processor, the **PREFETCHh** instruction will not result in any data movement. The **PREFETCHh** instructions do not affect functional behavior of the program.

See Section 11.6.13, “Cacheability Hint Instructions,” for additional information about the **PREFETCHh** instructions.

**Table 10-1. PREFETCHh Instructions Caching Hints**

| <b>PREFETCHh Instruction Mnemonic</b> | <b>Actions</b>                                                                                                                                                                                                                          |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PREFETCHT0                            | Temporal data—fetch data into all levels of cache hierarchy: <ul style="list-style-type: none"> <li>▪ Pentium III processor—1st-level cache or 2nd-level cache</li> <li>▪ Pentium 4 and Intel Xeon processor—2nd-level cache</li> </ul> |
| PREFETCHT1                            | Temporal data—fetch data into level 2 cache and higher <ul style="list-style-type: none"> <li>▪ Pentium III processor—2nd-level cache</li> <li>▪ Pentium 4 and Intel Xeon processor—2nd-level cache</li> </ul>                          |

Table 10-1. PREFETCHh Instructions Caching Hints (Contd.)

| PREFETCHh Instruction Mnemonic | Actions                                                                                                                                                                                                                                            |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PREFETCHT2                     | Temporal data—fetch data into level 2 cache and higher <ul style="list-style-type: none"><li>▪ Pentium III processor—2nd-level cache</li><li>▪ Pentium 4 and Intel Xeon processor—2nd-level cache</li></ul>                                        |
| PREFETCHNTA                    | Non-temporal data—fetch data into location close to the processor, minimizing cache pollution <ul style="list-style-type: none"><li>▪ Pentium III processor—1st-level cache</li><li>▪ Pentium 4 and Intel Xeon processor—2nd-level cache</li></ul> |

10.4.6.4 SFENCE Instruction

The SFENCE (Store Fence) instruction controls write ordering by creating a fence for memory store operations. This instruction guarantees that the result of every store instruction that precedes the store fence in program order is globally visible before any store instruction that follows the fence. The SFENCE instruction provides an efficient way of ensuring ordering between procedures that produce weakly-ordered data and procedures that consume that data.

10.5 FXSAVE AND FXRSTOR INSTRUCTIONS

The FXSAVE and FXRSTOR instructions were introduced into the IA-32 architecture in the Pentium II processor family (prior to the introduction of the SSE extensions). The original versions of these instructions performed a fast save and restore, respectively, of the x87 execution environment (**x87 state**). (By saving the state of the x87 FPU data registers, the FXSAVE and FXRSTOR instructions implicitly save and restore the state of the MMX registers.)

The SSE extensions expanded the scope of these instructions to save and restore the states of the XMM registers and the MXCSR register (**SSE state**), along with x87 state.

The FXSAVE and FXRSTOR instructions can be used in place of the FSAVE/FNSAVE and FRSTOR instructions; however, the operation of the FXSAVE and FXRSTOR instructions are not identical to the operation of FSAVE/FNSAVE and FRSTOR.

NOTE

The FXSAVE and FXRSTOR instructions are not considered part of the SSE instruction group. They have a separate CPUID feature bit to indicate whether they are present (if CPUID.01H:EDX.FXSR[24] = 1). The CPUID feature bit for SSE extensions does not indicate the presence of FXSAVE and FXRSTOR.

The FXSAVE and FXRSTOR instructions organize x87 state and SSE state in a region of memory called the **FXSAVE area**. Section 10.5.1 provides details of the FXSAVE area and its format. Section 10.5.2 describes operation of FXSAVE, and Section 10.5.3 describes the operation of FXRSTOR.

10.5.1 FXSAVE Area

The FXSAVE and FXRSTOR instructions organize x87 state and SSE state in a region of memory called the **FXSAVE area**. Each of the instructions takes a memory operand that specifies the 16-byte aligned base address of the FXSAVE area on which it operates.

Every FXSAVE area comprises the 512 bytes starting at the area's base address. Table 10-2 illustrates the format of the first 416 bytes of the legacy region of an FXSAVE area.

**Table 10-2. Format of an FXSAVE Area**

| 15 14      | 13 12                      | 11 10            | 9 8     | 7 6      | 5                             | 4   | 3 2              | 1 0 |            |  |  |  |  |  |  |  |  |  |  |
|------------|----------------------------|------------------|---------|----------|-------------------------------|-----|------------------|-----|------------|--|--|--|--|--|--|--|--|--|--|
| Reserved   | CS or FPU<br>IP bits 63:32 | FPU IP bits 31:0 |         | FOP      | Rsvd.                         | FTW | FSW              | FCW | <b>0</b>   |  |  |  |  |  |  |  |  |  |  |
| MXCSR_MASK |                            | MXCSR            |         | Reserved | DS or<br>FPU DP<br>bits 63:32 |     | FPU DP bits 31:0 |     | <b>16</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST0/MM0 |          |                               |     |                  |     | <b>32</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST1/MM1 |          |                               |     |                  |     | <b>48</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST2/MM2 |          |                               |     |                  |     | <b>64</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST3/MM3 |          |                               |     |                  |     | <b>80</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST4/MM4 |          |                               |     |                  |     | <b>96</b>  |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST5/MM5 |          |                               |     |                  |     | <b>112</b> |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST6/MM6 |          |                               |     |                  |     | <b>128</b> |  |  |  |  |  |  |  |  |  |  |
| Reserved   |                            |                  | ST7/MM7 |          |                               |     |                  |     | <b>144</b> |  |  |  |  |  |  |  |  |  |  |
| XMM0       |                            |                  |         |          |                               |     |                  |     | <b>160</b> |  |  |  |  |  |  |  |  |  |  |
| XMM1       |                            |                  |         |          |                               |     |                  |     | <b>176</b> |  |  |  |  |  |  |  |  |  |  |
| XMM2       |                            |                  |         |          |                               |     |                  |     | <b>192</b> |  |  |  |  |  |  |  |  |  |  |
| XMM3       |                            |                  |         |          |                               |     |                  |     | <b>208</b> |  |  |  |  |  |  |  |  |  |  |
| XMM4       |                            |                  |         |          |                               |     |                  |     | <b>224</b> |  |  |  |  |  |  |  |  |  |  |
| XMM5       |                            |                  |         |          |                               |     |                  |     | <b>240</b> |  |  |  |  |  |  |  |  |  |  |
| XMM6       |                            |                  |         |          |                               |     |                  |     | <b>256</b> |  |  |  |  |  |  |  |  |  |  |
| XMM7       |                            |                  |         |          |                               |     |                  |     | <b>272</b> |  |  |  |  |  |  |  |  |  |  |
| XMM8       |                            |                  |         |          |                               |     |                  |     | <b>288</b> |  |  |  |  |  |  |  |  |  |  |
| XMM9       |                            |                  |         |          |                               |     |                  |     | <b>304</b> |  |  |  |  |  |  |  |  |  |  |
| XMM10      |                            |                  |         |          |                               |     |                  |     | <b>320</b> |  |  |  |  |  |  |  |  |  |  |
| XMM11      |                            |                  |         |          |                               |     |                  |     | <b>336</b> |  |  |  |  |  |  |  |  |  |  |
| XMM12      |                            |                  |         |          |                               |     |                  |     | <b>352</b> |  |  |  |  |  |  |  |  |  |  |
| XMM13      |                            |                  |         |          |                               |     |                  |     | <b>368</b> |  |  |  |  |  |  |  |  |  |  |
| XMM14      |                            |                  |         |          |                               |     |                  |     | <b>384</b> |  |  |  |  |  |  |  |  |  |  |
| XMM15      |                            |                  |         |          |                               |     |                  |     | <b>400</b> |  |  |  |  |  |  |  |  |  |  |

The x87 state component comprises bytes 23:0 and bytes 159:32. The SSE state component comprises bytes 31:24 and bytes 415:160. FXSAVE and FXRSTOR do not use bytes 511:416; bytes 463:416 are reserved. Section 10.5.2 and Section 10.5.3 provide details of how FXSAVE and FXRSTOR use an FXSAVE area.

### 10.5.1.1 x87 State

Table 10-2 illustrates how FXSAVE and FXRSTOR organize x87 state and SSE state; the x87 state is listed below, along with details of its interactions with FXSAVE and FXRSTOR:

- Bytes 1:0, 3:2, and 7:6 are used for x87 FPU Control Word (FCW), x87 FPU Status Word (FSW), and x87 FPU Opcode (FOP), respectively.

- Byte 4 is used for an abridged version of the x87 FPU Tag Word (FTW). The following items describe its usage:
  - For each  $j$ ,  $0 \leq j \leq 7$ , FXSAVE saves a 0 into bit  $j$  of byte 4 if x87 FPU data register  $ST_j$  has an empty tag; otherwise, FXSAVE saves a 1 into bit  $j$  of byte 4.
  - For each  $j$ ,  $0 \leq j \leq 7$ , FXRSTOR establishes the tag value for x87 FPU data register  $ST_j$  as follows. If bit  $j$  of byte 4 is 0, the tag for  $ST_j$  in the tag register for that data register is marked empty (11B); otherwise, the x87 FPU sets the tag for  $ST_j$  based on the value being loaded into that register (see below).
- Bytes 15:8 are used as follows:
  - If the instruction has no REX prefix, or if  $REX.W = 0$ :
    - Bytes 11:8 are used for bits 31:0 of the x87 FPU Instruction Pointer Offset (FIP).
    - If  $CPUID.07H.00H:EBX[13] = 0$ , bytes 13:12 are used for x87 FPU Instruction Pointer Selector (FPU CS). Otherwise, the processor deprecates the FPU CS value: FXSAVE saves it as 0000H.
    - Bytes 15:14 are not used.
  - If the instruction has a REX prefix with  $REX.W = 1$ , bytes 15:8 are used for the full 64 bits of FIP.
- Bytes 23:16 are used as follows:
  - If the instruction has no REX prefix, or if  $REX.W = 0$ :
    - Bytes 19:16 are used for bits 31:0 of the x87 FPU Data Pointer Offset (FDP).
    - If  $CPUID.07H.00H:EBX[13] = 0$ , bytes 21:20 are used for x87 FPU Data Pointer Selector (FPU DS). Otherwise, the processor deprecates the FPU DS value: FXSAVE saves it as 0000H.
    - Bytes 23:22 are not used.
  - If the instruction has a REX prefix with  $REX.W = 1$ , bytes 23:16 are used for the full 64 bits of FDP.
- Bytes 31:24 are used for SSE state (see Section 10.5.1.2).
- Bytes 159:32 are used for the registers  $ST_0$ – $ST_7$  ( $MM_0$ – $MM_7$ ). Each of the 8 registers is allocated a 128-bit region, with the low 80 bits used for the register and the upper 48 bits unused.

### 10.5.1.2 SSE State

Table 10-2 illustrates how FXSAVE and FXRSTOR organize x87 state and SSE state; the SSE state is listed below, along with details of its interactions with FXSAVE and FXRSTOR:

- Bytes 23:0 are used for x87 state (see Section 10.5.1.1).
- Bytes 27:24 are used for the MXCSR register. FXRSTOR generates a general-protection fault (#GP) in response to an attempt to set any of the reserved bits in the MXCSR register.
- Bytes 31:28 are used for the MXCSR\_MASK value. FXRSTOR ignores this field.
- Bytes 159:32 are used for x87 state.
- Bytes 287:160 are used for the registers  $XMM_0$ – $XMM_7$ .
- Bytes 415:288 are used for the registers  $XMM_8$ – $XMM_{15}$ . These fields are used only in 64-bit mode. Executions of FXSAVE outside 64-bit mode do not write to these bytes; executions of FXRSTOR outside 64-bit mode do not read these bytes and do not update  $XMM_8$ – $XMM_{15}$ .

If  $CR4.OSFXSR = 0$ , FXSAVE and FXRSTOR may or may not operate on SSE state; this behavior is implementation dependent. Moreover, SSE instructions cannot be used unless  $CR4.OSFXSR = 1$ .

## 10.5.2 Operation of FXSAVE

The FXSAVE instruction takes a single memory operand, which is an FXSAVE area. The instruction stores x87 state and SSE state to the FXSAVE area. See Section 10.5.1.1 and Section 10.5.1.2 for details regarding mode-specific operation and operation determined by instruction prefixes.

### 10.5.3 Operation of FXRSTOR

The FXRSTOR instruction takes a single memory operand, which is an FXSAVE area. If the value at bytes 27:24 of the FXSAVE area is not a legal value for the MXCSR register (e.g., the value sets reserved bits), execution of FXRSTOR results in a general-protection fault (#GP). Otherwise, the instruction loads x87 state and SSE state from the FXSAVE area. See Section 10.5.1.1 and Section 10.5.1.2 for details regarding mode-specific operation and operation determined by instruction prefixes.

## 10.6 HANDLING INTEL® SSE INSTRUCTION EXCEPTIONS

See Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions,” for a detailed discussion of the general and SIMD floating-point exceptions that can be generated with the Intel SSE instructions and for guidelines for handling these exceptions when they occur.

## 10.7 WRITING APPLICATIONS WITH INTEL® SSE

See Section 11.6, “Writing Applications with Intel® SSE and SSE2,” for additional information about writing applications and operating-system code using Intel SSE.


