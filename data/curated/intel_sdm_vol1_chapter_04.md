---
architecture: x86_32
component: data_types
mode: protected
tags: ['data_types', 'addressing_modes', 'floating_point']
source: intel_sdm_vol1_chapter_4.md
---

# Intel SDM Volume 1 - Chapter 4


## 4.1 FUNDAMENTAL DATA TYPES

The fundamental data types are bytes, words, doublewords, quadwords, and double quadwords (see Figure 4-1). A byte is eight bits, a word is 2 bytes (16 bits), a doubleword is 4 bytes (32 bits), a quadword is 8 bytes (64 bits), and a double quadword is 16 bytes (128 bits). A subset of the IA-32 architecture instructions operates on these fundamental data types without any additional operand typing.

![Diagram illustrating the fundamental data types: Byte, Word, Doubleword, Quadword, and Double Quadword, showing their bit ranges and memory addresses.](28f2f470a7b2446ae5f525123534383c_img.jpg)

The diagram illustrates the fundamental data types and their memory layout. It shows the bit ranges and memory addresses for each type, starting from address N:

- Byte:** Bits 7 to 0, located at address N.
- Word:** Bits 15 to 0, located at address N. It is composed of a High Byte (bits 15 to 8) and a Low Byte (bits 7 to 0).
- Doubleword:** Bits 31 to 0, located at address N. It is composed of a High Word (bits 31 to 16) and a Low Word (bits 15 to 0).
- Quadword:** Bits 63 to 0, located at address N. It is composed of a High Doubleword (bits 63 to 32) and a Low Doubleword (bits 31 to 0).
- Double Quadword:** Bits 127 to 0, located at address N. It is composed of a High Quadword (bits 127 to 64) and a Low Quadword (bits 63 to 0).

Diagram illustrating the fundamental data types: Byte, Word, Doubleword, Quadword, and Double Quadword, showing their bit ranges and memory addresses.

Figure 4-1. Fundamental Data Types

The quadword data type was introduced into the IA-32 architecture in the Intel486 processor; the double quadword data type was introduced in the Pentium III processor with the Intel SSE extensions.

Figure 4-2 shows the byte order of each of the fundamental data types when referenced as operands in memory. The low byte (bits 0 through 7) of each data type occupies the lowest address in memory and that address is also the address of the operand.

![Diagram illustrating memory alignment for various data types. A central vertical column shows addresses from 0H to FH in 2H increments. To the left, specific data types are shown at specific addresses: a byte at 9H (1FH), words at 6H (230BH), 2H (74CBH), and 1H (CB31H). To the right, larger data types are shown: a doubleword at AH (7AFE0636H), a quadword at 6H (7AFE06361FA4230BH), and a double quadword at 0H (4E127AFE06361FA4230B456774CB311). Arrows indicate the size of each data type relative to the address boundaries.](f4fdce3ce1c0fd291f31813f83d0d0d3_img.jpg)

|     |    |
|-----|----|
| 4EH | FH |
| 12H | EH |
| 7AH | DH |
| FEH | CH |
| 06H | BH |
| 36H | AH |
| 1FH | 9H |
| A4H | 8H |
| 23H | 7H |
| 0BH | 6H |
| 45H | 5H |
| 67H | 4H |
| 74H | 3H |
| CBH | 2H |
| 31H | 1H |
| 12H | 0H |

Diagram illustrating memory alignment for various data types. A central vertical column shows addresses from 0H to FH in 2H increments. To the left, specific data types are shown at specific addresses: a byte at 9H (1FH), words at 6H (230BH), 2H (74CBH), and 1H (CB31H). To the right, larger data types are shown: a doubleword at AH (7AFE0636H), a quadword at 6H (7AFE06361FA4230BH), and a double quadword at 0H (4E127AFE06361FA4230B456774CB311). Arrows indicate the size of each data type relative to the address boundaries.

Figure 4-2. Bytes, Words, Doublewords, Quadwords, and Double Quadwords in Memory

### 4.1.1 Alignment of Words, Doublewords, Quadwords, and Double Quadwords

Words, doublewords, and quadwords do not need to be aligned in memory on natural boundaries. The natural boundaries for words, doublewords, and quadwords are even-numbered addresses, addresses evenly divisible by four, and addresses evenly divisible by eight, respectively. However, to improve the performance of programs, data structures (especially stacks) should be aligned on natural boundaries whenever possible. The reason for this is that the processor requires two memory accesses to make an unaligned memory access; aligned accesses require only one memory access. A word or doubleword operand that crosses a 4-byte boundary or a quadword operand that crosses an 8-byte boundary is considered unaligned and requires two separate memory bus cycles for access.

Some instructions that operate on double quadwords require memory operands to be aligned on a natural boundary. These instructions generate a general-protection exception (#GP) if an unaligned operand is specified. A natural boundary for a double quadword is any address evenly divisible by 16. Other instructions that operate on double quadwords permit unaligned access (without generating a general-protection exception). However, additional memory bus cycles are required to access unaligned data from memory.

## 4.2 NUMERIC DATA TYPES

Although bytes, words, and doublewords are fundamental data types, some instructions support additional interpretations of these data types to allow operations to be performed on numeric data types (signed and unsigned integers, and floating-point numbers). Single precision (32-bit) floating-point and double precision (64-bit) floating-point data types are supported across all generations of Intel SSE extensions and Intel AVX extensions. The half precision (16-bit) floating-point data type was supported only with F16C extensions (VCVTPH2PS and VCVTPS2PH) beginning with the third generation of Intel® Core™ processors based on Ivy Bridge microarchitecture. Starting with the 4th generation Intel® Xeon® Scalable Processor Family, an Intel® AVX-512 instruction set architecture (ISA) for FP16 was added, supporting a wide range of general-purpose numeric operations for 16-bit half precision floating-point values (binary16 in IEEE Standard 754-2019 for Floating-Point Arithmetic, aka half precision or FP16), which complements the existing 32-bit and 64-bit floating-point instructions already available in the Intel Xeon processor-based products. This ISA also provides complex-valued native hardware support for half precision floating-point. See Figure 4-3.

![Figure 4-3: Numeric Data Types. A diagram showing the bit layouts for various Intel numeric data types. Unsigned integers (Byte, Word, Doubleword, Quadword) are shown as simple rectangles with bit ranges from 0 to 7, 15, 31, and 63 respectively. Signed integers (Byte, Word, Doubleword, Quadword) show a 'Sign' bit at the most significant position (bit 7, 15, 31, or 63). Floating-point types (Half Precision, Single Precision, Double Precision, Double Extended Precision) show a 'Sign' bit and an 'Integer Bit' field. The Double Extended Precision type has a Sign bit at bit 79 and an Integer Bit field from bit 64 to bit 62.](775d698643bcbd76feaf24ee29e5ed31_img.jpg)

Figure 4-3 illustrates the bit layouts for various numeric data types. The diagram is organized into three main sections: Unsigned Integers, Signed Integers, and Floating-Point numbers.

- Unsigned Integers:**
  - Byte Unsigned Integer:** A single rectangle representing bits 0 to 7.
  - Word Unsigned Integer:** A rectangle representing bits 0 to 15.
  - Doubleword Unsigned Integer:** A rectangle representing bits 0 to 31.
  - Quadword Unsigned Integer:** A rectangle representing bits 0 to 63.
- Signed Integers:**
  - Byte Signed Integer:** A rectangle representing bits 0 to 7, with a 'Sign' bit at bit 7.
  - Word Signed Integer:** A rectangle representing bits 0 to 15, with a 'Sign' bit at bit 15.
  - Doubleword Signed Integer:** A rectangle representing bits 0 to 31, with a 'Sign' bit at bit 31.
  - Quadword Signed Integer:** A rectangle representing bits 0 to 63, with a 'Sign' bit at bit 63.
- Floating-Point Numbers:**
  - Half Precision Floating Point:** A rectangle representing bits 0 to 15, with a 'Sign' bit at bit 15 and an 'Integer Bit' field from bit 14 to bit 9.
  - Single Precision Floating Point:** A rectangle representing bits 0 to 31, with a 'Sign' bit at bit 31 and an 'Integer Bit' field from bit 30 to bit 22.
  - Double Precision Floating Point:** A rectangle representing bits 0 to 63, with a 'Sign' bit at bit 63 and an 'Integer Bit' field from bit 62 to bit 51.
  - Double Extended Precision Floating Point:** A rectangle representing bits 0 to 79, with a 'Sign' bit at bit 79 and an 'Integer Bit' field from bit 64 to bit 62.

Figure 4-3: Numeric Data Types. A diagram showing the bit layouts for various Intel numeric data types. Unsigned integers (Byte, Word, Doubleword, Quadword) are shown as simple rectangles with bit ranges from 0 to 7, 15, 31, and 63 respectively. Signed integers (Byte, Word, Doubleword, Quadword) show a 'Sign' bit at the most significant position (bit 7, 15, 31, or 63). Floating-point types (Half Precision, Single Precision, Double Precision, Double Extended Precision) show a 'Sign' bit and an 'Integer Bit' field. The Double Extended Precision type has a Sign bit at bit 79 and an Integer Bit field from bit 64 to bit 62.

Figure 4-3. Numeric Data Types

## 4.2.1 Integers

The Intel 64 and IA-32 architectures define two types of integers: unsigned and signed. Unsigned integers are ordinary binary values ranging from 0 to the maximum positive number that can be encoded in the selected operand size. Signed integers are two's complement binary values that can be used to represent both positive and negative integer values.

Some integer instructions (such as the ADD, SUB, PADDB, and PSUBB instructions) operate on either unsigned or signed integer operands. Other integer instructions (such as IMUL, MUL, IDIV, DIV, FIADD, and FISUB) operate on only one integer type.

The following sections describe the encodings and ranges of the two types of integers.

### 4.2.1.1 Unsigned Integers

Unsigned integers are unsigned binary numbers contained in a byte, word, doubleword, and quadword. Their values range from 0 to 255 for an unsigned byte integer, from 0 to 65,535 for an unsigned word integer, from 0

to  $2^{32} - 1$  for an unsigned doubleword integer, and from 0 to  $2^{64} - 1$  for an unsigned quadword integer. Unsigned integers are sometimes referred to as **ordinals**.

4.2.1.2 Signed Integers

Signed integers are signed binary numbers held in a byte, word, doubleword, or quadword. All operations on signed integers assume a two's complement representation. The sign bit is located in bit 7 in a byte integer, bit 15 in a word integer, bit 31 in a doubleword integer, and bit 63 in a quadword integer (see the signed integer encodings in Table 4-1).

Table 4-1. Signed Integer Encodings

| Class              |          | Two's Complement Encoding  |             |
|--------------------|----------|----------------------------|-------------|
|                    |          | Sign                       |             |
| Positive           | Largest  | 0                          | 11..11      |
|                    |          | .                          | .           |
|                    | Smallest | 0                          | 00..01      |
| Zero               |          | 0                          | 00..00      |
| Negative           | Smallest | 1                          | 11..11      |
|                    |          | .                          | .           |
|                    | Largest  | 1                          | 00..00      |
| Integer indefinite |          | 1                          | 00..00      |
|                    |          | Signed Byte Integer:       | ← 7 bits →  |
|                    |          | Signed Word Integer:       | ← 15 bits → |
|                    |          | Signed Doubleword Integer: | ← 31 bits → |
|                    |          | Signed Quadword Integer:   | ← 63 bits → |

The sign bit is set for negative integers and cleared for positive integers and zero. Integer values range from -128 to +127 for a byte integer, from -32,768 to +32,767 for a word integer, from  $-2^{31}$  to  $+2^{31} - 1$  for a doubleword integer, and from  $-2^{63}$  to  $+2^{63} - 1$  for a quadword integer.

When storing integer values in memory, word integers are stored in 2 consecutive bytes; doubleword integers are stored in 4 consecutive bytes; and quadword integers are stored in 8 consecutive bytes.

The integer indefinite is a special value that is sometimes returned by the x87 FPU when operating on integer values. For more information, see Section 8.2.1, "Indefinites."

4.2.2 Floating-Point Data Types

The IA-32 architecture defines and operates on four floating-point data types: half precision floating-point, single precision floating-point, double precision floating-point, and double-extended precision floating-point (see Figure 4-3). The data formats for these data types correspond directly to formats specified in the IEEE Standard 754 for Floating-Point Arithmetic.

The half precision (16-bit) floating-point data type was supported only with F16C extensions (VCVTPH2PS and VCVTPS2PH) beginning with the third generation of Intel Core processors based on Ivy Bridge microarchitecture. Starting with the 4th generation Intel Xeon Scalable Processor Family, an Intel AVX-512 instruction set architecture (ISA) for FP16 was added, supporting a wide range of general-purpose numeric operations for 16-bit half precision floating-point values (binary16 in the IEEE Standard 754-2019 for Floating-Point Arithmetic, aka half precision or FP16), which complements the existing 32-bit and 64-bit floating-point instructions already available in the Intel Xeon processor-based products.

Table 4-2 gives the length, precision, and approximate normalized range that can be represented by each of these data types. Denormal values are also supported in each of these types.

Table 4-2. Length, Precision, and Range of Floating-Point Data Types

| Data Type                 | Length<br>(Bits) | Precision<br>(Bits) | Approximate Normalized Range |                                                     |
|---------------------------|------------------|---------------------|------------------------------|-----------------------------------------------------|
|                           |                  |                     | Binary                       | Decimal                                             |
| Half Precision            | 16               | 11                  | $2^{-14}$ to $2^{16}$        | $6.10 \times 10^{-5}$ to $6.55 \times 10^4$         |
| Single Precision          | 32               | 24                  | $2^{-126}$ to $2^{128}$      | $1.18 \times 10^{-38}$ to $3.40 \times 10^{38}$     |
| Double Precision          | 64               | 53                  | $2^{-1022}$ to $2^{1024}$    | $2.23 \times 10^{-308}$ to $1.80 \times 10^{308}$   |
| Double-Extended Precision | 80               | 64                  | $2^{-16382}$ to $2^{16384}$  | $3.36 \times 10^{-4932}$ to $1.19 \times 10^{4932}$ |

NOTE

Section 4.8, “Real Numbers and Floating-Point Formats,” gives an overview of the IEEE Standard 754 floating-point formats and defines the terms integer bit, QNaN, SNaN, and denormal value.

Table 4-3 shows the floating-point encodings for zeros, denormalized finite numbers, normalized finite numbers, infinities, and NaNs for each of the three floating-point data types. It also gives the format for the QNaN floating-point indefinite value. (See Section 4.8.3.7, “QNaN Floating-Point Indefinite,” for a discussion of the use of the QNaN floating-point indefinite value.)

For the half precision, single precision, and double precision formats, only the fraction part of the significand is encoded. The integer is assumed to be 1 for all numbers except 0 and denormalized finite numbers. For the double extended precision format, the integer is contained in bit 63, and the most-significant fraction bit is bit 62. Here, the integer is explicitly set to 1 for normalized numbers, infinities, and NaNs, and to 0 for zero and denormalized numbers.

Table 4-3. Floating-Point Number and NaN Encodings

| Class      |            | Sign   | Biased Exponent | Significand          |          |
|------------|------------|--------|-----------------|----------------------|----------|
|            |            |        |                 | Integer <sup>1</sup> | Fraction |
| Positive   | +∞         | 0      | 11..11          | 1                    | 00..00   |
|            | +Normals   | 0      | 11..10          | 1                    | 11..11   |
|            |            | .      | .               | .                    | .        |
|            |            | 0      | 00..01          | 1                    | 00..00   |
|            | +Denormals | 0      | 00..00          | 0                    | 11.11    |
|            |            | .      | .               | .                    | .        |
| Negative   |            | 0      | 00..00          | 0                    | 00..01   |
| +Zero      | 0          | 00..00 | 0               | 00..00               |          |
| −Denormals | 1          | 00..00 | 0               | 00..01               |          |
|            | .          | .      | .               | .                    |          |
|            | 1          | 00..00 | 0               | 11..11               |          |
| −Normals   | 1          | 00..01 | 1               | 00..00               |          |
|            | .          | .      | .               | .                    |          |
|            | 1          | 11..10 | 1               | 11..11               |          |
| −∞         | 1          | 11..11 | 1               | 00..00               |          |

Table 4-3. Floating-Point Number and NaN Encodings (Contd.)

| Class |                                | Sign        | Biased Exponent | Significand          |                     |
|-------|--------------------------------|-------------|-----------------|----------------------|---------------------|
|       |                                |             |                 | Integer <sup>1</sup> | Fraction            |
| NaNs  | SNaN                           | X           | 11..11          | 1                    | 0X..XX <sup>2</sup> |
|       | QNaN                           | X           | 11..11          | 1                    | 1X..XX              |
|       | QNaN Floating-Point Indefinite | 1           | 11..11          | 1                    | 10..00              |
|       | Half Precision                 | ← 5 Bits →  |                 |                      | ← 10 Bits →         |
|       | Single Precision:              | ← 8 Bits →  |                 |                      | ← 23 Bits →         |
|       | Double Precision:              | ← 11 Bits → |                 |                      | ← 52 Bits →         |
|       | Double Extended Precision:     | ← 15 Bits → |                 |                      | ← 63 Bits →         |

NOTES:

- 1. Integer bit is implied and not stored for half precision, single precision, and double precision formats.
- 2. The fraction for SNaN encodings must be non-zero with the most-significant bit 0.

The exponent of each floating-point data type is encoded in biased format; see Section 4.8.2.2, “Biased Exponent.” The biasing constant is 15 for the half precision format, 127 for the single precision format, 1023 for the double precision format, and 16,383 for the double extended precision format.

When storing floating-point values in memory, half precision values are stored in 2 consecutive bytes in memory; single precision values are stored in 4 consecutive bytes in memory; double precision values are stored in 8 consecutive bytes; and double extended precision values are stored in 10 consecutive bytes.

The single precision and double precision floating-point data types are operated on by x87 FPU, and Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions. The double extended precision floating-point format is only operated on by the x87 FPU. See Section 11.6.8, “Compatibility of SIMD and x87 FPU Floating-Point Data Types,” for a discussion of the compatibility of single precision and double precision floating-point data types between the x87 FPU and Intel SSE/SSE2/SSE3 extensions.

4.2.3 Brain Float16

Brain Float16 (BF16 or bfloat16) is a shortened 16-bit version of the IEEE Standard 754 floating-point 32-bit format. It aims to speed up training and inference for AI workloads. Figure 4-4 illustrates BF16 versus FP16 and FP32.

![Diagram comparing FP32, FP16, and BF16 floating-point formats. FP32 has a sign bit, 8-bit exponent, and 23-bit mantissa. FP16 has a sign bit, 5-bit exponent, and 10-bit mantissa. BF16 has a sign bit, 8-bit exponent, and 7-bit mantissa.](4ee2de50739c96fd7bd5a38150ec9c78_img.jpg)

The diagram illustrates the bit layouts for three floating-point formats: FP32, FP16, and BF16. Each format is shown as a horizontal rectangle divided into three sections: a sign bit (s), an exponent field, and a mantissa field.

- FP32:** Consists of a 1-bit sign (s), an 8-bit exponent (8 bit exp), and a 23-bit mantissa (23 bit mantissa).
- FP16:** Consists of a 1-bit sign (s), a 5-bit exponent (5 bit exp), and a 10-bit mantissa (10 bit mantissa).
- BF16:** Consists of a 1-bit sign (s), an 8-bit exponent (8 bit exp), and a 7-bit mantissa (7 bit mantissa).

The BF16 format is shown as a shortened version of FP32, retaining the full 8-bit exponent but reducing the mantissa to 7 bits.

BFP10001

Diagram comparing FP32, FP16, and BF16 floating-point formats. FP32 has a sign bit, 8-bit exponent, and 23-bit mantissa. FP16 has a sign bit, 5-bit exponent, and 10-bit mantissa. BF16 has a sign bit, 8-bit exponent, and 7-bit mantissa.

Figure 4-4. Comparison of BF16 to FP16 and FP32

4.2.3.1 Numeric Definition

BF16 has one sign bit, eight exponent bits, and seven mantissa bits.

Table 4-4. BF16 Format Numeric Definitions

| Number           | BF16 (E8M7)                                                             |
|------------------|-------------------------------------------------------------------------|
| Exponent Bias    | 127                                                                     |
| Maximum Normal   | S 11111110 11111111 = $\pm 2^{127} * 1.99 \approx \pm 3.39 * 10^{38}$   |
| Minimum Normal   | S 00000001 00000000 = $\pm 2^{-126} \approx \pm 1.18 * 10^{-38}$        |
| Maximum Denormal | S 00000000 11111111 = $\pm 2^{-126} * 0.99 \approx \pm 1.17 * 10^{-38}$ |
| Minimum Denormal | S 00000000 00000001 = $\pm 2^{-133} \approx \pm 9.18 * 10^{-41}$        |
| NaNs             | S 11111111 {non-zero}                                                   |
| Infinity         | S 11111111 00000000                                                     |
| Zeros            | S 00000000 00000000                                                     |

Although denormal values are shown in the table, they are not used in computations (see Section 4.2.3.2).

### 4.2.3.2 Rounding, Denormal Handling, and FP Exceptions

Intel architecture supports BF16 in AMX dot product instructions, AVX dot product instructions, and AVX convert instructions.

- Rounding: All operations are executed using Round to nearest (even) mode (e.g., for convert instructions).
- Denormal Handling: For BF16, input denormal values are replaced with zeros and FP32 underflow results are flushed to zero. All instructions that accept BF16 inputs have FP32 results.
- Floating-point exceptions:
  - Instructions operating on BF16 values neither consult nor update the MXCSR.
  - Instructions operating on BF16 values do not raise exceptions.

## 4.3 POINTER DATA TYPES

Pointers are addresses of locations in memory.

In non-64-bit modes, the architecture defines two types of pointers: a **near pointer** and a **far pointer**. A near pointer is a 32-bit (or 16-bit) offset (also called an **effective address**) within a segment. Near pointers are used for all memory references in a flat memory model or for references in a segmented model where the identity of the segment being accessed is implied.

A far pointer is a logical address, consisting of a 16-bit segment selector and a 32-bit (or 16-bit) offset. Far pointers are used for memory references in a segmented memory model where the identity of a segment being accessed must be specified explicitly. Near and far pointers with 32-bit offsets are shown in Figure 4-5.

![Diagram illustrating Near Pointer and Far Pointer or Logical Address structures.](0726a03ffb4e106eb90cd4f9283a6347_img.jpg)

The diagram shows two pointer structures within a rectangular frame. The top structure is labeled 'Near Pointer' and consists of a single horizontal bar labeled 'Offset' with bit positions 31 on the left and 0 on the right. The bottom structure is labeled 'Far Pointer or Logical Address' and consists of two horizontal bars. The left bar is labeled 'Segment Selector' with bit positions 47 on the left and 32 on the right. The right bar is labeled 'Offset' with bit positions 31 on the left and 0 on the right.

Diagram illustrating Near Pointer and Far Pointer or Logical Address structures.

Figure 4-5. Pointer Data Types

4.3.1 Pointer Data Types in 64-Bit Mode

In 64-bit mode (a sub-mode of IA-32e mode), a **near pointer** is 64 bits. This equates to an effective address. **Far pointers** in 64-bit mode can be one of three forms:

- 16-bit segment selector, 16-bit offset if the operand size is 32 bits.
- 16-bit segment selector, 32-bit offset if the operand size is 32 bits.
- 16-bit segment selector, 64-bit offset if the operand size is 64 bits.

See Figure 4-6.

![Diagram showing four pointer formats in 64-bit mode: Near Pointer, Far Pointer with 64-bit Operand Size, Far Pointer with 32-bit Operand Size (64-bit offset), and Far Pointer with 32-bit Operand Size (16-bit offset).](a4eb9fe011f0e6dc8405f777c5f3f766_img.jpg)

The diagram illustrates four pointer formats within a 64-bit structure:

- Near Pointer:** A single 64-bit field labeled "64-bit Offset" spanning from bit 63 to bit 0.
- Far Pointer with 64-bit Operand Size:** A 16-bit "16-bit Segment Selector" field from bit 79 to bit 64, followed by a 64-bit "64-bit Offset" field from bit 63 to bit 0.
- Far Pointer with 32-bit Operand Size (64-bit offset):** A 16-bit "16-bit Segment Selector" field from bit 47 to bit 32, followed by a 32-bit "32-bit Offset" field from bit 31 to bit 0.
- Far Pointer with 32-bit Operand Size (16-bit offset):** A 16-bit "16-bit Segment Selector" field from bit 31 to bit 16, followed by a 16-bit "16-bit Offset" field from bit 15 to bit 0.

Diagram showing four pointer formats in 64-bit mode: Near Pointer, Far Pointer with 64-bit Operand Size, Far Pointer with 32-bit Operand Size (64-bit offset), and Far Pointer with 32-bit Operand Size (16-bit offset).

Figure 4-6. Pointers in 64-Bit Mode

4.4 BIT FIELD DATA TYPE

A **bit field** (see Figure 4-7) is a contiguous sequence of bits. It can begin at any bit position of any byte in memory and can contain up to 32 bits.

![Diagram showing a Bit Field structure with a Field Length and Least Significant Bit indicated.](69733eeb3ef32197543f66f22a431771_img.jpg)

The diagram shows a horizontal rectangle representing a bit field. Below the rectangle, a bracket indicates the "Field Length". Below the bracket, the text "Least Significant Bit" is written.

Diagram showing a Bit Field structure with a Field Length and Least Significant Bit indicated.

Figure 4-7. Bit Field Data Type

## 4.5 STRING DATA TYPES

Strings are continuous sequences of bits, bytes, words, or doublewords. A **bit string** can begin at any bit position of any byte and can contain up to  $2^{32} - 1$  bits. A **byte string** can contain bytes, words, or doublewords and can range from zero to  $2^{32} - 1$  bytes (4 GBytes).

## 4.6 PACKED SIMD DATA TYPES

Intel 64 and IA-32 architectures define and operate on a set of 64-bit and 128-bit packed data type for use in SIMD operations. These data types consist of fundamental data types (packed bytes, words, doublewords, and quadwords) and numeric interpretations of fundamental types for use in packed integer and packed floating-point operations.

### 4.6.1 64-Bit SIMD Packed Data Types

The 64-bit packed SIMD data types were introduced into the IA-32 architecture in the Intel MMX technology. They are operated on in MMX registers. The fundamental 64-bit packed data types are packed bytes, packed words, and packed doublewords (see Figure 4-8). When performing numeric SIMD operations on these data types, these data types are interpreted as containing byte, word, or doubleword integer values.

![Diagram illustrating 64-bit packed SIMD data types. It shows three fundamental types: Packed Bytes (8 segments of 8 bits each), Packed Words (4 segments of 16 bits each), and Packed Doublewords (2 segments of 32 bits each). Below these are three integer interpretations: Packed Byte Integers (8 segments of 8 bits each), Packed Word Integers (4 segments of 16 bits each), and Packed Doubleword Integers (2 segments of 32 bits each). Each diagram is a horizontal bar with bit positions 63 and 0 marked.](49806c5ac206335a657bc126f17d37e8_img.jpg)

Fundamental 64-Bit Packed SIMD Data Types

Packed Bytes: 8 segments of 8 bits each, bit positions 63 to 0.

Packed Words: 4 segments of 16 bits each, bit positions 63 to 0.

Packed Doublewords: 2 segments of 32 bits each, bit positions 63 to 0.

64-Bit Packed Integer Data Types

Packed Byte Integers: 8 segments of 8 bits each, bit positions 63 to 0.

Packed Word Integers: 4 segments of 16 bits each, bit positions 63 to 0.

Packed Doubleword Integers: 2 segments of 32 bits each, bit positions 63 to 0.

Diagram illustrating 64-bit packed SIMD data types. It shows three fundamental types: Packed Bytes (8 segments of 8 bits each), Packed Words (4 segments of 16 bits each), and Packed Doublewords (2 segments of 32 bits each). Below these are three integer interpretations: Packed Byte Integers (8 segments of 8 bits each), Packed Word Integers (4 segments of 16 bits each), and Packed Doubleword Integers (2 segments of 32 bits each). Each diagram is a horizontal bar with bit positions 63 and 0 marked.

Figure 4-8. 64-Bit Packed SIMD Data Types

### 4.6.2 128-Bit Packed SIMD Data Types

The 128-bit packed SIMD data types were introduced into the IA-32 architecture in the Intel SSE extensions and used with Intel SSE2, SSE3, SSSE3, SSE4.1, and AVX extensions. They are operated on primarily in the 128-bit XMM registers and memory. The fundamental 128-bit packed data types are packed bytes, packed words, packed doublewords, and packed quadwords (see Figure 4-9). When performing SIMD operations on these fundamental data types in XMM registers, these data types are interpreted as containing packed or scalar half precision floating-point, single precision floating-point or double precision floating-point values, or as containing packed byte, word, doubleword, or quadword integer values.

![Diagram showing fundamental 128-bit packed SIMD data types: Packed Bytes, Packed Words, Packed Doublewords, and Packed Quadwords. Each type is represented by a horizontal bar divided into segments, with bit positions 127 and 0 marked. Diagram showing 128-bit packed floating-point and integer data types: Packed Half Precision Floating-Point, Packed Single Precision Floating-Point, Packed Double Precision Floating-Point, Packed Byte Integers, Packed Word Integers, Packed Doubleword Integers, and Packed Quadword Integers. Each type is represented by a horizontal bar divided into segments, with bit positions 127 and 0 marked.](2fb80a12eb86e56acbd06b36b6a32b97_img.jpg)

Fundamental 128-bit Packed SIMD Data Types

127 0 Packed Bytes

127 0 Packed Words

127 0 Packed Doublewords

127 0 Packed Quadwords

128-bit Packed Floating-Point and Integer Data Types

127 0 Packed Half Precision Floating-Point

127 0 Packed Single Precision Floating-Point

127 0 Packed Double Precision Floating-Point

127 0 Packed Byte Integers

127 0 Packed Word Integers

127 0 Packed Doubleword Integers

127 0 Packed Quadword Integers

Diagram showing fundamental 128-bit packed SIMD data types: Packed Bytes, Packed Words, Packed Doublewords, and Packed Quadwords. Each type is represented by a horizontal bar divided into segments, with bit positions 127 and 0 marked. Diagram showing 128-bit packed floating-point and integer data types: Packed Half Precision Floating-Point, Packed Single Precision Floating-Point, Packed Double Precision Floating-Point, Packed Byte Integers, Packed Word Integers, Packed Doubleword Integers, and Packed Quadword Integers. Each type is represented by a horizontal bar divided into segments, with bit positions 127 and 0 marked.

Figure 4-9. 128-Bit Packed SIMD Data Types

### 4.7 BCD AND PACKED BCD INTEGERS

Binary-coded decimal integers (BCD integers) are unsigned 4-bit integers with valid values ranging from 0 to 9. IA-32 architecture defines operations on BCD integers located in one or more general-purpose registers or in one or more x87 FPU registers (see Figure 4-10).

![Diagram showing BCD data types: BCD Integers, Packed BCD Integers, and 80-Bit Packed BCD Decimal Integers.](a447b2987d1c97785a18fc8c036ab70c_img.jpg)

The diagram illustrates three BCD data types:

- BCD Integers:** A 2-byte structure. The high byte (bits 7-4) is labeled 'X' and the low byte (bits 3-0) is labeled 'BCD'.
- Packed BCD Integers:** A 2-byte structure. Both the high byte (bits 7-4) and the low byte (bits 3-0) are labeled 'BCD'.
- 80-Bit Packed BCD Decimal Integers:** An 80-bit structure. Bit 79 is the 'Sign' bit (labeled 'X'). Bits 78-72 are the first 7 BCD digits (labeled '79 78' and '72 71'). Bits 71-0 are the remaining 18 BCD digits (labeled 'D17' through 'D0').

A note at the bottom right states: 4 Bits = 1 BCD Digit.

Diagram showing BCD data types: BCD Integers, Packed BCD Integers, and 80-Bit Packed BCD Decimal Integers.

Figure 4-10. BCD Data Types

When operating on BCD integers in general-purpose registers, the BCD values can be unpacked (one BCD digit per byte) or packed (two BCD digits per byte). The value of an unpacked BCD integer is the binary value of the low half-byte (bits 0 through 3). The high half-byte (bits 4 through 7) can be any value during addition and subtraction, but must be zero during multiplication and division. Packed BCD integers allow two BCD digits to be contained in one byte. Here, the digit in the high half-byte is more significant than the digit in the low half-byte.

When operating on BCD integers in x87 FPU data registers, BCD values are packed in an 80-bit format and referred to as decimal integers. In this format, the first 9 bytes hold 18 BCD digits, 2 digits per byte. The least-significant digit is contained in the lower half-byte of byte 0 and the most-significant digit is contained in the upper half-byte of byte 9. The most significant bit of byte 10 contains the sign bit (0 = positive and 1 = negative; bits 0 through 6 of byte 10 are don't care bits). Negative decimal integers are not stored in two's complement form; they are distinguished from positive decimal integers only by the sign bit. The range of decimal integers that can be encoded in this format is  $-10^{18} + 1$  to  $10^{18} - 1$ .

The decimal integer format exists in memory only. When a decimal integer is loaded in an x87 FPU data register, it is automatically converted to the double extended precision floating-point format. All decimal integers are exactly representable in double extended precision format.

Table 4-5 gives the possible encodings of value in the decimal integer data type.

Table 4-5. Packed Decimal Integer Encodings

| Class               | Sign |         | Magnitude |       |       |       |     |       |
|---------------------|------|---------|-----------|-------|-------|-------|-----|-------|
|                     |      |         | digit     | digit | digit | digit | ... | digit |
| Positive<br>Largest | 0    | 0000000 | 1001      | 1001  | 1001  | 1001  | ... | 1001  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |
| Smallest            | 0    | 0000000 | 0000      | 0000  | 0000  | 0000  | ... | 0001  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |
| Zero                | 0    | 0000000 | 0000      | 0000  | 0000  | 0000  | ... | 0000  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |
| Negative<br>Zero    | 1    | 0000000 | 0000      | 0000  | 0000  | 0000  | ... | 0000  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |
| Smallest            | 1    | 0000000 | 0000      | 0000  | 0000  | 0000  | ... | 0001  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |
| Largest             | 1    | 0000000 | 1001      | 1001  | 1001  | 1001  | ... | 1001  |
|                     |      |         |           |       |       |       |     |       |
|                     |      |         |           |       |       |       |     |       |

Table 4-5. Packed Decimal Integer Encodings (Contd.)

| Class                         | Sign       |         | Magnitude   |       |       |       |     |       |
|-------------------------------|------------|---------|-------------|-------|-------|-------|-----|-------|
|                               |            |         | digit       | digit | digit | digit | ... | digit |
| Packed BCD Integer Indefinite | 1          | 1111111 | 1111        | 1111  | 1100  | 0000  | ... | 0000  |
|                               | ← 1 byte → |         | ← 9 bytes → |       |       |       |     |       |

The packed BCD integer indefinite encoding (FFFFC000000000000000H) is stored by the FBSTP instruction in response to a masked floating-point invalid-operation exception. Attempting to load this value with the FBLD instruction produces an undefined result.

4.8 REAL NUMBERS AND FLOATING-POINT FORMATS

This section describes how real numbers are represented in floating-point format in x87 FPU and SSE/SSE2/SSE3/SSE4.1 and Intel AVX floating-point instructions. It also introduces terms such as normalized numbers, denormalized numbers, biased exponents, signed zeros, and NaNs. Readers who are already familiar with floating-point processing techniques and the IEEE Standard 754 for Floating-Point Arithmetic may wish to skip this section.

4.8.1 Real Number System

As shown in Figure 4-11, the real-number system comprises the continuum of real numbers from minus infinity (−∞) to plus infinity (+∞). Because the size and number of registers that any computer can have is limited, only a subset of the real-number continuum can be used in real-number (floating-point) calculations. As shown at the bottom of Figure 4-11, the subset of real numbers that the IA-32 architecture supports represents an approximation of the real number system. The range and precision of this real-number subset is determined by the IEEE Standard 754 floating-point formats.

4.8.2 Floating-Point Format

To increase the speed and efficiency of real-number computations, computers and microprocessors typically represent real numbers in a binary floating-point format. In this format, a real number has three parts: a sign, a significand, and an exponent (see Figure 4-12). The sign is a binary value that indicates whether the number is positive (0) or negative (1). The significand has two parts: a 1-bit binary integer (also referred to as the J-bit) and a binary fraction. The integer-bit is often not represented, but instead is an implied value. The exponent is a binary integer that represents the base-2 power by which the significand is multiplied. Table 4-6 shows how the real number 178.125 (in ordinary decimal format) is stored in IEEE Standard 754 floating-point format. The table lists a progression of real number notations that leads to the single precision, 32-bit floating-point format. In this format, the significand is normalized (see Section 4.8.2.1, “Normalized Numbers”) and the exponent is biased (see Section 4.8.2.2, “Biased Exponent”). For the single precision floating-point format, the biasing constant is +127.

![](a05ad7b3a9ed890d8ef5f717f1b912b1_img.jpg)

Binary Real Number System

-100      -10    -1   0   1    10      100

Subset of binary real numbers that can be represented with IEEE single precision (32-bit) floating-point format

-100      -10    -1   0   1    10      100

+10

10.000000000000000000000000

1.111111111111111111111111

Precision ← 24 Binary Digits →

Numbers within this range cannot be represented.

Figure 4-11. Binary Real Number System

![](e16bfa31d748f4d99ec4ae3d16656926_img.jpg)

|      |          |             |
|------|----------|-------------|
| Sign | Exponent | Significand |
|      |          | Fraction    |

Integer or J-Bit

Figure 4-12. Binary Floating-Point Format

Table 4-6. Real and Floating-Point Number Notation

| Notation                            | Value                               |                 |                                         |
|-------------------------------------|-------------------------------------|-----------------|-----------------------------------------|
| Ordinary Decimal                    | 178.125                             |                 |                                         |
| Scientific Decimal                  | 1.78125E <sub>10</sub> 2            |                 |                                         |
| Scientific Binary                   | 1.0110010001E <sub>2</sub> 111      |                 |                                         |
| Scientific Binary (Biased Exponent) | 1.0110010001E <sub>2</sub> 10000110 |                 |                                         |
| IEEE Single Precision Format        | Sign                                | Biased Exponent | Normalized Significand                  |
|                                     | 0                                   | 10000110        | 01100100010000000000000<br>1. (Implied) |

### 4.8.2.1 Normalized Numbers

In most cases, floating-point numbers are encoded in normalized form. This means that except for zero, the significand is always made up of an integer of 1 and the following fraction:

1.fff...ff

For values less than 1, leading zeros are eliminated. (For each leading zero eliminated, the exponent is decremented by one.)

Representing numbers in normalized form maximizes the number of significant digits that can be accommodated in a significand of a given width. To summarize, a normalized real number consists of a normalized significand that represents a real number between 1 and 2 and an exponent that specifies the number's binary point.

### 4.8.2.2 Biased Exponent

In the IA-32 architecture, the exponents of floating-point numbers are encoded in a biased form. This means that a constant is added to the actual exponent so that the biased exponent is always a positive number. The value of the biasing constant depends on the number of bits available for representing exponents in the floating-point format being used. The biasing constant is chosen so that the smallest normalized number can be reciprocated without overflow.

See Section 4.2.2, "Floating-Point Data Types," for a list of the biasing constants that the IA-32 architecture uses for the various sizes of floating-point data-types.

## 4.8.3 Real Number and Non-number Encodings

A variety of real numbers and special values can be encoded in the IEEE Standard 754 floating-point format. These numbers and values are generally divided into the following classes:

- Signed zeros
- Denormalized finite numbers
- Normalized finite numbers
- Signed infinities
- NaNs
- Indefinite numbers

(The term NaN stands for "Not a Number.")

Figure 4-13 shows how the encodings for these numbers and non-numbers fit into the real number continuum. The encodings shown here are for the IEEE single precision floating-point format. The term "S" indicates the sign bit, "E" the biased exponent, and "Sig" the significand. The exponent values are given in decimal. The integer bit is shown for the significands, even though the integer bit is implied in single precision floating-point format.

![Figure 4-13: Real Numbers and NaNs. A diagram showing the IEEE 754-2008 floating-point format for 32-bit. At the top, a number line shows the range from -infinity to +infinity, with categories: NaN, -Denormalized Finite, -0+0, +Denormalized Finite, -Normalized Finite, +Normalized Finite, and +infinity. Below this, a table shows the bit fields for various values. The table has two columns for negative and positive values. Each row shows the sign bit (S), exponent (E), and significand (Sig). The rows are: -0 (S=1, E=0, Sig=0.000...), +0 (S=0, E=0, Sig=0.000...), -Denormalized Finite (S=1, E=0, Sig=0.XXX...), +Denormalized Finite (S=0, E=0, Sig=0.XXX...), -Normalized Finite (S=1, E=1...254, Sig=1.XXX...), +Normalized Finite (S=0, E=1...254, Sig=1.XXX...), -infinity (S=1, E=255, Sig=1.000...), +infinity (S=0, E=255, Sig=1.000...), SNaN (S=X^3, E=255, Sig=1.0XX...), and QNaN (S=X^3, E=255, Sig=1.1XX...). Below the table are three notes: 1. Integer bit of fraction implied for single precision floating-point format. 2. Fraction must be non-zero. 3. Sign bit ignored.](7c6fd006fc4d304794392d41fab4ee10_img.jpg)

**Real Number and NaN Encodings For 32-Bit Floating-Point Format**

| S              | E       | Sig <sup>1</sup>      |                       | S              | E       | Sig <sup>1</sup>      |                       |
|----------------|---------|-----------------------|-----------------------|----------------|---------|-----------------------|-----------------------|
| 1              | 0       | 0.000...              | - 0                   | 0              | 0       | 0.000...              | + 0                   |
| 1              | 0       | 0.XXX... <sup>2</sup> | - Denormalized Finite | 0              | 0       | 0.XXX... <sup>2</sup> | + Denormalized Finite |
| 1              | 1...254 | 1.XXX...              | - Normalized Finite   | 0              | 1...254 | 1.XXX...              | + Normalized Finite   |
| 1              | 255     | 1.000...              | - ∞                   | 0              | 255     | 1.000...              | + ∞                   |
| X <sup>3</sup> | 255     | 1.0XX... <sup>2</sup> | SNaN                  | X <sup>3</sup> | 255     | 1.0XX... <sup>2</sup> | SNaN                  |
| X <sup>3</sup> | 255     | 1.1XX...              | QNaN                  | X <sup>3</sup> | 255     | 1.1XX...              | QNaN                  |

**NOTES:**

1. Integer bit of fraction implied for single precision floating-point format.
2. Fraction must be non-zero.
3. Sign bit ignored.

Figure 4-13: Real Numbers and NaNs. A diagram showing the IEEE 754-2008 floating-point format for 32-bit. At the top, a number line shows the range from -infinity to +infinity, with categories: NaN, -Denormalized Finite, -0+0, +Denormalized Finite, -Normalized Finite, +Normalized Finite, and +infinity. Below this, a table shows the bit fields for various values. The table has two columns for negative and positive values. Each row shows the sign bit (S), exponent (E), and significand (Sig). The rows are: -0 (S=1, E=0, Sig=0.000...), +0 (S=0, E=0, Sig=0.000...), -Denormalized Finite (S=1, E=0, Sig=0.XXX...), +Denormalized Finite (S=0, E=0, Sig=0.XXX...), -Normalized Finite (S=1, E=1...254, Sig=1.XXX...), +Normalized Finite (S=0, E=1...254, Sig=1.XXX...), -infinity (S=1, E=255, Sig=1.000...), +infinity (S=0, E=255, Sig=1.000...), SNaN (S=X^3, E=255, Sig=1.0XX...), and QNaN (S=X^3, E=255, Sig=1.1XX...). Below the table are three notes: 1. Integer bit of fraction implied for single precision floating-point format. 2. Fraction must be non-zero. 3. Sign bit ignored.

Figure 4-13. Real Numbers and NaNs

An IA-32 processor can operate on and/or return any of these values, depending on the type of computation being performed. The following sections describe these number and non-number classes.

#### 4.8.3.1 Signed Zeros

Zero can be represented as a +0 or a -0 depending on the sign bit. Both encodings are equal in value. The sign of a zero result depends on the operation being performed and the rounding mode being used. Signed zeros have been provided to aid in implementing interval arithmetic. The sign of a zero may indicate the direction from which underflow occurred, or it may indicate the sign of an  $\infty$  that has been reciprocated.

#### 4.8.3.2 Normalized and Denormalized Finite Numbers

Non-zero, finite numbers are divided into two classes: normalized and denormalized. The normalized finite numbers comprise all the non-zero finite values that can be encoded in a normalized real number format between zero and  $\infty$ . In the single precision floating-point format shown in Figure 4-13, this group of numbers includes all the numbers with biased exponents ranging from 1 to 254<sub>10</sub> (unbiased, the exponent range is from -126<sub>10</sub> to +127<sub>10</sub>).

When floating-point numbers become very close to zero, the normalized-number format can no longer be used to represent the numbers. This is because the range of the exponent is not large enough to compensate for shifting the binary point to the right to eliminate leading zeros.

When the biased exponent is zero, smaller numbers can only be represented by making the integer bit (and perhaps other leading bits) of the significand zero. The numbers in this range are called **denormalized** numbers. The use of leading zeros with denormalized numbers allows smaller numbers to be represented. However, this denormalization may cause a loss of precision (the number of significant bits is reduced by the leading zeros).

When performing normalized floating-point computations, an IA-32 processor normally operates on normalized numbers and produces normalized numbers as results. Denormalized numbers represent an **underflow** condition. The exact conditions are specified in Section 4.9.1.5, "Numeric Underflow Exception (#U)."

A denormalized number is computed through a technique called gradual underflow. Table 4-7 gives an example of gradual underflow in the denormalization process. Here the single precision format is being used, so the minimum exponent (unbiased) is -126<sub>10</sub>. The true result in this example requires an exponent of -129<sub>10</sub> in order to have a

normalized number. Since  $-129_{10}$  is beyond the allowable exponent range, the result is denormalized by inserting leading zeros until the minimum exponent of  $-126_{10}$  is reached.

Table 4-7. Denormalization Process

| Operation       | Sign | Exponent* | Significand        |
|-----------------|------|-----------|--------------------|
| True Result     | 0    | -129      | 1.01011100000...00 |
| Denormalize     | 0    | -128      | 0.10101110000...00 |
| Denormalize     | 0    | -127      | 0.01010111000...00 |
| Denormalize     | 0    | -126      | 0.00101011100...00 |
| Denormal Result | 0    | -126      | 0.00101011100...00 |

\* Expressed as an unbiased, decimal number.

In the extreme case, all the significant bits are shifted out to the right by leading zeros, creating a zero result. The Intel 64 and IA-32 architectures deal with denormal values in the following ways:

- It avoids creating denormals by normalizing numbers whenever possible.
- It provides the floating-point underflow exception to permit programmers to detect cases when denormals are created.
- It provides the floating-point denormal-operand exception to permit procedures or programs to detect when denormals are being used as source operands for computations.

4.8.3.3 Signed Infinities

The two infinities,  $+\infty$  and  $-\infty$ , represent the maximum positive and negative real numbers, respectively, that can be represented in the floating-point format. Infinity is always represented by a significand of 1.00...00 (the integer bit may be implied) and the maximum biased exponent allowed in the specified format (for example,  $255_{10}$  for the single precision format).

The signs of infinities are observed, and comparisons are possible. Infinities are always interpreted in the affine sense; that is,  $-\infty$  is less than any finite number and  $+\infty$  is greater than any finite number. Arithmetic on infinities is always exact. Exceptions are generated only when the use of an infinity as a source operand constitutes an invalid operation.

Whereas denormalized numbers may represent an underflow condition, the two  $\infty$  numbers may represent the result of an overflow condition. Here, the normalized result of a computation has a biased exponent greater than the largest allowable exponent for the selected result format.

4.8.3.4 NaNs

Since NaNs are non-numbers, they are not part of the real number line. In Figure 4-13, the encoding space for NaNs in the floating-point formats is shown above the ends of the real number line. This space includes any value with the maximum allowable biased exponent and a non-zero fraction (the sign bit is ignored for NaNs).

The IA-32 architecture defines two classes of NaNs: quiet NaNs (QNaNs) and signaling NaNs (SNaNs). A QNaN is a NaN with the most significant fraction bit set; an SNaN is a NaN with the most significant fraction bit clear. QNaNs are allowed to propagate through most arithmetic operations without signaling an exception. SNaNs generally signal a floating-point invalid-operation exception whenever they appear as operands in arithmetic operations.

SNaNs are typically used to trap or invoke an exception handler. They must be inserted by software; that is, the processor never generates an SNaN as a result of a floating-point operation.

### 4.8.3.5 Operating on SNaNs and QNaNs

When a floating-point operation is performed on an SNaN and/or a QNaN, the result of the operation is either a QNaN delivered to the destination operand or the generation of a floating-point invalid operation exception, depending on the following rules:

- If one of the source operands is an SNaN and the floating-point invalid-operation exception is not masked (see Section 4.9.1.1, “Invalid Operation Exception (#I)”), then a floating-point invalid-operation exception is signaled and no result is stored in the destination operand. If one of the source operands is a QNaN and the floating-point invalid-operation exception is not masked and the operation is one that generates an invalid-operation exception for QNaN operands as described in Section 8.5.1.2, “Invalid Arithmetic Operand Exception (#IA),” or Section 11.5.2.1, “Invalid Operation Exception (#I),” then a floating-point invalid-operation exception is signaled and no result is stored in the destination operand.
- If either or both of the source operands are NaNs and floating-point invalid-operation exception is masked, the result is as shown in Table 4-8. When an SNaN is converted to a QNaN, the conversion is handled by setting the most-significant fraction bit of the SNaN to 1. Also, when one of the source operands is an SNaN, or when it is a QNaN and the operation is one that generates an invalid-operation exception for QNaN operands as described in Section 8.5.1.2, “Invalid Arithmetic Operand Exception (#IA),” or Section 11.5.2.1, “Invalid Operation Exception (#I),” then the floating-point invalid-operation exception flag is set. Note that for some combinations of source operands, the result is different for x87 FPU operations and for Intel SSE/SSE2/SSE3/SSE4.1 operations. Intel AVX follows the same behavior as Intel SSE/SSE2/SSE3/SSE4.1 in this respect.
- When neither of the source operands is a NaN, but the operation generates a floating-point invalid-operation exception (see Tables 8-10 and 11-1), the result is commonly a QNaN FP Indefinite (Section 4.8.3.7).

Any exceptions to the behavior described in Table 4-8 are described in Section 8.5.1.2, “Invalid Arithmetic Operand Exception (#IA),” and Section 11.5.2.1, “Invalid Operation Exception (#I).”

**Table 4-8. Rules for Handling NaNs**

| Source Operands                                    | Result <sup>1</sup>                                                                                                                                       |
|----------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| SNaN and QNaN                                      | X87 FPU — QNaN source operand.<br>SSE/SSE2/SSE3/SSE4.1/AVX — First source operand (if this operand is an SNaN, it is converted to a QNaN).                |
| Two SNaNs                                          | X87 FPU — SNaN source operand with the larger significand, converted into a QNaN.<br>SSE/SSE2/SSE3/SSE4.1/AVX — First source operand converted to a QNaN. |
| Two QNaNs                                          | X87 FPU — QNaN source operand with the larger significand.<br>SSE/SSE2/SSE3/SSE4.1/AVX — First source operand.                                            |
| SNaN and a floating-point value                    | SNaN source operand, converted into a QNaN.                                                                                                               |
| QNaN and a floating-point value                    | QNaN source operand.                                                                                                                                      |
| SNaN (for instructions that take only one operand) | SNaN source operand, converted into a QNaN.                                                                                                               |
| QNaN (for instructions that take only one operand) | QNaN source operand.                                                                                                                                      |

**NOTE:**

1. For SSE/SSE2/SSE3/SSE4.1 instructions, the first operand is generally a source operand that becomes the destination operand. For AVX instructions, the first source operand is usually the 2nd operand in a non-destructive source syntax. Within the **Result** column, the x87 FPU notation also applies to the FISTTP instruction in SSE3; the SSE3 notation applies to the SIMD floating-point instructions.

### 4.8.3.6 Using SNaNs and QNaNs in Applications

Except for the rules given at the beginning of Section 4.8.3.4, “NaNs,” for encoding SNaNs and QNaNs, software is free to use the bits in the significand of a NaN for any purpose. Both SNaNs and QNaNs can be encoded to carry and store data, such as diagnostic information.

By unmasking the invalid operation exception, the programmer can use signaling NaNs to trap to the exception handler. The generality of this approach and the large number of NaN values that are available provide the sophisticated programmer with a tool that can be applied to a variety of special situations.

For example, a compiler can use signaling NaNs as references to uninitialized (real) array elements. The compiler can preinitialize each array element with a signaling NaN whose significand contains the index (relative position) of the element. Then, if an application program attempts to access an element that it has not initialized, it can use the NaN placed there by the compiler. If the invalid operation exception is unmasked, an interrupt will occur, and the exception handler will be invoked. The exception handler can determine which element has been accessed, since the operand address field of the exception pointer will point to the NaN, and the NaN will contain the index number of the array element.

Quiet NaNs are often used to speed up debugging. In its early testing phase, a program often contains multiple errors. An exception handler can be written to save diagnostic information in memory whenever it is invoked. After storing the diagnostic data, it can supply a quiet NaN as the result of the erroneous instruction, and that NaN can point to its associated diagnostic area in memory. The program will then continue, creating a different NaN for each error. When the program ends, the NaN results can be used to access the diagnostic data saved at the time the errors occurred. Many errors can thus be diagnosed and corrected in one test run.

In embedded applications that use computed results in further computations, an undetected QNaN can invalidate all subsequent results. Such applications should therefore periodically check for QNaNs and provide a recovery mechanism to be used if a QNaN result is detected.

#### 4.8.3.7 QNaN Floating-Point Indefinite

For the floating-point data type encodings (single precision, double precision, and double extended precision), one unique encoding (a QNaN) is reserved for representing the special value QNaN floating-point indefinite. The x87 FPU and the Intel SSE/SSE2/SSE3/SSE4.1/AVX extensions return these indefinite values as responses to some masked floating-point exceptions. Table 4-3 shows the encoding used for the QNaN floating-point indefinite.

#### 4.8.3.8 Half Precision Floating-Point Operation

Two instructions, VCVTPH2PS and VCVTPS2PH, which provide conversion only between half precision and single precision floating-point values, were introduced with the F16C extensions beginning with the third generation of Intel Core processors based on Ivy Bridge microarchitecture. Starting with the 4th generation Intel Xeon Scalable Processor Family, an Intel AVX-512 instruction set architecture (ISA) for FP16 was added, supporting a wide range of general-purpose numeric operations for 16-bit half precision floating-point values (binary16 in the IEEE Standard 754-2019 for Floating-Point Arithmetic, aka half precision or FP16). These additions complement the existing 32-bit and 64-bit floating-point instructions already available in the Intel Xeon processor-based products.

The SIMD floating-point exception behavior of the VCVTPH2PS and VCVTPS2PH instructions, as well as of the other half precision instructions, are described in Section 14.4.1.

### 4.8.4 Rounding

When performing floating-point operations, the processor produces an infinitely precise floating-point result in the destination format (half precision, single precision, double precision, or double extended precision floating-point) whenever possible. However, because only a subset of the numbers in the real number continuum can be represented in IEEE Standard 754 floating-point formats, it is often the case that an infinitely precise result cannot be encoded exactly in the format of the destination operand.

For example, the following value (*a*) has a 24-bit fraction. The least-significant bit of this fraction (the underlined bit) cannot be encoded exactly in the single precision format (which has only a 23-bit fraction):

(*a*) 1.0001 0000 1000 0011 1001 0111E<sub>2</sub> 101

To round this result (*a*), the processor first selects two representable fractions *b* and *c* that most closely bracket *a* in value ( $b < a < c$ ).

(*b*) 1.0001 0000 1000 0011 1001 011E<sub>2</sub> 101

(*c*) 1.0001 0000 1000 0011 1001 100E<sub>2</sub> 101

The processor then sets the result to  $b$  or to  $c$  according to the selected rounding mode. Rounding introduces an error in a result that is less than one unit in the last place (the least significant bit position of the floating-point value) to which the result is rounded.

The IEEE Standard 754 defines four rounding modes (see Table 4-9): round to nearest, round up, round down, and round toward zero. The default rounding mode (for the Intel 64 and IA-32 architectures) is round to nearest. This mode provides the most accurate and statistically unbiased estimate of the true result and is suitable for most applications.

**Table 4-9. Rounding Modes and Encoding of Rounding Control (RC) Field**

| Rounding Mode                  | RC Field Setting | Description                                                                                                                                                                                      |
|--------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Round to nearest (even)        | 00B              | Rounded result is the closest to the infinitely precise result. If two values are equally close, the result is the even value (that is, the one with the least-significant bit of zero). Default |
| Round down (toward $-\infty$ ) | 01B              | Rounded result is closest to but no greater than the infinitely precise result.                                                                                                                  |
| Round up (toward $+\infty$ )   | 10B              | Rounded result is closest to but no less than the infinitely precise result.                                                                                                                     |
| Round toward zero (Truncate)   | 11B              | Rounded result is closest to but no greater in absolute value than the infinitely precise result.                                                                                                |

The round up and round down modes are termed **directed rounding** and can be used to implement interval arithmetic. Interval arithmetic is used to determine upper and lower bounds for the true result of a multistep computation, when the intermediate results of the computation are subject to rounding.

The round toward zero mode (sometimes called the “chop” mode) is commonly used when performing integer arithmetic with the x87 FPU.

The rounded result is called the inexact result. When the processor produces an inexact result, the floating-point precision (inexact) flag (PE) is set (see Section 4.9.1.6, “Inexact-Result (Precision) Exception (#P)”).

The rounding modes have no effect on comparison operations, operations that produce exact results, or operations that produce NaN results.

#### 4.8.4.1 Rounding Control (RC) Fields

In the Intel 64 and IA-32 architectures, the rounding mode is controlled by a 2-bit rounding-control (RC) field (Table 4-9 shows the encoding of this field). The RC field is implemented in two different locations:

- X87 FPU control register (bits 10 and 11).
- The MXCSR register (bits 13 and 14).

Although these two RC fields perform the same function, they control rounding for different execution environments within the processor. The RC field in the x87 FPU control register controls rounding for computations performed with the x87 FPU instructions; the RC field in the MXCSR register controls rounding for SIMD floating-point computations performed with the Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions.

#### 4.8.4.2 Truncation with Intel® SSE, SSE2, and AVX Conversion Instructions

The following Intel SSE/SSE2 instructions automatically truncate the results of conversions from floating-point values to integers when the result is inexact: CVTTPD2DQ, CVTTPS2DQ, CVTTPD2PI, CVTTPS2PI, CVTTSD2SI, and CVTTSS2SI. Here, truncation means the round toward zero mode described in Table 4-9. There are also several Intel AVX2 and AVX-512 instructions which use truncation (VCVTT\*).

## 4.9 OVERVIEW OF FLOATING-POINT EXCEPTIONS

The following section provides an overview of floating-point exceptions and their handling in the IA-32 architecture. For information specific to the x87 FPU and to the Intel SSE/SSE2/SSE3/SSE4.1/AVX extensions, refer to the following sections:

- Section 4.9, “Overview of Floating-Point Exceptions.”
- Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions.”
- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

When operating on floating-point operands, the IA-32 architecture recognizes and detects six classes of exception conditions:

- Invalid operation (#I).
- Divide-by-zero (#Z).
- Denormalized operand (#D).
- Numeric overflow (#O).
- Numeric underflow (#U).
- Inexact result (precision) (#P).

The nomenclature of “#” symbol followed by one or two letters (for example, #P) is used in this manual to indicate exception conditions. It is merely a short-hand form and is not related to assembler mnemonics.

### NOTE

All of the exceptions listed above except the denormal-operand exception (#D) are defined in IEEE Standard 754.

The invalid-operation, divide-by-zero and denormal-operand exceptions are pre-computation exceptions (that is, they are detected before any arithmetic operation occurs). The numeric-underflow, numeric-overflow and precision exceptions are post-computation exceptions.

Each of the six exception classes has a corresponding flag bit (IE, ZE, OE, UE, DE, or PE) and mask bit (IM, ZM, OM, UM, DM, or PM). When one or more floating-point exception conditions are detected, the processor sets the appropriate flag bits, then takes one of two possible courses of action, depending on the settings of the corresponding mask bits:

- Mask bit set. Handles the exception automatically, producing a predefined (and often times usable) result, while allowing program execution to continue undisturbed.
- Mask bit clear. Invokes a software exception handler to handle the exception.

The masked (default) responses to exceptions have been chosen to deliver a reasonable result for each exception condition and are generally satisfactory for most floating-point applications. By masking or unmasking specific floating-point exceptions, programmers can delegate responsibility for most exceptions to the processor and reserve the most severe exception conditions for software exception handlers.

Because the exception flags are “sticky,” they provide a cumulative record of the exceptions that have occurred since they were last cleared. A programmer can thus mask all exceptions, run a calculation, and then inspect the exception flags to see if any exceptions were detected during the calculation.

In the IA-32 architecture, floating-point exception flag and mask bits are implemented in two different locations:

- X87 FPU status word and control word. The flag bits are located at bits 0 through 5 of the x87 FPU status word and the mask bits are located at bits 0 through 5 of the x87 FPU control word (see Figures 8-4 and 8-6).
- MXCSR register. The flag bits are located at bits 0 through 5 of the MXCSR register and the mask bits are located at bits 7 through 12 of the register (see Figure 10-3).

Although these two sets of flag and mask bits perform the same function, they report on and control exceptions for different execution environments within the processor. The flag and mask bits in the x87 FPU status and control words control exception reporting and masking for computations performed with the x87 FPU instructions; the

companion bits in the MXCSR register control exception reporting and masking for SIMD floating-point computations performed with the Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions.

Note that when exceptions are masked, the processor may detect multiple exceptions in a single instruction, because it continues executing the instruction after performing its masked response. For example, the processor can detect a denormalized operand, perform its masked response to this exception, and then detect numeric underflow.

See Section 4.9.2, “Floating-Point Exception Priority,” for a description of the rules for exception precedence when more than one floating-point exception condition is detected for an instruction.

## 4.9.1 Floating-Point Exception Conditions

The following sections describe the various conditions that cause a floating-point exception to be generated and the masked response of the processor when these conditions are detected. The Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volumes 3A, 3B, 3C, & 3D, lists the floating-point exceptions that can be signaled for each floating-point instruction.

### 4.9.1.1 Invalid Operation Exception (#I)

The processor reports an invalid operation exception in response to one or more invalid arithmetic operands. If the invalid operation exception is masked, the processor sets the IE flag and returns an indefinite value or a QNaN. This value overwrites the destination register specified by the instruction. If the invalid operation exception is not masked, the IE flag is set, a software exception handler is invoked, and the operands remain unaltered.

See Section 4.8.3.6, “Using SNaNs and QNaNs in Applications,” for information about the result returned when an exception is caused by an SNaN.

The processor can detect a variety of invalid arithmetic operations that can be coded in a program. These operations generally indicate a programming error, such as dividing  $\infty$  by  $\infty$ . See the following sections for information regarding the invalid-operation exception when detected while executing x87 FPU or Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions:

- X87 FPU; Section 8.5.1, “Invalid Operation Exception.”
- SIMD floating-point exceptions; Section 11.5.2.1, “Invalid Operation Exception (#I).”
- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

### 4.9.1.2 Denormal Operand Exception (#D)

The processor reports the denormal-operand exception if an arithmetic instruction attempts to operate on a denormal operand (see Section 4.8.3.2, “Normalized and Denormalized Finite Numbers”). When the exception is masked, the processor sets the DE flag and proceeds with the instruction. Operating on denormal numbers will produce results at least as good as, and often better than, what can be obtained when denormal numbers are flushed to zero. Programmers can mask this exception so that a computation may proceed, then analyze any loss of accuracy when the final result is delivered.

When a denormal-operand exception is not masked, the DE flag is set, a software exception handler is invoked, and the operands remain unaltered. When denormal operands have reduced significance due to loss of low-order bits, it may be advisable to not operate on them. Precluding denormal operands from computations can be accomplished by an exception handler that responds to unmasked denormal-operand exceptions.

See the following sections for information regarding the denormal-operand exception when detected while executing x87 FPU or Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions:

- X87 FPU; Section 8.5.2, “Denormal Operand Exception (#D).”
- SIMD floating-point exceptions; Section 11.5.2.2, “Denormal-Operand Exception (#D).”
- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

4.9.1.3 Divide-By-Zero Exception (#Z)

The processor reports the floating-point divide-by-zero exception whenever an instruction attempts to divide a finite non-zero operand by 0. The masked response for the divide-by-zero exception is to set the ZE flag and return an infinity signed with the exclusive OR of the sign of the operands. If the divide-by-zero exception is not masked, the ZE flag is set, a software exception handler is invoked, and the operands remain unaltered.

See the following sections for information regarding the divide-by-zero exception when detected while executing x87 FPU or Intel SSE/SSE2/AVX instructions:

- X87 FPU; Section 8.5.3, "Divide-By-Zero Exception (#Z)."
- SIMD floating-point exceptions; Section 11.5.2.3, "Divide-By-Zero Exception (#Z)."
- Section 12.8.4, "IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions."
- Section 14.10, "SIMD Floating-Point Exceptions."

4.9.1.4 Numeric Overflow Exception (#O)

The processor reports a floating-point numeric overflow exception whenever the rounded result of an instruction exceeds the largest allowable finite value that will fit into the destination operand. Table 4-10 shows the threshold range for numeric overflow for each of the floating-point formats; overflow occurs when a rounded result falls at or outside this threshold range.

Table 4-10. Numeric Overflow Thresholds

| Floating-Point Format     | Overflow Thresholds        |
|---------------------------|----------------------------|
| Half Precision            | $ x  \geq 1.0 * 2^{16}$    |
| Single Precision          | $ x  \geq 1.0 * 2^{128}$   |
| Double Precision          | $ x  \geq 1.0 * 2^{1024}$  |
| Double Extended Precision | $ x  \geq 1.0 * 2^{16384}$ |

When a numeric-overflow exception occurs and the exception is masked, the processor sets the OE flag and returns one of the values shown in Table 4-11, according to the current rounding mode. See Section 4.8.4, "Rounding."

When numeric overflow occurs and the numeric-overflow exception is not masked, the OE flag is set, a software exception handler is invoked, and the source and destination operands either remain unchanged or a biased result is stored in the destination operand (depending whether the overflow exception was generated during an Intel SSE/SSE2/SSE3/SSE4.1/AVX floating-point operation or an x87 FPU operation).

Table 4-11. Masked Responses to Numeric Overflow

| Rounding Mode    | Sign of True Result | Result                         |
|------------------|---------------------|--------------------------------|
| To nearest       | +                   | $+\infty$                      |
|                  | -                   | $-\infty$                      |
| Toward $-\infty$ | +                   | Largest finite positive number |
|                  | -                   | $-\infty$                      |
| Toward $+\infty$ | +                   | $+\infty$                      |
|                  | -                   | Largest finite negative number |
| Toward zero      | +                   | Largest finite positive number |
|                  | -                   | Largest finite negative number |

See the following sections for information regarding the numeric overflow exception when detected while executing x87 FPU instructions or while executing Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions:

- X87 FPU; Section 8.5.4, "Numeric Overflow Exception (#O)."
- SIMD floating-point exceptions; Section 11.5.2.4, "Numeric Overflow Exception (#O)."

- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

#### 4.9.1.5 Numeric Underflow Exception (#U)

The processor detects a potential floating-point numeric underflow condition whenever the result of rounding with unbounded exponent (taking into account precision control for x87) is non-zero and tiny; that is, non-zero and less than the smallest possible normalized, finite value that will fit into the destination operand. Table 4-12 shows the threshold range for numeric underflow for each of the floating-point formats (assuming normalized results); underflow occurs when a rounded result falls strictly within the threshold range. The ability to detect and handle underflow is provided to prevent a very small result from propagating through a computation and causing another exception (such as overflow during division) to be generated at a later time. Results which trigger underflow are also potentially less accurate.

**Table 4-12. Numeric Underflow (Normalized) Thresholds**

| Floating-Point Format     | Underflow Thresholds <sup>1</sup> |
|---------------------------|-----------------------------------|
| Half Precision            | $ x  < 1.0 * 2^{-14}$             |
| Single Precision          | $ x  < 1.0 * 2^{-126}$            |
| Double Precision          | $ x  < 1.0 * 2^{-1022}$           |
| Double Extended Precision | $ x  < 1.0 * 2^{-16382}$          |

#### NOTES:

1. Where ‘x’ is the result rounded to destination precision with an unbounded exponent range.

How the processor handles an underflow condition, depends on two related conditions:

- Creation of a tiny, non-zero result.
- Creation of an inexact result; that is, a result that cannot be represented exactly in the destination format.

Which of these events causes an underflow exception to be reported and how the processor responds to the exception condition depends on whether the underflow exception is masked:

- **Underflow exception masked** — The underflow exception is reported (the UE flag is set) only when the result is both tiny and inexact. The processor returns a correctly signed result whose magnitude is less than or equal to the smallest positive normal floating-point number to the destination operand, regardless of inexactness.
- **Underflow exception not masked** — The underflow exception is reported when the result is non-zero tiny, regardless of inexactness. The processor leaves the source and destination operands unaltered or stores a biased result in the destination operand (depending whether the underflow exception was generated during an Intel SSE/SSE2/SSE3/AVX floating-point operation or an x87 FPU operation) and invokes a software exception handler.

See the following sections for information regarding the numeric underflow exception when detected while executing x87 FPU instructions or while executing Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions:

- X87 FPU; Section 8.5.5, “Numeric Underflow Exception (#U).”
- SIMD floating-point exceptions; Section 11.5.2.5, “Numeric Underflow Exception (#U).”
- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

#### 4.9.1.6 Inexact-Result (Precision) Exception (#P)

The inexact-result exception (also called the precision exception) occurs if the result of an operation is not exactly representable in the destination format. For example, the fraction 1/3 cannot be precisely represented in binary floating-point form. This exception occurs frequently and indicates that some (normally acceptable) accuracy will be lost due to rounding. The exception is supported for applications that need to perform exact arithmetic only. Because the rounded result is generally satisfactory for most applications, this exception is commonly masked.

If the inexact-result exception is masked when an inexact-result condition occurs and a numeric overflow or underflow condition has not occurred, the processor sets the PE flag and stores the rounded result in the destination operand. The current rounding mode determines the method used to round the result. See Section 4.8.4, “Rounding.”

If the inexact-result exception is not masked when an inexact result occurs and numeric overflow or underflow has not occurred, the PE flag is set, the rounded result is stored in the destination operand, and a software exception handler is invoked.

If an inexact result occurs in conjunction with numeric overflow or underflow, one of the following operations is carried out:

- If an inexact result occurs along with masked overflow or underflow, the OE flag or UE flag and the PE flag are set and the result is stored as described for the overflow or underflow exceptions; see Section 4.9.1.4, “Numeric Overflow Exception (#O),” or Section 4.9.1.5, “Numeric Underflow Exception (#U).” If the inexact result exception is unmasked, the processor also invokes a software exception handler.
- If an inexact result occurs along with unmasked overflow or underflow and the destination operand is a register, the OE or UE flag and the PE flag are set, the result is stored as described for the overflow or underflow exceptions, and a software exception handler is invoked.

If an unmasked numeric overflow or underflow exception occurs and the destination operand is a memory location (which can happen only for a floating-point store), the inexact-result condition is not reported and the C1 flag is cleared.

See the following sections for information regarding the inexact-result exception when detected while executing x87 FPU or Intel SSE/SSE2/SSE3/SSE4.1/AVX instructions:

- X87 FPU; Section 8.5.6, “Inexact-Result (Precision) Exception (#P).”
- SIMD floating-point exceptions; Section 11.5.2.3, “Divide-By-Zero Exception (#Z).”
- Section 12.8.4, “IEEE 754 Compliance of Intel® SSE4.1 Floating-Point Instructions.”
- Section 14.10, “SIMD Floating-Point Exceptions.”

## 4.9.2 Floating-Point Exception Priority

The processor handles exceptions according to a predetermined precedence. When an instruction generates two or more exception conditions, the exception precedence sometimes results in the higher-priority exception being handled and the lower-priority exceptions being ignored. For example, dividing an SNaN by zero can potentially signal an invalid-operation exception (due to the SNaN operand) and a divide-by-zero exception. Here, if both exceptions are masked, the processor handles the higher-priority exception only (the invalid-operation exception), returning a QNaN to the destination. Alternately, a denormal-operand or inexact-result exception can accompany a numeric underflow or overflow exception with both exceptions being handled.

The precedence for floating-point exceptions is as follows:

1. Invalid-operation exception, subdivided as follows:
  - a. Stack underflow (occurs with x87 FPU only).
  - b. Stack overflow (occurs with x87 FPU only).
  - c. Operand of unsupported format (occurs with x87 FPU only when using the double extended precision floating-point format).
  - d. SNaN operand.
2. QNaN operand. Though this is not an exception, the handling of a QNaN operand has precedence over lower-priority exceptions. For example, a QNaN divided by zero results in a QNaN, not a zero-divide exception.
3. Any other invalid-operation exception not mentioned above or a divide-by-zero exception.
4. Denormal-operand exception. If masked, then instruction execution continues, and a lower-priority exception can occur as well.
5. Numeric overflow and underflow exceptions; possibly in conjunction with the inexact-result exception.
6. Inexact-result exception.

Invalid operation, zero divide, and denormal operand exceptions are detected before a floating-point operation begins. Overflow, underflow, and precision exceptions are not detected until a true result has been computed. When an unmasked **pre-operation** exception is detected, the destination operand has not yet been updated, and appears as if the offending instruction has not been executed. When an unmasked **post-operation** exception is detected, the destination operand may be updated with a result, depending on the nature of the exception (except for Intel SSE/SSE2/SSE3/AVX instructions, which do not update their destination operands in such cases).

### 4.9.3 Typical Actions of a Floating-Point Exception Handler

After the floating-point exception handler is invoked, the processor handles the exception in the same manner that it handles non-floating-point exceptions. The floating-point exception handler is normally part of the operating system or executive software, and it usually invokes a user-registered floating-point exception handle.

A typical action of the exception handler is to store state information in memory. Other typical exception handler actions include:

- Examining the stored state information to determine the nature of the error.
- Taking actions to correct the condition that caused the error.
- Clearing the exception flags.
- Returning to the interrupted program and resuming normal execution.

In lieu of writing recovery procedures, the exception handler can do the following:

- Increment in software an exception counter for later display or printing.
- Print or display diagnostic information (such as the state information).
- Halt further program execution.



This chapter provides an abridged overview of Intel 64 and IA-32 instructions. Instructions are divided into the following groups:

- Section 5.1, "General-Purpose Instructions."
- Section 5.2, "x87 FPU Instructions."
- Section 5.3, "x87 FPU AND SIMD State Management Instructions."
- Section 5.4, "MMX Instructions."
- Section 5.5, "Intel® SSE Instructions."
- Section 5.6, "Intel® SSE2 Instructions."
- Section 5.7, "Intel® SSE3 Instructions."
- Section 5.8, "Supplemental Streaming SIMD Extensions 3 (SSSE3) Instructions."
- Section 5.9, "Intel® SSE4 Instructions."
- Section 5.10, "Intel® SSE4.1 Instructions."
- Section 5.11, "Intel® SSE4.2 Instruction Set."
- Section 5.12, "Intel® AES-NI and PCLMULQDQ."
- Section 5.13, "Intel® Advanced Vector Extensions (Intel® AVX)."
- Section 5.14, "16-bit Floating-Point Conversion."
- Section 5.15, "Fused-Multiply-ADD (FMA)."
- Section 5.16, "Intel® Advanced Vector Extensions 2 (Intel® AVX2)."
- Section 5.17, "Intel® Transactional Synchronization Extensions (Intel® TSX)."
- Section 5.18, "Intel® SHA Extensions."
- Section 5.19, "Intel® Advanced Vector Extensions 512 (Intel® AVX-512)."
- Section 5.20, "System Instructions."
- Section 5.21, "64-Bit Mode Instructions."
- Section 5.22, "Virtual-Machine Extensions."
- Section 5.23, "Safer Mode Extensions."
- Section 5.24, "Intel® Memory Protection Extensions."
- Section 5.25, "Intel® Software Guard Extensions."
- Section 5.26, "Shadow Stack Management Instructions."
- Section 5.27, "Control Transfer Terminating Instructions."
- Section 5.28, "Intel® AMX Instructions."
- Section 5.29, "User Interrupt Instructions."
- Section 5.30, "Enqueue Store Instructions."
- Section 5.31, "Intel® Advanced Vector Extensions 10 Version 1 Instructions."

Table 5-1 lists the groups and IA-32 processors that support each group. More recent instruction set extensions are listed in Table 5-2. Within these groups, most instructions are collected into functional subgroups.

**Table 5-1. Instruction Groups in Intel® 64 and IA-32 Processors**

| Instruction Set Architecture          | Intel 64 and IA-32 Processor Support                                                                                                                                                                                                                                |
|---------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| General Purpose                       | All Intel 64 and IA-32 processors.                                                                                                                                                                                                                                  |
| X87 FPU                               | Intel486, Pentium, Pentium with MMX Technology, Celeron, Pentium Pro, Pentium II, Pentium II Xeon, Pentium III, Pentium III Xeon, Pentium 4, Intel Xeon processors, Pentium M, Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Atom processors. |
| X87 FPU and SIMD State Management     | Pentium II, Pentium II Xeon, Pentium III, Pentium III Xeon, Pentium 4, Intel Xeon processors, Pentium M, Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Atom processors.                                                                       |
| MMX Technology                        | Pentium with MMX Technology, Celeron, Pentium II, Pentium II Xeon, Pentium III, Pentium III Xeon, Pentium 4, Intel Xeon processors, Pentium M, Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Atom processors.                                 |
| SSE Extensions                        | Pentium III, Pentium III Xeon, Pentium 4, Intel Xeon processors, Pentium M, Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Atom processors.                                                                                                    |
| SSE2 Extensions                       | Pentium 4, Intel Xeon processors, Pentium M, Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Atom processors.                                                                                                                                   |
| SSE3 Extensions                       | Pentium 4 supporting HT Technology (built on 90 nm process technology), Intel Core Solo, Intel Core Duo, Intel Core 2 Duo processors, Intel Xeon processor 3xxx, 5xxx, 7xxx Series, Intel Atom processors.                                                          |
| SSSE3 Extensions                      | Intel Xeon processor 3xxx, 5100, 5200, 5300, 5400, 5500, 5600, 7300, 7400, 7500 series, Intel Core 2 Extreme processors QX6000 series, Intel Core 2 Duo, Intel Core 2 Quad processors, Intel Pentium Dual-Core processors, Intel Atom processors.                   |
| IA-32e mode: 64-bit mode instructions | Intel 64 processors.                                                                                                                                                                                                                                                |
| System Instructions                   | Intel 64 and IA-32 processors.                                                                                                                                                                                                                                      |
| VMX Instructions                      | Intel 64 and IA-32 processors supporting Intel Virtualization Technology.                                                                                                                                                                                           |
| SMX Instructions                      | Intel Core 2 Duo processor E6x50, E8xxx; Intel Core 2 Quad processor Q9xxx.                                                                                                                                                                                         |

**Table 5-2. Instruction Set Extensions Introduction in Intel® 64 and IA-32 Processors**

| Instruction Set Architecture     | Processor Generation Introduction                                                                                                                                                                                                                                                       |
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SSE4.1 Extensions                | Intel® Xeon® processor 3100, 3300, 5200, 5400, 7400, 7500 series, Intel® Core™ 2 Extreme processors QX9000 series, Intel® Core™ 2 Quad processor Q9000 series, Intel® Core™ 2 Duo processors 8000 series and T9000 series, Intel Atom® processor based on Silvermont microarchitecture. |
| SSE4.2 Extensions, CRC32, POPCNT | Intel® Core™ i7 965 processor, Intel® Xeon® processors X3400, X3500, X5500, X6500, X7500 series, Intel Atom processor based on Silvermont microarchitecture.                                                                                                                            |
| Intel® AES-NI, PCLMULQDQ         | Intel® Xeon® processor E7 series, Intel® Xeon® processors X3600 and X5600, Intel® Core™ i7 980X processor, Intel Atom processor based on Silvermont microarchitecture. Use CPUID to verify presence of Intel AES-NI and PCLMULQDQ across Intel® Core™ processor families.               |
| Intel® AVX                       | Intel® Xeon® processor E3 and E5 families, 2nd Generation Intel® Core™ i7, i5, i3 processor 2xxx families.                                                                                                                                                                              |
| F16C                             | 3rd Generation Intel® Core™ processors, Intel® Xeon® processor E3-1200 v2 product family, Intel® Xeon® processor E5 v2 and E7 v2 families.                                                                                                                                              |
| RDRAND                           | 3rd Generation Intel Core processors, Intel Xeon processor E3-1200 v2 product family, Intel Xeon processor E5 v2 and E7 v2 families, Intel Atom processor based on Silvermont microarchitecture.                                                                                        |
| FS/GS base access                | 3rd Generation Intel Core processors, Intel Xeon processor E3-1200 v2 product family, Intel Xeon processor E5 v2 and E7 v2 families, Intel Atom® processor based on Goldmont microarchitecture.                                                                                         |

**Table 5-2. Instruction Set Extensions Introduction in Intel® 64 and IA-32 Processors (Contd.)**

| <b>Instruction Set Architecture</b>               | <b>Processor Generation Introduction</b>                                                                                                                                                                                                                       |
|---------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FMA, AVX2, BMI1, BMI2, INVPCID, LZCNT, Intel® TSX | Intel® Xeon® processor E3/E5/E7 v3 product families, 4th Generation Intel® Core™ processor family.                                                                                                                                                             |
| MOVBE                                             | Intel Xeon processor E3/E5/E7 v3 product families, 4th Generation Intel Core processor family, Intel Atom processors.                                                                                                                                          |
| PREFETCHW                                         | Intel® Core™ M processor family; 5th Generation Intel® Core™ processor family, Intel Atom processor based on Silvermont microarchitecture.                                                                                                                     |
| ADX                                               | Intel Core M processor family, 5th Generation Intel Core processor family.                                                                                                                                                                                     |
| RDSEED, CLAC, STAC                                | Intel Core M processor family, 5th Generation Intel Core processor family, Intel Atom processor based on Goldmont microarchitecture.                                                                                                                           |
| AVX512ER, AVX512PF, PREFETCHWT1                   | Intel® Xeon Phi™ Processor 3200, 5200, 7200 Series.                                                                                                                                                                                                            |
| AVX512F, AVX512CD                                 | Intel Xeon Phi Processor 3200, 5200, 7200 Series, Intel® Xeon® Scalable Processor Family, Intel® Core™ i3-8121U processor.                                                                                                                                     |
| CLFLUSHOPT, XSAVEC, XSAVES, Intel® MPX            | Intel Xeon Scalable Processor Family, 6th Generation Intel® Core™ processor family, Intel Atom processor based on Goldmont microarchitecture.                                                                                                                  |
| SGX1                                              | 6th Generation Intel Core processor family, Intel Atom® processor based on Goldmont Plus microarchitecture.                                                                                                                                                    |
| AVX512DQ, AVX512BW, AVX512VL                      | Intel Xeon Scalable Processor Family, Intel Core i3-8121U processor based on Cannon Lake microarchitecture.                                                                                                                                                    |
| CLWB                                              | Intel Xeon Scalable Processor Family, Intel Atom® processor based on Tremont microarchitecture, 11th Generation Intel Core processor family based on Tiger Lake microarchitecture.                                                                             |
| PKU                                               | Intel Xeon Scalable Processor Family, 10th generation Intel® Core™ processors based on Comet Lake microarchitecture.                                                                                                                                           |
| AVX512_IFMA, AVX512_VBMI                          | Intel Core i3-8121U processor based on Cannon Lake microarchitecture.                                                                                                                                                                                          |
| Intel® SHA Extensions                             | Intel Core i3-8121U processor based on Cannon Lake microarchitecture, Intel Atom processor based on Goldmont microarchitecture, 3rd Generation Intel® Xeon® Scalable Processor Family based on Ice Lake microarchitecture.                                     |
| UMIP                                              | Intel Core i3-8121U processor based on Cannon Lake microarchitecture, Intel Atom processor based on Goldmont Plus microarchitecture.                                                                                                                           |
| PTWRITE                                           | Intel Atom processor based on Goldmont Plus microarchitecture, 12th generation Intel® Core™ processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture. |
| RDPID                                             | 10th Generation Intel® Core™ processor family based on Ice Lake microarchitecture, Intel Atom processor based on Goldmont Plus microarchitecture.                                                                                                              |
| AVX512_4FMAPS, AVX512_4VNNIW                      | Intel® Xeon Phi™ Processor 7215, 7285, 7295 Series.                                                                                                                                                                                                            |
| AVX512_VNNI                                       | 2nd Generation Intel® Xeon® Scalable Processor Family, 10th Generation Intel Core processor family based on Ice Lake microarchitecture.                                                                                                                        |
| AVX512_VPOPCNTDQ                                  | Intel Xeon Phi Processor 7215, 7285, 7295 Series, 10th Generation Intel Core processor family based on Ice Lake microarchitecture.                                                                                                                             |
| Fast Short REP MOVSB                              | 10th Generation Intel Core processor family based on Ice Lake microarchitecture.                                                                                                                                                                               |
| GFNI (SSE)                                        | 10th Generation Intel Core processor family based on Ice Lake microarchitecture, Intel Atom processor based on Tremont microarchitecture.                                                                                                                      |

**Table 5-2. Instruction Set Extensions Introduction in Intel® 64 and IA-32 Processors (Contd.)**

| Instruction Set Architecture                                                   | Processor Generation Introduction                                                                                                                                                                                                                                                      |
|--------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| VAES, GFNI (AVX/AVX512), AVX512_VBMI2, VPCLMULQDQ, AVX512_BITALG               | 10th Generation Intel Core processor family based on Ice Lake microarchitecture.                                                                                                                                                                                                       |
| Split Lock Detection                                                           | 10th Generation Intel Core processor family based on Ice Lake microarchitecture, Intel Atom processor based on Tremont microarchitecture.                                                                                                                                              |
| CLDEMOT                                                                        | Intel Atom processor based on Tremont microarchitecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                                             |
| Direct stores: MOVDIRI, MOVDIR64B                                              | Intel Atom processor based on Tremont microarchitecture, 11th Generation Intel Core processor family based on Tiger Lake microarchitecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                          |
| User wait: TPAUSE, UMONITOR, UMWAIT                                            | Intel Atom processor based on Tremont microarchitecture, 12th generation Intel Core processor based on Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                   |
| AVX512-BF16                                                                    | 3rd Generation Intel® Xeon® Scalable Processor Family based on Cooper Lake product, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                  |
| AVX512_VP2INTERSECT                                                            | 11th Generation Intel Core processor family based on Tiger Lake microarchitecture. (Not currently supported in any other processors).                                                                                                                                                  |
| Key Locker <sup>1</sup>                                                        | 11th Generation Intel Core processor family based on Tiger Lake microarchitecture, 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture.                                                                                                         |
| Control-flow Enforcement Technology (CET)                                      | 11th Generation Intel Core processor family based on Tiger Lake microarchitecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.                        |
| TME-MK <sup>2</sup> , PCONFIG                                                  | 3rd Generation Intel® Xeon® Scalable Processor Family based on Ice Lake microarchitecture.                                                                                                                                                                                             |
| WBNOINVD                                                                       | 3rd Generation Intel® Xeon® Scalable Processor Family based on Ice Lake microarchitecture.                                                                                                                                                                                             |
| LBRs (architectural)                                                           | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.               |
| Intel® Virtualization Technology - Redirect Protection (Intel® VT-rp) and HLAT | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.               |
| AVX-VNNI                                                                       | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture <sup>3</sup> , 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture. |
| SERIALIZE                                                                      | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.               |
| Intel® Thread Director and HRESET                                              | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture.                                                                                                                                                                                            |
| Fast zero-length REP MOVSB, fast short REP STOSB                               | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                          |
| Fast Short REP CMPSB, fast short REP SCASB                                     | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                                                                                                      |
| Supervisor Memory Protection Keys (PKS)                                        | 12th generation Intel Core processor supporting Alder Lake performance hybrid architecture, 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.               |

**Table 5-2. Instruction Set Extensions Introduction in Intel® 64 and IA-32 Processors (Contd.)**

| <b>Instruction Set Architecture</b>                                                                                                                  | <b>Processor Generation Introduction</b>                                                                                                                                                                                                                                                                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Attestation Services for Intel® SGX                                                                                                                  | 3rd Generation Intel® Xeon® Scalable Processor Family based on Ice Lake microarchitecture.                                                                                                                                                                                                                                                           |
| Enqueue Stores: ENQCMD and ENQCMD5                                                                                                                   | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture.                                                                                                                                                                         |
| Intel® TSX Suspend Load Address Tracking (TSXLDTRK)                                                                                                  | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                                                                                                                                                                    |
| Intel® Advanced Matrix Extensions (Intel® AMX)<br>Includes CPUID.1EH, “TMUL Information Main Leaf”, and CPUID bits AMX_BF16, AMX_TILE, and AMX_INT8. | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                                                                                                                                                                    |
| User Interrupts (UINTR)                                                                                                                              | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture. |
| IPI Virtualization                                                                                                                                   | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture. |
| AVX512-FP16 for the FP16 Data Type                                                                                                                   | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture.                                                                                                                                                                                                                                                    |
| Virtualization of guest accesses to IA32_SPEC_CTRL                                                                                                   | 4th generation Intel® Xeon® Scalable Processor Family based on Sapphire Rapids microarchitecture, Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture.                                                                                                  |
| Linear Address Masking (LAM)                                                                                                                         | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| Linear Address Space Separation (LASS)                                                                                                               | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| PREFETCHIT0/1                                                                                                                                        | Intel® Xeon® 6 P-core processors based on Granite Rapids microarchitecture.                                                                                                                                                                                                                                                                          |
| AMX_FP16                                                                                                                                             | Intel® Xeon® 6 P-core processors based on Granite Rapids microarchitecture.                                                                                                                                                                                                                                                                          |
| CMPPCXADD                                                                                                                                            | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| AVX-IFMA                                                                                                                                             | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| AVX-NE-CONVERT                                                                                                                                       | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| AVX-VNNI-INT8                                                                                                                                        | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                   |
| AVX-VNNI-INT16                                                                                                                                       | Intel® Core™ Ultra 200S Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                                                                                                                                                                     |
| SHA512                                                                                                                                               | Intel® Core™ Ultra 200S Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                                                                                                                                                                     |

**Table 5-2. Instruction Set Extensions Introduction in Intel® 64 and IA-32 Processors (Contd.)**

| Instruction Set Architecture                                    | Processor Generation Introduction                                                                                                                                                                                                                  |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SM3                                                             | Intel® Core™ Ultra 200S Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                                                                   |
| SM4                                                             | Intel® Core™ Ultra 200S Series processors supporting Arrow Lake performance hybrid architecture.                                                                                                                                                   |
| RDMSRLIST, WRMSRLIST, and WRMSRNS                               | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture.                                                                                                  |
| UC Lock Disable Causes #AC                                      | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture.                                                                                                  |
| LBR Event Logging                                               | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200S Series processors supporting Arrow Lake performance hybrid architecture. |
| UIRET flexibly updates UIF                                      | Intel® Xeon® 6 E-core processors based on Sierra Forest microarchitecture, Intel® Atom® P6900 Processor based on the Crestmont microarchitecture, Intel® Core™ Ultra 200H Series processors supporting Arrow Lake performance hybrid architecture. |
| Intel® Advanced Vector Extensions 10 Version 1 (Intel® AVX10.1) | Intel® Xeon® 6 P-core processors based on Granite Rapids microarchitecture.                                                                                                                                                                        |

**NOTES:**

1. Details on Key Locker can be found in the Intel Key Locker Specification here:  
<https://software.intel.com/content/www/us/en/develop/download/intel-key-locker-specification.html>.
2. Further details on TME-MK usage can be found here:  
<https://software.intel.com/sites/default/files/managed/a5/16/Multi-Key-Total-Memory-Encryption-Spec.pdf>.
3. Alder Lake performance hybrid architecture does not support Intel® AVX-512. ISA features such as Intel® AVX, AVX-VNNI, Intel® AVX2, and UMONITOR/UMWAIT/TPAUSE are supported.

The following sections list instructions in each major group and subgroup. Given for each instruction is its mnemonic and descriptive names. When two or more mnemonics are given (for example, CMOVA/CMOVNBE), they represent different mnemonics for the same instruction opcode. Assemblers support redundant mnemonics for some instructions to make it easier to read code listings. For instance, CMOVA (Conditional move if above) and CMOVNBE (Conditional move if not below or equal) represent the same condition. For detailed information about specific instructions, see the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volumes 2A, 2B, 2C, & 2D.