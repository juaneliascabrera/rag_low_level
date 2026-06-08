---
architecture: x86_32
component: processor_identification
mode: protected
tags: ['cpuid', 'feature_detection']
source: intel_sdm_vol1_chapter_21.md
---

# Intel SDM Volume 1 - Chapter 21

# CHAPTER 21

## PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

---

When writing software intended to run on Intel processors, it is necessary to identify the type of processor present in a system and the processor features that are available to an application.

The CPUID instruction, known as CPU Identification, was introduced with the Intel® Pentium processor to query the processor's information name space for its identity and supported features. Logically, the CPUID name space comprises a series of nodes indexed by leaf (using the input value of EAX) and in some cases further indexed by sub-leaf (using the input value of ECX). The value of a queried node is returned in EAX, EBX, ECX, and EDX. Note that not all leaves have sub-leaf indexing and the input ECX value will be ignored in those cases. The full description of CPUID can be found in Chapter 3 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 2A.

All references to "MAX\_LEAF" throughout this chapter are used as an abbreviation of "CPUID.00H:EAX.MAX\_LEAF".

### 21.1 IMPORTANT CONSIDERATIONS WHEN USING THE CPUID INSTRUCTION

This section outlines additional factors to consider when using the CPUID instruction.

#### 21.1.1 Guidelines for Using the CPUID Instruction

Use the CPUID instruction for processor identification in the Pentium M processor family, Pentium 4 processor family, Intel Xeon processor family, P6 family, Pentium processor, and later Intel486 processors. This instruction returns the family, model, and (for some processors) a brand string for the processor that executes the instruction. It also indicates the features that are present in the processor and gives information about the processor's caches and TLB.

The ID flag (bit 21) in the EFLAGS register indicates support for the CPUID instruction. If a software procedure can set and clear this flag, the processor executing the procedure supports the CPUID instruction. The CPUID instruction will cause the invalid opcode exception (#UD) if executed on a processor that does not support it.

To obtain processor identification information, a source operand value is placed in the EAX register to select the type of information to be returned. When the CPUID instruction is executed, selected information is returned in the EAX, EBX, ECX, and EDX registers.

The following guidelines are among the most important and should always be followed when using the CPUID instruction to determine available features:

- Always begin by testing for the "GenuineIntel," message in the EBX, EDX, and ECX registers when the CPUID instruction is executed with EAX equal to 0. If the processor is not genuine Intel, the feature identification flags may have different meanings than are described in Intel documentation.
- Test feature identification flags individually and do not make assumptions about undefined bits.

#### 21.1.2 Identification of Earlier Processors

The CPUID instruction is not available in earlier Intel processors up through the earlier Intel 486 processors. For these processors, several other architectural features can be exploited to identify the processor.

The settings of bits 12 and 13 (IOPL), 14 (NT), and 15 (reserved) in the EFLAGS register are different for Intel's 32-bit processors than for the Intel 8086 and Intel 286 processors. By examining the settings of these bits (with the PUSHF/PUSHFD and POPF/POPF instructions), an application program can determine whether the processor is an 8086, Intel 286, or one of the Intel 32-bit processors:

- 8086 processor — Bits 12 through 15 of the EFLAGS register are always set.
- Intel 286 processor — Bits 12 through 15 are always clear in real-address mode.

- 32-bit processors — In real-address mode, bit 15 is always clear and bits 12 through 14 have the last value loaded into them. In protected mode, bit 15 is always clear, bit 14 has the last value loaded into it, and the IOPL bits depend on the current privilege level (CPL). The IOPL field can be changed only if the CPL is 0.

Other EFLAGS register bits that can be used to differentiate between the 32-bit processors:

- Bit 18 (AC) — Implemented only on the Pentium 4, Intel Xeon, P6 family, Pentium, and Intel486 processors. The inability to set or clear this bit distinguishes an Intel386 processor from the later IA-32 processors.
- Bit 21 (ID) — Determines if the processor is able to execute the CPUID instruction. The ability to set and clear this bit indicates that it is a Pentium 4, Intel Xeon, P6 family, Pentium, or later-version Intel486 processor.

To determine whether an x87 FPU or Numeric Processor Extension (NPX) is present in a system, applications can write to the x87 FPU status and control registers using the FNINIT instruction and then verify that the correct values are read back using the FNSTENV instruction.

After determining that an x87 FPU or NPX is present, its type can then be determined. In most cases, the processor type will determine the type of FPU or NPX; however, an Intel386 processor is compatible with either an Intel 287 or Intel 387 math coprocessor.

The method the coprocessor uses to represent  $\infty$  (after the execution of the FINIT, FNINIT, or RESET instruction) indicates which coprocessor is present. The Intel 287 math coprocessor uses the same bit representation for  $+\infty$  and  $-\infty$ ; whereas, the Intel 387 math coprocessor uses different representations for  $+\infty$  and  $-\infty$ .

### 21.1.3 CPUID Basic and Extended Range

The CPUID basic range starts at CPUID.00H and ends at the maximum leaf enumerated in CPUID.00H:EAX.MAX\_LEAF[31:0].

The legacy set of CPUID leaves are defined as leaves 00H, 01H, and 02H, which represent the architecture up to and including Pentium II. Processors provided legacy compatibility by limiting the exposed number of leaves to just these legacy leaves by setting IA32\_MISC\_ENABLE[22] (Limit CPUID Maxval). This is no longer supported on processors that report CPUID.07H.01H:EBX.CPUIDMAXVAL\_LIM\_RMV[3] as 1; for such processors, IA32\_MISC\_ENABLE[22] cannot be set to 1 to limit the value returned by CPUID.00H:EAX.MAX\_LEAF.

The extended CPUID range starts at leaf 80000000H and ends at the maximum leaf enumerated in CPUID.80000000H:EAX.MAX\_EXTENDED\_LEAF[31:0].

Older processors before the Pentium 4 do not support the extended CPUID range and treat bit 31 of CPUID's input EAX value as zero.

If a value entered for CPUID.EAX is higher than the maximum input value for basic or extended function for that processor then the data for the highest basic information leaf is returned. Software should not rely on the values returned by the processor outside of the above ranges.

The range CPUID.40000000H to CPUID.4FFFFFFFH do not return feature information for the processor. These are allocated for emulation by software.

### 21.1.4 CPUID Domains

The fields of each CPUID node are classified into one of several CPUID domains. The fields may be classified separately within a specific node or in aggregate for all the nodes in a leaf or sub-leaf. On a properly configured platform, all logical processors within a CPUID domain return a consistent output value for fields belonging to that domain. As an example, the initial X2APIC ID value returned in CPUID.1FH.00H:EDX[31:0] is classified as being in the Logical Processor Domain because the value is unique for each logical processor in the platform. Whereas, the CLFLUSH Line Size returned in CPUID.00H:EBX[15:8] is classified as Platform Domain because it must be consistent for all logical processor within the entire platform.

- **Platform Domain**—A properly configured platform would provide consistent values for these CPUID fields for each logical processor in the platform.
- **Package Domain**—A properly configured platform provides consistent values for these CPUID fields for each logical processor within the same processor package. These values however can be different when comparing the values of logical processors on different packages.

- **Logical Processor Domain**—A properly configured platform can provide different values for these CPUID fields for each logical processor in the platform. The values contained within these may have their own scope as per a specific shared resource (i.e., cache, hybrid, etc.); in that case, each logical processor may need to be queried to obtain the full platform view of given features.

### 21.1.5 CPUID Runtime Mutable Fields

A CPUID field is said to be mutable if it can change during runtime. Such fields are affected by supervisor-mode operations that can affect processor mode, status bits, or privileged registers. Mutable fields that are expected to change dynamically as part of normal operation are shown in the table Table 21-1. Mutable fields that should remain consistent are shown in the table Table 21-2. Note all of the listed controls may not be available on all Intel processors.

**Table 21-1. Runtime Mutable CPUID Fields Expected to Change During Normal Operation**

| Leaf      | Sub-Leaf | Register  | Field Name                  | Description and Mutability Control                                                                                                                                  |
|-----------|----------|-----------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 01H       | Ignored  | ECX[27]   | OSXSAVE                     | If 1, the OS has set CR4.OSXSAVE[bit 18] to enable XSETBV/XGETBV instructions to access XCR0 and to support processor extended state management using XSAVE/XRSTOR. |
| 07H       | 00H      | ECX[4]    | OSPKE                       | If 1, OS has set CR4.PKE to enable protection keys (and the RDPKRU/WRPKRU instructions).                                                                            |
| 0DH       | 00H      | EBX[31:0] | XSAVE_BYTES_ENABLED_FEATURE | The size of the XSAVE/XRSTOR area required for the state bits enabled in XCR0.                                                                                      |
| 0DH       | 01H      | EBX[31:0] | XSAVE_BYTES_ENABLED_FEATURE | The size of the XSAVES/XRSTORS area required for the state bits enabled in XCR0 and IA32_XSS.                                                                       |
| 19H       | 00H      | EBX[0]    | AESKLE                      | If 1, if the AES Key Locker instructions have been activated by system firmware and the OS has set CR4.KL[bit 19] = 1.                                              |
| 80000001H | Ignored  | EDX[20]   | SYSCALL_SYSRET_64           | Intel processors support SYSCALL and SYSRET only in 64-bit mode. This feature flag is always enumerated as 0 outside 64-bit mode.                                   |

**Table 21-2. Runtime Mutable CPUID Fields That Should Remain Consistent**

| Leaf | Sub-Leaf | Register  | Field Name               | Description and Mutability Control                                                                                                                        |
|------|----------|-----------|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| 00H  | Ignored  | EAX[31:0] | MAX_LEAF                 | Support for legacy software by limiting CPUID number of leaves reporting to a maximum of 2. This is set by using IA32_MISC_ENABLE[22] Limit CPUID Maxval. |
| 01H  | Ignored  | ECX[3]    | MONITOR                  | This feature flag reflects the setting in IA32_MISC_ENABLE[18] Enable Monitor FSM.                                                                        |
| 01H  | Ignored  | ECX[7]    | EIST                     | This feature flag reflects the setting in IA32_MISC_ENABLE[16] Enhanced Intel SpeedStep Technology Enable.                                                |
| 01H  | Ignored  | EDX[9]    | APIC                     | This feature flag reflects IA32_APIC_BASE[11], APIC Global Enable.                                                                                        |
| 05H  | Ignored  | ECX[0]    | MONITOR_MWAIT_EXTENSIONS | This field not available when CPUID.01H:ECX.MONITOR[3] = 0.                                                                                               |

**Table 21-2. Runtime Mutable CPUID Fields That Should Remain Consistent (Contd.)**

| Leaf | Sub-Leaf | Register  | Field Name                 | Description and Mutability Control                          |
|------|----------|-----------|----------------------------|-------------------------------------------------------------|
| 05H  | Ignored  | ECX[1]    | INTERRUPT_AS_BREAK_EVENT   | This field not available when CPUID.01H:ECX.MONITOR[3] = 0. |
| 05H  | Ignored  | EDX[15:0] | LARGEST_MONITOR_LINE_SIZE  | This field not available when CPUID.01H:ECX.MONITOR[3] = 0. |
| 05H  | Ignored  | EAX[15:0] | SMALLEST_MONITOR_LINE_SIZE | This field not available when CPUID.01H:ECX.MONITOR[3] = 0. |

### 21.1.6 CPUID Reserved Fields

Software must ignore and not rely upon the values returned by reserved fields of a CPUID leaf or sub-leaf because they may have meaning on future processors. Once a previously-reserved field becomes defined, this specification will be updated to reflect that.

### 21.1.7 CPUID Instruction for Serialization

Although the CPUID instruction provides serialization, it is not the preferred method on newer processors that support the SERIALIZE instruction, which is enumerated via CPUID.07H.00H:EDX[14]=1. If backward compatibility is required with older processors, use leaf 00H [CPUID.00H] for serialization because it has the lowest latency when executed. See “Serializing Instructions” in Chapter 11 of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A for more details.

### 21.1.8 IA32\_BIOS\_SIGN\_ID Returns Microcode Update Signature

For processors that support the microcode update facility, the IA32\_BIOS\_SIGN\_ID MSR is loaded with the update signature whenever CPUID executes. The signature is returned in the upper DWORD. For details, see Chapter 11 in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A.

## 21.2 METHODS FOR RETURNING BRANDING INFORMATION USING CPUID

Use the following techniques to access branding information:

1. Processor brand string method.
2. Processor brand index; this method uses a software supplied brand string table.

These two methods are discussed in the following sections. For methods that are available in early processors, see Section 21.1.2, “Identification of Earlier Processors,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1.

### 21.2.1 The Processor Brand String Method

Figure 21-1 describes the algorithm used for detection of the brand string. Processor brand identification software should execute this algorithm on all Intel 64 and IA-32 processors.

This method (introduced with Pentium 4 processors) returns an ASCII brand identification string and the Processor Base frequency of the processor to the EAX, EBX, ECX, and EDX registers.

![Flowchart for Determination of Support for the Processor Brand String. The process starts with 'Input: EAX= 0x80000000', followed by a 'CUID' step. A decision diamond asks 'IF (EAX & 0x80000000)'. If 'False', it leads to 'Processor Brand String Not Supported'. If 'True', it leads to 'CUID Function Supported' and then 'True ≥ Extended'. This is followed by 'EAX Return Value = Max. Extended CUID Function Index'. A second decision diamond asks 'IF (EAX Return Value ≥ 0x80000004)'. If 'True', it leads to 'Processor Brand String Supported'. The ID 'OM15194' is at the bottom right.](707eda2498b30c4fe45ac9feeefccb06_img.jpg)

```

graph TD
    Start[Input: EAX= 0x80000000] --> CUID[CUID]
    CUID --> Dec1{IF (EAX & 0x80000000)}
    Dec1 -- False --> NotSupported[Processor Brand String Not Supported]
    Dec1 -- True --> CUID_Supported[CUID Function Supported]
    CUID_Supported -- True ≥ Extended --> EAX_Return[EAX Return Value = Max. Extended CUID Function Index]
    EAX_Return --> Dec2{IF (EAX Return Value ≥ 0x80000004)}
    Dec2 -- True --> Supported[Processor Brand String Supported]
    
```

OM15194

Flowchart for Determination of Support for the Processor Brand String. The process starts with 'Input: EAX= 0x80000000', followed by a 'CUID' step. A decision diamond asks 'IF (EAX & 0x80000000)'. If 'False', it leads to 'Processor Brand String Not Supported'. If 'True', it leads to 'CUID Function Supported' and then 'True ≥ Extended'. This is followed by 'EAX Return Value = Max. Extended CUID Function Index'. A second decision diamond asks 'IF (EAX Return Value ≥ 0x80000004)'. If 'True', it leads to 'Processor Brand String Supported'. The ID 'OM15194' is at the bottom right.

Figure 21-1. Determination of Support for the Processor Brand String

## 21.2.2 The Processor Brand Index Method

The brand index method (introduced with Pentium® III Xeon® processors) provides an entry point into a brand identification table that is maintained in memory by software. In this table, each brand index is associated with an ASCII brand identification string that identifies the official Intel family and model number of a processor.

When CUID executes with EAX set to 1, the processor returns a brand index to the low byte in EBX. Software can then use this index to locate the brand identification string for the processor in the brand identification table. The first entry (brand index 0) in this table is reserved, allowing for backward compatibility with processors that do not support the brand identification feature. Starting with processor signature family ID = 0FH, model = 03H, brand index method is no longer supported. Use brand string method instead.

Table 21-3 shows brand indices that have identification strings associated with them.

**Table 21-3. Mapping of Brand Indices; and Intel 64 and IA-32 Processor Brand Strings**

| Brand Index | Brand String                                                                                            |
|-------------|---------------------------------------------------------------------------------------------------------|
| 00H         | This processor does not support the brand identification feature                                        |
| 01H         | Intel® Celeron® processor <sup>1</sup>                                                                  |
| 02H         | Intel® Pentium® III processor <sup>1</sup>                                                              |
| 03H         | Intel® Pentium® III Xeon® processor; If processor signature = 000006B1h, then Intel® Celeron® processor |
| 04H         | Intel® Pentium® III processor                                                                           |
| 06H         | Mobile Intel® Pentium® III processor-M                                                                  |
| 07H         | Mobile Intel® Celeron® processor <sup>1</sup>                                                           |

Table 21-3. Mapping of Brand Indices; and Intel 64 and IA-32 Processor Brand Strings

|            |                                                                                                       |
|------------|-------------------------------------------------------------------------------------------------------|
| 08H        | Intel® Pentium® 4 processor                                                                           |
| 09H        | Intel® Pentium® 4 processor                                                                           |
| 0AH        | Intel® Celeron® processor <sup>1</sup>                                                                |
| 0BH        | Intel® Xeon® processor; If processor signature = 00000F13h, then Intel® Xeon® processor MP            |
| 0CH        | Intel® Xeon® processor MP                                                                             |
| 0EH        | Mobile Intel® Pentium® 4 processor-M; If processor signature = 00000F13h, then Intel® Xeon® processor |
| 0FH        | Mobile Intel® Celeron® processor <sup>1</sup>                                                         |
| 11H        | Mobile Genuine Intel® processor                                                                       |
| 12H        | Intel® Celeron® M processor                                                                           |
| 13H        | Mobile Intel® Celeron® processor <sup>1</sup>                                                         |
| 14H        | Intel® Celeron® processor                                                                             |
| 15H        | Mobile Genuine Intel® processor                                                                       |
| 16H        | Intel® Pentium® M processor                                                                           |
| 17H        | Mobile Intel® Celeron® processor <sup>1</sup>                                                         |
| 18H – 0FFH | RESERVED                                                                                              |

NOTES:

1. Indicates versions of these processors that were introduced after the Pentium III.

21.3 CPUID LEAVES

The remainder of this chapter provides CPUID enumeration information for Intel® 64 and IA-32 architectures.

## CPUID.00H -- Maximum Input for Basic CPUID and Vendor ID

CPUID.00H returns the highest value the CPUID recognizes for returning basic processor information. The value is returned in the EAX register and is processor specific.

- This leaf is always valid.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-4. Leaf 00H Maximum Input for Basic CPUID and Vendor ID**

| Register  | Field Name  | Description                                      | Domain   |
|-----------|-------------|--------------------------------------------------|----------|
| EAX[31:0] | MAX_LEAF    | Maximum input value for basic CPUID Information. | Platform |
| EBX[31:0] | VENDOR_ID_1 | "Genu"                                           | Platform |
| ECX[31:0] | VENDOR_ID_2 | "ntel"                                           | Platform |
| EDX[31:0] | VENDOR_ID_3 | "inel"                                           | Platform |

A vendor identification string is also returned in EBX, EDX, and ECX. For Intel processors, the string is "GenuineIntel" and is expressed:

EBX := 756e6547h (\* "Genu", with G in the low eight bits of BL \*)

EDX := 49656e69h (\* "ineI", with i in the low eight bits of DL \*)

ECX := 6c65746eh (\* "ntel", with n in the low eight bits of CL \*)

CPUID.01H -- Version and Features

- CPUID.01H returns type, family, model, stepping, and feature information.
- This leaf is valid if MAX\_LEAF ≥ 01H.
  - This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-5. Leaf 01H Output Registers

| CPUID Output Registers | Description                                                                                                                               |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| EAX[31:0]              | Version information: Type, Family, Model, and Stepping ID (see “CPUID.01H:EAX—Version Information: Type, Family, Model and Stepping ID”). |
| EBX[31:0]              | Feature information (see “CPUID.01H:EBX—Feature Information”).                                                                            |
| ECX[31:0]              | Feature information (see “CPUID.01H:ECX—Feature Information”).                                                                            |
| EDX[31:0]              | Feature information (see “CPUID.01H:EDX—Feature Information”).                                                                            |

CPUID.01H:EAX Version Information: Type, Family, Model and Stepping ID

The EAX register of CPUID.01H returns the information shown below.

Table 21-6. Leaf 01H Version and Features Returned in EAX

| Register   | Field Name         | Description                                                                                                                                                                                                    | Domain   |
|------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[3:0]   | STEPPING_ID        | Identifies a revision of the specific processor family and model.<br>The stepping information is specified as a per-package basis for legacy processors. More recent processors do not allow mixing steppings. | Package  |
| EAX[7:4]   | MODEL_ID           | Identifies a set of processors within a family. Certain models of Pentium® 4 processors allowed mixed Model IDs and would have this identified as a Package Domain.                                            | Platform |
| EAX[11:8]  | FAMILY_ID          | Identifies a set of processors that have a general architectural similarity.                                                                                                                                   | Platform |
| EAX[13:12] | PROCESSOR_TYPE     | Identifies specific type of processor.                                                                                                                                                                         | Platform |
| EAX[15:14] | Reserved           | Reserved.                                                                                                                                                                                                      |          |
| EAX[19:16] | EXTENDED_MODEL_ID  | When the Family ID is 06H or 0FH, this field is prepended to the Model ID to provide an 8-bit model identification.                                                                                            | Platform |
| EAX[27:20] | EXTENDED_FAMILY_ID | When the Family ID is 0FH, this field is added to the Family ID to provide an 8-bit family identification.                                                                                                     | Platform |
| EAX[31:28] | Reserved           | Reserved.                                                                                                                                                                                                      |          |

- CPUID.01H returns version information in EAX. For example: model, family, and processor type for the Intel Xeon processor 5100 series is as follows:
- Model — 1111B
  - Family — 0101B
  - Processor Type — 00B
- See table below for available processor type values. Stepping IDs are provided as needed.

**Table 21-7. Processor Type Field**

| Type                                                   | Encoding |
|--------------------------------------------------------|----------|
| Original OEM Processor                                 | 00B      |
| Intel OverDrive® Processor                             | 01B      |
| Dual processor (not applicable to Intel486 processors) | 10B      |
| Intel reserved                                         | 11B      |

**NOTE**

See Section 21.1.2, “Identification of Earlier Processors,” for information on identifying earlier IA-32 processors. The Extended Family ID needs to be examined only when the Family ID is 0FH. Integrate the fields into a display using the following rule:

```

IF Family_ID ≠ 0FH THEN
    DisplayFamily = Family_ID;
ELSE
    DisplayFamily = Extended_Family_ID + Family_ID;
FI;

```

The Extended Model ID needs to be examined only when the Family ID is 06H or 0FH. Integrate the field into a display using the following rule:

```

IF (Family_ID = 06H or Family_ID = 0FH) THEN
    DisplayModel = (Extended_Model_ID « 4) + Model_ID;
ELSE
    DisplayModel = Model_ID;
FI;

```

**CPUID.01H:EBX Feature information.**

The EBX register of CPUID.01H returns the information shown below.

**Table 21-8. Leaf 01H Version and Features Returned in EBX**

| Register   | Field Name        | Description                                                                                                                                                                                                                                                                                                                                                                               | Domain   |
|------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EBX[7:0]   | BRAND_INDEX       | This number provides an entry into a brand string table that contains brand strings for IA-32 processors. More information about this field is provided in Section 21.2.2, “The Processor Brand Index Method.”                                                                                                                                                                            | Platform |
| EBX[15:8]  | CLFLUSH_LINE_SIZE | Value * 8 = cache line size in bytes.<br>This number indicates the size of the cache line flushed by the CLFLUSH and CLFLUSHOPT instructions in 8-byte increments.<br>This field was introduced in the Pentium 4 processor.                                                                                                                                                               | Platform |
| EBX[23:16] | APIC_ID_SPACE     | Maximum number of addressable IDs for logical processors in this physical package.<br>The nearest power-of-2 integer that is not smaller than EBX[23:16] is the number of unique initial APIC IDs reserved for addressing different logical processors in a physical package. This field is only valid if CPUID.01H.EDX.HTT[28]= 1. See further details below on the usage of this field. | Platform |

|            |                 |                                                                                                                                                                                                                                                                            |                   |
|------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EBX[31:24] | INITIAL_APIC_ID | This number is the 8-bit ID that is assigned to the local APIC on the processor during power up. This field was introduced in the Pentium 4 processor.<br>The 8-bit initial APIC ID in EBX[31:24] is replaced by the 32-bit x2APIC ID, available in Leaf 0BH and Leaf 1FH. | Logical Processor |
|------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|

The Maximum Addressable IDs for logical processors in this package should not be used on platforms that support CPUID leaf 0BH or CPUID leaf 1FH as it can be saturated and incorrect. Modern platforms can have many more processors than can be enumerated or have topology domains with discontinuous APIC ID reservations. To correctly enumerate APIC ID information on modern platforms, use CPUID.0BH or CPUID.1FH.

## CPUID.01H:ECX Feature Information

The ECX register of CPUID.01H returns the information shown below. For all feature flags, a 1 indicates that the feature is supported. Software should identify Intel as the vendor to properly interpret feature flags. Software must confirm that a processor feature is present using feature flags returned by CPUID prior to using the feature. Software should not depend on future offerings retaining all features.

**Table 21-9. Leaf 01H Version and Features Returned in ECX**

| Register | Field Name      | Description                                                                                                                                                                 | Domain   |
|----------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| ECX[0]   | SSE3            | If 1, supports Streaming SIMD Extensions 3.                                                                                                                                 | Platform |
| ECX[1]   | PCLMULQDQ       | If 1, supports the PCLMULQDQ instruction.                                                                                                                                   | Platform |
| ECX[2]   | DTES64          | 64-bit DS Area. If 1, supports DS area using 64-bit layout.                                                                                                                 | Platform |
| ECX[3]   | MONITOR         | If 1, supports the MONITOR/MWAIT and CPUID.05H.                                                                                                                             | Platform |
| ECX[4]   | DS_CPL          | If 1, supports the extensions to the Debug Store feature to allow for branch message storage qualified by CPL.                                                              | Platform |
| ECX[5]   | VMX             | If 1, supports the Virtual Machine Extensions.                                                                                                                              | Platform |
| ECX[6]   | SMX             | If 1, supports Safer Mode Extensions. See Chapter 7, "Safer Mode Extensions Reference."                                                                                     | Platform |
| ECX[7]   | EIST            | If 1, supports Enhanced Intel SpeedStep® technology.                                                                                                                        | Platform |
| ECX[8]   | TM2             | If 1, supports Thermal Monitor 2.                                                                                                                                           | Platform |
| ECX[9]   | SSSE3           | If 1, supports Supplemental Streaming SIMD Extensions 3.                                                                                                                    | Platform |
| ECX[10]  | L1_CONTEXT_ID   | If 1, the L1 data cache mode can be set to either adaptive mode or shared mode. See definition of the IA32_MISC_ENABLE MSR Bit 24 (L1 Data Cache Context Mode) for details. | Platform |
| ECX[11]  | DEBUG_INTERFACE | If 1, supports IA32_DEBUG_INTERFACE MSR for silicon debug.                                                                                                                  | Platform |
| ECX[12]  | FMA             | If 1, supports FMA extensions using YMM state.                                                                                                                              | Platform |

|         |                     |                                                                                                                                                                     |                   |
|---------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| ECX[13] | CMPXCHG16B          | If 1, supports this instruction. See the “CMPXCHG8B/CMPXCHG16B—Compare and Exchange Bytes” section in this chapter for a description.                               | Platform          |
| ECX[14] | XTPR_UPDATE_CONTROL | If 1, supports changing IA32_MISC_ENABLE[bit 23].                                                                                                                   | Platform          |
| ECX[15] | PERF_CAPABILITIES   | If 1, supports the performance and debug feature indication MSR IA32_PERF_CAPABILITIES.                                                                             | Platform          |
| ECX[16] | Reserved            | Reserved.                                                                                                                                                           |                   |
| ECX[17] | PCID                | If 1, supports Process-context identifiers and software setting CR4.PCIDE to 1.Process-context identifiers.                                                         | Platform          |
| ECX[18] | DCA                 | If 1, supports the ability to prefetch data from a memory mapped device. See CPUID.09H.                                                                             | Platform          |
| ECX[19] | SSE4_1              | If 1, supports SSE4.1.                                                                                                                                              | Platform          |
| ECX[20] | SSE4_2              | If 1, supports SSE4.2.                                                                                                                                              | Platform          |
| ECX[21] | X2APIC              | If 1, supports x2APIC feature.                                                                                                                                      | Platform          |
| ECX[22] | MOVBE               | If 1, supports MOVBE instruction.                                                                                                                                   | Platform          |
| ECX[23] | POPCNT              | If 1, supports the POPCNT instruction.                                                                                                                              | Platform          |
| ECX[24] | TSC_DEADLINE        | If 1, the processor's local APIC timer supports one-shot operation using a TSC deadline value.                                                                      | Platform          |
| ECX[25] | AESNI               | If 1, supports the AESNI instruction extensions.                                                                                                                    | Platform          |
| ECX[26] | XSAVE               | If 1, supports the XSAVE/XRSTOR processor extended states feature, the XSETBV/XGETBV instructions, and XCRO.                                                        | Platform          |
| ECX[27] | OSXSAVE             | If 1, the OS has set CR4.OSXSAVE[bit 18] to enable XSETBV/XGETBV instructions to access XCRO and to support processor extended state management using XSAVE/XRSTOR. | Logical Processor |
| ECX[28] | AVX                 | If 1, supports the AVX instruction extensions.                                                                                                                      | Platform          |
| ECX[29] | F16C                | If 1, supports 16-bit floating-point conversion instructions.                                                                                                       | Platform          |
| ECX[30] | RDRAND              | If 1, supports RDRAND instruction.                                                                                                                                  | Platform          |
| ECX[31] | Not Used            | Intel processors always return 0. Allocated for use by software emulation.                                                                                          | Platform          |

## CPUID.01H:EDX Feature Information

The EDX register of CPUID.01H returns the information shown below. For all feature flags, a 1 indicates that the feature is supported. Software should identify Intel as the vendor to properly interpret feature flags. Software must confirm that a processor feature is present using feature flags returned by CPUID prior to using the feature. Software should not depend on future offerings retaining all features.

**Table 21-10. Leaf 01H Version and Features Returned in EDX**

| Register | Field Name | Description                                                     | Domain   |
|----------|------------|-----------------------------------------------------------------|----------|
| EDX[0]   | FPU        | Floating Point Unit On-Chip. The processor contains an x87 FPU. | Platform |

## PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

|         |           |                                                                                                                                                                                                                                                                                                                                                                                                                     |          |
|---------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[1]  | VME       | If 1, supports Virtual 8086 mode enhancements, including CR4.VME for controlling the feature; CR4.PVI for protected mode virtual interrupts; software interrupt indirection; expansion of the TSS with the software indirection bitmap; and EFLAGS.VIF and EFLAGS.VIP flags.                                                                                                                                        | Platform |
| EDX[2]  | DE        | If 1, supports I/O breakpoints debugging extensions, including CR4.DE for controlling the feature, and optional trapping of accesses to DR4 and DR5.                                                                                                                                                                                                                                                                | Platform |
| EDX[3]  | PSE       | P If 1, supports page size extensions for large pages of size 4 MByte, including: CR4.PSE for controlling the feature; the defined dirty bit in PDE (Page Directory Entries); optional reserved bit trapping in CR3; PDEs; and PTEs.                                                                                                                                                                                | Platform |
| EDX[4]  | TSC       | If 1, supports the Time Stamp Counter, RDTSC instruction, including CR4.TSD for controlling privilege.                                                                                                                                                                                                                                                                                                              | Platform |
| EDX[5]  | MSR       | If 1, supports the Model Specific Registers RDMSR and WRMSR Instructions. Some of the MSRs are implementation dependent.                                                                                                                                                                                                                                                                                            | Platform |
| EDX[6]  | PAE       | If 1, supports the Physical Address Extension which is for physical addresses greater than 32 bits, including: extended page table entry formats; an extra level in the page translation tables; and 2-MByte pages rather than 4 Mbyte pages.                                                                                                                                                                       | Platform |
| EDX[7]  | MCE       | If 1, supports exception 18 for Machine Checks, including CR4.MCE for controlling the feature. This feature does not define the modelspecific implementations of machine-check error logging, reporting, and processor shutdowns. Machine Check exception handlers may have to depend on processor version to do model specific processing of the exception, or test for the presence of the Machine Check feature. | Platform |
| EDX[8]  | CMPXCHG8B | If 1, supports the CMPXCHG8B (64 bits) Instruction, implicitly locked and atomic.                                                                                                                                                                                                                                                                                                                                   | Platform |
| EDX[9]  | APIC      | If 1, the processor contains an Advanced Programmable Interrupt Controller (APIC), responding to memory mapped commands in the physical address range FEE00000H to FEE00FFFH (by default - some processors permit the APIC to be relocated).                                                                                                                                                                        | Platform |
| EDX[10] | Reserved  | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                           |          |
| EDX[11] | SEP       | If 1 supports the SYSENTER and SYSEXIT Instructions and associated MSRs.                                                                                                                                                                                                                                                                                                                                            | Platform |

|         |          |                                                                                                                                                                                                                                                                                                                                                                                                                                       |          |
|---------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[12] | MTRR     | If 1, supports the Memory Type Range Registers. (The MTRRcap MSR contains feature bits that describe what memory types are supported, how many variable MTRRs are supported, and whether fixed MTRRs are supported.)                                                                                                                                                                                                                  | Platform |
| EDX[13] | PGE      | If 1, supports the global bit in paging-structure entries that map a page, indicating TLB entries that are common to different processes and need not be flushed. The CR4.PGE bit controls this feature.                                                                                                                                                                                                                              | Platform |
| EDX[14] | MCA      | If 1, supports the Machine Check Architecture feature. The MCG_CAP MSR contains feature bits describing how many banks of error reporting MSRs are supported.                                                                                                                                                                                                                                                                         | Platform |
| EDX[15] | CMOV     | If 1, supports the Conditional Move Instructions. If CPUID.01H:EDX.FPU[0] (x87 FPU present) is 1 also, supports the FCOMI and FCMOV instructions.                                                                                                                                                                                                                                                                                     | Platform |
| EDX[16] | PAT      | If 1, supports the Page Attribute Table feature. (This feature augments the Memory Type Range Registers (MTRRs), allowing an operating system to specify attributes of memory accessed through a linear address on a 4KB granularity.)                                                                                                                                                                                                | Platform |
| EDX[17] | PSE_36   | If 1, supports the 36-Bit Page Size Extension which enables 4-MByte pages addressing physical memory beyond 4 GBytes with 32-bit paging. This feature indicates that upper bits of the physical address of a 4-MByte page are encoded in bits 20:13 of the page directory entry. Such physical addresses are limited by MAXPHYADDR and may be up to 40 bits in size.                                                                  | Platform |
| EDX[18] | PSN      | If 1, supports the 96-bit Processor Serial Number identification number feature, and the feature is enabled. Available only in Pentium III, see CPUID.03H.                                                                                                                                                                                                                                                                            | Platform |
| EDX[19] | CLFLUSH  | If 1, supports the CLFLUSH instruction.                                                                                                                                                                                                                                                                                                                                                                                               | Platform |
| EDX[20] | Reserved | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                             |          |
| EDX[21] | DS       | If 1, supports the Debug Store feature which provides the ability to write debug information into a memory resident buffer. This feature is used by the branch trace store (BTS) and processor event-based sampling (PEBS) facilities (see Chapter 19, “Debug, Branch Profile, TSC, and Intel® Resource Director Technology (Intel® RDT) Features,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3B). | Platform |

## PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

|         |            |                                                                                                                                                                                                                                                                                                    |          |
|---------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[22] | ACPI       | If 1, supports the Thermal Monitor and Software Controlled Clock Facilities. These are internal MSRs that allow processor temperature to be monitored and processor performance to be modulated in predefined duty cycles under software control.                                                  | Platform |
| EDX[23] | MMX        | If 1, supports the Intel MMX Technology.                                                                                                                                                                                                                                                           | Platform |
| EDX[24] | FXSR       | If 1, supports the FXSAVE and FXRSTOR Instructions, which are fast save and restore of the floating-point context, and the availability of CR4.OSFXSR for an operating system to indicate support of same.                                                                                         | Platform |
| EDX[25] | SSE        | If 1, supports SSE.                                                                                                                                                                                                                                                                                | Platform |
| EDX[26] | SSE2       | If 1, supports SSE2.                                                                                                                                                                                                                                                                               | Platform |
| EDX[27] | SELF_SNOOP | If 1, supports Self Snoop which is the management of conflicting memory types by performing a snoop of its own cache structure for transactions issued to the bus.                                                                                                                                 | Platform |
| EDX[28] | HTT        | If 1, the value in CPUID.1.EBX[23:16] (the Maximum number of addressable IDs for logical processors in this package) is valid for the package. If 0, there is only a single logical processor in the package and software should assume only a single APIC ID is reserved.                         | Platform |
| EDX[29] | TM         | If 1, supports the Thermal Monitor feature in which the processor implements the thermal monitor automatic thermal control circuitry (TCC). Thermal Monitor.                                                                                                                                       | Platform |
| EDX[30] | Reserved   | Reserved.                                                                                                                                                                                                                                                                                          |          |
| EDX[31] | PBE        | If 1, supports the Pending Break Enable feature, which is the use of the FERR#/PBE# pin when the processor is in the stop-clock state (STPCLK# is asserted) to signal the processor that an interrupt is pending and that the processor should return to normal operation to handle the interrupt. | Platform |

## CPUID.02H -- TLB/Cache/Prefetch Information

CPUID.02H returns TLB, cache, and prefetch information. This leaf has been superseded by CPUID.04H for cache enumeration and CPUID.18H for TLB enumeration. These processors will also report new descriptor values of types 0FEh or 0FFh to refer enumerations to CPUID.04H and CPUID.18H.

- This leaf is valid if MAX\_LEAF  $\geq$  02H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-11. Leaf 02H TLB/Cache/Prefetch Information**

| Register   | Field Name    | Description                                                        | Domain            |
|------------|---------------|--------------------------------------------------------------------|-------------------|
| EAX[7:0]   | Reserved      | Reserved with a value of 1                                         |                   |
| EAX[15:8]  | DESCRIPTOR_1  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EAX[23:16] | DESCRIPTOR_2  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EAX[31:24] | DESCRIPTOR_3  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EBX[7:0]   | DESCRIPTOR_4  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EBX[15:8]  | DESCRIPTOR_5  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EBX[23:16] | DESCRIPTOR_6  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EBX[31:24] | DESCRIPTOR_7  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| ECX[7:0]   | DESCRIPTOR_8  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| ECX[15:8]  | DESCRIPTOR_9  | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| ECX[23:16] | DESCRIPTOR_10 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| ECX[31:24] | DESCRIPTOR_11 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EDX[7:0]   | DESCRIPTOR_12 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EDX[15:8]  | DESCRIPTOR_13 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EDX[23:16] | DESCRIPTOR_14 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |
| EDX[31:24] | DESCRIPTOR_15 | See Table “Encoding of CPUID Leaf 2 Descriptors” below this table. | Logical Processor |

CPUID.02H returns information about the processor’s internal TLBs, cache, and prefetch hardware in the EAX, EBX, ECX, and EDX registers. The information is reported in encoded form and fall into the following categories:

- The least-significant byte in register EAX (register AL) will always return 01H. Software should ignore this value and not interpret it as an informational descriptor.
- The most significant bit (bit 31) of each register indicates whether the register contains valid information (set to 0) or is reserved (set to 1).
- If a register contains valid information, the information is contained in 1-byte descriptors. There are four types of encoding values for the byte descriptor, the encoding of these descriptors and encoding type are listed in the table

below.

Note that the order of descriptors in the EAX, EBX, ECX, and EDX registers is not defined; that is, specific bytes are not designated to contain descriptors for specific cache, prefetch, or TLB types. The descriptors may appear in any order. Note also a processor may report a general descriptor type FFH and FEH and not report any byte descriptor of “cache type” or “\*TLB type” via CPUID.02H.

**Table 21-12. Encoding of CPUID Leaf 2 Descriptors**

| Descriptor Value | Type    | Cache or TLB Description                                                                                                                                                              |
|------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 00H              | General | Null descriptor, this byte contains no information.                                                                                                                                   |
| 01H              | TLB     | Instruction TLB: 4 KByte pages, 4-way set associative, 32 entries.                                                                                                                    |
| 02H              | TLB     | Instruction TLB: 4 MByte pages, fully associative, 2 entries.                                                                                                                         |
| 03H              | TLB     | Data TLB: 4 KByte pages, 4-way set associative, 64 entries.                                                                                                                           |
| 04H              | TLB     | Data TLB: 4 MByte pages, 4-way set associative, 8 entries.                                                                                                                            |
| 05H              | TLB     | Data TLB1: 4 MByte pages, 4-way set associative, 32 entries.                                                                                                                          |
| 06H              | Cache   | 1st-level instruction cache: 8 KBytes, 4-way set associative, 32 byte line size.                                                                                                      |
| 08H              | Cache   | 1st-level instruction cache: 16 KBytes, 4-way set associative, 32 byte line size.                                                                                                     |
| 09H              | Cache   | 1st-level instruction cache: 32KBytes, 4-way set associative, 64 byte line size.                                                                                                      |
| 0AH              | Cache   | 1st-level data cache: 8 KBytes, 2-way set associative, 32 byte line size.                                                                                                             |
| 0BH              | TLB     | Instruction TLB: 4 MByte pages, 4-way set associative, 4 entries.                                                                                                                     |
| 0CH              | Cache   | 1st-level data cache: 16 KBytes, 4-way set associative, 32 byte line size.                                                                                                            |
| 0DH              | Cache   | 1st-level data cache: 16 KBytes, 4-way set associative, 64 byte line size.                                                                                                            |
| 0EH              | Cache   | 1st-level data cache: 24 KBytes, 6-way set associative, 64 byte line size.                                                                                                            |
| 1DH              | Cache   | 2nd-level cache: 128 KBytes, 2-way set associative, 64 byte line size.                                                                                                                |
| 21H              | Cache   | 2nd-level cache: 256 KBytes, 8-way set associative, 64 byte line size.                                                                                                                |
| 22H              | Cache   | 3rd-level cache: 512 KBytes, 4-way set associative, 64 byte line size, 2 lines per sector.                                                                                            |
| 23H              | Cache   | 3rd-level cache: 1 MBytes, 8-way set associative, 64 byte line size, 2 lines per sector.                                                                                              |
| 24H              | Cache   | 2nd-level cache: 1 MBytes, 16-way set associative, 64 byte line size.                                                                                                                 |
| 25H              | Cache   | 3rd-level cache: 2 MBytes, 8-way set associative, 64 byte line size, 2 lines per sector.                                                                                              |
| 29H              | Cache   | 3rd-level cache: 4 MBytes, 8-way set associative, 64 byte line size, 2 lines per sector.                                                                                              |
| 2CH              | Cache   | 1st-level data cache: 32 KBytes, 8-way set associative, 64 byte line size.                                                                                                            |
| 30H              | Cache   | 1st-level instruction cache: 32 KBytes, 8-way set associative, 64 byte line size.                                                                                                     |
| 40H              | Cache   | No 2nd-level cache or, if processor contains a valid 2nd-level cache, no 3rd-level cache.                                                                                             |
| 41H              | Cache   | 2nd-level cache: 128 KBytes, 4-way set associative, 32 byte line size.                                                                                                                |
| 42H              | Cache   | 2nd-level cache: 256 KBytes, 4-way set associative, 32 byte line size.                                                                                                                |
| 43H              | Cache   | 2nd-level cache: 512 KBytes, 4-way set associative, 32 byte line size.                                                                                                                |
| 44H              | Cache   | 2nd-level cache: 1 MByte, 4-way set associative, 32 byte line size.                                                                                                                   |
| 45H              | Cache   | 2nd-level cache: 2 MByte, 4-way set associative, 32 byte line size.                                                                                                                   |
| 46H              | Cache   | 3rd-level cache: 4 MByte, 4-way set associative, 64 byte line size.                                                                                                                   |
| 47H              | Cache   | 3rd-level cache: 8 MByte, 8-way set associative, 64 byte line size.                                                                                                                   |
| 48H              | Cache   | 2nd-level cache: 3MByte, 12-way set associative, 64 byte line size.                                                                                                                   |
| 49H              | Cache   | 3rd-level cache: 4MB, 16-way set associative, 64-byte line size (Intel Xeon processor MP, Family 0FH, Model 06H) 2nd-level cache: 4 MByte, 16-way set associative, 64 byte line size. |

|     |       |                                                                                                                                                  |
|-----|-------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| 4AH | Cache | 3rd-level cache: 6MByte, 12-way set associative, 64 byte line size.                                                                              |
| 4BH | Cache | 3rd-level cache: 8MByte, 16-way set associative, 64 byte line size.                                                                              |
| 4CH | Cache | 3rd-level cache: 12MByte, 12-way set associative, 64 byte line size.                                                                             |
| 4DH | Cache | 3rd-level cache: 16MByte, 16-way set associative, 64 byte line size.                                                                             |
| 4EH | Cache | 2nd-level cache: 6MByte, 24-way set associative, 64 byte line size.                                                                              |
| 4FH | TLB   | Instruction TLB: 4 KByte pages, 32 entries.                                                                                                      |
| 50H | TLB   | Instruction TLB: 4 KByte and 2-MByte or 4-MByte pages, 64 entries.                                                                               |
| 51H | TLB   | Instruction TLB: 4 KByte and 2-MByte or 4-MByte pages, 128 entries.                                                                              |
| 52H | TLB   | Instruction TLB: 4 KByte and 2-MByte or 4-MByte pages, 256 entries.                                                                              |
| 55H | TLB   | Instruction TLB: 2-MByte or 4-MByte pages, fully associative, 7 entries.                                                                         |
| 56H | TLB   | Data TLB0: 4 MByte pages, 4-way set associative, 16 entries.                                                                                     |
| 57H | TLB   | Data TLB0: 4 KByte pages, 4-way associative, 16 entries.                                                                                         |
| 59H | TLB   | Data TLB0: 4 KByte pages, fully associative, 16 entries.                                                                                         |
| 5AH | TLB   | Data TLB0: 2 MByte or 4 MByte pages, 4-way set associative, 32 entries.                                                                          |
| 5BH | TLB   | Data TLB: 4 KByte and 4 MByte pages, 64 entries.                                                                                                 |
| 5CH | TLB   | Data TLB: 4 KByte and 4 MByte pages, 128 entries.                                                                                                |
| 5DH | TLB   | Data TLB: 4 KByte and 4 MByte pages, 256 entries.                                                                                                |
| 60H | Cache | 1st-level data cache: 16 KByte, 8-way set associative, 64 byte line size.                                                                        |
| 61H | TLB   | Instruction TLB: 4 KByte pages, fully associative, 48 entries.                                                                                   |
| 63H | TLB   | Data TLB: 2 MByte or 4 MByte pages, 4-way set associative, 32 entries and a separate array with 1 GByte pages, 4-way set associative, 4 entries. |
| 64H | TLB   | Data TLB: 4 KByte pages, 4-way set associative, 512 entries.                                                                                     |
| 66H | Cache | 1st-level data cache: 8 KByte, 4-way set associative, 64 byte line size.                                                                         |
| 67H | Cache | 1st-level data cache: 16 KByte, 4-way set associative, 64 byte line size.                                                                        |
| 68H | Cache | 1st-level data cache: 32 KByte, 4-way set associative, 64 byte line size.                                                                        |
| 6AH | Cache | uTLB: 4 KByte pages, 8-way set associative, 64 entries.                                                                                          |
| 6BH | Cache | DTLB: 4 KByte pages, 8-way set associative, 256 entries.                                                                                         |
| 6CH | Cache | DTLB: 2M/4M pages, 8-way set associative, 128 entries.                                                                                           |
| 6DH | Cache | DTLB: 1 GByte pages, fully associative, 16 entries.                                                                                              |
| 70H | Cache | Trace cache: 12 K-?op, 8-way set associative.                                                                                                    |
| 71H | Cache | Trace cache: 16 K-?op, 8-way set associative.                                                                                                    |
| 72H | Cache | Trace cache: 32 K-?op, 8-way set associative.                                                                                                    |
| 76H | TLB   | Instruction TLB: 2M/4M pages, fully associative, 8 entries.                                                                                      |
| 78H | Cache | 2nd-level cache: 1 MByte, 4-way set associative, 64byte line size.                                                                               |
| 79H | Cache | 2nd-level cache: 128 KByte, 8-way set associative, 64 byte line size, 2 lines per sector.                                                        |
| 7AH | Cache | 2nd-level cache: 256 KByte, 8-way set associative, 64 byte line size, 2 lines per sector.                                                        |
| 7BH | Cache | 2nd-level cache: 512 KByte, 8-way set associative, 64 byte line size, 2 lines per sector.                                                        |
| 7CH | Cache | 2nd-level cache: 1 MByte, 8-way set associative, 64 byte line size, 2 lines per sector.                                                          |
| 7DH | Cache | 2nd-level cache: 2 MByte, 8-way set associative, 64byte line size.                                                                               |
| 7FH | Cache | 2nd-level cache: 512 KByte, 2-way set associative, 64-byte line size.                                                                            |

## PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

|     |          |                                                                                                                      |
|-----|----------|----------------------------------------------------------------------------------------------------------------------|
| 80H | Cache    | 2nd-level cache: 512 KByte, 8-way set associative, 64-byte line size.                                                |
| 82H | Cache    | 2nd-level cache: 256 KByte, 8-way set associative, 32 byte line size.                                                |
| 83H | Cache    | 2nd-level cache: 512 KByte, 8-way set associative, 32 byte line size.                                                |
| 84H | Cache    | 2nd-level cache: 1 MByte, 8-way set associative, 32 byte line size.                                                  |
| 85H | Cache    | 2nd-level cache: 2 MByte, 8-way set associative, 32 byte line size.                                                  |
| 86H | Cache    | 2nd-level cache: 512 KByte, 4-way set associative, 64 byte line size.                                                |
| 87H | Cache    | 2nd-level cache: 1 MByte, 8-way set associative, 64 byte line size.                                                  |
| A0H | DTLB     | DTLB: 4k pages, fully associative, 32 entries.                                                                       |
| B0H | TLB      | Instruction TLB: 4 KByte pages, 4-way set associative, 128 entries.                                                  |
| B1H | TLB      | Instruction TLB: 2M pages, 4-way, 8 entries or 4M pages, 4-way, 4 entries.                                           |
| B2H | TLB      | Instruction TLB: 4KByte pages, 4-way set associative, 64 entries.                                                    |
| B3H | TLB      | Data TLB: 4 KByte pages, 4-way set associative, 128 entries.                                                         |
| B4H | TLB      | Data TLB1: 4 KByte pages, 4-way associative, 256 entries.                                                            |
| B5H | TLB      | Instruction TLB: 4KByte pages, 8-way set associative, 64 entries.                                                    |
| B6H | TLB      | Instruction TLB: 4KByte pages, 8-way set associative, 128 entries.                                                   |
| BAH | TLB      | Data TLB1: 4 KByte pages, 4-way associative, 64 entries.                                                             |
| COH | TLB      | Data TLB: 4 KByte and 4 MByte pages, 4-way associative, 8 entries.                                                   |
| C1H | STLB     | Shared 2nd-Level TLB: 4 KByte/2MByte pages, 8-way associative, 1024 entries.                                         |
| C2H | DTLB     | DTLB: 2 MByte/4 MByte pages, 4-way associative, 16 entries.                                                          |
| C3H | STLB     | Shared 2nd-Level TLB: 4 KByte /2 MByte pages, 6-way associative, 1536 entries. Also 1GByte pages, 4-way, 16 entries. |
| C4H | DTLB     | DTLB: 2 MByte/ 4MByte pages, 4-way associative, 32 entries.                                                          |
| CAH | STLB     | Shared 2nd-Level TLB: 4 KByte pages, 4-way associative, 512 entries.                                                 |
| D0H | Cache    | 3rd-level cache: 512 KByte, 4-way set associative, 64 byte line size.                                                |
| D1H | Cache    | 3rd-level cache: 1 MByte, 4-way set associative, 64 byte line size.                                                  |
| D2H | Cache    | 3rd-level cache: 2 MByte, 4-way set associative, 64 byte line size.                                                  |
| D6H | Cache    | 3rd-level cache: 1 MByte, 8-way set associative, 64 byte line size.                                                  |
| D7H | Cache    | 3rd-level cache: 2 MByte, 8-way set associative, 64 byte line size.                                                  |
| D8H | Cache    | 3rd-level cache: 4 MByte, 8-way set associative, 64 byte line size.                                                  |
| DCH | Cache    | 3rd-level cache: 1.5 MByte, 12-way set associative, 64 byte line size.                                               |
| DDH | Cache    | 3rd-level cache: 3 MByte, 12-way set associative, 64 byte line size.                                                 |
| DEH | Cache    | 3rd-level cache: 6 MByte, 12-way set associative, 64 byte line size.                                                 |
| E2H | Cache    | 3rd-level cache: 2 MByte, 16-way set associative, 64 byte line size.                                                 |
| E3H | Cache    | 3rd-level cache: 4 MByte, 16-way set associative, 64 byte line size.                                                 |
| E4H | Cache    | 3rd-level cache: 8 MByte, 16-way set associative, 64 byte line size.                                                 |
| EAH | Cache    | 3rd-level cache: 12MByte, 24-way set associative, 64 byte line size.                                                 |
| EBH | Cache    | 3rd-level cache: 18MByte, 24-way set associative, 64 byte line size.                                                 |
| ECH | Cache    | 3rd-level cache: 24MByte, 24-way set associative, 64 byte line size.                                                 |
| FOH | Prefetch | 64-Byte prefetching.                                                                                                 |
| F1H | Prefetch | 128-Byte prefetching.                                                                                                |

|     |         |                                                                                                                                    |
|-----|---------|------------------------------------------------------------------------------------------------------------------------------------|
| FEH | General | CPUID leaf 2 does not report TLB descriptor information; use CPUID leaf 18H to query TLB and other address translation parameters. |
| FFH | General | CPUID leaf 2 does not report cache descriptor information, use CPUID leaf 4 to query cache parameters.                             |

### Example 21-1. Example of Cache and TLB Interpretation

The first member of the family of Pentium 4 processors returns the following information about caches and TLBs when the CPUID executes with an input value of 2:

EAX 66 5B 50 01H

EBX 0H

ECX 0H

EDX 00 7A 70 00H

Which means:

- The least-significant byte (byte 0) of register EAX is set to 01H. This value should be ignored.
- The most-significant bit of all four registers (EAX, EBX, ECX, and EDX) is set to 0, indicating that each register contains valid 1-byte descriptors.
- Bytes 1, 2, and 3 of register EAX indicate that the processor has:
  - 50H - a 64-entry instruction TLB, for mapping 4-KByte and 2-MByte or 4-MByte pages.
  - 5BH - a 64-entry data TLB, for mapping 4-KByte and 4-MByte pages.
  - 66H - an 8-KByte 1st level data cache, 4-way set associative, with a 64-Byte cache line size.
- The descriptors in registers EBX and ECX are valid, but contain NULL descriptors.
- Bytes 0, 1, 2, and 3 of register EDX indicate that the processor has:
  - 00H - NULL descriptor.
  - 70H - Trace cache: 12 K- $\mu$ op, 8-way set associative.
  - 7AH - a 256-KByte 2nd level cache, 8-way set associative, with a sectored, 64-byte cache line size.
  - 00H - NULL descriptor.

CPUID.03H -- Processor Serial Number

CPUID.03H returns the processor serial number, if available. Processor serial number (PSN) is not supported in the Pentium 4 processor or later.

- This leaf is valid if MAX\_LEAF ≥ 03H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-13. Leaf 03H Processor Serial Number

| Register  | Field Name | Description                                                                                                                                 | Domain  |
|-----------|------------|---------------------------------------------------------------------------------------------------------------------------------------------|---------|
| EAX[31:0] | Reserved   | Reserved.                                                                                                                                   |         |
| EBX[31:0] | Reserved   | Reserved.                                                                                                                                   |         |
| ECX[31:0] | PSN_31_0   | Bits 00-31 of 96-bit processor serial number. (Available in Pentium III processor only; otherwise, the value in this register is reserved.) | Package |
| EDX[31:0] | PSN_63_32  | Bits 32-63 of 96-bit processor serial number. (Available in Pentium III processor only; otherwise, the value in this register is reserved.) | Package |

## CPUID.04H -- Deterministic Cache Parameters

CPUID.04H returns the deterministic cache parameters for each cache level.

- This leaf is valid if CPUID.04H.00H:EAX[4:0]  $\neq$  0 and MAX\_LEAF  $\geq$  04H.
- The sub-leaves are enumerated until sub-leaf n returns 0 in EAX[4:0].
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n+1 is invalid if sub-leaf n returns EAX[4:0] as 0.

**Table 21-14. Leaf 04H Deterministic Cache Parameters**

| Register   | Field Name                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Domain            |
|------------|-------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[4:0]   | CACHE_TYPE                    | 0 = Null, no more caches.<br>1 = Data Cache.<br>2 = Instruction Cache.<br>3 = Unified Cache. 4-31 = Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Logical Processor |
| EAX[7:5]   | CACHE_LEVEL                   | Cache level (starts at 1).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Logical Processor |
| EAX[8]     | SELF_INITIALIZING_CACHE       | Self initializing cache level (does not need software initialization).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Logical Processor |
| EAX[9]     | FULLY_ASSOC                   | Fully associative cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Logical Processor |
| EAX[13:10] | Reserved                      | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                   |
| EAX[25:14] | MAX_LP_ADDRESSABLE_IDS        | Maximum number of addressable IDs for logical processors sharing this cache.<br>Add one to the return value to get the result.<br>The nearest power-of-2 integer that is not smaller than (1 + EAX[25:14]) is the number of unique initial APIC IDs reserved for addressing different logical processors sharing this cache.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Logical Processor |
| EAX[31:26] | MAX_CORES_ADDRESSABLE_IDS_PKG | Maximum number of addressable IDs for processor cores in the physical package.<br>Add one to the return value to get the result.<br>The nearest power-of-2 integer that is not smaller than (1 + EAX[31:26]) is the number of unique Core_IDs reserved for addressing different processor cores in a physical package.<br>Core ID is a subset of bits of the initial APIC ID.<br>The returned value is constant for valid initial values in ECX. Valid ECX values start from 0.<br>The maximum number of addressable IDs for processor cores in the physical package field may contain a saturated value and will not correctly identify the addressable ID reservations for cores in this package on processors where CPUID.0BH and/or CPUID.1FH exist. Processors which enumerate topology information in either CPUID.0BH or CPUID.1FH need to use those leaves to obtain the correct topology details. | Platform          |
| EBX[11:0]  | LINE_SIZE                     | System Coherency Line Size.<br>Add one to the return value to get the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Platform          |
| EBX[21:12] | PHYS_LINE_PARTITIONS          | Physical line partitions.<br>Add one to the return value to get the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Logical Processor |
| EBX[31:22] | NUM_WAYS                      | Ways of associativity.<br>Add one to the return value to get the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Logical Processor |

|           |                        |                                                                                                                                                                                                                                 |                   |
|-----------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| ECX[31:0] | NUM_SETS               | Number of sets.<br>Add one to the return value to get the result.                                                                                                                                                               | Logical Processor |
| EDX[0]    | NOT_LWR_CACHE_FLUSH    | 0 = WBINVD/INVD from threads sharing this cache acts upon lower level caches for threads sharing this cache.<br>1 = WBINVD/INVD is not guaranteed to act upon lower level caches of non-originating threads sharing this cache. | Logical Processor |
| EDX[1]    | INCLUSIVE_CACHE        | 0 = Cache is not inclusive of lower cache levels.<br>1 = Cache is inclusive of lower cache levels.                                                                                                                              | Logical Processor |
| EDX[2]    | COMPLEX_CACHE_INDEXING | 0 = Direct mapped cache.<br>1 = A complex function is used to index the cache, potentially using all address bits.                                                                                                              | Logical Processor |
| EDX[31:3] | Reserved               | Reserved.                                                                                                                                                                                                                       |                   |

When CPUID executes with EAX set to 04H and ECX contains an index value, the processor returns encoded data that describe a set of deterministic cache parameters (for the cache level associated with the input in ECX). Valid index values start from 0. Software can enumerate the deterministic cache parameters for each level of the cache hierarchy starting with an index value of 0, until the parameters report the value associated with the cache type field is 0.

This Cache Size in Bytes

= (Ways + 1) \* (Partitions + 1) \* (Line\_Size + 1) \* (Sets + 1)

= (EBX[31:22] + 1) \* (EBX[21:12] + 1) \* (EBX[11:0] + 1) \* (ECX + 1)

The CPUID.04H also reports data that can be used to derive the topology of processor cores in a physical package on legacy processors. This information is constant for all valid index values. Software can query the raw data reported by executing CPUID with EAX=04H and ECX=0 and use it as part of the topology enumeration algorithm on processors that do not enumerate either CPUID.0BH or CPUID.1FH as described in Chapter 10, "Multiple-Processor Management," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A.

## CPUID.05H -- MONITOR and MWAIT Features

CPUID.05H returns the MONITOR and MWAIT feature information.

- This leaf is valid if MAX\_LEAF  $\geq$  05H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-15. Leaf 05H MONITOR and MWAIT Features**

| Register   | Field Name                 | Description                                                                                     | Domain   |
|------------|----------------------------|-------------------------------------------------------------------------------------------------|----------|
| EAX[15:0]  | SMALLEST_MONITOR_LINE_SIZE | Smallest monitor-line size in bytes (default is processor's monitor granularity).               | Platform |
| EAX[31:16] | Reserved                   | Reserved.                                                                                       |          |
| EBX[15:0]  | LARGEST_MONITOR_LINE_SIZE  | Largest monitor-line size in bytes (default is processor's monitor granularity).                | Platform |
| EBX[31:16] | Reserved                   | Reserved.                                                                                       |          |
| ECX[0]     | MONITOR_MWAIT_EXTENSIONS   | If 1, supports enumeration of MONITOR/MWAIT extensions (beyond EAX and EBX registers).          | Platform |
| ECX[1]     | INTERRUPT_AS_BREAK_EVENT   | If 1, supports treating interrupts as break-event for MWAIT, even when interrupts are disabled. | Platform |
| ECX[31:2]  | Reserved                   | Reserved.                                                                                       |          |
| EDX[3:0]   | C0_SUB_STATES              | Number of C0* sub C-states supported using MWAIT.                                               | Platform |
| EDX[7:4]   | C1_SUB_STATES              | Number of C1* sub C-states supported using MWAIT.                                               | Platform |
| EDX[11:8]  | C2_SUB_STATES              | Number of C2* sub C-states supported using MWAIT.                                               | Platform |
| EDX[15:12] | C3_SUB_STATES              | Number of C3* sub C-states supported using MWAIT.                                               | Platform |
| EDX[19:16] | C4_SUB_STATES              | Number of C4* sub C-states supported using MWAIT.                                               | Platform |
| EDX[23:20] | C5_SUB_STATES              | Number of C5* sub C-states supported using MWAIT.                                               | Platform |
| EDX[27:24] | C6_SUB_STATES              | Number of C6* sub C-states supported using MWAIT.                                               | Platform |
| EDX[31:28] | C7_SUB_STATES              | Number of C7* sub C-states supported using MWAIT.                                               | Platform |

### NOTE

The definition of C0 through C7 states for MWAIT extensions are processor-specific C-states, not ACPI C-state.

CPUID.05H returns information about features available to MONITOR/MWAIT instructions. The MONITOR instruction is used for address-range monitoring in conjunction with MWAIT instruction. The MWAIT instruction optionally provides additional extensions for advanced power management.

## CPUID.06H -- Thermal and Power Management Features

CPUID.06H returns information about thermal and power management features.

- This leaf is valid if MAX\_LEAF  $\geq$  06H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-16. Leaf 06H Thermal and Power Management Features**

| Register | Field Name                | Description                                                                                                                                              | Domain   |
|----------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[0]   | DIGITAL_TEMP_SENSOR       | If 1, supports Digital Temperature Sensor.                                                                                                               | Platform |
| EAX[1]   | TURBO_BOOST               | If 1, supports Intel Turbo Boost Technology. (see description of IA32_MISC_ENABLE[38]).                                                                  | Platform |
| EAX[2]   | ALWAYS_RUNNING_APIC_TIMER | If 1, supports APIC-Timer-always-running feature.                                                                                                        | Platform |
| EAX[3]   | Reserved                  | Reserved.                                                                                                                                                |          |
| EAX[4]   | POWER_LIMIT_NOTIFY        | If 1, supports power limit notification controls.                                                                                                        | Platform |
| EAX[5]   | EXT_CLOCK_MOD             | If 1, supports clock modulation duty cycle extension.                                                                                                    | Platform |
| EAX[6]   | PKG_THERM_MGMT            | If 1, supports package thermal management.                                                                                                               | Platform |
| EAX[7]   | HWP                       | If 1, supports HWP base registers (IA32_PM_ENABLE[bit 0], IA32_HWP_CAPABILITIES, IA32_HWP_REQUEST, IA32_HWP_STATUS).                                     | Platform |
| EAX[8]   | HWP_INTERRUPT             | If 1, supports IA32_HWP_INTERRUPT MSR.                                                                                                                   | Platform |
| EAX[9]   | HWP_ACTIVITY_WINDOW       | If 1, supports IA32_HWP_REQUEST[bits 41:32].                                                                                                             | Platform |
| EAX[10]  | HWP_EPP                   | If 1, supports IA32_HWP_REQUEST[bits 31:24].                                                                                                             | Platform |
| EAX[11]  | HWP_REQUEST_PKG           | If 1, supports IA32_HWP_REQUEST_PKG MSR.                                                                                                                 | Platform |
| EAX[12]  | Reserved                  | Reserved.                                                                                                                                                |          |
| EAX[13]  | HDC                       | If 1, supports HDC base registers IA32_PKG_HDC_CTL, IA32_PM_CTL1, and IA32_THREAD_STALL MSRs.                                                            | Platform |
| EAX[14]  | TURBO_BOOST_MAX           | If 1, supports Intel® Turbo Boost Max Technology 3.0.                                                                                                    | Platform |
| EAX[15]  | HWP_CAP                   | If 1, supports Highest Performance change capability.                                                                                                    | Platform |
| EAX[16]  | HWP_PECI_OVERRIDE         | If 1, supports HWP Peci override.                                                                                                                        | Platform |
| EAX[17]  | FLEXIBLE_HWP              | If 1, supports Flexible HWP.                                                                                                                             | Platform |
| EAX[18]  | HWP_REQUEST_FAST_ACCESS   | If 1, supports Fast access mode for the IA32_HWP_REQUEST MSR.                                                                                            | Platform |
| EAX[19]  | HW_FEEDBACK               | If 1, supports IA32_HW_FEEDBACK_PTR MSR, IA32_HW_FEEDBACK_CONFIG MSR, IA32_PACKAGE_THERM_STATUS MSR bit 26, and IA32_PACKAGE_THERM_INTERRUPT MSR bit 25. | Platform |
| EAX[20]  | HWP_REQUEST_IGNORE_IDLE   | If 1, supports Ignoring Idle Logical Processor HWP request.                                                                                              | Platform |
| EAX[21]  | Reserved                  | Reserved.                                                                                                                                                |          |
| EAX[22]  | HWP_CTL                   | If 1, supports IA32_HWP_CTL MSR.                                                                                                                         | Platform |

|            |                         |                                                                                                                                                                                                                                                                                                                  |                   |
|------------|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[23]    | THREAD_DIRECTOR         | If 1, supports Intel® Thread Director. IA32_HW_FEEDBACK_CHAR and IA32_HW_FEEDBACK_THREAD_CONFIG MSRs are supported if set.                                                                                                                                                                                       | Platform          |
| EAX[31:24] | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| EBX[3:0]   | DTS_NUM_INT_THRESHOLDS  | Number of Interrupt Thresholds in Digital Thermal Sensor.                                                                                                                                                                                                                                                        | Platform          |
| EBX[31:4]  | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| ECX[0]     | HW_FEEDBACK_CAP         | If 1, supports IA32_MPERF and IA32_APERF which provide a measure of delivered processor performance (since last reset of the counters), as a percentage of the expected processor performance when running at the TSC frequency.                                                                                 | Platform          |
| ECX[2:1]   | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| ECX[3]     | ENERGY_PERF_BIAS        | If 1, supports performance-energy bias preference and a new architectural MSR called IA32_ENERGY_PERF_BIAS (1BOH).                                                                                                                                                                                               | Platform          |
| ECX[7:4]   | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| ECX[15:8]  | HW_FEEDBACK_NUM_CLASSES | Number of Intel® Thread Director classes supported by the processor. Information for that many classes is written into the Intel Thread Director Table by the hardware.                                                                                                                                          | Platform          |
| ECX[31:16] | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| EDX[7:0]   | HW_FEEDBACK_CAPS        | Bitmap of supported hardware feedback interface capabilities.<br>0 = If 1, supports performance capability reporting.<br>1 = If 1, supports energy efficiency capability reporting.<br>2-7 = Reserved.<br>Bits 0 and 1 will always be set together.                                                              | Package           |
| EDX[11:8]  | HW_FEEDBACK_TABLE_SIZE  | Enumerates the size of the hardware feedback interface structure in number of 4 KB pages. Add one to the return value to get the result.                                                                                                                                                                         | Package           |
| EDX[15:12] | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                        |                   |
| EDX[31:16] | HW_FEEDBACK_TABLE_INDEX | Index (starting at 0) of this logical processor's row in the hardware feedback interface structure. Note that on some parts the index may be same for multiple logical processors. On some parts the indices may not be contiguous, i.e., there may be unused rows in the hardware feedback interface structure. | Logical Processor |

Details around these features are described in Chapter 16, "Power and Thermal Management," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3B.

## CPUID.07H -- Structured Extended Feature Flags

CPUID.07H returns structured extended feature flags enumeration information. The sub-sections of Section provide leaf 07H information.

- This leaf is valid if MAX\_LEAF  $\geq$  07H.
- The maximum sub-leaf value for ECX is specified in CPUID.07H.00H.EAX[31:0] MAX\_SUBLEAF.
- If ECX contains an invalid Sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

### CPUID.07H.00H -- Structured Extended Feature Flags Main Sub-Leaf

CPUID.07H.00H returns the maximum input value of the highest leaf 07H sub-leaf; and EBX, ECX, and EDX contain information of extended feature flags.

**Table 21-17. Leaf 07H Sub-Leaf (ECX=0) Output Registers**

| CPUID Output Registers | Field Name  | Description                                                                                            | CPUID Domain |
|------------------------|-------------|--------------------------------------------------------------------------------------------------------|--------------|
| EAX[31:0]              | MAX_SUBLEAF | Reports the maximum input value for supported leaf 07H subleaves.                                      | Platform     |
| EBX[31:0]              |             | Extended Feature Flags Information in EBX (see "CPUID.07H.00H:EBX—Extended Feature Flags Information") |              |
| ECX[31:0]              |             | Extended Feature Flags Information in ECX (see "CPUID.07H.00H:ECX—Extended Feature Flags Information") |              |
| EDX[31:0]              |             | Extended Feature Flags Information in EDX (see "CPUID.07H.00H:EDX—Extended Feature Flags Information") |              |

**Table 21-18. Leaf 07H.00H Structured Extended Feature Flags Returned in EAX**

| Register  | Field Name  | Description                                                        | Domain   |
|-----------|-------------|--------------------------------------------------------------------|----------|
| EAX[31:0] | MAX_SUBLEAF | Reports the maximum input value for supported leaf 07H sub-leaves. | Platform |

### CPUID.07H.00H:EBX Extended Feature Flags Information

The EBX register of CPUID.07H.00H returns the information shown below.

**Table 21-19. Leaf 07H.00H Structured Extended Feature Flags Returned in EBX**

| Register | Field Name | Description                                                              | Domain   |
|----------|------------|--------------------------------------------------------------------------|----------|
| EBX[0]   | FSGSBASE   | If 1, supports RDFSBASE/RDGSBASE/WRFS-BASE/WRGSBASE.                     | Platform |
| EBX[1]   | TSC_ADJUST | If 1, the IA32_TSC_ADJUST MSR is supported.                              | Platform |
| EBX[2]   | SGX        | If 1, supports Intel® Software Guard Extensions (Intel® SGX Extensions). | Platform |
| EBX[3]   | BMI1       | If 1, supports the BMI1 instructions.                                    | Platform |
| EBX[4]   | HLE        | If 1, supports the Hardware Lock Elision instruction set.                | Platform |
| EBX[5]   | AVX2       | If 1, supports Intel® Advanced Vector Extensions 2 (Intel® AVX2).        | Platform |

|         |                      |                                                                                                  |          |
|---------|----------------------|--------------------------------------------------------------------------------------------------|----------|
| EBX[6]  | FDP_EXCPTN_ONLY      | If 1, the x87 FPU Data Pointer is updated only on x87 exceptions.                                | Platform |
| EBX[7]  | SMEP                 | If 1, supports Supervisor-Mode Execution Prevention.                                             | Platform |
| EBX[8]  | BMI2                 | If 1, supports the BMI2 instructions.                                                            | Platform |
| EBX[9]  | ENH_REP_MOVSBS_STOSB | If 1, supports Enhanced REP MOVSB/STOSB.                                                         | Platform |
| EBX[10] | INVPCID              | If 1, supports INVPCID instruction for system software that manages process-context identifiers. | Platform |
| EBX[11] | RTM                  | If 1, supports the Restricted Transactional Memory instruction set.                              | Platform |
| EBX[12] | RDT_M                | If 1, supports Intel® Resource Director Technology (Intel® RDT) Monitoring capability.           | Platform |
| EBX[13] | FCS_FDS_DEPRECATION  | If 1, deprecates FPU CS and FPU DS values.                                                       | Platform |
| EBX[14] | MPX                  | If 1, supports Intel® Memory Protection Extensions.                                              | Platform |
| EBX[15] | RDT_A                | If 1, supports Intel® Resource Director Technology (Intel® RDT) Allocation capability.           | Platform |
| EBX[16] | AVX512F              | If 1, supports the AVX512F instructions.                                                         | Platform |
| EBX[17] | AVX512DQ             | If 1, supports the AVX512DQ instructions.                                                        | Platform |
| EBX[18] | RDSEED               | If 1, supports the RDSEED instruction.                                                           | Platform |
| EBX[19] | ADX                  | If 1, supports the ADX instructions.                                                             | Platform |
| EBX[20] | SMAP                 | If 1, supports Supervisor-Mode Access Prevention and the CLAC/STAC instructions.                 | Platform |
| EBX[21] | AVX512_IFMA          | If 1, supports the AVX512_IFMA instructions.                                                     | Platform |
| EBX[22] | Reserved             | Reserved.                                                                                        |          |
| EBX[23] | CLFLUSHOPT           | If 1, supports the CLFLUSHOPT instruction.                                                       | Platform |
| EBX[24] | CLWB                 | If 1, supports the CLWB instruction.                                                             | Platform |
| EBX[25] | INTEL_PROC_TRACE     | If 1, supports Intel® Processor Trace.                                                           | Platform |
| EBX[26] | AVX512PF             | If 1, supports the AVX512PF instructions. (Intel® Xeon Phi™ only.)                               | Platform |
| EBX[27] | AVX512ER             | If 1, supports the AVX512ER instructions. (Intel® Xeon Phi™ only.)                               | Platform |
| EBX[28] | AVX512CD             | If 1, supports the AVX512CD instructions.                                                        | Platform |
| EBX[29] | SHA                  | If 1, supports Intel® Secure Hash Algorithm Extensions (Intel® SHA Extensions).                  | Platform |
| EBX[30] | AVX512BW             | If 1, supports the AVX512BW instructions.                                                        | Platform |
| EBX[31] | AVX512VL             | If 1, supports the AVX512VL instructions.                                                        | Platform |

## CPUID.07H.00H:ECX Extended Feature Flags Information

The ECX register of CPUID.07H.00H returns the information shown below.

**Table 21-20. Leaf 07H.00H Structured Extended Feature Flags Returned in ECX**

| Register | Field Name | Description | Domain |
|----------|------------|-------------|--------|
|----------|------------|-------------|--------|

|            |                  |                                                                                                                                                                                                                                                                     |                   |
|------------|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| ECX[0]     | PREFETCHWT1      | If 1, supports the PREFETCHWT1 instruction. (Intel® Xeon Phi™ only.)                                                                                                                                                                                                | Platform          |
| ECX[1]     | AVX512_VBMI      | If 1, supports the AVX512_VBMI instructions.                                                                                                                                                                                                                        | Platform          |
| ECX[2]     | UMIP             | If 1, supports user-mode instruction prevention.                                                                                                                                                                                                                    | Platform          |
| ECX[3]     | PKU              | If 1, supports protection keys for user-mode pages.                                                                                                                                                                                                                 | Platform          |
| ECX[4]     | OSPKE            | If 1, the OS has set CR4.PKE to enable protection keys and the RDPKRU/WRPKRU instructions.                                                                                                                                                                          | Logical Processor |
| ECX[5]     | WAITPKG          | If 1, supports the TPAUSE, UMONITOR, and UMWAIT instructions.                                                                                                                                                                                                       | Platform          |
| ECX[6]     | AVX512_VBMI2     | If 1, supports the AVX512_VBMI2 instructions.                                                                                                                                                                                                                       | Platform          |
| ECX[7]     | CET_SS           | If 1, supports CET shadow stack features. Processors that set this bit define bits 1:0 of the IA32_U_CET and IA32_S_CET MSRs. Enumerates support for the following MSRs: IA32_INTERRUPT_SPP_TABLE_ADDR, IA32_PL3_SSP, IA32_PL2_SSP, IA32_PL1_SSP, and IA32_PLO_SSP. | Platform          |
| ECX[8]     | GFNI             | If 1, supports the GFNI instruction set.                                                                                                                                                                                                                            | Platform          |
| ECX[9]     | VAES             | If 1 and Intel AVX supported, supports the VEX-encoded AES instruction set.                                                                                                                                                                                         | Platform          |
| ECX[10]    | VPCLMULQDQ       | If 1 and Intel AVX supported, supports the VPCLMULQDQ instruction.                                                                                                                                                                                                  | Platform          |
| ECX[11]    | AVX512_VNNI      | If 1, supports the AVX512_VNNI instructions.                                                                                                                                                                                                                        | Platform          |
| ECX[12]    | AVX512_BITALG    | If 1, supports the AVX512_BITALG instructions.                                                                                                                                                                                                                      | Platform          |
| ECX[13]    | TME_EN           | If 1, the following MSRs are supported: IA32_TME_CAPABILITY, IA32_TME_ACTIVATE, IA32_TME_EXCLUDE_MASK, and IA32_TME_EXCLUDE_BASE.                                                                                                                                   | Platform          |
| ECX[14]    | AVX512_VPOPCNTDQ | If 1, supports the AVX512_VPOPCNTDQ instructions.                                                                                                                                                                                                                   | Platform          |
| ECX[15]    | Reserved         | Reserved.                                                                                                                                                                                                                                                           |                   |
| ECX[16]    | LA57             | If 1, supports 57-bit linear addresses and five-level paging.                                                                                                                                                                                                       | Platform          |
| ECX[21:17] | MPX_MAWAU        | The value of MAWAU used by the BNDLDX and BNDSTX instructions in 64-bit mode.                                                                                                                                                                                       | Platform          |
| ECX[22]    | RDPID            | If 1, RDPID and the IA32_TSC_AUX MSR are available.                                                                                                                                                                                                                 | Platform          |
| ECX[23]    | KEY_LOCKER       | If 1, supports Key Locker.                                                                                                                                                                                                                                          | Platform          |
| ECX[24]    | BUS_LOCK_DETECT  | If 1, indicates support for OS bus-lock detection.                                                                                                                                                                                                                  | Platform          |
| ECX[25]    | CLDEMOTE         | If 1, supports cache line demote.                                                                                                                                                                                                                                   | Platform          |
| ECX[26]    | Reserved         | Reserved.                                                                                                                                                                                                                                                           |                   |
| ECX[27]    | MOVDIRI          | If 1, supports the MOVDIRI instruction.                                                                                                                                                                                                                             | Platform          |
| ECX[28]    | MOVDIR64B        | If 1, supports the MOVDIR64B instruction.                                                                                                                                                                                                                           | Platform          |
| ECX[29]    | ENQCMD           | If 1, supports Enqueue Stores.                                                                                                                                                                                                                                      | Platform          |

|         |        |                                                           |          |
|---------|--------|-----------------------------------------------------------|----------|
| ECX[30] | SGX_LC | If 1, supports SGX Launch Configuration.                  | Platform |
| ECX[31] | PKS    | If 1, supports protection keys for supervisor-mode pages. | Platform |

## CPUID.07H.00H:EDX Extended Feature Flags Information

The EDX register of CPUID.07H.00H returns the information shown below.

**Table 21-21. Leaf 07H.00H Structured Extended Feature Flags Returned in EDX**

| Register | Field Name           | Description                                                                                                                                                  | Domain   |
|----------|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[0]   | Reserved             | Reserved.                                                                                                                                                    |          |
| EDX[1]   | SGX_KEYS             | If 1, supports Attestation Services for Intel® SGX.                                                                                                          | Platform |
| EDX[2]   | AVX512_4VNNIW        | If 1, supports the AVX512_4VNNIW instructions. (Intel® Xeon Phi™ only.)                                                                                      | Platform |
| EDX[3]   | AVX512_4FMAPS        | If 1, supports the AVX512_4FMAPS instructions. (Intel® Xeon Phi™ only.)                                                                                      | Platform |
| EDX[4]   | FAST_SHORT_REP_MOVSB | If 1, supports Fast Short REP MOVSB.                                                                                                                         | Platform |
| EDX[5]   | UINTR                | If 1, supports user interrupts.                                                                                                                              | Platform |
| EDX[7:6] | Reserved             | Reserved.                                                                                                                                                    |          |
| EDX[8]   | AVX512_VP2INTERSECT  | If 1, supports the AVX512_VP2INTERSECT instruction.                                                                                                          | Platform |
| EDX[9]   | MCU_OPT_CTRL         | If 1, supports both the IA32_MCU_OPT_CTRL MSR and its bit 0 (RNGDS_MITG_DIS).                                                                                | Platform |
| EDX[10]  | MD_CLEAR             | If 1, supports MD_CLEAR.                                                                                                                                     | Platform |
| EDX[11]  | RTM_ALWAYS_ABORT     | If 1, any execution of XBEGIN immediately aborts and transitions to the specified fallback address.                                                          | Platform |
| EDX[12]  | Reserved             | Reserved.                                                                                                                                                    |          |
| EDX[13]  | RTM_FORCE_ABORT      | If 1, supports RTM_FORCE_ABORT and the IA32_TSX_FORCE_ABORT MSR. These allow software to set IA32_TSX_FORCE_ABORT[0] (RTM_FORCE_ABORT).                      | Platform |
| EDX[14]  | SERIALIZE            | If 1, supports SERIALIZE instruction.                                                                                                                        | Platform |
| EDX[15]  | HYBRID               | If 1, the processor is identified as a hybrid part. If CPUID.00H.MAXLEAF ≥ 1AH and CPUID.1AH:EAX <> 0, then the Native Model ID Enumeration Leaf 1AH exists. | Platform |
| EDX[16]  | TSXLDTRK             | If 1, supports Intel TSX suspend/resume of load address tracking.                                                                                            | Platform |
| EDX[17]  | Reserved             | Reserved.                                                                                                                                                    |          |
| EDX[18]  | PCONFIG              | If 1, supports the PCONFIG instruction.                                                                                                                      | Platform |
| EDX[19]  | ARCH_LBRS            | If 1, supports architectural LBRS.                                                                                                                           | Platform |
| EDX[20]  | CET_IBT              | If 1, supports CET indirect branch tracking features. Processors that set this bit define bits 5:2 and bits 63:10 of the IA32_U_CET and IA32_S_CET MSRs.     | Platform |

|         |                         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |          |
|---------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[21] | Reserved                | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |          |
| EDX[22] | AMX_BF16                | If 1, supports tile computational operations on bfloat16 numbers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Platform |
| EDX[23] | AVX512_FP16             | If 1, supports the FP16 data type with AVX512 instructions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Platform |
| EDX[24] | AMX_TILE                | If 1, supports tile architecture.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Platform |
| EDX[25] | AMX_INT8                | If 1, supports tile computational operations on 8-bit integers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Platform |
| EDX[26] | IBRS_IBPB               | If 1, supports indirect branch restricted speculation (IBRS) and the indirect branch predictor barrier (IBPB). Processors that set this bit support the IA32_SPEC_CTRL MSR and the IA32_PRED_CMD MSR.<br>They allow software to set IA32_SPEC_CTRL[0] (IBRS) and IA32_PRED_CMD[0] (IBPB).                                                                                                                                                                                                                                                                                                                                                                                                               | Platform |
| EDX[27] | SPEC_CTRL_ST_PREDICTORS | If 1, supports single thread indirect branch predictors (STIBP). Processors that set this bit support the IA32_SPEC_CTRL MSR. They allow software to set IA32_SPEC_CTRL[1] (STIBP).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Platform |
| EDX[28] | L1D_FLUSH_INTERFACE     | If 1, supports L1D_FLUSH. Processors that set this bit support the IA32_FLUSH_CMD MSR.<br>They allow software to set IA32_FLUSH_CMD[0] (L1D_- FLUSH).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Platform |
| EDX[29] | ARCH_CAPABILITIES       | If 1, supports the IA32_ARCH_CAPABILITIES MSR.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Platform |
| EDX[30] | CORE_CAPABILITIES       | If 1, supports the IA32_CORE_CAPABILITIES MSR.<br>IA32_CORE_CAPABILITIES is an architectural MSR that enumerates model-specific features. A bit being set in this MSR indicates that a model specific feature is supported; software must still consult CPUID family/model/stepping to determine the behavior of the enumerated feature as features enumerated in IA32_CORE_CAPABILITIES may have different behavior on different processor models. Some of these features may have behavior that is consistent across processor models (and for which consultation of CPUID family/model/stepping is not necessary); such features are identified explicitly where they are documented in this manual. | Platform |
| EDX[31] | SPEC_CTRL_SSBD          | If 1, supports Speculative Store Bypass Disable (SSBD). Processors that set this bit support the IA32_SPEC_CTRL MSR. They allow software to set IA32_SPEC_CTRL[2] (SSBD).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Platform |

## CPUID.07H.01H -- Structured Extended Feature Sub-Leaf 1

### CPUID.07H.01H:EAX Extended Feature Information

The EAX register of CPUID.07H.01H returns the information shown below.

**Table 21-22. Leaf 07H.01H Structured Extended Feature Flags Returned in EAX**

| Register   | Field Name                  | Description                                                                                                                                                                                                  | Domain   |
|------------|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[0]     | SHA512                      | If 1, supports the SHA512 instructions.                                                                                                                                                                      | Platform |
| EAX[1]     | SM3                         | If 1, supports the SM3 instructions.                                                                                                                                                                         | Platform |
| EAX[2]     | SM4                         | If 1, supports the SM4 instructions.                                                                                                                                                                         | Platform |
| EAX[3]     | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[4]     | AVX_VNNI                    | If 1, supports the VEX-encoded versions of the Vector Neural Network Instructions.                                                                                                                           | Platform |
| EAX[5]     | AVX512_BF16                 | If 1, supports the Vector Neural Network Instructions supporting BFLOAT16 inputs and conversion instructions from IEEE single precision.                                                                     | Platform |
| EAX[6]     | LASS                        | If 1, supports Linear Address Space Separation.                                                                                                                                                              | Platform |
| EAX[7]     | CMPCCXADD                   | If 1, supports the CMPccXADD instruction.                                                                                                                                                                    | Platform |
| EAX[8]     | ARCH_PERFMON_EXT            | If 1, supports ArchPerfmonExt. When set, indicates that the Architectural Performance Monitoring Extended Leaf (EAX=23H) is valid.                                                                           | Platform |
| EAX[9]     | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[10]    | FAST_REP_MOVS               | If 1, supports fast zero-length REP MOVS.                                                                                                                                                                    | Platform |
| EAX[11]    | FAST_REP_STOS               | If 1, supports fast short REP STOS.                                                                                                                                                                          | Platform |
| EAX[12]    | FAST_REP_CMPSB_SCASB        | If 1, supports fast short REP CMPSB, REP SCASB.                                                                                                                                                              | Platform |
| EAX[16:13] | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[17]    | FRED                        | If 1, supports Flexible Return and Event Delivery and the architectural state (MSRs) defined by FRED. Any Intel processor that enumerates support for FRED transitions will also enumerate support for LKGS. | Platform |
| EAX[18]    | LKGS                        | If 1, supports the LKGS (load into IA32_KERNEL_GS_BASE) instruction.                                                                                                                                         | Platform |
| EAX[19]    | WRMSRNS                     | If 1, supports the WRMSRNS instruction.                                                                                                                                                                      | Platform |
| EAX[20]    | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[21]    | AMX_FP16                    | If 1, supports tile computational operations on FP16 numbers.                                                                                                                                                | Platform |
| EAX[22]    | HRESET                      | If 1, supports history reset via the HRESET instruction and the IA32_HRESET_ENABLE MSR. When set, indicates that the Processor History Reset Leaf (EAX = 20H) is valid.                                      | Platform |
| EAX[23]    | AVX_IFMA                    | If 1, supports the AVX-IFMA instructions.                                                                                                                                                                    | Platform |
| EAX[25:24] | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[26]    | LAM                         | If 1, supports Linear Address Masking.                                                                                                                                                                       | Platform |
| EAX[27]    | MSRLIST                     | If 1, supports the RDMSRLIST and WRMSRLIST instructions and the IA32_BARRIER MSR.                                                                                                                            | Platform |
| EAX[29:28] | Reserved                    | Reserved.                                                                                                                                                                                                    |          |
| EAX[30]    | INVD_DISABLE_POST_BIOS_DONE | If 1, supports INVD execution prevention after BIOS Done.                                                                                                                                                    | Platform |

|         |          |           |  |
|---------|----------|-----------|--|
| EAX[31] | Reserved | Reserved. |  |
|---------|----------|-----------|--|

## CPUID.07H.01H:EBX Extended Feature Information

The EBX register of CPUID.07H.01H returns the information shown below.

**Table 21-23. Leaf 07H.01H Structured Extended Feature Flags Returned in EBX**

| Register  | Field Name          | Description                                                                                          | Domain   |
|-----------|---------------------|------------------------------------------------------------------------------------------------------|----------|
| EBX[0]    | PPIN                | If 1, supports the IA32_PPIN and IA32_PPIN_CTL MSRs.                                                 | Platform |
| EBX[1]    | PBNDKB              | If 1, supports the PBNDKB instruction and enumerates the existence of the IA32_TSE_CAPABILITY MSR.   | Platform |
| EBX[2]    | Reserved            | Reserved.                                                                                            |          |
| EBX[3]    | CPUIDMAXVAL_LIM_RMV | If 1, IA32_MISC_ENABLE[bit 22] cannot be set to 1 to limit the value returned by CPUID.00H:EAX[7:0]. | Platform |
| EBX[31:4] | Reserved            | Reserved.                                                                                            |          |

## CPUID.07H.01H:ECX Extended Feature Information

The ECX register of CPUID.07H.01H returns the information shown below.

**Table 21-24. Leaf 07H.01H Structured Extended Feature Flags Returned in ECX**

| Register  | Field Name | Description                                                                                                   | Domain |
|-----------|------------|---------------------------------------------------------------------------------------------------------------|--------|
| ECX[0]    | RDT_M_ASYM | If 1, at least one logical processor on this platform supports Asymmetrical Intel® RDT Monitoring capability. |        |
| ECX[1]    | RDT_A_ASYM | If 1, at least one logical processor on this platform supports Asymmetrical Intel® RDT Allocation capability. |        |
| ECX[31:2] | Reserved   | Reserved.                                                                                                     |        |

## CPUID.07H.01H:EDX Extended Feature Information

The EDX register of CPUID.07H.01H returns the information shown below.

**Table 21-25. Leaf 07H.01H Structured Extended Feature Flags Returned in EDX**

| Register | Field Name     | Description                                     | Domain   |
|----------|----------------|-------------------------------------------------|----------|
| EDX[3:0] | Reserved       | Reserved.                                       |          |
| EDX[4]   | AVX_VNNI_INT8  | If 1, supports the AVX-VNNI-INT8 instructions.  | Platform |
| EDX[5]   | AVX_NE_CONVERT | If 1, supports the AVX-NE-CONVERT instructions. | Platform |
| EDX[7:6] | Reserved       | Reserved.                                       |          |
| EDX[8]   | AMX_COMPLEX    | If 1, supports the AMX_COMPLEX instructions.    |          |
| EDX[9]   | Reserved       | Reserved.                                       |          |
| EDX[10]  | AVX_VNNI_INT16 | If 1, supports the AVX-VNNI-INT16 instructions. | Platform |

|            |                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |          |
|------------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[13:11] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |          |
| EDX[14]    | PREFETCHI           | If 1, supports the PREFETCHIT0/1 instructions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Platform |
| EDX[16:15] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |          |
| EDX[17]    | UIRET_UIF           | If 1, UIRET sets UIF to the value of bit 1 of the RFLAGS image loaded from the stack.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Platform |
| EDX[18]    | CET_SSS             | If 1, indicates that an operating system can enable supervisor shadow stacks as long as it ensures that a supervisor shadow stack cannot become prematurely busy due to page faults (see Section 17.2.3 of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1). When emulating the CPUID instruction, a virtual-machine monitor (VMM) should return this bit as 1 only if it ensures that VM exits cannot cause a guest supervisor shadow stack to appear to be prematurely busy. Such a VMM could set the “prematurely busy shadow stack” VM-exit control and use the additional information that it provides. | Platform |
| EDX[19]    | AVX10               | If 1, supports the Intel® AVX10 instructions and indicates the presence of CPUID.24H, which enumerates the version number.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Platform |
| EDX[21:20] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |          |
| EDX[22]    | SEC-TEE-ATTESTATION | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Platform |
| EDX[23]    | MWAIT               | If 1, MWAIT is supported (even if CPUID.01H:ECX.MONITOR[3] is enumerated as 0).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Platform |
| EDX[24]    | SLSM                | Static LSM is supported on this platform. If set, IA32_INTEGRITY_STATUS (0x2DC) is available for software use.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Platform |
| EDX[31:25] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |          |

## CPUID.07H.02H -- Structured Extended Feature Sub-Leaf 2

CPUID.07H.02H returns the structured extended feature information contained in the sub-sections of this section.

**Table 21-26. Leaf 07H Sub-Leaf (ECX=2) Output Registers**

| CPUID Output Registers | Description                                                                         |
|------------------------|-------------------------------------------------------------------------------------|
| EAX[31:0]              | Reserved                                                                            |
| EBX[31:0]              | Reserved                                                                            |
| ECX[31:0]              | Reserved                                                                            |
| EDX[31:0]              | Extended Feature Information (see “CPUID.07H.02H:EDX—Extended Feature Information”) |

## CPUID.07H.02H:EDX Extended Feature Information

The EDX register of CPUID.07H.02H returns the information shown below.

Table 21-27. CPUID.07H.02H Extended Feature Information Provided in EDX<sup>1</sup>

| Register  | Field Name      | Description                                                                                                                                                                                                                                      | Domain   |
|-----------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EDX[0]    | PSFD            | If 1, supports bit 7 of the IA32_SPEC_CTRL MSR. Bit 7 of this MSR disables Fast Store Forwarding Predictor without disabling Speculative Store Bypass.                                                                                           | Platform |
| EDX[1]    | IPRED_CTRL      | If 1, supports bits 3 and 4 of the IA32_SPEC_CTRL MSR. Bit 3 of this MSR enables IPRED_DIS control for CPL3. Bit 4 of this MSR enables IPRED_DIS control for CPL0/1/2.                                                                           | Platform |
| EDX[2]    | RRSBA_CTRL      | If 1, supports bits 5 and 6 of the IA32_SPEC_CTRL MSR. Bit 5 of this MSR disables RRSBA behavior for CPL3. Bit 6 of this MSR disables RRSBA behavior for CPL0/1/2.                                                                               | Platform |
| EDX[3]    | DDPD_U          | If 1, supports bit 8 of the IA32_SPEC_CTRL MSR. Bit 8 of this MSR disables Data Dependent Prefetcher.                                                                                                                                            | Platform |
| EDX[4]    | BHI_CTRL        | If 1, supports bit 10 of the IA32_SPEC_CTRL MSR. Bit 10 of this MSR enables BHI_DIS_S behavior.                                                                                                                                                  | Platform |
| EDX[5]    | MCDT_NO         | If 1, the processor does not exhibit MXCSR Configuration Dependent Timing (MCDT) behavior and does not need to be mitigated to avoid data-dependent behavior for certain instructions.                                                           | Platform |
| EDX[6]    | UC_LOCK_DISABLE | If 1, supports the UC-lock disable feature and it causes #AC.                                                                                                                                                                                    | Platform |
| EDX[7]    | MONITOR_MITG_NO | If 1, the MONITOR/UMONITOR instructions are not affected by performance or power issues due to MONITOR/UMONITOR instructions exceeding the capacity of an internal monitor tracking table. If 0, then the product may be affected by this issue. | Platform |
| EDX[31:8] | Reserved        | Reserved.                                                                                                                                                                                                                                        |          |

**NOTE**

1. Leaf 07H output depends on the initial value in ECX. If ECX contains an invalid sub-leaf index, EDX returns 0.

## CPUID.08H -- Reserved

This leaf is reserved.

**Table 21-28. Leaf 08H Reserved**

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

CPUID.09H -- Direct Cache Access Information

- CPUID.09H returns information about Direct Cache Access capabilities.
- This leaf is valid if CPUID.01H:ECX.DCA[18] = 1 and MAX\_LEAF ≥ 09H.
  - This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-29. Leaf 09H Direct Cache Access Information

| Register  | Field Name       | Description                                                       | Domain   |
|-----------|------------------|-------------------------------------------------------------------|----------|
| EAX[31:0] | PLATFORM_DCA_CAP | Value of bits [31:0] of IA32_PLATFORM_DCA_CAP MSR (address 1F8H). | Platform |
| EBX[31:0] | Reserved         | Reserved.                                                         |          |
| ECX[31:0] | Reserved         | Reserved.                                                         |          |
| EDX[31:0] | Reserved         | Reserved.                                                         |          |

The IA32\_PLATFORM\_DCA\_CAP MSR is valid when CPUID.01H:ECX.DCA[18] = 1.

## CPUID.0AH -- Architectural Performance Monitoring

CPUID.0AH returns information about support for architectural performance monitoring capabilities.

- This leaf is valid if CPUID.0AH:EAX[7:0] (Version ID) > 0 and MAX\_LEAF ≥ 0AH.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-30. Leaf 0AH Architectural Performance Monitoring**

| Register   | Field Name        | Description                                                                                                                                        | Domain   |
|------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[7:0]   | VERSION           | Version ID of architectural performance monitoring.                                                                                                | Platform |
| EAX[15:8]  | NUM_GP_CTRS       | Number of general-purpose performance monitoring counter(s) per logical processor.                                                                 | Platform |
| EAX[23:16] | GP_CTR_WIDTH      | Bit width of general-purpose, performance monitoring counter.                                                                                      | Platform |
| EAX[31:24] | EVENT_ENUM_LENGTH | Length of EBX bit vector to enumerate architectural performance monitoring events. Architectural event x is supported if EBX[x]=0 && EAX[31:24]>x. | Platform |
| EBX[0]     | CORE_CYC_NA       | Core cycle event not available if 1 or if EAX[31:24]<1.                                                                                            | Platform |
| EBX[1]     | INTR_RET_NA       | Instruction retired event not available if 1 or if EAX[31:24]<2.                                                                                   | Platform |
| EBX[2]     | REF_CYC_NA        | Reference cycles event not available if 1 or if EAX[31:24]<3.                                                                                      | Platform |
| EBX[3]     | LLC_CYC_NA        | Last-level cache reference event not available if 1 or if EAX[31:24]<4.                                                                            | Platform |
| EBX[4]     | LLC_MISSES_NA     | Last-level cache misses event not available if 1 or if EAX[31:24]<5.                                                                               | Platform |
| EBX[5]     | BR_INSTR_RET_NA   | Branch instruction retired event not available if 1 or if EAX[31:24]<6.                                                                            | Platform |
| EBX[6]     | BR_MISPRED_RET_NA | Branch mispredict retired event not available if 1 or if EAX[31:24]<7.                                                                             | Platform |
| EBX[7]     | SLOTS_NA          | Top-down slots event not available if 1 or if EAX[31:24]<8.                                                                                        | Platform |
| EBX[8]     | BACKEND_NA        | Topdown backend bound not available if 1 or if EAX[31:24] < 9.                                                                                     | Platform |
| EBX[9]     | BADSPEC_NA        | Topdown bad speculation not available if 1 or if EAX[31:24] < 10.                                                                                  | Platform |
| EBX[10]    | FRONTEND_NA       | Topdown frontend bound not available if 1 or if EAX[31:24] < 11.                                                                                   | Platform |
| EBX[11]    | RETIRING_NA       | Topdown retiring not available if 1 or if EAX[31:24] < 12.                                                                                         | Platform |
| EBX[12]    | LBR_INSERTS_NA    | LBR inserts not available if 1 or if EAX[31:24] < 13.                                                                                              | Platform |
| EBX[31:13] | Reserved          | Reserved.                                                                                                                                          |          |

|            |                       |                                                                                                                                                                                                                                                                                                                                                                                         |          |
|------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| ECX[31:0]  | FIXED_CTR_MASK        | Supported fixed counters bit mask. Fixed-function performance counter 'i' is supported if bit 'i' is 1 (first counter index starts at zero). It is recommended to use the following logic to determine if a Fixed Counter is supported:<br>FxCtr[i]_is_supported := ECX[i]    (EDX[4:0] > i);                                                                                           | Platform |
| EDX[4:0]   | NUM_FIXED_CTR         | Number of contiguous fixed-function performance counters starting from 0 (if Version ID > 1).                                                                                                                                                                                                                                                                                           | Platform |
| EDX[12:5]  | FIXED_CTR_WIDTH       | Bit width of fixed-function performance counters (if Version ID > 1).                                                                                                                                                                                                                                                                                                                   | Platform |
| EDX[14:13] | Reserved              | Reserved.                                                                                                                                                                                                                                                                                                                                                                               |          |
| EDX[15]    | ANYTHREAD_DEPRECATION | Starting with Architectural Performance Monitoring Version 5, this field indicates that a processor supports AnyThread mode deprecation. If this field is set, software can choose to ignore guidelines in "AnyThread Counting and Software Evolution" of Chapter 21, "Performance Monitoring," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3B         | Platform |
| EDX[19:16] | SLOTS_PER_CYC         | If this field is non-zero, it represents the number of Top-down Microarchitecture Analysis (TMA) slots per cycle. This number can be multiplied by the number of cycles (from CPU_CLK_UNHALTED.THREAD / CPU_CLK_UNHALTED.CORE or IA32_FIXED_CTR1) to determine the total number of slots. If this field is zero, IA32_FIXED_CTR3 should be used to determine the total number of slots. | Platform |
| EDX[31:20] | Reserved              | Reserved.                                                                                                                                                                                                                                                                                                                                                                               |          |

For each version of architectural performance monitoring capability, software must enumerate this leaf to discover the programming facilities and the architectural performance events available in the processor. The details are described in Chapter 21, "Performance Monitoring," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3C.

## CPUID.0BH -- Extended Topology

CPUID.0BH returns information about Extended Topology. CPUID.1FH is a preferred superset to leaf 0BH. Intel recommends first checking for the existence of leaf 1FH before using leaf 0BH.

- This leaf is valid if CPUID.0BH.00H:EBX[15:0]  $\neq$  0 and MAX\_LEAF  $\geq$  0BH.
  - When the leaf is invalid, CPUID.0BH.00H:ECX.DOMAIN\_TYPE[15:8] will report the Domain Type ID as Invalid (0).
- The sub-leaves are enumerated until sub-leaf n returns 0 in EBX[15:0].
- If ECX contains an invalid sub-leaf index, EAX/EBX return 0. Sub-leaf index n+1 is invalid if sub-leaf n returns EBX[15:0] as 0.

## CPUID.0BH -- ECX $\geq$ 0

Table 21-31. Leaf 0BH Extended Topology

| Register   | Field Name        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Domain            |
|------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[4:0]   | SHIFT_COUNT       | The number of bits that the x2APIC ID must be shifted to the right to address instances of the next higher-scoped domain. When logical processor is not supported by the processor, the value of this field at the Logical Processor domain sub-leaf may be returned as either 0 (no allocated bits in the x2APIC ID) or 1 (one allocated bit in the x2APIC ID); software should plan accordingly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Platform          |
| EAX[31:5]  | Reserved          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                   |
| EBX[15:0]  | NEXT_LEVEL_NUM_LP | The number of logical processors across all instances of this domain within the next higher-scoped domain. (For example, in a processor socket/package comprising “M” cores of “N” logical processors each, the “core” domain sub-leaf value of this field would be M*N.) This number reflects configuration as shipped by Intel. This field may also contain asymmetric values across different logical processors, as an example of a mix of cores that support more than one logical processor with cores that support only one logical processor.<br>Note, software must not use this field to enumerate processor topology.<br>Software must not use the value of EBX[15:0] to enumerate processor topology of the system. The value is only intended for display and diagnostic purposes. The actual number of logical processors available to BIOS/OS/Applications may be different from the value of EBX[15:0], depending on software and platform hardware configurations. | Logical Processor |
| EBX[31:16] | Reserved          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |                   |
| ECX[7:0]   | LEVEL_NUM         | The input ECX sub-leaf index.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Platform          |

|            |             |                                                                                                                                                                                                                                                                       |                   |
|------------|-------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| ECX[15:8]  | DOMAIN_TYPE | This field provides an identification value which indicates the domain shown in the table. Although domains are ordered, their assigned identification values are not and software should not depend on it. Note that enumeration values of 0 and 3-255 are reserved. | Platform          |
| ECX[31:16] | Reserved    | Reserved.                                                                                                                                                                                                                                                             |                   |
| EDX[31:0]  | X2APIC_ID   | The X2APIC ID of this logical processor.                                                                                                                                                                                                                              | Logical Processor |

The sub-leaves of CPUID.0BH describe an ordered hierarchy of logical processors starting from the smallest-scoped domain of a Logical Processor (sub-leaf index 0) to the Core domain (sub-leaf index 1) to the largest-scoped domain (the last valid sub-leaf index) that is implicitly subordinate to the unenumerated highest-scoped domain of the processor package (socket). The details of each valid domain is enumerated by a corresponding sub-leaf. Details for a domain include its type and how all instances of that domain determine the number of logical processors and x2 APIC ID partitioning at the next higher-scoped domain. The ordering of domains within the hierarchy is fixed architecturally as shown below. For a given processor, not all domains may be relevant or enumerated; however, the logical processor and core domains are always enumerated. For two valid sub-leaves N and N+1, sub-leaf N+1 represents the next immediate higher-scoped domain with respect to the domain of sub-leaf N for the given processor. If sub-leaf index “N” returns an invalid domain type in ECX[15:08] (00H), then all sub-leaves with an index greater than “N” also return an invalid domain type. A sub-leaf returning an invalid domain always returns 0 in EAX and EBX.

Table 21-32. Hierarchy of Valid Domain Enumerations in CPUID.0BH:ECX[15:8]

| Hierarchy | Domain            | Domain Type ID Value |
|-----------|-------------------|----------------------|
| Invalid   | Invalid           | 0                    |
| Lowest    | Logical Processor | 1                    |
| ...       | Core              | 2                    |
| Highest   | Package/Socket    | (Implied)            |
| Reserved  | Reserved          | 3-255                |

## CPUID.0CH -- Reserved

Table 21-33. Leaf 0CH Reserved

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.0DH -- Processor Extended State

CPUID.0DH returns a bit-vector representation of all processor state extensions that are supported in the processor and storage size requirements of the XSAVE/XRSTOR area.

- This leaf is valid if CPUID.01H:ECX.XSAVE[26] = 1 and MAX\_LEAF ≥ 0DH.
- Sub-leaves 0 and 1 are always valid; consult them to determine which other sub-leaves are present as described in “CPUID.0DH.n, n>01H—State Sub-Leaves”.

## CPUID.0DH.00H -- Processor Extended State Main Sub-Leaf

CPUID.0DH.00H returns the processor extended state information.

**Table 21-34. Leaf 0DH.00H Processor Extended State**

| Register   | Field Name                     | Description                                                                                                                                                                                                | Domain            |
|------------|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[0]     | X87                            | x87 state.                                                                                                                                                                                                 | Platform          |
| EAX[1]     | SSE                            | SSE state.                                                                                                                                                                                                 | Platform          |
| EAX[2]     | AVX                            | AVX state.                                                                                                                                                                                                 | Platform          |
| EAX[3]     | MPX_BNDREGS                    | MPX state.                                                                                                                                                                                                 | Platform          |
| EAX[4]     | MPX_BNDCSR                     | MPX state.                                                                                                                                                                                                 | Platform          |
| EAX[5]     | AVX512_OPMASK                  | AVX-512 Opmask state.                                                                                                                                                                                      | Platform          |
| EAX[6]     | AVX512_ZMM_HI256               | AVX-512 ZMM upper 256 data state.                                                                                                                                                                          | Platform          |
| EAX[7]     | AVX512_HI16_ZMM                | AVX-512 upper 16 ZMM registers state.                                                                                                                                                                      | Platform          |
| EAX[8]     | N/A                            | Always returns 0 (Allocated for IA32_XSS).                                                                                                                                                                 | Platform          |
| EAX[9]     | PKRU                           | PKRU state.                                                                                                                                                                                                | Platform          |
| EAX[16:10] | N/A                            | Always returns 0 (Allocated for IA32_XSS).                                                                                                                                                                 | Platform          |
| EAX[17]    | AMX_TILECFG                    | TILECFG state.                                                                                                                                                                                             | Platform          |
| EAX[18]    | AMX_TILEDATA                   | TILEDATA state.                                                                                                                                                                                            | Platform          |
| EAX[31:19] | Reserved                       | Reserved.                                                                                                                                                                                                  |                   |
| EBX[31:0]  | XSAVE_BYTES_ENABLED_FEATURES   | Maximum size (bytes, from the beginning of the XSAVE/XRSTOR save area) required by enabled features in XCRO. May be different than ECX if some features at the end of the XSAVE save area are not enabled. | Logical Processor |
| ECX[31:0]  | XSAVE_BYTES_SUPPORTED_FEATURES | Maximum size (bytes, from the beginning of the XSAVE/XRSTOR save area) of the XSAVE/XRSTOR save area required by all supported features in the processors, i.e. all the valid bit fields in XCRO.          | Platform          |
| EDX[31:0]  | VALID_XCRO_UPPER_32            | Reports the supported bits of the upper 32 bits of XCRO. XCRO[n+32] can be set to 1 only if EDX[n] is 1.                                                                                                   | Platform          |

The EAX register of CPUID.0DH.00H reports the supported bits of the lower 32 bits of XCRO. XCRO[n] can be set to 1 only if EAX[n] is 1. The details are described in Chapter 13.2, “Enumeration of CPUID Support for XSAVE Instructions and XSAVE-Supported Features,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1.

## CPUID.0DH.01H -- Feature and Supervisor State Sub-Leaf

CPUID.0DH.01H returns feature and supervisor state information.

**Table 21-35. Leaf 0DH.01H Processor Extended State**

| Register   | Field Name                    | Description                                                                                                                                                                                                                                                                                            | Domain            |
|------------|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[0]     | XSAVEOPT                      | If 1, supports XSAVEOPT.                                                                                                                                                                                                                                                                               | Platform          |
| EAX[1]     | XSAVEC                        | If 1, supports XSAVEC and the compacted form of XRSTOR.                                                                                                                                                                                                                                                | Platform          |
| EAX[2]     | XGETBV1                       | If 1, supports XGETBV with ECX = 1.                                                                                                                                                                                                                                                                    | Platform          |
| EAX[3]     | XSAVES                        | If 1, supports XSAVES/XRSTORS and IA32_XSS.                                                                                                                                                                                                                                                            | Platform          |
| EAX[4]     | XFD                           | If 1, supports extended feature disable (XFD).                                                                                                                                                                                                                                                         | Platform          |
| EAX[31:5]  | Reserved                      | Reserved.                                                                                                                                                                                                                                                                                              |                   |
| EBX[31:0]  | XSAVES_BYTES_ENABLED_FEATURES | The size in bytes of the XSAVE area containing all states enabled by XCRO   IA32_XSS. If EAX[3] is enumerated as 0 and EAX[1] is enumerated as 1, EBX enumerates the size of the XSAVE area containing all states enabled by XCRO. If EAX[1] and EAX[3] are both enumerated as 0, EBX enumerates zero. | Logical Processor |
| ECX[7:0]   | N/A                           | Always returns 0 (Allocated for XCRO).                                                                                                                                                                                                                                                                 | Platform          |
| ECX[8]     | PT                            | PT state.                                                                                                                                                                                                                                                                                              | Platform          |
| ECX[9]     | Reserved                      | Always returns 0 (Allocated for XCRO).                                                                                                                                                                                                                                                                 |                   |
| ECX[10]    | PASID                         | PASID state.                                                                                                                                                                                                                                                                                           | Platform          |
| ECX[11]    | CET_U                         | CET user state.                                                                                                                                                                                                                                                                                        | Platform          |
| ECX[12]    | CET_S                         | CET supervisor state.                                                                                                                                                                                                                                                                                  | Platform          |
| ECX[13]    | HDC                           | HDC state.                                                                                                                                                                                                                                                                                             | Platform          |
| ECX[14]    | UINTR                         | UINTR state.                                                                                                                                                                                                                                                                                           | Platform          |
| ECX[15]    | LBR                           | LBR state (only for the architectural LBR feature).                                                                                                                                                                                                                                                    | Platform          |
| ECX[16]    | HWP                           | HWP state.                                                                                                                                                                                                                                                                                             | Platform          |
| ECX[18:17] | N/A                           | Always returns 0 (Allocated for XCRO).                                                                                                                                                                                                                                                                 | Platform          |
| ECX[31:19] | Reserved                      | Reserved.                                                                                                                                                                                                                                                                                              |                   |
| EDX[31:0]  | Reserved                      | Reserved                                                                                                                                                                                                                                                                                               |                   |

### NOTE

ECX reports the supported bits of the lower 32 bits of the IA32\_XSS MSR. IA32\_XSS[n] can be set to 1 only if ECX[n] is 1. EDX reports the supported bits of the upper 32 bits of the IA32\_XSS MSR. IA32\_XSS[n+32] can be set to 1 only if EDX[n] is 1. The details are described in Chapter 13.2, "Enumeration of CPUID Support for XSAVE Instructions and XSAVE-Supported Features," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 1.

## CPUID.0DH.SUB-LEAVES -- Sub-leaves

CPUID.0DH.n, where  $n > 1$ , returns information about the size and offset of each processor extended state save area within the XSAVE/XRSTOR area. Software can use the forward-extendable technique depicted below to query in bulk the valid sub-leaves and obtain size and offset information for each processor extended state save area that is supported:

```

//* For each supported feature indicated by sub-leaf 0 and 1, read the size and offset sub-leaf */
For j= 2 to 62
    If (CPUID.0DH.00H:<EDX:EAX>[j] == 1 or // Use 64-bit value of EDX:EAX
        CPUID.0DH.01H:<EDX:ECX>[j] == 1) // Use 64-bit value of EDX:ECX
        Read(CPUID.0DH.j) // Examine the size and offset.
    END IF
END FOR

```

Table 21-36. Leaf 0DH.SUB-LEAVES Processor Extended State

| Register  | Field Name       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Domain   |
|-----------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | COMP_SIZE        | The size in bytes (from the offset specified in EBX) of the save area for an extended state feature associated with a valid sub-leaf index n.                                                                                                                                                                                                                                                                                                                                                                                  | Platform |
| EBX[31:0] | COMP_OFFSET      | The offset in bytes of this extended state component's save area from the beginning of the XSAVE/XRSTOR area. This field reports 0 if the sub-leaf index, n, does not map to a valid bit in the XCRO register.<br>If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf n ( $0 \le n \le 31$ ) is invalid if sub-leaf 0 returns 0 in EAX[n] and sub-leaf 1 returns 0 in ECX[n]. Sub-leaf n ( $32 \le n \le 63$ ) is invalid if sub-leaf 0 returns 0 in EDX[n-32] and sub-leaf 1 returns 0 in EDX[n-32] | Platform |
| ECX[0]    | COMP_SUP         | This bit is set if the bit n (corresponding to the sub-leaf index) is supported in the IA32_XSS MSR; it is clear if bit n is instead supported in XCRO.                                                                                                                                                                                                                                                                                                                                                                        | Platform |
| ECX[1]    | COMP_64B_ALIGNED | This bit is set if, when the compacted format of an XSAVE area is used, this extended state component located on the next 64-byte boundary following the preceding state component (otherwise, it is located immediately following the preceding state component)                                                                                                                                                                                                                                                              | Platform |
| ECX[2]    | COMP_XFD         | This bit is set to indicate support for XFD faulting.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | Platform |
| ECX[31:3] | Reserved         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |          |
| EDX[31:0] | Reserved         | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |          |

## CPUID.0EH -- Reserved

This leaf is reserved.

**Table 21-37. Leaf 0EH Reserved**

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.0FH -- Intel® Resource Director Technology (Intel® RDT) Monitoring

CPUID.0FH returns information for the Intel Resource Director Technology Monitoring capabilities. As described below, software uses the bit vector returned in EDX by sub-leaf 00H to determine the available resource types (ResID) that can be monitored. This information is necessary for software to program the IA32\_PQR\_ASSOC and IA32\_QM\_EVTSEL MSRs such that Quality-of-Service data can be read afterwards from the IA32\_QM\_CTR MSR.

- This leaf is valid if CPUID.07H.00H:EBX.RDT\_M[12] = 1 and MAX\_LEAF ≥ 0FH.
- If the leaf is valid, sub-leaf 00H is always valid. Sub-leaf n (n ≥ 1) is only valid when (CPUID.0FH.00H:EDX[n] == 1).

### CPUID.0FH.00H -- Intel® RDT Monitoring Main Sub-Leaf

CPUID.0FH.00H returns information about Intel RDT Monitoring.

**Table 21-38. Leaf 0FH.00H Intel® Resource Director Technology (Intel® RDT) Monitoring**

| Register  | Field Name | Description                                                                                                                   | Domain   |
|-----------|------------|-------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | Reserved   | Reserved.                                                                                                                     |          |
| EBX[31:0] | MAX_RMID   | Maximum range (zero-based) of RMID within this physical processor of all types.                                               | Platform |
| ECX[31:0] | Reserved   | Reserved.                                                                                                                     |          |
| EDX[0]    | Reserved   | Reserved.                                                                                                                     |          |
| EDX[1]    | L3_MON     | If 1, supports L3 Cache Intel RDT Monitoring. Sub-leaf index 0 reports valid resource type starting at bit position 1 of EDX. | Platform |
| EDX[31:2] | Reserved   | Reserved.                                                                                                                     |          |

CPUID.0FH.00H returns information about the bit-vector representation of QoS monitoring resource types that are supported in the processor and maximum range of RMID values the processor can use to monitor of any supported resource types. Each bit, starting from bit 1, corresponds to a specific resource type if the bit is set. The bit position corresponds to the sub-leaf index (or ResID) that software must use to query QoS monitoring capability available for that type.

### CPUID.0FH.01H -- L3 Cache Intel® Resource Director Technology Monitoring

CPUID.0FH.01H returns information about L3 Cache Intel RDT monitoring.

**Table 21-39. Leaf 0FH.01H Intel® Resource Director Technology (Intel® RDT) Monitoring**

| Register | Field Name | Description                                                                                                                                                                                              | Domain   |
|----------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[7:0] | CTR_WIDTH  | The counter width is encoded as an offset from 24b. A value of zero in this field indicates that 24-bit counters are supported. A value of 8 in this field indicates that 32-bit counters are supported. | Platform |
| EAX[8]   | RDT_M_OVF  | If 1, supports an overflow bit in the IA32_QM_CTR MSR (bit 61).                                                                                                                                          | Platform |
| EAX[9]   | IO_RDT_CMT | If 1, indicates the presence of non-CPU agent supporting Intel RDT CMT.                                                                                                                                  | Platform |
| EAX[10]  | IO_RDT_MBM | If 1, indicates the presence of non-CPU agent supporting Intel RDT MBM support.                                                                                                                          | Platform |

|            |              |                                                                                                                                           |          |
|------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:11] | Reserved     | Reserved.                                                                                                                                 |          |
| EBX[31:0]  | CONV_FACTOR  | Factor used to convert from reported IA32_QM_CTR value to derived occupancy metric (bytes) and Memory Bandwidth Monitoring (MBM) metrics. | Platform |
| ECX[31:0]  | MAX_RMID_L3  | Maximum range (zero-based) of RMID of this resource type.                                                                                 | Platform |
| EDX[0]     | CMT_L3_OCCUP | If 1, supports L3 occupancy monitoring.                                                                                                   | Platform |
| EDX[1]     | MBM_L3_TOTAL | If 1, supports L3 total bandwidth monitoring.                                                                                             | Platform |
| EDX[2]     | MBM_L3_LOCAL | If 1, supports L3 local bandwidth monitoring.                                                                                             | Platform |
| EDX[31:3]  | Reserved     | Reserved.                                                                                                                                 |          |

## CPUID.10H -- Intel® Resource Director Technology (Intel® RDT) Allocation

CPUID.10H returns information for Intel Resource Director Technology Allocation. This leaf is valid when CPUID.07H.00H:EBX.RDT\_A[15] = 1. As described below, software uses the bit vector returned in EBX by subleaf 00H to determine the available QoS Enforcement (allocation) resource types that are supported in the processor. This information is necessary for software to configure each class of services using capability bit masks in the QoS Mask registers, IA32\_resourceType\_Mask\_n.

- This leaf is valid if CPUID.07H.00H:EBX.RDT\_A[15] = 1 and MAX\_LEAF ≥ 10H.
- If the leaf is valid, sub-leaf 00H is always valid. Sub-leaf n (n ≥ 1) is only valid when (CPUID.10H.00H:EBX[n] == 1).

### CPUID.10H.00H -- Intel® RDT Allocation Main Sub-Leaf

CPUID.10H.00H returns information about Intel RDT Allocation.

**Table 21-40. Leaf 10H.00H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register  | Field Name        | Description                                                                                                                                      | Domain   |
|-----------|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | Reserved          | Reserved.                                                                                                                                        |          |
| EBX[0]    | Reserved          | Reserved.                                                                                                                                        |          |
| EBX[1]    | CAT_L3            | If 1, supports L3 Cache Allocation Technology. Sub-leaf index 0 reports valid resource identification (ResID) starting at bit position 1 of EBX. | Platform |
| EBX[2]    | CAT_L2            | If 1, supports L2 Cache Allocation Technology.                                                                                                   | Platform |
| EBX[3]    | MBA               | If 1, supports Memory Bandwidth Allocation.                                                                                                      | Platform |
| EBX[4]    | Reserved          | Reserved.                                                                                                                                        |          |
| EBX[5]    | CBA               | If 1, supports Cache Bandwidth Allocation.                                                                                                       | Platform |
| EBX[6]    | RESOURCE_PRIORITY | If 1, supports Resource Priority.                                                                                                                | Platform |
| EBX[31:7] | Reserved          | Reserved.                                                                                                                                        |          |
| ECX[31:0] | Reserved          | Reserved.                                                                                                                                        |          |
| EDX[31:0] | Reserved          | Reserved.                                                                                                                                        |          |

CPUID.10H.00H returns information about the bit-vector representation of QoS Enforcement resource types that are supported in the processor. Each bit, starting from bit 1, corresponds to a specific resource type if the bit is set. The bit position corresponds to the sub-leaf index (or ResID) that software must use to query QoS enforcement capability available for that type.

### CPUID.10H.01H -- L3 Cache Allocation Technology

CPUID.10H.ResID=1 returns information about L3 Cache Allocation Technology.

**Table 21-41. Leaf 10H.01H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register  | Field Name            | Description                                                                                                 | Domain   |
|-----------|-----------------------|-------------------------------------------------------------------------------------------------------------|----------|
| EAX[4:0]  | CAT_L3_BITMASK_LENGTH | Length of the capacity bit mask for the corresponding ResID. Add one to the return value to get the result. | Platform |
| EAX[31:5] | Reserved              | Reserved.                                                                                                   |          |
| EBX[31:0] | CAT_L3_CONTENTION     | Bit-granular map of isolation/contention of allocation units.                                               | Platform |

|            |                  |                                                                                                                                              |          |
|------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------|
| ECX[0]     | Reserved         | Reserved.                                                                                                                                    |          |
| ECX[1]     | CAT_L3_NONCPU    | If 1, supports L3 CAT for non-CPU agents.                                                                                                    | Platform |
| ECX[2]     | CAT_L3_CDP       | If 1, supports L3 Code and Data Prioritization Technology.                                                                                   | Platform |
| ECX[3]     | CAT_L3_NONCONTIG | If 1, supports non-contiguous capacity bitmasks. The bits that are set in the various IA32_L3_MASK_n registers do not have to be contiguous. | Platform |
| ECX[31:4]  | Reserved         | Reserved.                                                                                                                                    |          |
| EDX[15:0]  | CAT_L3_MAX_CLOS  | Highest Class of Service (COS) number supported for this ResID.                                                                              | Platform |
| EDX[31:16] | Reserved         | Reserved.                                                                                                                                    |          |

## CPUID.10H.02H -- L2 Cache Allocation Technology

CPUID.10H.ResID=2 returns information about L2 Cache Allocation Technology.

**Table 21-42. Leaf 10H.02H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register   | Field Name            | Description                                                                                                                                  | Domain   |
|------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[4:0]   | CAT_L2_BITMASK_LENGTH | Length of the capacity bit mask for the corresponding ResID.<br>Add one to the return value to get the result.                               | Platform |
| EAX[31:5]  | Reserved              | Reserved.                                                                                                                                    |          |
| EBX[31:0]  | CAT_L2_CONTENTION     | Bit-granular map of isolation/contention of allocation units.                                                                                | Platform |
| ECX[1:0]   | Reserved              | Reserved.                                                                                                                                    |          |
| ECX[2]     | CAT_L2_CDP            | If 1, supports L2 Code and Data Prioritization Technology.                                                                                   | Platform |
| ECX[3]     | CAT_L2_NONCONTIG      | If 1, supports non-contiguous capacity bitmasks. The bits that are set in the various IA32_L2_MASK_n registers do not have to be contiguous. | Platform |
| ECX[31:4]  | Reserved              | Reserved.                                                                                                                                    |          |
| EDX[15:0]  | CAT_L2_MAX_CLOS       | Highest Class of Service (COS) number supported for this ResID.                                                                              | Platform |
| EDX[31:16] | Reserved              | Reserved.                                                                                                                                    |          |

## CPUID.10H.03H -- Memory Bandwidth Allocation

CPUID.10H.ResID=3 returns information about Memory Bandwidth Allocation.

**Table 21-43. Leaf 10H.03H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register   | Field Name | Description                                                                                                                       | Domain   |
|------------|------------|-----------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[11:0]  | MBA_MAX    | Reports the maximum MBA throttling value supported for the corresponding ResID.<br>Add one to the return value to get the result. | Platform |
| EAX[31:12] | Reserved   | Reserved.                                                                                                                         |          |

|            |                |                                                                 |          |
|------------|----------------|-----------------------------------------------------------------|----------|
| EBX[31:0]  | Reserved       | Reserved.                                                       |          |
| ECX[0]     | PER_THREAD_MBA | Per-thread MBA controls are supported.                          | Platform |
| ECX[1]     | Reserved       | Reserved.                                                       |          |
| ECX[2]     | MBA_LINEAR     | If 1, the response of the delay values is linear.               | Platform |
| ECX[31:3]  | Reserved       | Reserved.                                                       |          |
| EDX[15:0]  | MBA_MAX_CLOS   | Highest Class of Service (COS) number supported for this ResID. | Platform |
| EDX[31:16] | Reserved       | Reserved.                                                       |          |

## CPUID.10H.05H -- Cache Bandwidth Allocation

**Table 21-44. Leaf 10H.05H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register   | Field Name     | Description                                                                                                                                                    | Domain   |
|------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[7:0]   | CBA_MAX_LEVELS | Reports the maximum core throttling level supported for the corresponding ResID. Add one to the return value to get the number of throttling levels supported. | Platform |
| EAX[11:8]  | BW_SCOPE       | If 1, indicates the logical processor scope of the IA32_QoS_Core_BW_Thrtl_n MSRs. Other values are reserved.                                                   | Platform |
| EAX[31:12] | Reserved       | Reserved.                                                                                                                                                      |          |
| EBX[31:0]  | Reserved       | Reserved.                                                                                                                                                      |          |
| ECX[2:0]   | Reserved       | Reserved.                                                                                                                                                      |          |
| ECX[3]     | CBA_LINEAR     | If 1, the response of the bandwidth control is approximately linear. If 0, the response of the bandwidth control is non-linear.                                | Platform |
| ECX[31:4]  | Reserved       | Reserved.                                                                                                                                                      |          |
| EDX[15:0]  | CBA_MAX_CLOS   | Highest Class of Service (COS) number supported for this ResID.                                                                                                | Platform |
| EDX[31:16] | Reserved       | Reserved.                                                                                                                                                      |          |

## CPUID.10H.06H -- Resource Priority Control

**Table 21-45. Leaf 10H.06H Intel® Resource Director Technology (Intel® RDT) Allocation**

| Register  | Field Name     | Description                                                                                        | Domain   |
|-----------|----------------|----------------------------------------------------------------------------------------------------|----------|
| EAX[0]    | THREAD_ENABLE  | If 1, supports per-thread enable of RP through the IA32_RESOURCE_PRIORITY MSR.                     | Platform |
| EAX[1]    | PACKAGE_ENABLE | If 1, supports physical processor package enable of RP through the IA32_RESOURCE_PRIORITY_PKG MSR. | Platform |
| EAX[31:2] | Reserved       | Reserved.                                                                                          |          |
| EBX[31:0] | Reserved       | Reserved.                                                                                          |          |
| ECX[31:0] | Reserved       | Reserved.                                                                                          |          |
| EDX[31:0] | Reserved       | Reserved.                                                                                          |          |

## CPUID.11H -- Reserved

This leaf is reserved.

**Table 21-46. Leaf 11H Reserved**

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.12H -- Intel® Software Guard Extensions (Intel® SGX) Capability

CPUID.12H returns information about Intel® SGX capabilities. More details can be found in Chapter 35, “Introduction to Intel® Software Guard Extensions,” and Chapter 36, “Enclave Access Control and Data Structures,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3D.

- This leaf is valid when CPUID.07H.00H:EBX.SGX[2] = 1 and MAX\_LEAF ≥ 12H.
- If the leaf is valid, sub-leaf 00H and 01H are always valid. Sub-leaf n (n ≥ 2) is only valid when CPUID.12H.n:EAX[3:0] != 0.

### CPUID.12H.00H -- Intel® SGX Main Sub-Leaf

CPUID.12H.00H returns information about Intel® SGX capabilities. It is only valid when CPUID.07H.00H:EBX.SGX = 1.

**Table 21-47. Leaf 12H.00H Intel® Software Guard Extensions (Intel® SGX) Capability**

| Register   | Field Name              | Description                                                                                                                                                                                                           | Domain   |
|------------|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[0]     | SGX1                    | If 1, supports the collection of SGX1 Leaf functions.                                                                                                                                                                 | Platform |
| EAX[1]     | SGX2                    | If 1, supports the collection of SGX2 Leaf functions.                                                                                                                                                                 | Platform |
| EAX[6:2]   | Reserved                | Reserved.                                                                                                                                                                                                             |          |
| EAX[7]     | EVERIFYREPORT2          | If 1, supports the ENCLU instruction Leaf EVERIFYREPORT2.                                                                                                                                                             | Platform |
| EAX[9:8]   | Reserved                | Reserved.                                                                                                                                                                                                             |          |
| EAX[10]    | EUPDATESVN              | If 1, supports the ENCLS instruction Leaf EUPDATESVN.                                                                                                                                                                 | Platform |
| EAX[11]    | EDECCSSA                | If 1, supports the ENCLU instruction Leaf EDECCSSA.                                                                                                                                                                   | Platform |
| EAX[31:12] | Reserved                | Reserved.                                                                                                                                                                                                             |          |
| EBX[31:0]  | MISCSELECT              | Bit vector of supported extended SGX features. The definition of MISCSELECT can be found in Section 36.7.2, “SECS.MISCSELECT Field,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3D. | Platform |
| ECX[31:0]  | Reserved                | Reserved.                                                                                                                                                                                                             |          |
| EDX[7:0]   | MAX_ENCLAVE_SIZE_NOT_64 | The maximum supported enclave size in non-64-bit mode is 2 <sup>^(EDX[7:0])</sup> .                                                                                                                                   | Platform |
| EDX[15:8]  | MAX_ENCLAVE_SIZE_64     | The maximum supported enclave size in 64-bit mode is 2 <sup>^(EDX[15:8])</sup> .                                                                                                                                      | Platform |
| EDX[31:16] | Reserved                | Reserved.                                                                                                                                                                                                             |          |

### CPUID.12H.01H -- Intel® SGX Attributes

CPUID.12H.01H returns information about Intel® SGX Attributes. It is only valid when CPUID.07H.00H:EBX.SGX = 1.

**Table 21-48. Leaf 12H.01H Intel® Software Guard Extensions (Intel® SGX) Capability**

| Register | Field Name | Description | Domain |
|----------|------------|-------------|--------|
|----------|------------|-------------|--------|

|           |                                |                                                                                       |          |
|-----------|--------------------------------|---------------------------------------------------------------------------------------|----------|
| EAX[31:0] | ECREATE_SECS_ATTRIBUTES_31_0   | Reports the valid bits of SECS.ATTRIBUTES[31:0] that software can set with ECREATE.   | Platform |
| EBX[31:0] | ECREATE_SECS_ATTRIBUTES_63_32  | Reports the valid bits of SECS.ATTRIBUTES[63:32] that software can set with ECREATE.  | Platform |
| ECX[31:0] | ECREATE_SECS_ATTRIBUTES_95_64  | Reports the valid bits of SECS.ATTRIBUTES[95:64] that software can set with ECREATE.  | Platform |
| EDX[31:0] | ECREATE_SECS_ATTRIBUTES_127_96 | Reports the valid bits of SECS.ATTRIBUTES[127:96] that software can set with ECREATE. | Platform |

The definition of the attributes can be found in Section 36.7.1, "ATTRIBUTES," of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3D

### CPUID.12H -- $n \geq 2$ - Intel® SGX Enclave Page Cache

CPUID.12H with  $ECX \geq 2$  returns information about Intel® SGX Enclave Page Cache and is supported if CPUID.07H.00H:EBX.SGX = 1.

For sub-leaves where  $ECX \geq 2$ , the definition of EAX[31:4], EBX, ECX, and EDX depends on the sub-leaf type listed below.

#### Sub-Leaf Encoding Type EAX[3:0] = 0000b (Invalid)

This sub-leaf is invalid. EDX:ECX:EBX:EAX return 0.

### CPUID.12H -- Sub-Leaf Encoding Type EAX[3:0] = 0001b

This sub-leaf enumerates an EPC section with EDX:ECX, EBX:EAX defined as follows.

**Table 21-49. Leaf 12H.SUB-LEAF ENCODING TYPE EAX[3:0] = 0001B Intel® Software Guard Extensions (Intel® SGX) Capability**

| Register   | Field Name             | Description                                                        | Domain   |
|------------|------------------------|--------------------------------------------------------------------|----------|
| EAX[3:0]   | SUB_LEAF_TYPE          | Value is 0001b.                                                    | Platform |
| EAX[11:4]  | Reserved               | Reserved.                                                          |          |
| EAX[31:12] | EPC_SECTION_ADDR_31_12 | Bits 31:12 of the physical address of the base of the EPC section. | Platform |
| EBX[19:0]  | EPC_SECTION_ADDR_51_32 | Bits 51:32 of the physical address of the base of the EPC section. | Platform |
| EBX[31:20] | Reserved               | Reserved.                                                          |          |

|            |                        |                                                                                                                                                                                                                                                                                                                                                                   |          |
|------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| ECX[3:0]   | EPC_SECTION_PROPERTY   | EPC Section Property Encoding Definitions, as follows:<br>0000b – All bits in EDX:ECX are enumerated as 0.<br>0001b – This section has confidentiality, integrity, and replay protection.<br>0010b – This section has confidentiality protection only.<br>0011b – This section has confidentiality and integrity protection.<br>All other encodings are reserved. | Platform |
| ECX[11:4]  | Reserved               | Reserved.                                                                                                                                                                                                                                                                                                                                                         |          |
| ECX[31:12] | EPC_SECTION_SIZE_31_12 | Bits 31:12 of the size of the corresponding EPC section within the Processor Reserved Memory.                                                                                                                                                                                                                                                                     | Platform |
| EDX[19:0]  | EPC_SECTION_SIZE_51_32 | Bits 51:32 of the size of the corresponding EPC section within the Processor Reserved Memory.                                                                                                                                                                                                                                                                     | Platform |
| EDX[31:20] | Reserved               | Reserved.                                                                                                                                                                                                                                                                                                                                                         |          |

CPUID.13H -- Reserved

This leaf is reserved.

Table 21-50. Leaf 13H Reserved

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.14H -- Intel® Processor Trace (Intel® PT)

CPUID.14H returns information about Intel® Processor Trace (PT).

CPUID.14H.00H returns information about Intel Processor Trace extensions.

CPUID.14H.n (n > 0 and less than the number of non-zero bits in CPUID.14H.00H:EAX) returns information about packet generation in Intel Processor Trace.

For more details on Intel PT, see Chapter 34, “Intel® Processor Trace,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3D.

- This leaf is valid when CPUID.07H.00H:EBX.INTEL\_PROC\_TRACE[25] = 1 and MAX\_LEAF ≥ 14H.
- The maximum sub-leaf value for ECX is specified in CPUID.14H.00H:EAX[31:0] MAX\_SUBLEAF.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

## CPUID.14H.00H -- Intel® PT Main Sub-Leaf

CPUID.14H.00H returns information about Intel Processor Trace extensions.

**Table 21-51. Leaf 14H.00H Intel® Processor Trace (Intel® PT)**

| Register  | Field Name    | Description                                                                                                                                                                                                                                                                                                                                 | Domain   |
|-----------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | MAX_SUBLEAF   | Reports the maximum sub-leaf supported in leaf 14H.                                                                                                                                                                                                                                                                                         | Platform |
| EBX[0]    | CR3_FILTER    | If 1, supports that IA32_RTIT_CTL.CR3Filter can be set to 1, and that IA32_RTIT_CR3_MATCH MSR can be accessed.                                                                                                                                                                                                                              | Platform |
| EBX[1]    | CYC_ACC       | If 1, supports Configurable PSB and Cycle-Accurate Mode.                                                                                                                                                                                                                                                                                    | Platform |
| EBX[2]    | IP_FILTER     | If 1, supports IP Filtering, TraceStop filtering, and preservation of Intel PT MSRs across warm reset.                                                                                                                                                                                                                                      | Platform |
| EBX[3]    | MTC           | If 1, supports MTC timing packet and suppression of COFI-based packets.                                                                                                                                                                                                                                                                     | Platform |
| EBX[4]    | PTWRITE       | If 1, supports PTWRITE. Writes can set IA32_RTIT_CTL[12] (PTWEn) and IA32_RTIT_CTL[5] (FUPonPTW), and PTWRITE can generate packets.                                                                                                                                                                                                         | Platform |
| EBX[5]    | PWR_EVT_TRACE | If 1, supports Power Event Trace. Writes can set IA32_RTIT_CTL[4] (PwrEvtEn), enabling Power Event Trace packet generation.                                                                                                                                                                                                                 | Platform |
| EBX[6]    | PMI_PRESERVE  | If 1, supports the PSB and PMI preservation. Writes can set IA32_RTIT_CTL[56] (InjectPsbPmiOnEn-able), enabling the processor to set IA32_RTIT_STATUS[7] (PendToPaPMI) and/or IA32_RTIT_STATUS[6] (PendPSB) in order to preserve ToPA PMIs and/or PSBs otherwise lost due to Intel PT disable. Writes can also set PendToPAPMI and PendPSB. | Platform |
| EBX[7]    | EVENT_TRACE   | If 1, supports that writes can set IA32_RTIT_CTL[31] (EventEn), enabling Event Trace packet generation.                                                                                                                                                                                                                                     | Platform |
| EBX[8]    | TNT_DIS       | If 1, supports that writes can set IA32_RTIT_CTL[55] (DisTNT), disabling TNT packet generation.                                                                                                                                                                                                                                             | Platform |

|            |                           |                                                                                                                                                                                                                                                                                                    |                   |
|------------|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EBX[9]     | PTTT                      | If 1, Processor Trace Trigger Tracing (PTTT) is supported.                                                                                                                                                                                                                                         | Platform          |
| EBX[31:10] | Reserved                  | Reserved.                                                                                                                                                                                                                                                                                          |                   |
| ECX[0]     | TOPAOUT                   | If 1, supports that tracing can be enabled with IA32_RTIT_CTL.ToPA = 1, hence utilizing the ToPA output scheme; IA32_RTIT_OUTPUT_BASE and IA32_RTIT_OUTPUT_MASK_PTRS MSRs can be accessed.                                                                                                         | Platform          |
| ECX[1]     | MENTRY                    | If 1, supports that ToPA tables can hold any number of output entries, up to the maximum allowed by the MaskOrTableOffset field of IA32_RTIT_OUTPUT_MASK_PTRS.                                                                                                                                     | Platform          |
| ECX[2]     | SNGL_RNG_OUT              | If 1, supports the Single-Range Output scheme.                                                                                                                                                                                                                                                     | Platform          |
| ECX[3]     | TRACE_TRANSPORT_SUBSYSTEM | If 1, supports the output to Trace Transport subsystem.                                                                                                                                                                                                                                            | Platform          |
| ECX[30:4]  | Reserved                  | Reserved.                                                                                                                                                                                                                                                                                          |                   |
| ECX[31]    | LIP                       | If 1, the generated packets which contain IP payloads contain LIP. If 0, the generated packets which contain IP payloads contain Effective IP. Trace segments using a flat memory model will generate the same information regardless of how a logical processor reports this value since LIP=EIP. | Logical Processor |
| EDX[31:0]  | Reserved                  | Reserved.                                                                                                                                                                                                                                                                                          |                   |

## CPUID.14H.01H -- Feature Information Sub-Leaf

CPUID.14H.01H returns information about packet generation in Intel Processor Trace.

**Table 21-52. Leaf 14H.01H Intel® Processor Trace (Intel® PT)**

| Register   | Field Name      | Description                                                                               | Domain   |
|------------|-----------------|-------------------------------------------------------------------------------------------|----------|
| EAX[2:0]   | RANGECNT        | Number of configurable Address Ranges for filtering.                                      | Platform |
| EAX[7:3]   | Reserved        | Reserved.                                                                                 |          |
| EAX[10:8]  | TRIGGER_CFG_CNT | Number of IA32_RTIT_TRIGGERx_CFG MSRs. The number of triggers supported is 4x this value. | Platform |
| EAX[15:11] | Reserved        | Reserved.                                                                                 |          |
| EAX[31:16] | MTC_RATE        | Bitmap of supported MTC period encodings.                                                 | Platform |
| EBX[15:0]  | CYC_THRESHOLDS  | Bitmap of supported Cycle Threshold value encodings.                                      | Platform |
| EBX[31:16] | PSB_RATE        | Bitmap of supported Configurable PSB frequency encodings.                                 | Platform |
| ECX[0]     | ICNT            | If 1, the trigger action EN_ICNT is supported.                                            | Platform |
| ECX[1]     | TRIGGER_PAUSE   | If 1, the trigger actions TRACE_PAUSE and TRACE_RESUME are supported.                     | Platform |
| ECX[14:2]  | Reserved        | Reserved.                                                                                 |          |

PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

|            |                  |                                            |          |
|------------|------------------|--------------------------------------------|----------|
| ECX[15]    | TRIGGER_DR_MATCH | If 1, trigger input DR match is supported. | Platform |
| ECX[31:16] | Reserved         | Reserved.                                  |          |
| EDX[31:0]  | Reserved         | Reserved.                                  |          |

## CPUID.15H -- Time Stamp Counter and Nominal Core Crystal Clock

CPUID.15H returns information about the Time Stamp Counter and the Nominal Core Crystal Clock.

- This leaf is valid if MAX\_LEAF  $\geq$  15H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-53. Leaf 15H Time Stamp Counter and Nominal Core Crystal Clock**

| Register  | Field Name            | Description                                                                                                                                                                                                                                                  | Domain   |
|-----------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | DENOMINATOR           | An unsigned integer which is the denominator of the TSC/"core crystal clock" ratio.                                                                                                                                                                          | Platform |
| EBX[31:0] | NUMERATOR             | An unsigned integer which is the numerator of the TSC/"core crystal clock" ratio. If 0, the TSC/"core crystal clock" ratio is not enumerated.                                                                                                                | Platform |
| ECX[31:0] | NOMINAL_ART_FREQUENCY | An unsigned integer which is the nominal frequency of the core crystal clock in Hz. If 0, the nominal core crystal clock frequency is not enumerated. Note, the core crystal clock may differ from the reference clock, bus clock or core clock frequencies. | Platform |
| EDX[31:0] | Reserved              | Reserved.                                                                                                                                                                                                                                                    |          |

Dividing EBX[31:0] by EAX[31:0] provides the ratio of the TSC frequency to the core crystal clock frequency. The Timestamp Counter frequency is computed by multiplying that ratio by ECX[31:0], such as  $TSC\_frequency = ECX * EBX/EAX$ .

### CPUID.16H -- Processor Frequency Information

CPUID.16H returns information about processor frequency information. Data is returned from this interface in accordance with the processor's specification and does not reflect actual values. Suitable use of this data includes the display of processor information in like manner to the processor brand string and for determining the appropriate range to use when displaying processor information e.g. frequency history graphs. The returned information should not be used for any other purpose as the returned information does not accurately correlate to information / counters returned by other processor interfaces. While a processor may support the Processor Frequency Information leaf, fields that return a value of zero are not supported.

- This leaf is valid if MAX\_LEAF ≥ 16H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-54. Leaf 16H Processor Frequency Information

| Register   | Field Name               | Description                         | Domain            |
|------------|--------------------------|-------------------------------------|-------------------|
| EAX[15:0]  | PROCESSOR_BASE_FREQUENCY | Processor Base Frequency (in MHz).  | Logical Processor |
| EAX[31:16] | Reserved                 | Reserved.                           |                   |
| EBX[15:0]  | MAXIMUM_FREQUENCY        | Maximum Frequency (in MHz).         | Logical Processor |
| EBX[31:16] | Reserved                 | Reserved.                           |                   |
| ECX[15:0]  | BUS_FREQUENCY            | Bus (Reference) Frequency (in MHz). | Logical Processor |
| ECX[31:16] | Reserved                 | Reserved.                           |                   |
| EDX[31:0]  | Reserved                 | Reserved.                           |                   |

## CPUID.17H -- System-on-Chip Vendor Attribute

CPUID.17H returns System-on-Chip vendor attribute information.

- This leaf is valid if CPUID.17H.00H:EAX[31:0] (MaxSOCID\_Index)  $\geq 3$  and MAX\_LEAF  $\geq 17$ H.
- The maximum sub-leaf value for ECX is specified in CPUID.17H.00H:EAX[31:0] MaxSOCID\_Index.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

### CPUID.17H.00H -- Main Sub-Leaf

CPUID.17H.00H returns System-on-Chip vendor attribute information.

**Table 21-55. Leaf 17H.00H System-on-Chip Vendor Attribute**

| Register   | Field Name       | Description                                                                                                                                     | Domain   |
|------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0]  | MAX_SOCID_INDEX  | Reports the maximum input value of supported Sub-leaf in Leaf 17H.                                                                              | Platform |
| EBX[15:0]  | SOC_VENDOR_ID    | SOC Vendor ID.                                                                                                                                  | Platform |
| EBX[16]    | IS_VENDOR_SCHEME | If 1, the SOC Vendor ID field is assigned via an industry standard enumeration scheme. Otherwise, the SOC Vendor ID field is assigned by Intel. | Platform |
| EBX[31:17] | Reserved         | Reserved.                                                                                                                                       |          |
| ECX[31:0]  | PROJECT_ID       | A unique number an SOC vendor assigns to its SOC projects.                                                                                      | Platform |
| EDX[31:0]  | STEPPING_ID      | A unique number within an SOC project that an SOC vendor assigns.                                                                               | Package  |

### CPUID.17H.01H -- Vendor Brand String Sub-Leaf (Bytes 0 to 15)

CPUID.17H with ECX=1, 2, or 3 returns information for System-on-Chip vendor branding string.

SOC Vendor Brand String is a UTF-8 encoded string padded with trailing bytes of 00H. The complete SOC Vendor Brand String is constructed by concatenating in ascending order the output of each sub-leaf 1 to 3. For the output of each sub-leaf, byte are ordered in ascending order of EAX:EBX:ECX:EDX.

Leaf 17H sub-leaves 4 and above are reserved.

**Table 21-56. Leaf 17H.01H System-on-Chip Vendor Attribute**

| Register  | Field Name                         | Description                                    | Domain   |
|-----------|------------------------------------|------------------------------------------------|----------|
| EAX[31:0] | VENDOR_BRAND_STRING_BYTES_0_to_3   | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EBX[31:0] | VENDOR_BRAND_STRING_BYTES_4_to_7   | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| ECX[31:0] | VENDOR_BRAND_STRING_BYTES_8_to_11  | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EDX[31:0] | VENDOR_BRAND_STRING_BYTES_12_to_15 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |

### CPUID.17H.02H -- Vendor Brand String Sub-Leaf (Bytes 16 to 31)

**Table 21-57. Leaf 17H.02H System-on-Chip Vendor Attribute**

| Register  | Field Name                         | Description                                    | Domain   |
|-----------|------------------------------------|------------------------------------------------|----------|
| EAX[31:0] | VENDOR_BRAND_STRING_BYTES_16_to_19 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EBX[31:0] | VENDOR_BRAND_STRING_BYTES_20_to_23 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |

|           |                                    |                                                |          |
|-----------|------------------------------------|------------------------------------------------|----------|
| ECX[31:0] | VENDOR_BRAND_STRING_BYTES_24_to_27 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EDX[31:0] | VENDOR_BRAND_STRING_BYTES_28_to_31 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |

CPUID.17H.03H -- Vendor Brand String Sub-Leaf (Bytes 32 to 47)

Table 21-58. Leaf 17H.03H System-on-Chip Vendor Attribute

| Register  | Field Name                         | Description                                    | Domain   |
|-----------|------------------------------------|------------------------------------------------|----------|
| EAX[31:0] | VENDOR_BRAND_STRING_BYTES_32_to_35 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EBX[31:0] | VENDOR_BRAND_STRING_BYTES_36_to_39 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| ECX[31:0] | VENDOR_BRAND_STRING_BYTES_40_to_43 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |
| EDX[31:0] | VENDOR_BRAND_STRING_BYTES_44_to_47 | SOC Vendor Brand String. UTF-8 encoded string. | Platform |

CPUID.17H.M>MAXSOCID\_INDEX—RESERVED SUB-LEAVES -- m>MaxSOCID\_Index—Reserved Sub-Leaves

CPUID.17H with ECX > MaxSOCID\_Index is reserved and returns all zeroes.

Table 21-59. Leaf 17H.M>MAXSOCID\_INDEX—RESERVED SUB-LEAVES System-on-Chip Vendor Attribute

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved    |        |
| EBX[31:0] | Reserved   | Reserved    |        |
| ECX[31:0] | Reserved   | Reserved    |        |
| EDX[31:0] | Reserved   | Reserved    |        |

## CPUID.18H -- Deterministic Address Translation Parameters

CPUID.18H returns information about the Deterministic Address Translation Parameters. Each sub-leaf enumerates a different address translation structure.

- This leaf is valid if CPUID.18H.00H:EAX[31:0]  $\neq$  0 and MAX\_LEAF  $\geq$  18H.
- The maximum sub-leaf value for ECX is specified in CPUID.18H.00H:EAX[31:0] MAX\_SUBLEAF.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX. A sub-leaf index is also invalid if EDX[4:0] returns 0.
- Valid sub-leaves do not need to be contiguous or in any particular order. A valid sub-leaf may be in a higher input ECX value than an invalid sub-leaf or than a valid sub-leaf of a higher or lower-level structure.

### CPUID.18H.00H -- Main Sub-Leaf

Deterministic Address Translation Parameters Main Leaf

**Table 21-60. Leaf 18H.00H Deterministic Address Translation Parameters**

| Register  | Field Name  | Description                                                        | Domain            |
|-----------|-------------|--------------------------------------------------------------------|-------------------|
| EAX[31:0] | MAX_SUBLEAF | Reports the maximum input value of supported sub-leaf in leaf 18H. | Logical Processor |
| EBX[31:0] | Reserved    | Reserved.                                                          |                   |
| ECX[31:0] | Reserved    | Reserved.                                                          |                   |
| EDX[4:0]  | TYPE        | Will always return 0.                                              | Logical Processor |
| EDX[31:5] | Reserved    | Reserved.                                                          |                   |

### CPUID.18H.ECX $\geq$ 1 -- Sub-Leaves

CPUID.18H with ECX  $\geq$  1 returns Deterministic Address Translation Parameters information.

**Table 21-61. Leaf 18H.ECX  $\geq$  1 Deterministic Address Translation Parameters**

| Register   | Field Name   | Description                                                                               | Domain            |
|------------|--------------|-------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0]  | Reserved     | Reserved.                                                                                 |                   |
| EBX[0]     | 4KB_ENTRIES  | If 1, supports 4K page size entries in this structure.                                    | Logical Processor |
| EBX[1]     | 2MB_ENTRIES  | If 1, supports 2MB page size entries in this structure.                                   | Logical Processor |
| EBX[2]     | 4MB_ENTRIES  | If 1, supports 4MB page size entries in this structure.                                   | Logical Processor |
| EBX[3]     | 1GB_ENTRIES  | If 1, supports 1 GB page size entries in this structure.                                  | Logical Processor |
| EBX[7:4]   | Reserved     | Reserved.                                                                                 |                   |
| EBX[10:8]  | PARTITIONING | Partitioning (0:Soft partitioning between the logical processors sharing this structure). | Logical Processor |
| EBX[15:11] | Reserved     | Reserved.                                                                                 |                   |
| EBX[31:16] | NUM_WAYS     | W = ways of associativity.                                                                | Logical Processor |
| ECX[31:0]  | NUM_SETS     | S = number of sets.                                                                       | Logical Processor |

|            |                        |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |                   |
|------------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EDX[4:0]   | TYPE                   | 00000b: Null (indicates this Sub-leaf is not valid).<br>00001b: Data TLB.<br>00010b: Instruction TLB.<br>00011b: Unified TLB.1<br>00100b: Load Only TLB. Hit on loads; fills on both loads and stores.<br>00101b: Store Only TLB. Hit on stores; fill on stores.<br>All other encodings are reserved.<br>Some unified TLBs will allow a single TLB entry to satisfy data read/write and instruction fetches. Others will require separate entries (e.g., one loaded on data read/write and another loaded on an instruction fetch). See the Intel® 64 and IA-32 Architectures Optimization Reference Manual for details of a particular product. | Logical Processor |
| EDX[7:5]   | LEVEL_NUM              | Translation cache level (starts at 1).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Logical Processor |
| EDX[8]     | FULLY_ASSOC            | Fully associative structure.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Logical Processor |
| EDX[13:9]  | Reserved               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| EDX[25:14] | MAX_LP_ADDRESSABLE_IDS | Maximum number of addressable IDs for logical processors sharing this translation cache.<br>Add one to the return value to get the result.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Logical Processor |
| EDX[31:26] | Reserved               | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |

## CPUID.19H -- Key Locker

CPUID.19H returns Key Locker information.

- This leaf is valid if CPUID.07H.00H:ECX.KEY\_LOCKER[23] = 1 and MAX\_LEAF ≥ 19H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-62. Leaf 19H Key Locker**

| Register  | Field Name          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Domain            |
|-----------|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[0]    | CPLD_RESTRICT       | If 1, supports the Key Locker restriction of CPLD-only. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Platform          |
| EAX[1]    | NO_ENCRYPT_RESTRICT | If 1, supports the Key Locker restriction of no-encrypt. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Platform          |
| EAX[2]    | NO_DECRYPT_RESTRICT | If 1, supports the Key Locker restriction of no-decrypt. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Platform          |
| EAX[31:3] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| EBX[0]    | AESKLE              | If 1, the AES Key Locker instructions are fully enabled. CPUID.19H:EBX.AESKLE[0] is enumerated as 1 if the AES Key Locker instructions have been activated by system firmware and CR4.KL[bit 19] = 1. Software can check this bit after setting CR4.KL to determine whether AES Key Locker instructions have been enabled. Note that some processors may allow enabling of those instructions without activation by system firmware. Some processors may not support the use of AES Key Locker instructions in system-management-mode (SMM). Those processors enumerate CPUID.19H:EBX.AESKLE[0] as 0 in SMM regardless of the setting of CR4.KL. | Logical Processor |
| EBX[1]    | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| EBX[2]    | AES_WIDE            | If 1, supports the AES wide Key Locker instructions. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Platform          |
| EBX[3]    | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| EBX[4]    | IWKEYBACKUP         | If 1, supports the Key Locker MSRs (IA32_COPY_LOCAL_TO_PLATFORM, IA23_COPY_PLATFORM_TO_LOCAL, IA32_COPY_STATUS, and IA32_IWKEYBACKUP_STATUS) and backing up the internal wrapping key. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                              | Platform          |
| EBX[31:5] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| ECX[0]    | NOBACKUP            | If 1, supports the NoBackup parameter to LOADIWKEY. <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Platform          |
| ECX[1]    | RAND_IWKEY          | If 1, supports KeySource encoding of 1 (randomization of the internal wrapping key). <sup>1</sup>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Platform          |
| ECX[31:2] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |
| EDX[31:0] | Reserved            | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |                   |

### NOTE

1. This field is valid only if CPUID.19H:EBX.AESKLE[0] = 1.

CPUID.1AH -- Native Model ID Enumeration

CPUID.1AH returns Native Model ID information. This leaf exists on all logical processors in a hybrid package, it may also be present in other processor configurations.

- This leaf is valid if CPUID.1AH.00H:EAX[31:0] <> 0 and MAX\_LEAF ≥ 1AH.
- The only valid sub-leaf is 0 and ECX must be set to 0.

Table 21-63. Leaf 1AH Native Model ID Enumeration

| Register   | Field Name           | Description                                                                                                                                                                                                                                                                                                                                                                       | Domain            |
|------------|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[23:0]  | CORE_NATIVE_MODEL_ID | The core-type and native model ID can be used to uniquely identify the microarchitecture of the core. This native model ID is not unique across core types, and not related to the model ID reported in CPUID.01H, and does not identify the SOC.                                                                                                                                 | Logical Processor |
| EAX[31:24] | CORE_TYPE            | 10H: Reserved<br>20H: Intel® Atom®<br>30H: Reserved<br>40H: Intel® Core<br>The core type may only be used as an identification of the microarchitecture for this logical processor and its numeric value has no significance, neither large nor small. This field neither implies nor expresses any other attribute to this logical processor and software should not assume any. | Logical Processor |
| EBX[31:0]  | Reserved             | Reserved.                                                                                                                                                                                                                                                                                                                                                                         |                   |
| ECX[31:0]  | Reserved             | Reserved.                                                                                                                                                                                                                                                                                                                                                                         |                   |
| EDX[31:0]  | Reserved             | Reserved.                                                                                                                                                                                                                                                                                                                                                                         |                   |

## CPUID.1BH -- PCONFIG Information

### CPUID.1BH -- Output Registers Format for All Sub-Leaves

CPUID.1BH returns information for PCONFIG capabilities. This information is enumerated in sub-leaves selected by the value of ECX (starting with 0).

- This leaf is valid if CPUID.07H.00H:EDX.PCONFIG[18] = 1 and MAX\_LEAF  $\geq$  1BH.
- Sub-leaves are enumerated until sub-leaf n, where EAX[11:0] returns 0.

**Table 21-64. Leaf 1BH PCONFIG Information**

| Register   | Field Name    | Description | Domain   |
|------------|---------------|-------------|----------|
| EAX[11:0]  | SUB_LEAF_TYPE | 0 (Invalid) | Platform |
| EAX[31:12] | Reserved      | Reserved.   |          |
| EBX[31:0]  | Reserved      | Reserved.   |          |
| ECX[31:0]  | Reserved      | Reserved.   |          |
| EDX[31:0]  | Reserved      | Reserved.   |          |

Each sub-leaf of CPUID.1BH enumerates its sub-leaf type in EAX. If a sub-leaf type is 0, the sub-leaf is invalid and zero is returned in EBX, ECX, and EDX. In this case, all subsequent sub-leaves (selected by larger input values of ECX) are also invalid.

The only valid sub-leaf type currently defined is 1, indicating that the sub-leaf enumerates target identifiers for the PCONFIG instruction. Any non-zero value returned in EBX, ECX, or EDX indicates a valid target identifier of the PCONFIG instruction (any value of zero should be ignored). The only target identifier currently defined is 1, indicating TME-MK. See the “PCONFIG—Platform Configuration” instruction in Chapter 4 of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 2B, for more information.

### CPUID.1BH.OUTPUT REGISTERS FOR SUB-LEAF TYPE TARGET IDENTIFIER (1) -- Output Registers for Sub-Leaf Type Target Identifier (1)

**Table 21-65. Leaf 1BH.OUTPUT REGISTERS FOR SUB-LEAF TYPE TARGET IDENTIFIER (1) PCONFIG Information**

| Register   | Field Name          | Description           | Domain   |
|------------|---------------------|-----------------------|----------|
| EAX[11:0]  | SUB_LEAF_TYPE       | 1 (Target Identifier) | Platform |
| EAX[31:12] | Reserved            | Reserved.             |          |
| EBX[31:0]  | TARGET_IDENTIFIER_1 | Target identifier     | Platform |
| ECX[31:0]  | TARGET_IDENTIFIER_2 | Target identifier     | Platform |
| EDX[31:0]  | TARGET_IDENTIFIER_3 | Target identifier     | Platform |

The only current valid target identifier is 1 for MK-TME.

## CPUID.1CH -- Last Branch Records (LBR) Information

CPUID.1CH returns information about architectural Last Branch Records (LBR). For details on LBR, see Chapter 20, “Last Branch Records,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3B.

- This leaf is valid if CPUID.07H.00H:EDX.ARCH\_LBRS[19] = 1 and MAX\_LEAF ≥ 1CH.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-66. Leaf 1CH Last Branch Records (LBR) Information**

| Register   | Field Name                  | Description                                                                                                                                                                                                                        | Domain            |
|------------|-----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[7:0]   | LBR_DEPTH_VALUES            | For each bit n set in this field, the IA32_LBR_DEPTH.DEPTH value $8*(n+1)$ is supported.                                                                                                                                           | Platform          |
| EAX[29:8]  | Reserved                    | Reserved.                                                                                                                                                                                                                          |                   |
| EAX[30]    | DEEP_C_STATE_RESET          | If 1, supports that LBRs may be cleared on an MWAIT that requests a C-state numerically greater than C1.                                                                                                                           | Platform          |
| EAX[31]    | IP_VALUES_CONTAIN_LIP       | If 1, the LBR IP values contain LIP. If 0, IP values contain Effective IP.<br>Trace segments using a flat memory model will generate the same information regardless of how a logical processor reports this value since LIP = EIP | Logical Processor |
| EBX[0]     | CPL_FILTERING               | If 1, supports setting IA32_LBR_CTL[2:1] to a non-zero value.                                                                                                                                                                      | Platform          |
| EBX[1]     | BRANCH_FILTERING            | If 1, supports setting IA32_LBR_CTL[22:16] to a non-zero value.                                                                                                                                                                    | Platform          |
| EBX[2]     | CALL_STACK_MODE             | If 1, supports setting IA32_LBR_CTL[3] to 1.                                                                                                                                                                                       | Platform          |
| EBX[31:3]  | Reserved                    | Reserved.                                                                                                                                                                                                                          |                   |
| ECX[0]     | MISPREDICT_BIT              | If 1, IA32_LBR_x_INFO[63] holds indication of branch misprediction (MISPRED).                                                                                                                                                      | Platform          |
| ECX[1]     | TIMED_LBRS                  | If 1, IA32_LBR_x_INFO[15:0] holds CPU cycles since last LBR entry (CYC_CNT), and IA32_LBR_x_INFO[60] holds an indication of whether the value held there is valid (CYC_CNT_VALID).                                                 | Platform          |
| ECX[2]     | BRANCH_TYPE_FIELD_SUPPORTED | If 1, IA32_LBR_INFO_x[59:56] holds indication of the recorded operation’s branch type (BR_TYPE).                                                                                                                                   | Platform          |
| ECX[15:3]  | Reserved                    | Reserved.                                                                                                                                                                                                                          |                   |
| ECX[19:16] | EVENT_LOGGING_BITMAP        | The event logging bitmap, wherein each set bit corresponds to a programmable performance monitoring counter that supports LBR event logging.                                                                                       | Platform          |
| ECX[31:20] | Reserved                    | Reserved.                                                                                                                                                                                                                          |                   |
| EDX[31:0]  | Reserved                    | Reserved.                                                                                                                                                                                                                          |                   |

## CPUID.1DH -- Tile Information

CPUID.1DH returns information about tile architecture and tile palette 1 (see Chapter 19, “Programming with Intel® Advanced Matrix Extensions,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1).

- This leaf is valid if CPUID.07H.00H:EDX.AMX\_TILE[24] = 1 and MAX\_LEAF ≥ 1DH.
- The maximum sub-leaf value for ECX is specified in CPUID.1DH.00H:EAX[31:0] max\_palette.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

## CPUID.1DH.00H -- Tile Information Main Sub-Leaf

CPUID.1DH.00H returns the tile architecture information.

**Table 21-67. Leaf 1DH.00H Tile Information**

| Register  | Field Name  | Description                                   | Domain   |
|-----------|-------------|-----------------------------------------------|----------|
| EAX[31:0] | MAX_PALETTE | Highest numbered palette sub-leaf. Value = 1. | Platform |
| EBX[31:0] | Reserved    | Reserved.                                     |          |
| ECX[31:0] | Reserved    | Reserved.                                     |          |
| EDX[31:0] | Reserved    | Reserved.                                     |          |

## CPUID.1DH.01H -- Tile Palette 1

CPUID.1DH.01H returns tile palette information.

**Table 21-68. Leaf 1DH.01H Tile Information**

| Register   | Field Name       | Description                                                | Domain   |
|------------|------------------|------------------------------------------------------------|----------|
| EAX[15:0]  | TOTAL_TILE_BYTES | Palette 1 total_tile_bytes. Value = 8192.                  | Platform |
| EAX[31:16] | BYTES_PER_TILE   | Palette 1 bytes_per_tile. Value = 1024.                    | Platform |
| EBX[15:0]  | BYTES_PER_ROW    | Palette 1 bytes_per_row. Value = 64.                       | Platform |
| EBX[31:16] | MAX_NAMES        | Palette 1 max_names (number of tile registers). Value = 8. | Platform |
| ECX[15:0]  | MAX_ROWS         | Palette 1 max_rows. Value = 16.                            | Platform |
| ECX[31:16] | Reserved         | Reserved.                                                  |          |
| EDX[31:0]  | Reserved         | Reserved.                                                  |          |

CPUID.1EH -- TMUL Information

CPUID.1EH returns information about TMUL capabilities (see Chapter 19, “Programming with Intel® Advanced Matrix Extensions,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 1).

- This leaf is valid if CPUID.07H.00H:EDX.AMX\_TILE[24] = 1 and MAX\_LEAF ≥ 1EH.
- The only valid sub-leaf is 0 and ECX must be set to 0.

CPUID.1EH.00H -- TMUL Information Main Leaf

TMUL Main Leaf Information

Table 21-69. Leaf 1EH.00H TMUL Information

| Register   | Field Name | Description                              | Domain   |
|------------|------------|------------------------------------------|----------|
| EAX[31:0]  | Reserved   | Reserved.                                |          |
| EBX[7:0]   | TMUL_MAXK  | tmul_maxk (rows or columns). Value = 16. | Platform |
| EBX[23:8]  | TMUL_MAXN  | tmul_maxn (column bytes). Value = 64.    | Platform |
| EBX[31:24] | Reserved   | Reserved.                                |          |
| ECX[31:0]  | Reserved   | Reserved.                                |          |
| EDX[31:0]  | Reserved   | Reserved.                                |          |

## CPUID.1FH -- V2 Extended Topology

CPUID.1FH returns information about V2 Extended Topology.

CPUID.1FH is a preferred superset to leaf 0BH. Intel recommends using leaf 1FH when available rather than leaf 0BH and ensuring that any leaf 0BH algorithms are updated to support leaf 1FH.

- This leaf is valid if CPUID.1FH.00H:EBX[15:0]  $\neq$  0 and MAX\_LEAF  $\geq$  1FH.
  - When the leaf is invalid, CPUID.1FH.00H:ECX.DOMAIN\_TYPE[15:8] will report the Domain Type ID as Invalid (0).
- The sub-leaves are enumerated until sub-leaf n returns 0 in EBX[15:0].
- If ECX contains an invalid sub-leaf index, EAX/EBX return 0. Sub-leaf index n+1 is invalid if sub-leaf n returns EBX[15:0] as 0.

## CPUID.1FH -- ECX $\geq$ 0

Table 21-70. Leaf 1FH V2 Extended Topology

| Register   | Field Name        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Domain            |
|------------|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[4:0]   | SHIFT_COUNT       | The number of bits that the x2APIC ID must be shifted to the right to address instances of the next higher-scoped domain. When logical processor is not supported by the processor, the value of this field at the Logical Processor domain sub-leaf may be returned as either 0 (no allocated bits in the x2APIC ID) or 1 (one allocated bit in the x2APIC ID); software should plan accordingly.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Platform          |
| EAX[31:5]  | Reserved          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                   |
| EBX[15:0]  | NEXT_LEVEL_NUM_LP | The number of logical processors across all instances of this domain within the next higher-scoped domain relative to this current logical processor. (For example, in a processor socket/package comprising “M” dies of “N” cores each, where each core has “L” logical processors, the “die” domain sub-leaf value of this field would be M*N*L. In an asymmetric topology this would be the summation of the value across the lower domain level instances to create each upper domain level instance.) This number reflects configuration as shipped by Intel. Note that the number of logical processors can be asymmetric in which case “L” may be different on different logical processors, as an example a core with 2 logical processors on the same platform as a core with 1 logical processor.<br>Note, software must not use this field to enumerate processor topology.<br>Software must not use the value of EBX[15:0] to enumerate processor topology of the system. The value is only intended for display and diagnostic purposes. The actual number of logical processors available to BIOS/OS/Applications may be different from the value of EBX[15:0], depending on software and platform hardware configurations. | Logical Processor |
| EBX[31:16] | Reserved          | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                   |

|            |             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                   |
|------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| ECX[7:0]   | LEVEL_NUM   | The input ECX sub-leaf index.                                                                                                                                                                                                                                                                                                                                                                                                                                     | Platform          |
| ECX[15:8]  | DOMAIN_TYPE | This field provides an identification value which indicates the domain as shown in the table. Although domains are ordered, their assigned identification values are not and software should not depend on it. (For example, if a new domain between core and module is specified, it will have an identification value higher than 5.) See the table below for the current list of valid enumerations. Note that enumeration values of 0 and 7-255 are reserved. | Platform          |
| ECX[31:16] | Reserved    | Reserved.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |                   |
| EDX[31:0]  | X2APIC_ID   | The x2APIC ID of the current logical processor is always valid and does not vary with the sub-leaf index in ECX.                                                                                                                                                                                                                                                                                                                                                  | Logical Processor |

The sub-leaves of CPUID.1FH describe an ordered hierarchy of logical processors starting from the smallest scoped domain of a Logical Processor (sub-leaf index 0) to the Core domain (sub-leaf index 1) to the largest scoped domain (the last valid sub-leaf index) that is implicitly subordinate to the unenumerated highest-scoped domain of the processor package (socket).

The details of each valid domain is enumerated by a corresponding sub-leaf. Details for a domain include its type and how all instances of that domain determine the number of logical processors and x2 APIC ID partitioning at the next higher-scoped domain. The ordering of domains within the hierarchy is fixed architecturally as shown below. For a given processor, not all domains may be relevant or enumerated; however, the logical processor and core domains are always enumerated. As an example, a processor may report an ordered hierarchy consisting only of "Logical Processor," "Core," and "Die."

For two valid sub-leaves N and N+1, sub-leaf N+1 represents the next immediate higher-scoped domain with respect to the domain of sub-leaf N for the given processor.

If sub-leaf index "N" returns an invalid domain type in ECX[15:08] (00H), then all sub-leaves with an index greater than "N" also return an invalid domain type. A sub-leaf returning an invalid domain always returns 0 in EAX and EBX.

Table 21-71. Hierarchy of Valid Domain Enumerations in CPUID.1FH:ECX[15:8]

| Hierarchy | Domain            | Domain Type ID Value |
|-----------|-------------------|----------------------|
| Invalid   | Invalid           | 0                    |
| Lowest    | Logical Processor | 1                    |
| ...       | Core              | 2                    |
| ...       | Module            | 3                    |
| ...       | Tile              | 4                    |
| ...       | Die               | 5                    |
| ...       | DieGrp            | 6                    |
| Highest   | Package/Socket    | (Implied)            |
| Reserved  | Reserved          | 7-255                |

## CPUID.20H -- Processor History Reset Information

CPUID.20H returns information about processor history reset when CPUID.07H.01H:EAX.HRESET[22] = 1.

- This leaf is valid if CPUID.07H.01H:EAX.HRESET[22] = 1 and MAX\_LEAF  $\geq$  20H.
- The maximum sub-leaf value for ECX is specified in CPUID.20H.00H:EAX[31:0] MAX\_SUBLEAF.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

## CPUID.20H.00H -- Processor History Reset Sub-leaf

**Table 21-72. Leaf 20H.00H Processor History Reset Information**

| Register  | Field Name             | Description                                                                                                                                      | Domain   |
|-----------|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0] | MAX_SUBLEAF            | Reports the maximum number of sub-leaves that are supported in leaf 20H.                                                                         | Platform |
| EBX[0]    | THREAD_DIRECTOR_HRESET | Indicates support for both HRESET's EAX[0] parameter, and IA32_HRESET_ENABLE[0] set by the OS to enable reset of Intel® Thread Director history. | Platform |
| EBX[31:1] | Reserved               | Reserved.                                                                                                                                        |          |
| ECX[31:0] | Reserved               | Reserved.                                                                                                                                        |          |
| EDX[31:0] | Reserved               | Reserved.                                                                                                                                        |          |

## **CPUID.21H -- Unimplemented**

Does not return feature information for the processor. Allocated for use by TDX modules; see Intel® Trust Domain Extensions (Intel® TDX) Module Base Architecture Specification. Software emulating CPUID should not change the information returned for this leaf.

## CPUID.22H -- Reserved

This leaf is reserved.

Table 21-73. Leaf 22H Reserved

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.23H -- Architectural Performance Monitoring Extended

CPUID.23H returns architectural performance monitoring extended information.

- This leaf is valid if CPUID.07H.01H:EAX.ARCH\_PERFMON\_EXT[8] = 1 and MAX\_LEAF ≥ 23H.
- The sub-leaves of this leaf are enumerated by a bitmask specified in CPUID.23H.00H:EAX[31:0] SUBLEAF\_MASK. The bit numbers of set bits in the bitmask represent valid sub-leaf indexes.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index is invalid if the index as a bit number is clear in the Available Sub-Leaf Mask or is greater than 31.

### CPUID.23H.00H -- Main Sub-Leaf

**Table 21-74. Leaf 23H.00H Architectural Performance Monitoring Extended**

| Register  | Field Name    | Description                                                                                                                                                                                                                                                                                                                                                                             | Domain            |
|-----------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0] | SUBLEAF_MASK  | If bit n is set, sub-leaf n is supported. (For unsupported sub-leaves, 0 is returned in the registers EAX, EBX, ECX, and EDX.)                                                                                                                                                                                                                                                          | Logical Processor |
| EBX[0]    | UNITMASK2     | If 1, supports the UnitMask2 field in the IA32_PERFEVTSELx MSRs.                                                                                                                                                                                                                                                                                                                        | Logical Processor |
| EBX[1]    | EQ            | If 1, supports the equal flag in the IA32_PERFEVTSELx MSRS.                                                                                                                                                                                                                                                                                                                             | Logical Processor |
| EBX[31:2] | Reserved      | Reserved.                                                                                                                                                                                                                                                                                                                                                                               |                   |
| ECX[7:0]  | SLOTS_PER_CYC | If this field is non-zero, it represents the number of Top-down Microarchitecture Analysis (TMA) slots per cycle. This number can be multiplied by the number of cycles (from CPU_CLK_UNHALTED.THREAD / CPU_CLK_UNHALTED.CORE or IA32_FIXED_CTR1) to determine the total number of slots. If this field is zero, IA32_FIXED_CTR3 should be used to determine the total number of slots. | Logical Processor |
| ECX[31:8] | Reserved      | Reserved.                                                                                                                                                                                                                                                                                                                                                                               |                   |
| EDX[31:0] | Reserved      | Reserved.                                                                                                                                                                                                                                                                                                                                                                               |                   |

### CPUID.23H.01H -- Counter Information Sub-Leaf

**Table 21-75. Leaf 23H.01H Architectural Performance Monitoring Extended**

| Register  | Field Name     | Description                                                                                                                                                              | Domain            |
|-----------|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0] | GP_COUNTERS    | For each bit n set in this field, the processor supports general-purpose performance monitoring counter n.                                                               | Logical Processor |
| EBX[31:0] | FIXED_COUNTERS | For each bit m set in this field, the processor supports fixed-function performance monitoring counter m.<br>The valid range of fixed-function counters is 0 through 15. | Logical Processor |
| ECX[31:0] | Reserved       | Reserved.                                                                                                                                                                |                   |
| EDX[31:0] | Reserved       | Reserved.                                                                                                                                                                |                   |

## CPUID.23H.02H -- Bitmap of Auto Counter Reload Sub-Leaf

**Table 21-76. Leaf 23H.02H Architectural Performance Monitoring Extended**

| Register  | Field Name        | Description                                                                                                                                                                                                                                        | Domain            |
|-----------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0] | ACR_GP_RELOAD     | General counters that can be reloaded. For each bit n set in this field, the processor supports ACR for general-purpose performance monitoring counter n.                                                                                          | Logical Processor |
| EBX[31:0] | ACR_FIXED_RELOAD  | Fixed counters that can be reloaded. For each bit m set in this field, the processor supports ACR for fixed-function performance monitoring counter m.                                                                                             | Logical Processor |
| ECX[31:0] | ACR_GP_TRIGGER    | General counters that can cause reloads. For each bit y set in this field, the processor allows general-purpose performance monitoring counter y to reload all existing general-purpose performance monitoring counters capable of being reloaded. | Logical Processor |
| EDX[31:0] | ACR_FIXED_TRIGGER | Fixed counters that can cause reloads. For each bit x set in this field, the processor allows fixed-function performance monitoring counter x to reload all existing fixed-function performance monitoring counters capable of being reloaded.     | Logical Processor |

## CPUID.23H.03H -- Architectural Performance Monitoring Events Bitmap Sub-Leaf

For each bit n set in this field, the processor supports Architectural Performance Monitoring Event of index n.

**Table 21-77. Leaf 23H.03H Architectural Performance Monitoring Extended**

| Register | Field Name     | Description                           | Domain            |
|----------|----------------|---------------------------------------|-------------------|
| EAX[0]   | CORE_CYC       | If 1, supports architectural index 0. | Logical Processor |
| EAX[1]   | INSTR_RET      | If 1, supports architectural index 1. | Logical Processor |
| EAX[2]   | REF_CYC        | If 1, supports architectural index 2. | Logical Processor |
| EAX[3]   | LLC_REF        | If 1, supports architectural index 3. | Logical Processor |
| EAX[4]   | LLC_MISSES     | If 1, supports architectural index 4. | Logical Processor |
| EAX[5]   | BR_INSTR_RET   | If 1, supports architectural index 5  | Logical Processor |
| EAX[6]   | BR_MISPRED_RET | If 1, supports architectural index 6  | Logical Processor |
| EAX[7]   | SLOTS          | If 1, supports architectural index 7  | Logical Processor |
| EAX[8]   | BACKEND        | If 1, supports architectural index 8  | Logical Processor |
| EAX[9]   | BADSPEC        | If 1, supports architectural index 9  | Logical Processor |

|            |             |                                       |                   |
|------------|-------------|---------------------------------------|-------------------|
| EAX[10]    | FRONTEND    | If 1, supports architectural index 10 | Logical Processor |
| EAX[11]    | RETIRING    | If 1, supports architectural index 11 | Logical Processor |
| EAX[12]    | LBR_INSERTS | If 1, supports architectural index 12 | Logical Processor |
| EAX[31:13] | Reserved    | Reserved.                             |                   |
| EBX[31:0]  | Reserved    | Reserved.                             |                   |
| ECX[31:0]  | Reserved    | Reserved.                             |                   |
| EDX[31:0]  | Reserved    | Reserved.                             |                   |

## CPUID.23H.04H -- PEBS Capabilities

**Table 21-78. Leaf 23H.04H Architectural Performance Monitoring Extended**

| Register   | Field Name      | Description                                                                                                                | Domain            |
|------------|-----------------|----------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0]  | Reserved        | Reserved.                                                                                                                  |                   |
| EBX[2:0]   | Reserved        | Reserved.                                                                                                                  |                   |
| EBX[3]     | ALLOW_IN_RECORD | If 1, indicates that the ALLOW_IN_RECORD bit is available in the IA32_PMC_GpN_CFG_C and IA32_PMC_Fxm_CFG_C MSRs.           | Logical Processor |
| EBX[4]     | CNTR_GP         | If 1, indicates that counters group sub-group general-purpose counters is available.                                       | Logical Processor |
| EBX[5]     | CNTR_FIXED      | If 1, indicates that counters group sub-group fixed-function counters is available.                                        | Logical Processor |
| EBX[6]     | CNTR_METRICS    | If 1, indicates that counters group sub-group performance metrics is available.                                            | Logical Processor |
| EBX[7]     | Reserved        | Reserved.                                                                                                                  |                   |
| EBX[9:8]   | LBR             | LBR group and both bits [41:40] are available.                                                                             | Logical Processor |
| EBX[15:10] | Reserved        | Reserved.                                                                                                                  |                   |
| EBX[23:16] | XER             | XER group bits [50:49] and bits [55:53] are available. See Section 11.4.4, "XSAVEEnabled Registers Group," for XER fields. | Logical Processor |
| EBX[28:24] | Reserved        | Reserved.                                                                                                                  |                   |
| EBX[29]    | GPR             | If 1, the GPR group is available.                                                                                          | Logical Processor |
| EBX[30]    | AUX             | If 1, the AUX group is available.                                                                                          | Logical Processor |
| EBX[31]    | Reserved        | Reserved.                                                                                                                  |                   |
| ECX[31:0]  | Reserved        | Reserved.                                                                                                                  |                   |
| EDX[31:0]  | Reserved        | Reserved.                                                                                                                  |                   |

**CPUID.23H.05H -- Arch PEBS GP and Fixed Counters supported****Table 21-79. Leaf 23H.05H Architectural Performance Monitoring Extended**

| Register  | Field Name  | Description                                                                                                                                                                                                                                                                                                                                                                      | Domain            |
|-----------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0] | GP_PEBS     | Bit vector of general-purpose counters for which the Architectural PEBS mechanism is available (bit n == GP counter #n). If EAX[n] == 1, then the IA32_PMC_GPn_CFG_C MSR is available, and PEBS is supported on that counter; the PEBS_EN[63] field can be set; and the RELOAD[31:0] field can be set. Note that CPUID.23H.04H:EBX governs which adaptive group bits can be set. | Logical Processor |
| EBX[31:0] | GP_PDIST    | General-purpose counters for which PEBS supports PDIST.                                                                                                                                                                                                                                                                                                                          | Logical Processor |
| ECX[31:0] | FIXED_PEBS  | Bit vector of fixed-function counters for which the Architectural PEBS mechanism is available. If ECX[x] == 1, then the IA32_PMC_FXm_CFG_C MSR is available, and PEBS is supported; the PEBS_EN[63] field can be set; and the RELOAD[31:0] field can be set. Note that CPUID.23H.04H:EBX governs which adaptive group bits can be set.                                           | Logical Processor |
| EDX[31:0] | FIXED_PDIST | Fixed-function counters for which PEBS supports PDIST.                                                                                                                                                                                                                                                                                                                           | Logical Processor |

CPUID.24H -- Converged Vector ISA

When CPUID.24H, the processor returns Intel AVX10 converged vector ISA information. This leaf is supported when CPUID.07H.01H:EDX.AVX10[19] = 1.

- This leaf is valid if CPUID.07H.01H:EDX.AVX10[19] = 1 and MAX\_LEAF ≥ 24H.
- The maximum sub-leaf value for ECX is specified in CPUID.24H.00H.EAX[31:0] MAX\_SUBLEAF.
- If ECX contains an invalid sub-leaf index, EAX/EBX/ECX/EDX return 0. Sub-leaf index n is invalid if n exceeds the value that sub-leaf 0 returns in EAX.

CPUID.24H.00H -- Converged Vector ISA Main Sub-Leaf

Table 21-80. Leaf 24H.00H Converged Vector ISA

| Register   | Field Name         | Description                                                                                                                                                                                       | Domain   |
|------------|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0]  | MAX_SUBLEAF        | Reports the maximum number of sub-leaves that are supported in leaf 24H.                                                                                                                          | Platform |
| EBX[7:0]   | VECTOR_ISA_VERSION | Reports the Intel® AVX10 Converged Vector ISA version.                                                                                                                                            | Platform |
| EBX[15:8]  | Reserved           | Reserved.                                                                                                                                                                                         |          |
| EBX[18:16] | Reserved at 111    | Always 111b.<br>Earlier versions of this specification documented these bits as enumerating support for different vector lengths. Processors enumerating Intel® AVX10 support all vector lengths. | Platform |
| EBX[31:19] | Reserved           | Reserved.                                                                                                                                                                                         |          |
| ECX[31:0]  | Reserved           | Reserved.                                                                                                                                                                                         |          |
| EDX[31:0]  | Reserved           | Reserved.                                                                                                                                                                                         |          |

## CPUID.27H -- Intel® Resource Director Technology (Intel® RDT) Asymmetric Monitoring

CPUID.27H returns information for the Intel Resource Director Technology Monitoring capabilities with asymmetric topology.

As described below, software uses the bit vector returned in EDX by sub-leaf 00H to determine the available resource types (ResID) that can be monitored. This information is necessary for software to program the IA32\_PQR\_ASSOC and IA32\_QM\_EVTSEL MSRs such that Quality-of-Service data can be read afterwards from the IA32\_QM\_CTR MSR.

- This leaf is valid if CPUID.07H.01H:ECX.RDT\_M\_ASYM[0] = 1 and MAX\_LEAF ≥ 27H.
- If the leaf is valid, sub-leaf 00H is always valid. Sub-leaf n (n ≥ 1) is only valid when (CPUID.27H.00H:EDX[n] == 1).
- This leaf must be read on each logical processor to determine the support on each processor.

### CPUID.27H.00H -- Intel® RDT Asymmetric Monitoring Main Sub-Leaf

CPUID.27H.00H returns information about Intel RDT Monitoring Asymmetric.

**Table 21-81. Leaf 27H.00H Intel® Resource Director Technology (Intel® RDT) Asymmetric Monitoring**

| Register  | Field Name | Description                                                                                                                   | Domain            |
|-----------|------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0] | Reserved   | Reserved.                                                                                                                     |                   |
| EBX[31:0] | MAX_RMID   | Maximum range (zero-based) of RMID within this physical processor of all types.                                               | Logical Processor |
| ECX[31:0] | Reserved   | Reserved.                                                                                                                     |                   |
| EDX[0]    | Reserved   | Reserved.                                                                                                                     |                   |
| EDX[1]    | L3_MON     | If 1, supports L3 Cache Intel RDT Monitoring. Sub-leaf index 0 reports valid resource type starting at bit position 1 of EDX. | Logical Processor |
| EDX[31:2] | Reserved   | Reserved.                                                                                                                     |                   |

CPUID.27H.00H returns information about the bit-vector representation of QoS monitoring resource types that are supported in the processor and maximum range of RMID values the processor can use to monitor of any supported resource types. Each bit, starting from bit 1, corresponds to a specific resource type if the bit is set. The bit position corresponds to the sub-leaf index (or ResID) that software must use to query QoS monitoring capability available for that type.

### CPUID.27H.01H -- L3 Cache Intel® Resource Director Technology Asymmetric Monitoring

CPUID.27H.01H returns information about L3 Cache Intel RDT monitoring asymmetric.

**Table 21-82. Leaf 27H.01H Intel® Resource Director Technology (Intel® RDT) Asymmetric Monitoring**

| Register | Field Name | Description                                                                                                                                                                                              | Domain            |
|----------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[7:0] | CTR_WIDTH  | The counter width is encoded as an offset from 24b. A value of zero in this field indicates that 24-bit counters are supported. A value of 8 in this field indicates that 32-bit counters are supported. | Logical Processor |
| EAX[8]   | RDT_M_OVF  | If 1, supports an overflow bit in the IA32_QM_CTR MSR (bit 61).                                                                                                                                          | Logical Processor |

|            |              |                                                                                                                                           |                   |
|------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[9]     | IO_RDT_CMT   | If 1, indicates the presence of non-CPU agent supporting Intel RDT CMT.                                                                   | Logical Processor |
| EAX[10]    | IO_RDT_MBM   | If 1, indicates the presence of non-CPU agent supporting Intel RDT MBM support.                                                           | Logical Processor |
| EAX[31:11] | Reserved     | Reserved.                                                                                                                                 |                   |
| EBX[31:0]  | CONV_FACTOR  | Factor used to convert from reported IA32_QM_CTR value to derived occupancy metric (bytes) and Memory Bandwidth Monitoring (MBM) metrics. | Logical Processor |
| ECX[31:0]  | MAX_RMID_L3  | Maximum range (zero-based) of RMID of this resource type.                                                                                 | Logical Processor |
| EDX[0]     | CMT_L3_OCCUP | If 1, supports L3 occupancy monitoring.                                                                                                   | Logical Processor |
| EDX[1]     | MBM_L3_TOTAL | If 1, supports L3 total bandwidth monitoring.                                                                                             | Logical Processor |
| EDX[2]     | MBM_L3_LOCAL | If 1, supports L3 local bandwidth monitoring.                                                                                             | Logical Processor |
| EDX[31:3]  | Reserved     | Reserved.                                                                                                                                 |                   |

## CPUID.28H -- Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation

CPUID.28H returns information for Intel Resource Director Technology Allocation with asymmetric topology. This leaf is valid when CPUID.07H.01H:ECX.RDT\_A\_SYM[1] = 1. As described below, software uses the bit vector returned in EBX by subleaf 00H to determine the available QoS Enforcement (allocation) resource types that are supported in the processor. This information is necessary for software to configure each class of services using capability bit masks in the QoS Mask registers, IA32\_resourceType\_Mask\_n.

- This leaf is valid if CPUID.07H.01H:ECX.RDT\_A\_SYM[1] = 1 and MAX\_LEAF ≥ 28H.
- If the leaf is valid, sub-leaf 00H is always valid. Sub-leaf n (n ≥ 1) is only valid when (CPUID.28H.00H:EBX[n] == 1).

### CPUID.28H.00H -- Intel® RDT Asymmetric Allocation Main Sub-Leaf

CPUID.28H.00H returns information about Intel RDT Allocation Asymmetric.

**Table 21-83. Leaf 28H.00H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register  | Field Name        | Description                                   | Domain            |
|-----------|-------------------|-----------------------------------------------|-------------------|
| EAX[31:0] | Reserved          | Reserved.                                     |                   |
| EBX[0]    | Reserved          | Reserved.                                     |                   |
| EBX[1]    | CAT_L3            | Supports L3 Cache Allocation Technology if 1. | Logical Processor |
| EBX[2]    | CAT_L2            | Supports L2 Cache Allocation Technology if 1. | Logical Processor |
| EBX[3]    | MBA               | Supports Memory Bandwidth Allocation if 1.    | Logical Processor |
| EBX[4]    | Reserved          | Reserved.                                     |                   |
| EBX[5]    | CBA               | If 1, supports Cache Bandwidth Allocation.    | Logical Processor |
| EBX[6]    | RESOURCE_PRIORITY | If 1, supports Resource Priority.             | Platform          |
| EBX[31:7] | Reserved          | Reserved.                                     |                   |
| ECX[31:0] | Reserved          | Reserved.                                     |                   |
| EDX[31:0] | Reserved          | Reserved.                                     |                   |

CPUID.28H.00H returns information about the bit-vector representation of QoS Enforcement resource types that are supported in the processor. Each bit, starting from bit 1, corresponds to a specific resource type if the bit is set. The bit position corresponds to the sub-leaf index (or ResID) that software must use to query QoS enforcement capability available for that type.

### CPUID.28H.01H -- Asymmetric L3 Cache Allocation Technology

CPUID.28H.ResID=1 returns information about Asymmetric L3 Cache Allocation Technology.

**Table 21-84. Leaf 28H.01H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register  | Field Name            | Description                                                                                                 | Domain            |
|-----------|-----------------------|-------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[4:0]  | CAT_L3_BITMASK_LENGTH | Length of the capacity bit mask for the corresponding ResID. Add one to the return value to get the result. | Logical Processor |
| EAX[31:5] | Reserved              | Reserved.                                                                                                   |                   |

|            |                   |                                                                                                                                              |                   |
|------------|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EBX[31:0]  | CAT_L3_CONTENTION | Bit-granular map of isolation/contention of allocation units.                                                                                | Logical Processor |
| ECX[0]     | Reserved          | If 1, supports L3 CAT for non-CPU agents.                                                                                                    |                   |
| ECX[1]     | CAT_L3_NONCPU     | N/A                                                                                                                                          | Logical Processor |
| ECX[2]     | CAT_L3_CDP        | If 1, supports L3 Code and Data Prioritization Technology.                                                                                   | Logical Processor |
| ECX[3]     | CAT_L3_NONCONTIG  | If 1, supports non-contiguous capacity bitmasks. The bits that are set in the various IA32_L3_MASK_n registers do not have to be contiguous. | Logical Processor |
| ECX[31:4]  | Reserved          | Reserved.                                                                                                                                    |                   |
| EDX[15:0]  | CAT_L3_MAX_CLOS   | Highest Class of Service (COS) number supported for this ResID.                                                                              | Logical Processor |
| EDX[31:16] | Reserved          | Reserved.                                                                                                                                    |                   |

### CPUID.28H.02H -- Asymmetric L2 Cache Allocation Technology

CPUID.28H.ResID=2 returns information about Asymmetric L2 Cache Allocation Technology.

**Table 21-85. Leaf 28H.02H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register   | Field Name            | Description                                                                                                                                  | Domain            |
|------------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[4:0]   | CAT_L2_BITMASK_LENGTH | Length of the capacity bit mask for the corresponding ResID. Add one to the return value to get the result.                                  | Logical Processor |
| EAX[31:5]  | Reserved              | Reserved.                                                                                                                                    |                   |
| EBX[31:0]  | CAT_L2_CONTENTION     | Bit-granular map of isolation/contention of allocation units.                                                                                | Logical Processor |
| ECX[1:0]   | Reserved              | Reserved.                                                                                                                                    |                   |
| ECX[2]     | CAT_L2_CDP            | If 1, supports L2 Code and Data Prioritization Technology.                                                                                   | Logical Processor |
| ECX[3]     | CAT_L2_NONCONTIG      | If 1, supports non-contiguous capacity bitmasks. The bits that are set in the various IA32_L2_MASK_n registers do not have to be contiguous. | Logical Processor |
| ECX[31:4]  | Reserved              | Reserved.                                                                                                                                    |                   |
| EDX[15:0]  | CAT_L2_MAX_CLOS       | Highest Class of Service (COS) number supported for this ResID.                                                                              | Logical Processor |
| EDX[31:16] | Reserved              | Reserved.                                                                                                                                    |                   |

### CPUID.28H.03H -- Asymmetric Memory Bandwidth Allocation

CPUID.28H.ResID=3 returns information about Asymmetric Memory Bandwidth Allocation.

**Table 21-86. Leaf 28H.03H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register | Field Name | Description | Domain |
|----------|------------|-------------|--------|
|----------|------------|-------------|--------|

|            |                |                                                                                                                                |                   |
|------------|----------------|--------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[11:0]  | MBA_MAX        | Reports the maximum MBA throttling value supported for the corresponding ResID. Add one to the return value to get the result. | Logical Processor |
| EAX[31:12] | Reserved       | Reserved.                                                                                                                      |                   |
| EBX[31:0]  | Reserved       | Reserved.                                                                                                                      |                   |
| ECX[0]     | PER_THREAD_MBA | Per-thread MBA controls are supported.                                                                                         | Logical Processor |
| ECX[1]     | Reserved       | Reserved.                                                                                                                      |                   |
| ECX[2]     | MBA_LINEAR     | If 1, the response of the delay values is linear.                                                                              | Logical Processor |
| ECX[31:3]  | Reserved       | Reserved.                                                                                                                      |                   |
| EDX[15:0]  | MBA_MAX_CLOS   | Highest Class of Service (COS) number supported for this ResID.                                                                | Logical Processor |
| EDX[31:16] | Reserved       | Reserved.                                                                                                                      |                   |

## CPUID.28H.05H -- Asymmetric Cache Bandwidth Allocation

**Table 21-87. Leaf 28H.05H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register   | Field Name     | Description                                                                                                                                                    | Domain            |
|------------|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| EAX[7:0]   | CBA_MAX_LEVELS | Reports the maximum core throttling level supported for the corresponding ResID. Add one to the return value to get the number of throttling levels supported. | Logical Processor |
| EAX[11:8]  | BW_SCOPE       | If 1, indicates the logical processor scope of the IA32_QoS_Core_BW_Thrtl_n MSRs. Other values are reserved.                                                   | Logical Processor |
| EAX[31:12] | Reserved       | Reserved.                                                                                                                                                      |                   |
| EBX[31:0]  | Reserved       | Reserved.                                                                                                                                                      |                   |
| ECX[2:0]   | Reserved       | Reserved.                                                                                                                                                      |                   |
| ECX[3]     | CBA_LINEAR     | If 1, the response of the bandwidth control is approximately linear. If 0, the response of the bandwidth control is non-linear.                                | Logical Processor |
| ECX[31:4]  | Reserved       | Reserved.                                                                                                                                                      |                   |
| EDX[15:0]  | CBA_MAX_CLOS   | Highest Class of Service (COS) number supported for this ResID.                                                                                                | Logical Processor |
| EDX[31:16] | Reserved       | Reserved.                                                                                                                                                      |                   |

## CPUID.28H.06H -- Resource Priority Control

**Table 21-88. Leaf 28H.06H Intel® Resource Director Technology (Intel® RDT) Asymmetric Allocation**

| Register | Field Name    | Description                                                                    | Domain   |
|----------|---------------|--------------------------------------------------------------------------------|----------|
| EAX[0]   | THREAD_ENABLE | If 1, supports per-thread enable of RP through the IA32_RESOURCE_PRIORITY MSR. | Platform |

PROCESSOR IDENTIFICATION AND FEATURE DETERMINATION

|           |                |                                                                                                    |          |
|-----------|----------------|----------------------------------------------------------------------------------------------------|----------|
| EAX[1]    | PACKAGE_ENABLE | If 1, supports physical processor package enable of RP through the IA32_RESOURCE_PRIORITY_PKG MSR. | Platform |
| EAX[31:2] | Reserved       | Reserved.                                                                                          |          |
| EBX[31:0] | Reserved       | Reserved.                                                                                          |          |
| ECX[31:0] | Reserved       | Reserved.                                                                                          |          |
| EDX[31:0] | Reserved       | Reserved.                                                                                          |          |

## CPUID.80000000H -- Maximum Input Value for Extended Function CPUID Information

CPUID.80000000H returns the highest value the processor recognizes for returning extended processor information. The value is returned in the EAX register and is processor specific.

- This leaf is supported starting with Pentium 4.
- Processors prior to Pentium 4 treat bit 31 as 0, and this leaf returns the values from CPUID.00H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-89. Leaf 80000000H Maximum Input Value for Extended Function CPUID Information**

| Register  | Field Name        | Description                                                  | Domain   |
|-----------|-------------------|--------------------------------------------------------------|----------|
| EAX[31:0] | MAX_EXTENDED_LEAF | Maximum input value for Extended Function CPUID Information. | Platform |
| EBX[31:0] | Reserved          | Reserved.                                                    |          |
| ECX[31:0] | Reserved          | Reserved.                                                    |          |
| EDX[31:0] | Reserved          | Reserved.                                                    |          |

## CPUID.80000001H -- Extended Processor Signature and Feature Bits

CPUID.80000001H returns information about extended processor signature and features bits.

- This leaf is valid if MAX\_EXTENDED\_LEAF  $\geq$  80000001H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-90. Leaf 80000001H Extended Processor Signature and Feature Bits**

| Register   | Field Name        | Description                                                                                                                                                         | Domain   |
|------------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[31:0]  | Reserved          | Reserved.                                                                                                                                                           |          |
| EBX[31:0]  | Reserved          | Reserved.                                                                                                                                                           |          |
| ECX[0]     | LAHF_SAHF_64      | If 1, supports the LAHF/SAHF instructions in 64-bit mode.<br>LAHF and SAHF are always available in other modes, regardless of the enumeration of this feature flag. | Platform |
| ECX[4:1]   | Reserved          | Reserved.                                                                                                                                                           |          |
| ECX[5]     | LZCNT             | If 1, supports the LZCNT instruction.                                                                                                                               | Platform |
| ECX[7:6]   | Reserved          | Reserved.                                                                                                                                                           |          |
| ECX[8]     | PREFETCHW         | If 1, supports the PREFETCHW instruction.                                                                                                                           | Platform |
| ECX[31:9]  | Reserved          | Reserved.                                                                                                                                                           |          |
| EDX[10:0]  | Reserved          | Reserved.                                                                                                                                                           |          |
| EDX[11]    | SYSCALL_SYSRET_64 | If 1, supports SYSCALL/SYSRET.<br>Intel processors support SYSCALL and SYSRET only in 64-bit mode. This feature flag is always enumerated as 0 outside 64-bit mode. | Platform |
| EDX[19:12] | Reserved          | Reserved.                                                                                                                                                           |          |
| EDX[20]    | EXECUTE_DIS       | If 1, supports Execute Disable Bit.                                                                                                                                 | Platform |
| EDX[25:21] | Reserved          | Reserved.                                                                                                                                                           |          |
| EDX[26]    | PAGE_1GB          | If 1, supports 1-GByte pages.                                                                                                                                       | Platform |
| EDX[27]    | RDTSCP            | If 1, supports RDTSCP and IA32_TSC_AUX.                                                                                                                             | Platform |
| EDX[28]    | Reserved          | Reserved.                                                                                                                                                           |          |
| EDX[29]    | INTEL64           | If 1, supports Intel® 64 Architecture.                                                                                                                              | Platform |
| EDX[31:30] | Reserved          | Reserved.                                                                                                                                                           |          |

## CPUID.80000002H -- Processor Brand String (Bytes 0 to 15)

CPUID.80000002H returns information about the Processor Brand String. For additional details on Processor Brand String, see Section 21.2, “Methods for Returning Branding Information Using CPUID.”

- This leaf is valid if MAX\_EXTENDED\_LEAF  $\geq$  80000002H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-91. Leaf 80000002H Processor Brand String (Bytes 0 to 15)**

| Register  | Field Name   | Description                       | Domain   |
|-----------|--------------|-----------------------------------|----------|
| EAX[31:0] | BRAND_NAME_0 | Processor brand string.           | Platform |
| EBX[31:0] | BRAND_NAME_1 | Processor brand string continued. | Platform |
| ECX[31:0] | BRAND_NAME_2 | Processor brand string continued. | Platform |
| EDX[31:0] | BRAND_NAME_3 | Processor brand string continued. | Platform |

CPUID.80000003H -- Processor brand string (Bytes 16 to 31)

CPUID.80000003H returns information about the Processor Brand String. For additional details on Processor Brand String, see Section 21.2, “Methods for Returning Branding Information Using CPUID.”

- This leaf is valid if MAX\_EXTENDED\_LEAF ≥ 80000003H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-92. Leaf 80000003H Processor brand string (Bytes 16 to 31)

| Register  | Field Name   | Description                       | Domain   |
|-----------|--------------|-----------------------------------|----------|
| EAX[31:0] | BRAND_NAME_4 | Processor brand string continued. | Platform |
| EBX[31:0] | BRAND_NAME_5 | Processor brand string continued. | Platform |
| ECX[31:0] | BRAND_NAME_6 | Processor brand string continued. | Platform |
| EDX[31:0] | BRAND_NAME_7 | Processor brand string continued. | Platform |

## CPUID.80000004H -- Processor brand string (Bytes 32 to 47)

CPUID.80000004H returns information about the Processor Brand String. For additional details on Processor Brand String, see Section 21.2, “Methods for Returning Branding Information Using CPUID.”

- This leaf is valid if MAX\_EXTENDED\_LEAF  $\geq$  80000004H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-93. Leaf 80000004H Processor brand string (Bytes 32 to 47)**

| Register  | Field Name    | Description                       | Domain   |
|-----------|---------------|-----------------------------------|----------|
| EAX[31:0] | BRAND_NAME_8  | Processor brand string continued. | Platform |
| EBX[31:0] | BRAND_NAME_9  | Processor brand string continued. | Platform |
| ECX[31:0] | BRAND_NAME_10 | Processor brand string continued. | Platform |
| EDX[31:0] | BRAND_NAME_11 | Processor brand string continued. | Platform |

**CPUID.80000005H -- Reserved**

This leaf is reserved and returns all zeroes.

**Table 21-94. Leaf 80000005H Reserved**

| Register  | Field Name | Description | Domain |
|-----------|------------|-------------|--------|
| EAX[31:0] | Reserved   | Reserved.   |        |
| EBX[31:0] | Reserved   | Reserved.   |        |
| ECX[31:0] | Reserved   | Reserved.   |        |
| EDX[31:0] | Reserved   | Reserved.   |        |

## CPUID.80000006H -- Extended Function CPUID Information

CPUID.80000006H returns Extended Function CPUID information. The preferred method to enumerate caching information description>is to use CPUID.04H—Deterministic Cache Parameters.

- This leaf is valid if MAX\_EXTENDED\_LEAF  $\geq$  80000006H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX

**Table 21-95. Leaf 80000006H Extended Function CPUID Information**

| Register   | Field Name   | Description                                                                                 | Domain            |
|------------|--------------|---------------------------------------------------------------------------------------------|-------------------|
| EAX[31:0]  | Reserved     | Reserved.                                                                                   |                   |
| EBX[31:0]  | Reserved     | Reserved.                                                                                   |                   |
| ECX[7:0]   | L2_LINE_SIZE | Cache line size in bytes.                                                                   | Logical Processor |
| ECX[11:8]  | Reserved     | Reserved.                                                                                   |                   |
| ECX[15:12] | L2_ASSOC     | L2 associativity field. The L2 associativity field encodings are listed in the table below. | Logical Processor |
| ECX[31:16] | L2_SIZE      | Cache size in 1K units.                                                                     | Logical Processor |
| EDX[7:0]   | Reserved     | Reserved.                                                                                   |                   |
| EDX[31:8]  | Reserved     | Reserved.                                                                                   |                   |

**Table 21-96. L2 Associativity Field Encodings**

| Encoding Value | Description                              | Encoding Value | Description       |
|----------------|------------------------------------------|----------------|-------------------|
| 00H            | Disabled                                 | 08H            | 16 Ways           |
| 01H            | 1 Way (direct mapped)                    | 09H            | Reserved          |
| 02H            | 2 Ways                                   | 0AH            | 32 Ways           |
| 03H            | Reserved                                 | 0BH            | 48 Ways           |
| 04H            | 4 Ways                                   | 0CH            | 64 Ways           |
| 05H            | Reserved                                 | 0DH            | 96 Ways           |
| 06H            | 8 Ways                                   | 0EH            | 128 Ways          |
| 07H            | See CPUID leaf 4 sub-leaf 2 <sup>1</sup> | 0FH            | Fully Associative |

CPUID.80000007H -- Extended Function CPUID Information 1

- CPUID.80000007H returns Extended Function CPUID information.
- This leaf is valid if MAX\_EXTENDED\_LEAF ≥ 80000007H.
  - This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

Table 21-97. Leaf 80000007H Extended Function CPUID Information 1

| Register  | Field Name    | Description                   | Domain   |
|-----------|---------------|-------------------------------|----------|
| EAX[31:0] | Reserved      | Reserved.                     |          |
| EBX[31:0] | Reserved      | Reserved.                     |          |
| ECX[31:0] | Reserved      | Reserved.                     |          |
| EDX[7:0]  | Reserved      | Reserved.                     |          |
| EDX[8]    | TSC_INVARIANT | If 1, supports Invariant TSC. | Platform |
| EDX[31:9] | Reserved      | Reserved.                     |          |

## CPUID.80000008H -- Extended Function CPUID Information 2

CPUID.80000008H returns Extended Function CPUID information.

- This leaf is valid if MAX\_EXTENDED\_LEAF  $\geq$  80000008H.
- This leaf does not contain sub-leaves and provides the same information regardless of the value of ECX.

**Table 21-98. Leaf 80000008H Extended Function CPUID Information 2**

| Register   | Field Name           | Description                                                                                                                                                                                                                                    | Domain   |
|------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| EAX[7:0]   | PHYS_ADDR_SIZE       | Number of physical-address bits. If TME-MK is enabled, the number of bits that can be used to address memory may be reduced by IA32_TME_ACTIVATE[35:32].                                                                                       | Platform |
| EAX[15:8]  | LIN_ADDR_SIZE        | Number of linear-address bits.                                                                                                                                                                                                                 | Platform |
| EAX[23:16] | GUEST_PHYS_ADDR_SIZE | Number of guest-physical-address bits (for software operating in a virtual machine). If this field is zero, PHYS_ADDR_SIZE should be used. Intel processors return zero for this field. Software emulating CPUID may return a different value. | Platform |
| EAX[31:24] | Reserved             | Reserved.                                                                                                                                                                                                                                      |          |
| EBX[8:0]   | Reserved             | Reserved.                                                                                                                                                                                                                                      |          |
| EBX[9]     | WBNOINVD             | If 1, supports the WBNOINVD instruction.                                                                                                                                                                                                       | Platform |
| EBX[31:10] | Reserved             | Reserved.                                                                                                                                                                                                                                      |          |
| ECX[31:0]  | Reserved             | Reserved.                                                                                                                                                                                                                                      |          |
| EDX[31:0]  | Reserved             | Reserved.                                                                                                                                                                                                                                      |          |



### A.1 EFLAGS AND INSTRUCTIONS

Table A-2 summarizes how the instructions affect the flags in the EFLAGS register. The following codes describe how the flags are affected.

**Table A-1. Codes Describing Flags**

|       |                                                                          |
|-------|--------------------------------------------------------------------------|
| T     | Instruction tests flag.                                                  |
| M     | Instruction modifies flag (either sets or resets depending on operands). |
| 0     | Instruction resets flag.                                                 |
| 1     | Instruction sets flag.                                                   |
| —     | Instruction's effect on flag is undefined.                               |
| R     | Instruction restores prior value of flag.                                |
| Blank | Instruction does not affect flag.                                        |

**Table A-2. EFLAGS Cross-Reference**

| Instruction        | OF | SF | ZF | AF | PF | CF | TF | IF | DF | NT | RF |
|--------------------|----|----|----|----|----|----|----|----|----|----|----|
| AAA                | —  | —  | —  | TM | —  | M  |    |    |    |    |    |
| AAD                | —  | M  | M  | —  | M  | —  |    |    |    |    |    |
| AAM                | —  | M  | M  | —  | M  | —  |    |    |    |    |    |
| AAS                | —  | —  | —  | TM | —  | M  |    |    |    |    |    |
| ADC                | M  | M  | M  | M  | M  | TM |    |    |    |    |    |
| ADD                | M  | M  | M  | M  | M  | M  |    |    |    |    |    |
| AND                | 0  | M  | M  | —  | M  | 0  |    |    |    |    |    |
| ARPL               |    |    | M  |    |    |    |    |    |    |    |    |
| BOUND              |    |    |    |    |    |    |    |    |    |    |    |
| BSF/BSR            | 0  | 0  | M  | 0  | M  | 0  |    |    |    |    |    |
| BSWAP              |    |    |    |    |    |    |    |    |    |    |    |
| BT/BTS/BTR/BTC     | —  | —  |    | —  | —  | M  |    |    |    |    |    |
| CALL               |    |    |    |    |    |    |    |    |    |    |    |
| CBW                |    |    |    |    |    |    |    |    |    |    |    |
| CLC                |    |    |    |    |    | 0  |    |    |    |    |    |
| CLD                |    |    |    |    |    |    |    |    | 0  |    |    |
| CLI                |    |    |    |    |    |    |    | 0  |    |    |    |
| CLTS               |    |    |    |    |    |    |    |    |    |    |    |
| CMC                |    |    |    |    |    | M  |    |    |    |    |    |
| CMOV <sub>cc</sub> | T  | T  | T  |    | T  | T  |    |    |    |    |    |
| CMP                | M  | M  | M  | M  | M  | M  |    |    |    |    |    |

Table A-2. EFLAGS Cross-Reference (Contd.)

| Instruction                    | OF | SF | ZF | AF | PF | CF | TF | IF | DF | NT | RF |
|--------------------------------|----|----|----|----|----|----|----|----|----|----|----|
| CMPS                           | M  | M  | M  | M  | M  | M  |    |    | T  |    |    |
| CMPXCHG                        | M  | M  | M  | M  | M  | M  |    |    |    |    |    |
| CMPXCHG8B                      |    |    | M  |    |    |    |    |    |    |    |    |
| COMISD                         | 0  | 0  | M  | 0  | M  | M  |    |    |    |    |    |
| COMISS                         | 0  | 0  | M  | 0  | M  | M  |    |    |    |    |    |
| CPUID                          |    |    |    |    |    |    |    |    |    |    |    |
| CWD                            |    |    |    |    |    |    |    |    |    |    |    |
| DAA                            | —  | M  | M  | TM | M  | TM |    |    |    |    |    |
| DAS                            | —  | M  | M  | TM | M  | TM |    |    |    |    |    |
| DEC                            | M  | M  | M  | M  | M  |    |    |    |    |    |    |
| DIV                            | —  | —  | —  | —  | —  | —  |    |    |    |    |    |
| ENTER                          |    |    |    |    |    |    |    |    |    |    |    |
| ESC                            |    |    |    |    |    |    |    |    |    |    |    |
| FCMOV <sub>cc</sub>            |    |    | T  |    | T  | T  |    |    |    |    |    |
| FCOMI, FCOMIP, FUCOMI, FUCOMIP | 0  | 0  | M  | 0  | M  | M  |    |    |    |    |    |
| HLT                            |    |    |    |    |    |    |    |    |    |    |    |
| IDIV                           | —  | —  | —  | —  | —  | —  |    |    |    |    |    |
| IMUL                           | M  | —  | —  | —  | —  | M  |    |    |    |    |    |
| IN                             |    |    |    |    |    |    |    |    |    |    |    |
| INC                            | M  | M  | M  | M  | M  |    |    |    |    |    |    |
| INS                            |    |    |    |    |    |    |    |    | T  |    |    |
| INT                            |    |    |    |    |    |    | 0  |    |    | 0  |    |
| INTO                           | T  |    |    |    |    |    | 0  |    |    | 0  |    |
| INVD                           |    |    |    |    |    |    |    |    |    |    |    |
| INVLPG                         |    |    |    |    |    |    |    |    |    |    |    |
| UCOMISD                        | 0  | 0  | M  | 0  | M  | M  |    |    |    |    |    |
| UCOMISS                        | 0  | 0  | M  | 0  | M  | M  |    |    |    |    |    |
| IRET                           | R  | R  | R  | R  | R  | R  | R  | R  | R  | T  |    |
| J <sub>cc</sub>                | T  | T  | T  |    | T  | T  |    |    |    |    |    |
| JCXZ                           |    |    |    |    |    |    |    |    |    |    |    |
| JMP                            |    |    |    |    |    |    |    |    |    |    |    |
| LAHF                           |    |    |    |    |    |    |    |    |    |    |    |
| LAR                            |    |    | M  |    |    |    |    |    |    |    |    |
| LDS/LES/LSS/LFS/LGS            |    |    |    |    |    |    |    |    |    |    |    |
| LEA                            |    |    |    |    |    |    |    |    |    |    |    |
| LEAVE                          |    |    |    |    |    |    |    |    |    |    |    |
| LGDT/LIDT/LLDT/LMSW            |    |    |    |    |    |    |    |    |    |    |    |
| LOCK                           |    |    |    |    |    |    |    |    |    |    |    |

Table A-2. EFLAGS Cross-Reference (Contd.)

| Instruction              | OF | SF | ZF | AF | PF | CF | TF | IF | DF | NT | RF |
|--------------------------|----|----|----|----|----|----|----|----|----|----|----|
| LODS                     |    |    |    |    |    |    |    |    | T  |    |    |
| LOOP                     |    |    |    |    |    |    |    |    |    |    |    |
| LOOPE/LOOPNE             |    |    | T  |    |    |    |    |    |    |    |    |
| LSL                      |    |    | M  |    |    |    |    |    |    |    |    |
| LTR                      |    |    |    |    |    |    |    |    |    |    |    |
| MONITOR                  |    |    |    |    |    |    |    |    |    |    |    |
| MWAIT                    |    |    |    |    |    |    |    |    |    |    |    |
| MOV                      |    |    |    |    |    |    |    |    |    |    |    |
| MOV control, debug, test | —  | —  | —  | —  | —  | —  |    |    |    |    |    |
| MOVS                     |    |    |    |    |    |    |    |    | T  |    |    |
| MOVSX/MOVZX              |    |    |    |    |    |    |    |    |    |    |    |
| MUL                      | M  | —  | —  | —  | —  | M  |    |    |    |    |    |
| NEG                      | M  | M  | M  | M  | M  | M  |    |    |    |    |    |
| NOP                      |    |    |    |    |    |    |    |    |    |    |    |
| NOT                      |    |    |    |    |    |    |    |    |    |    |    |
| OR                       | 0  | M  | M  | —  | M  | 0  |    |    |    |    |    |
| OUT                      |    |    |    |    |    |    |    |    |    |    |    |
| OUTS                     |    |    |    |    |    |    |    |    | T  |    |    |
| POP/POPA                 |    |    |    |    |    |    |    |    |    |    |    |
| POPF                     | R  | R  | R  | R  | R  | R  | R  | R  | R  | R  |    |
| PUSH/PUSHA/PUSHF         |    |    |    |    |    |    |    |    |    |    |    |
| RCL/RCR 1                | M  |    |    |    |    | TM |    |    |    |    |    |
| RCL/RCR count            | —  |    |    |    |    | TM |    |    |    |    |    |
| RDMSR                    |    |    |    |    |    |    |    |    |    |    |    |
| RDPMC                    |    |    |    |    |    |    |    |    |    |    |    |
| RDTSC                    |    |    |    |    |    |    |    |    |    |    |    |
| REP/REPE/REPNE           |    |    |    |    |    |    |    |    |    |    |    |
| RET                      |    |    |    |    |    |    |    |    |    |    |    |
| ROL/ROR 1                | M  |    |    |    |    | M  |    |    |    |    |    |
| ROL/ROR count            | —  |    |    |    |    | M  |    |    |    |    |    |
| RSM                      | M  | M  | M  | M  | M  | M  | M  | M  | M  | M  | M  |
| SAHF                     |    | R  | R  | R  | R  | R  |    |    |    |    |    |
| SAL/SAR/SHL/SHR 1        | M  | M  | M  | —  | M  | M  |    |    |    |    |    |
| SAL/SAR/SHL/SHR count    | —  | M  | M  | —  | M  | M  |    |    |    |    |    |
| SBB                      | M  | M  | M  | M  | M  | TM |    |    |    |    |    |
| SCAS                     | M  | M  | M  | M  | M  | M  |    |    | T  |    |    |
| SETcc                    | T  | T  | T  |    | T  | T  |    |    |    |    |    |
| SGDT/SIDT/SLDT/SMSW      |    |    |    |    |    |    |    |    |    |    |    |

Table A-2. EFLAGS Cross-Reference (Contd.)

| Instruction | OF | SF | ZF | AF | PF | CF | TF | IF | DF | NT | RF |
|-------------|----|----|----|----|----|----|----|----|----|----|----|
| SHLD/SHRD   | —  | M  | M  | —  | M  | M  |    |    |    |    |    |
| STC         |    |    |    |    |    | 1  |    |    |    |    |    |
| STD         |    |    |    |    |    |    |    |    | 1  |    |    |
| STI         |    |    |    |    |    |    |    | 1  |    |    |    |
| STOS        |    |    |    |    |    |    |    |    | T  |    |    |
| STR         |    |    |    |    |    |    |    |    |    |    |    |
| SUB         | M  | M  | M  | M  | M  | M  |    |    |    |    |    |
| TEST        | 0  | M  | M  | —  | M  | 0  |    |    |    |    |    |
| UD          |    |    |    |    |    |    |    |    |    |    |    |
| VERR/VERRW  |    |    | M  |    |    |    |    |    |    |    |    |
| WAIT        |    |    |    |    |    |    |    |    |    |    |    |
| WBINVD      |    |    |    |    |    |    |    |    |    |    |    |
| WRMSR       |    |    |    |    |    |    |    |    |    |    |    |
| XADD        | M  | M  | M  | M  | M  | M  |    |    |    |    |    |
| XCHG        |    |    |    |    |    |    |    |    |    |    |    |
| XLAT        |    |    |    |    |    |    |    |    |    |    |    |
| XOR         | 0  | M  | M  | —  | M  | 0  |    |    |    |    |    |

### B.1 CONDITION CODES

Table B-1 lists condition codes that can be queried using *CMOVcc*, *FCMOVcc*, *Jcc*, and *SETcc*. Condition codes refer to the setting of one or more status flags (CF, OF, SF, ZF, and PF) in the EFLAGS register. In the table below:

- The “Mnemonic” column provides the suffix (cc) added to the instruction to specify a test condition.
- “Condition Tested For” describes the targeted condition.
- “Instruction Subcode” provides the opcode suffix added to the main opcode to specify the test condition.
- “Status Flags Setting” describes the flag setting.

**Table B-1. EFLAGS Condition Codes**

| Mnemonic (cc)  | Condition Tested For                      | Instruction Subcode | Status Flags Setting    |
|----------------|-------------------------------------------|---------------------|-------------------------|
| O              | Overflow                                  | 0000                | OF = 1                  |
| NO             | No overflow                               | 0001                | OF = 0                  |
| B<br>C<br>NAE  | Below<br>Carry<br>Neither above nor equal | 0010                | CF = 1                  |
| NB<br>NC<br>AE | Not below<br>Not carry<br>Above or equal  | 0011                | CF = 0                  |
| E<br>Z         | Equal<br>Zero                             | 0100                | ZF = 1                  |
| NE<br>NZ       | Not equal<br>Not zero                     | 0101                | ZF = 0                  |
| BE<br>NA       | Below or equal<br>Not above               | 0110                | (CF OR ZF) = 1          |
| NBE<br>A       | Neither below nor equal<br>Above          | 0111                | (CF OR ZF) = 0          |
| S              | Sign                                      | 1000                | SF = 1                  |
| NS             | No sign                                   | 1001                | SF = 0                  |
| P<br>PE        | Parity<br>Parity even                     | 1010                | PF = 1                  |
| NP<br>PO       | No parity<br>Parity odd                   | 1011                | PF = 0                  |
| L<br>NGE       | Less<br>Neither greater nor equal         | 1100                | (SF XOR OF) = 1         |
| NL<br>GE       | Not less<br>Greater or equal              | 1101                | (SF XOR OF) = 0         |
| LE<br>NG       | Less or equal<br>Not greater              | 1110                | ((SF XOR OF) OR ZF) = 1 |
| NLE<br>G       | Neither less nor equal<br>Greater         | 1111                | ((SF XOR OF) OR ZF) = 0 |

## EFLAGS CONDITION CODES

Many of the test conditions are described in two different ways. For example, LE (less or equal) and NG (not greater) describe the same test condition. Alternate mnemonics are provided to make code more intelligible.

The terms "above" and "below" are associated with the CF flag and refer to the relation between two unsigned integer values. The terms "greater" and "less" are associated with the SF and OF flags and refer to the relation between two signed integer values.

## APPENDIX C FLOATING-POINT EXCEPTIONS SUMMARY

### C.1 OVERVIEW

This appendix shows which of the floating-point exceptions can be generated for:

- x87 FPU instructions — see Table C-2.
- Intel SSE instructions — see Table C-3.
- Intel SSE2 instructions — see Table C-4.
- Intel SSE3 instructions — see Table C-5.
- Intel SSE4 instructions — see Table C-6.

Table C-1 lists types of floating-point exceptions that potentially can be generated by the x87 FPU and by Intel SSE, SSE2, and SSE3 instructions.

**Table C-1. x87 FPU and SIMD Floating-Point Exceptions**

| Floating-point Exception | Description                                                                                                         |
|--------------------------|---------------------------------------------------------------------------------------------------------------------|
| #IS                      | Invalid-operation exception for stack underflow or stack overflow (can only be generated for x87 FPU instructions)* |
| #IA or #I                | Invalid-operation exception for invalid arithmetic operands and unsupported formats*                                |
| #D                       | Denormal-operand exception                                                                                          |
| #Z                       | Divide-by-zero exception                                                                                            |
| #O                       | Numeric-overflow exception                                                                                          |
| #U                       | Numeric-underflow exception                                                                                         |
| #P                       | Inexact-result (precision) exception                                                                                |

**NOTE:**

\* The x87 FPU instruction set generates two types of invalid-operation exceptions: #IS (stack underflow or stack overflow) and #IA (invalid arithmetic operation due to invalid arithmetic operands or unsupported formats). Intel SSE, SSE2, and SSE3 instructions potentially generate #I (invalid operation exceptions due to invalid arithmetic operands or unsupported formats).

The floating-point exceptions shown in Table C-1 (except for #D and #IS) are defined in IEEE Standard 754-1985 for Binary Floating-Point Arithmetic. See Section 4.9.1, "Floating-Point Exception Conditions," for a detailed discussion of floating-point exceptions.

### C.2 X87 FPU INSTRUCTIONS

Table C-2 lists the x87 FPU instructions in alphabetical order. For each instruction, it summarizes the floating-point exceptions that the instruction can generate.

**Table C-2. Exceptions Generated with x87 FPU Floating-Point Instructions**

| Mnemonic | Instruction        | #IS | #IA | #D | #Z | #O | #U | #P |
|----------|--------------------|-----|-----|----|----|----|----|----|
| F2XM1    | Exponential        | Y   | Y   | Y  |    |    | Y  | Y  |
| FABS     | Absolute value     | Y   |     |    |    |    |    |    |
| FADD(P)  | Add floating-point | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FBLD     | BCD load           | Y   |     |    |    |    |    |    |

**Table C-2. Exceptions Generated with x87 FPU Floating-Point Instructions (Contd.)**

| Mnemonic                       | Instruction                               | #IS | #IA | #D | #Z | #O | #U | #P |
|--------------------------------|-------------------------------------------|-----|-----|----|----|----|----|----|
| FBSTP                          | BCD store and pop                         | Y   | Y   |    |    |    |    | Y  |
| FCHS                           | Change sign                               | Y   |     |    |    |    |    |    |
| FCLEX                          | Clear exceptions                          |     |     |    |    |    |    |    |
| FCMOV $cc$                     | Floating-point conditional move           | Y   |     |    |    |    |    |    |
| FCOM, FCOMP, FCOMPP            | Compare floating-point                    | Y   | Y   | Y  |    |    |    |    |
| FCOMI, FCOMIP, FUCOMI, FUCOMIP | Compare floating-point and set EFLAGS     | Y   | Y   | Y  |    |    |    |    |
| FCOS                           | Cosine                                    | Y   | Y   | Y  |    |    |    | Y  |
| FDECSTP                        | Decrement stack pointer                   |     |     |    |    |    |    |    |
| FDIV(R)(P)                     | Divide floating-point                     | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FFREE                          | Free register                             |     |     |    |    |    |    |    |
| FIADD                          | Integer add                               | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FICOM(P)                       | Integer compare                           | Y   | Y   | Y  |    |    |    |    |
| FIDIV                          | Integer divide                            | Y   | Y   | Y  | Y  |    | Y  | Y  |
| FIDIVR                         | Integer divide reversed                   | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FILD                           | Integer load                              | Y   |     |    |    |    |    |    |
| FIMUL                          | Integer multiply                          | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FINCSTP                        | Increment stack pointer                   |     |     |    |    |    |    |    |
| FINIT                          | Initialize processor                      |     |     |    |    |    |    |    |
| FIST(P)                        | Integer store                             | Y   | Y   |    |    |    |    | Y  |
| FISTTP                         | Truncate to integer<br>(SSE3 instruction) | Y   | Y   |    |    |    |    | Y  |
| FISUB(R)                       | Integer subtract                          | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FLD extended or stack          | Load floating-point                       | Y   |     |    |    |    |    |    |
| FLD single or double           | Load floating-point                       | Y   | Y   | Y  |    |    |    |    |
| FLD1                           | Load + 1.0                                | Y   |     |    |    |    |    |    |
| FLDCW                          | Load Control word                         | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FLDENV                         | Load environment                          | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FLDL2E                         | Load $\log_2 e$                           | Y   |     |    |    |    |    |    |
| FLDL2T                         | Load $\log_2 10$                          | Y   |     |    |    |    |    |    |
| FLDLG2                         | Load $\log_{10} 2$                        | Y   |     |    |    |    |    |    |
| FLDLN2                         | Load $\log_e 2$                           | Y   |     |    |    |    |    |    |
| FLDPI                          | Load $\pi$                                | Y   |     |    |    |    |    |    |
| FLDZ                           | Load + 0.0                                | Y   |     |    |    |    |    |    |
| FMUL(P)                        | Multiply floating-point                   | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FNOP                           | No operation                              |     |     |    |    |    |    |    |
| FPATAN                         | Partial arctangent                        | Y   | Y   | Y  |    |    | Y  | Y  |
| FPREM                          | Partial remainder                         | Y   | Y   | Y  |    |    | Y  |    |
| FPREM1                         | IEEE partial remainder                    | Y   | Y   | Y  |    |    | Y  |    |

**Table C-2. Exceptions Generated with x87 FPU Floating-Point Instructions (Contd.)**

| Mnemonic                 | Instruction                      | #IS | #IA | #D | #Z | #O | #U | #P |
|--------------------------|----------------------------------|-----|-----|----|----|----|----|----|
| FPTAN                    | Partial tangent                  | Y   | Y   | Y  |    |    | Y  | Y  |
| FRNDINT                  | Round to integer                 | Y   | Y   | Y  |    |    |    | Y  |
| FRSTOR                   | Restore state                    | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FSAVE                    | Save state                       |     |     |    |    |    |    |    |
| FSCALE                   | Scale                            | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FSIN                     | Sine                             | Y   | Y   | Y  |    |    | Y  | Y  |
| FSINCOS                  | Sine and cosine                  | Y   | Y   | Y  |    |    | Y  | Y  |
| FSQRT                    | Square root                      | Y   | Y   | Y  |    |    |    | Y  |
| FST(P) stack or extended | Store floating-point             | Y   |     |    |    |    |    |    |
| FST(P) single or double  | Store floating-point             | Y   | Y   |    |    | Y  | Y  | Y  |
| FSTCW                    | Store control word               |     |     |    |    |    |    |    |
| FSTENV                   | Store environment                |     |     |    |    |    |    |    |
| FSTSW (AX)               | Store status word                |     |     |    |    |    |    |    |
| FSUB(R)(P)               | Subtract floating-point          | Y   | Y   | Y  |    | Y  | Y  | Y  |
| FTST                     | Test                             | Y   | Y   | Y  |    |    |    |    |
| FUCOM(P)(P)              | Unordered compare floating-point | Y   | Y   | Y  |    |    |    |    |
| FWAIT                    | CPU Wait                         |     |     |    |    |    |    |    |
| FXAM                     | Examine                          |     |     |    |    |    |    |    |
| FXCH                     | Exchange registers               | Y   |     |    |    |    |    |    |
| FXTRACT                  | Extract                          | Y   | Y   | Y  | Y  |    |    |    |
| FYL2X                    | Logarithm                        | Y   | Y   | Y  | Y  | Y  | Y  | Y  |
| FYL2XP1                  | Logarithm epsilon                | Y   | Y   | Y  |    | Y  | Y  | Y  |

## C.3 INTEL® SSE INSTRUCTIONS

Table C-3 lists the Intel SSE instructions with at least one of the following characteristics:

- Has floating-point operands.
- Generates floating-point results.
- Reads or writes floating-point status and control information.

The table also summarizes the floating-point exceptions that each instruction can generate.

**Table C-3. Exceptions Generated with Intel® SSE Instructions**

| Mnemonic | Instruction                    | #I | #D | #Z | #O | #U | #P |
|----------|--------------------------------|----|----|----|----|----|----|
| ADDPS    | Packed add.                    | Y  | Y  |    | Y  | Y  | Y  |
| ADDSS    | Scalar add.                    | Y  | Y  |    | Y  | Y  | Y  |
| ANDNPS   | Packed logical INVERT and AND. |    |    |    |    |    |    |
| ANDPS    | Packed logical AND.            |    |    |    |    |    |    |
| CMPPS    | Packed compare.                | Y  | Y  |    |    |    |    |
| CMPSS    | Scalar compare.                | Y  | Y  |    |    |    |    |

Table C-3. Exceptions Generated with Intel® SSE Instructions (Contd.)

| Mnemonic  | Instruction                                                                                                                                               | #I | #D | #Z | #O | #U | #P |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|----|----|----|----|----|----|
| COMISS    | Scalar ordered compare lower SP FP numbers and set the status flags.                                                                                      | Y  | Y  |    |    |    |    |
| CVTPI2PS  | Convert two 32-bit signed integers from MM2/Mem to two SP FP.                                                                                             |    |    |    |    |    | Y  |
| CVTPS2PI  | Convert lower two SP FP from XMM/Mem to two 32-bit signed integers in MM using rounding specified by MXCSR.                                               | Y  |    |    |    |    | Y  |
| CVTSI2SS  | Convert one 32-bit or 64-bit signed integer from Integer Reg/Mem to one SP FP.                                                                            |    |    |    |    |    | Y  |
| CVTSS2SI  | Convert one SP FP from XMM/Mem to one 32-bit or 64-bit signed integer using rounding mode specified by MXCSR, and move the result to an integer register. | Y  |    |    |    |    | Y  |
| CVTTPS2PI | Convert two SP FP from XMM2/Mem to two 32-bit signed integers in MM1 using truncate.                                                                      | Y  |    |    |    |    | Y  |
| CVTTSS2SI | Convert lowest SP FP from XMM/Mem to one 32-bit signed integer using truncate, and move the result to an integer register.                                | Y  |    |    |    |    | Y  |
| DIVPS     | Packed divide.                                                                                                                                            | Y  | Y  | Y  | Y  | Y  | Y  |
| DIVSS     | Scalar divide.                                                                                                                                            | Y  | Y  | Y  | Y  | Y  | Y  |
| LDMXCSR   | Load control/status word.                                                                                                                                 |    |    |    |    |    |    |
| MAXPS     | Packed maximum.                                                                                                                                           | Y  | Y  |    |    |    |    |
| MAXSS     | Scalar maximum.                                                                                                                                           | Y  | Y  |    |    |    |    |
| MINPS     | Packed minimum.                                                                                                                                           | Y  | Y  |    |    |    |    |
| MINSS     | Scalar minimum.                                                                                                                                           | Y  | Y  |    |    |    |    |
| MOVAPS    | Move four packed SP values.                                                                                                                               |    |    |    |    |    |    |
| MOVHLPS   | Move packed SP high to low.                                                                                                                               |    |    |    |    |    |    |
| MOVHPS    | Move two packed SP values between memory and the high half of an XMM register.                                                                            |    |    |    |    |    |    |
| MOVLHPS   | Move packed SP low to high.                                                                                                                               |    |    |    |    |    |    |
| MOVLPS    | Move two packed SP values between memory and the low half of an XMM register.                                                                             |    |    |    |    |    |    |
| MOVMSKPS  | Move sign mask to r32.                                                                                                                                    |    |    |    |    |    |    |
| MOVSS     | Move scalar SP number between an XMM register and memory or a second XMM register.                                                                        |    |    |    |    |    |    |
| MOVUPS    | Move unaligned packed data.                                                                                                                               |    |    |    |    |    |    |
| MULPS     | Packed multiply.                                                                                                                                          | Y  | Y  |    | Y  | Y  | Y  |
| MULSS     | Scalar multiply.                                                                                                                                          | Y  | Y  |    | Y  | Y  | Y  |
| ORPS      | Packed OR.                                                                                                                                                |    |    |    |    |    |    |
| RCPPS     | Packed reciprocal.                                                                                                                                        |    |    |    |    |    |    |
| RCPSS     | Scalar reciprocal.                                                                                                                                        |    |    |    |    |    |    |
| RSQRTPS   | Packed reciprocal square root.                                                                                                                            |    |    |    |    |    |    |
| RSQRTSS   | Scalar reciprocal square root.                                                                                                                            |    |    |    |    |    |    |
| SHUFPS    | Shuffle.                                                                                                                                                  |    |    |    |    |    |    |
| SQRTPS    | Square Root of the packed SP FP numbers.                                                                                                                  | Y  | Y  |    |    |    | Y  |
| SQRTSS    | Scalar square root.                                                                                                                                       | Y  | Y  |    |    |    | Y  |

**Table C-3. Exceptions Generated with Intel® SSE Instructions (Contd.)**

| Mnemonic | Instruction                                                     | #I | #D | #Z | #O | #U | #P |
|----------|-----------------------------------------------------------------|----|----|----|----|----|----|
| STMXCSR  | Store control/status word.                                      |    |    |    |    |    |    |
| SUBPS    | Packed subtract.                                                | Y  | Y  |    | Y  | Y  | Y  |
| SUBSS    | Scalar subtract.                                                | Y  | Y  |    | Y  | Y  | Y  |
| UCOMISS  | Unordered compare lower SP FP numbers and set the status flags. | Y  | Y  |    |    |    |    |
| UNPCKHPS | Interleave SP FP numbers.                                       |    |    |    |    |    |    |
| UNPCKLPS | Interleave SP FP numbers.                                       |    |    |    |    |    |    |
| XORPS    | Packed XOR.                                                     |    |    |    |    |    |    |

## C.4 INTEL® SSE2 INSTRUCTIONS

Table C-4 lists the Intel SSE2 instructions with at least one of the following characteristics:

- Floating-point operands.
- Floating-point results.

For each instruction, the table summarizes the floating-point exceptions that the instruction can generate.

**Table C-4. Exceptions Generated with Intel® SSE2 Instructions**

| Instruction | Description                                                                                                          | #I | #D | #Z | #O | #U | #P |
|-------------|----------------------------------------------------------------------------------------------------------------------|----|----|----|----|----|----|
| ADDPD       | Add two packed DP FP numbers from XMM2/Mem to XMM1.                                                                  | Y  | Y  |    | Y  | Y  | Y  |
| ADDSD       | Add the lower DP FP number from XMM2/Mem to XMM1.                                                                    | Y  | Y  |    | Y  | Y  | Y  |
| ANDNPD      | Invert the 128 bits in XMM1 and then AND the result with 128 bits from XMM2/Mem.                                     |    |    |    |    |    |    |
| ANDPD       | Logical And of 128 bits from XMM2/Mem to XMM1 register.                                                              |    |    |    |    |    |    |
| CMPPD       | Compare packed DP FP numbers from XMM2/Mem to packed DP FP numbers in XMM1 register using imm8 as predicate.         | Y  | Y  |    |    |    |    |
| CMPSD       | Compare lowest DP FP number from XMM2/Mem to lowest DP FP number in XMM1 register using imm8 as predicate.           | Y  | Y  |    |    |    |    |
| COMISD      | Compare lower DP FP number in XMM1 register with lower DP FP number in XMM2/Mem and set the status flags accordingly | Y  | Y  |    |    |    |    |
| CVTDQ2PS    | Convert four 32-bit signed integers from XMM/Mem to four SP FP.                                                      |    |    |    |    |    | Y  |
| CVTPS2DQ    | Convert four SP FP from XMM/Mem to four 32-bit signed integers in XMM using rounding specified by MXCSR.             | Y  |    |    |    |    | Y  |
| CVTTPS2DQ   | Convert four SP FP from XMM/Mem to four 32-bit signed integers in XMM using truncate.                                | Y  |    |    |    |    | Y  |
| CVTDQ2PD    | Convert two 32-bit signed integers in XMM2/Mem to 2 DP FP in xmm1 using rounding specified by MXCSR.                 |    |    |    |    |    |    |
| CVTPD2DQ    | Convert two DP FP from XMM2/Mem to two 32-bit signed integers in xmm1 using rounding specified by MXCSR.             | Y  |    |    |    |    | Y  |
| CVTPD2PI    | Convert lower two DP FP from XMM/Mem to two 32-bit signed integers in MM using rounding specified by MXCSR.          | Y  |    |    |    |    | Y  |
| CVTPD2PS    | Convert two DP FP to two SP FP.                                                                                      | Y  | Y  |    | Y  | Y  | Y  |
| CVTPI2PD    | Convert two 32-bit signed integers from MM2/Mem to two DP FP.                                                        |    |    |    |    |    |    |
| CVTPS2PD    | Convert two SP FP to two DP FP.                                                                                      | Y  | Y  |    |    |    |    |

**Table C-4. Exceptions Generated with Intel® SSE2 Instructions (Contd.)**

| Instruction | Description                                                                                                                                                                   | #I | #D | #Z | #O | #U | #P |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|----|----|----|----|----|
| CVTSD2SI    | Convert one DP FP from XMM/Mem to one 32-bit or 64-bit signed integer using rounding mode specified by MXCSR, and move the result to an integer register.                     | Y  |    |    |    |    | Y  |
| CVTSD2SS    | Convert scalar DP FP to scalar SP FP.                                                                                                                                         | Y  | Y  |    | Y  | Y  | Y  |
| CVTSI2SD    | Convert one 32-bit or 64-bit signed integer from Integer Reg/Mem to one DP FP.                                                                                                |    |    |    |    |    |    |
| CVTSS2SD    | Convert scalar SP FP to scalar DP FP.                                                                                                                                         | Y  | Y  |    |    |    |    |
| CVTTPD2DQ   | Convert two DP FP from XMM2/Mem to two 32-bit signed integers in XMM1 using truncate.                                                                                         | Y  |    |    |    |    | Y  |
| CVTTPD2PI   | Convert two DP FP from XMM2/Mem to two 32-bit signed integers in MM1 using truncate.                                                                                          | Y  |    |    |    |    | Y  |
| CVTTSD2SI   | Convert lowest DP FP from XMM/Mem to one 32 bit signed integer using truncate, and move the result to an integer register.                                                    | Y  |    |    |    |    | Y  |
| DIVPD       | Divide packed DP FP numbers in XMM1 by XMM2/Mem                                                                                                                               | Y  | Y  | Y  | Y  | Y  | Y  |
| DIVSD       | Divide lower DP FP numbers in XMM1 by XMM2/Mem                                                                                                                                | Y  | Y  | Y  | Y  | Y  | Y  |
| MAXPD       | Return the maximum DP FP numbers between XMM2/Mem and XMM1.                                                                                                                   | Y  | Y  |    |    |    |    |
| MAXSD       | Return the maximum DP FP number between the lower DP FP numbers from XMM2/Mem and XMM1.                                                                                       | Y  | Y  |    |    |    |    |
| MINPD       | Return the minimum DP numbers between XMM2/Mem and XMM1.                                                                                                                      | Y  | Y  |    |    |    |    |
| MINSD       | Return the minimum DP FP number between the lowest DP FP numbers from XMM2/Mem and XMM1.                                                                                      | Y  | Y  |    |    |    |    |
| MOVAPD      | Move 128 bits representing 2 packed DP data from XMM2/Mem to XMM1 register.<br><br>Or Move 128 bits representing 2 packed DP from XMM1 register to XMM2/Mem.                  |    |    |    |    |    |    |
| MOVHPD      | Move 64 bits representing one DP operand from Mem to upper field of XMM register.<br><br>Or move 64 bits representing one DP operand from upper field of XMM register to Mem. |    |    |    |    |    |    |
| MOVLPD      | Move 64 bits representing one DP operand from Mem to lower field of XMM register.<br><br>Or move 64 bits representing one DP operand from lower field of XMM register to Mem. |    |    |    |    |    |    |
| MOVMSKPD    | Move the sign mask to r32.                                                                                                                                                    |    |    |    |    |    |    |
| MOVSD       | Move 64 bits representing one scalar DP operand from XMM2/Mem to XMM1 register.<br><br>Or move 64 bits representing one scalar DP operand from XMM1 register to XMM2/Mem.     |    |    |    |    |    |    |
| MOVUPD      | Move 128 bits representing 2 DP data from XMM2/Mem to XMM1 register.<br><br>Or move 128 bits representing 2 DP data from XMM1 register to XMM2/Mem.                           |    |    |    |    |    |    |
| MULPD       | Multiply packed DP FP numbers in XMM2/Mem to XMM1.                                                                                                                            | Y  | Y  |    | Y  | Y  | Y  |

**Table C-4. Exceptions Generated with Intel® SSE2 Instructions (Contd.)**

| Instruction | Description                                                                                                           | #I | #D | #Z | #O | #U | #P |
|-------------|-----------------------------------------------------------------------------------------------------------------------|----|----|----|----|----|----|
| MULSD       | Multiply the lowest DP FP number in XMM2/Mem to XMM1.                                                                 | Y  | Y  |    | Y  | Y  | Y  |
| ORPD        | OR 128 bits from XMM2/Mem to XMM1 register.                                                                           |    |    |    |    |    |    |
| SHUFPD      | Shuffle Double.                                                                                                       |    |    |    |    |    |    |
| SQRTPD      | Square Root Packed Double Precision                                                                                   | Y  | Y  |    |    |    | Y  |
| SQRTSD      | Square Root Scaler Double Precision                                                                                   | Y  | Y  |    |    |    | Y  |
| SUBPD       | Subtract Packed Double Precision.                                                                                     | Y  | Y  |    | Y  | Y  | Y  |
| SUBSD       | Subtract Scaler Double Precision.                                                                                     | Y  | Y  |    | Y  | Y  | Y  |
| UCOMISD     | Compare lower DP FP number in XMM1 register with lower DP FP number in XMM2/Mem and set the status flags accordingly. | Y  | Y  |    |    |    |    |
| UNPCKHPD    | Interleaves DP FP numbers from the high halves of XMM1 and XMM2/Mem into XMM1 register.                               |    |    |    |    |    |    |
| UNPCKLPD    | Interleaves DP FP numbers from the low halves of XMM1 and XMM2/Mem into XMM1 register.                                |    |    |    |    |    |    |
| XORPD       | XOR 128 bits from XMM2/Mem to XMM1 register.                                                                          |    |    |    |    |    |    |

## C.5 INTEL® SSE3 INSTRUCTIONS

Table C-5 lists the Intel SSE3 instructions that have at least one of the following characteristics:

- Has floating-point operands.
- Generates floating-point results.

For each instruction, the table summarizes the floating-point exceptions that the instruction can generate.

**Table C-5. Exceptions Generated with Intel® SSE3 Instructions**

| Instruction | Description                                             | #I | #D | #Z | #O | #U | #P |
|-------------|---------------------------------------------------------|----|----|----|----|----|----|
| ADDSD       | Add /Sub packed DP FP numbers from XMM2/Mem to XMM1.    | Y  | Y  |    | Y  | Y  | Y  |
| ADDSS       | Add /Sub packed SP FP numbers from XMM2/Mem to XMM1.    | Y  | Y  |    | Y  | Y  | Y  |
| FISTTP      | See Table C-2.                                          | Y  |    |    |    |    | Y  |
| HADDPD      | Add horizontally packed DP FP numbers XMM2/Mem to XMM1. | Y  | Y  |    | Y  | Y  | Y  |
| HADDPS      | Add horizontally packed SP FP numbers XMM2/Mem to XMM1  | Y  | Y  |    | Y  | Y  | Y  |
| HSUBPD      | Sub horizontally packed DP FP numbers XMM2/Mem to XMM1  | Y  | Y  |    | Y  | Y  | Y  |
| HSUBPS      | Sub horizontally packed SP FP numbers XMM2/Mem to XMM1  | Y  | Y  |    | Y  | Y  | Y  |

Other Intel SSE3 instructions do not generate floating-point exceptions.

## C.6 SSSE3 INSTRUCTIONS

SSSE3 instructions operate on integer data elements. They do not generate floating-point exceptions.

## C.7 INTEL® SSE4 INSTRUCTIONS

Table C-6 lists the Intel SSE4.1 instructions that generate floating-point results.

For each instruction, the table summarizes the floating-point exceptions that the instruction can generate.

Table C-6. Exceptions Generated with Intel® SSE4 Instructions

| Instruction | Description                                     | #I | #D | #Z | #O | #U | #P             |
|-------------|-------------------------------------------------|----|----|----|----|----|----------------|
| DPPD        | DP FP dot product.                              | Y  | Y  |    | Y  | Y  | Y              |
| DPPS        | SP FP dot product.                              | Y  | Y  |    | Y  | Y  | Y              |
| ROUNDPD     | Round packed DP FP values to integer FP values. | Y  |    |    |    |    | Y <sup>1</sup> |
| ROUNDPS     | Round packed SP FP values to integer FP values. | Y  |    |    |    |    | Y <sup>1</sup> |
| ROUNDSD     | Round scalar DP FP value to integer FP value.   | Y  |    |    |    |    | Y <sup>1</sup> |
| ROUNDSS     | Round scalar SP FP value to integer FP value.   | Y  |    |    |    |    | Y <sup>1</sup> |

NOTES:

1. If bit 3 of immediate operand is 0.

Other Intel SSE4.1 and SSE4.2 instructions do not generate floating-point exceptions.

# APPENDIX D

## GUIDELINES FOR WRITING SIMD FLOATING-POINT EXCEPTION HANDLERS

---

See Section 11.5, “Intel® SSE, SSE2, and SSE3 Exceptions,” for a detailed discussion of SIMD floating-point exceptions.

This appendix considers only Intel SSE, SSE2, and SSE3 instructions that can generate numeric (SIMD floating-point) exceptions, and gives an overview of the necessary support for handling such exceptions. This appendix does not address instructions that do not generate floating-point exceptions (such as RSQRTSS, RSQRTPS, RCPSS, or RCPPS), any x87 instructions, or any unlisted instruction.

For detailed information on which instructions generate numeric exceptions, and a listing of those exceptions, refer to Appendix C, “Floating-Point Exceptions Summary.” Non-numeric exceptions are handled in a way similar to that for the standard IA-32 instructions.

### D.1 TWO OPTIONS FOR HANDLING FLOATING-POINT EXCEPTIONS

Just as for x87 FPU floating-point exceptions, the processor takes one of two possible courses of action when an SSE/SSE2/SSE3 instruction raises a floating-point exception:

- If the exception being raised is masked (by setting the corresponding mask bit in the MXCSR to 1), then a default result is produced which is acceptable in most situations. No external indication of the exception is given, but the corresponding exception flags in the MXCSR are set and may be examined later. Note though that for packed operations, an exception flag that is set in the MXCSR will not tell which of the sub-operands caused the event to occur.
- If the exception being raised is not masked (by setting the corresponding mask bit in the MXCSR to 0), a software exception handler previously registered by the user with operating system support will be invoked through the SIMD floating-point exception (#XM, exception 19). This case is discussed below in Section D.2, “Software Exception Handling.”

### D.2 SOFTWARE EXCEPTION HANDLING

The #XM handler is usually part of the system software (the operating system kernel). Note that an interrupt descriptor table (IDT) entry must have been previously set up for exception 19 (refer to Chapter 7, “Interrupt and Exception Handling,” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A). Some compilers use specific run-time libraries to assist in floating-point exception handling. If any x87 FPU floating-point operations are going to be performed that might raise floating-point exceptions, then the exception handling routine must either disable all floating-point exceptions (for example, loading a local control word with FLDCW), or it must be implemented as re-entrant. If this is not the case, the routine has to clear the status flags for x87 FPU exceptions or to mask all x87 FPU floating-point exceptions. For SIMD floating-point exceptions though, the exception flags in MXCSR do not have to be cleared, even if they remain unmasked (but they may still be cleared). Exceptions are in this case precise and occur immediately, and a SIMD floating-point exception status flag that is set when the corresponding exception is unmasked will not generate an exception.

Typical actions performed by this low-level exception handling routine are:

- Incrementing an exception counter for later display or printing.
- Printing or displaying diagnostic information (e.g., the MXCSR and XMM registers).
- Aborting further execution, or using the exception pointers to build an instruction that will run without exception and executing it.
- Storing information about the exception in a data structure that will be passed to a higher level user exception handler.

In most cases (and this applies also to the Intel SSE, SSE2, and SSE3 instructions), there will be three main components of a low-level floating-point exception handler: a prologue, a body, and an epilogue.

The prologue performs functions that must be protected from possible interruption by higher-priority sources - typically saving registers and transferring diagnostic information from the processor to memory. When the critical processing has been completed, the prologue may re-enable interrupts to allow higher-priority interrupt handlers to preempt the exception handler (assuming that the interrupt handler was called through an interrupt gate, meaning that the processor cleared the interrupt enable (IF) flag in the EFLAGS register - refer to Section 6.5.1, "Call and Return Operation for Interrupt or Exception Handling Procedures").

The body of the exception handler examines the diagnostic information and makes a response that is application-dependent. It may range from halting execution, to displaying a message, to attempting to fix the problem and then proceeding with normal execution, to setting up a data structure, calling a higher-level user exception handler and continuing execution upon return from it. This latter case will be assumed in Section D.4, "SIMD Floating-Point Exceptions and the IEEE Standard 754," below.

Finally, the epilogue essentially reverses the actions of the prologue, restoring the processor state so that normal execution can be resumed.

The following example represents a typical exception handler. To link it with Example D-2 that will follow in Section D.4.3, "Example SIMD Floating-Point Emulation Implementation," assume that the body of the handler (not shown here in detail) passes the saved state to a routine that will examine in turn all the sub-operands of the excepting instruction, invoking a user floating-point exception handler if a particular set of sub-operands raises an unmasked (enabled) exception, or emulating the instruction otherwise.

#### Example D-1. SIMD Floating-Point Exception Handler

SIMD\_FP\_EXC\_HANDLER PROC

;PROLOGUE

;SAVE REGISTERS THAT MIGHT BE USED BY THE EXCEPTION HANDLER

|                          |                                       |
|--------------------------|---------------------------------------|
| PUSH EBP                 | ;SAVE EBP                             |
| PUSH EAX                 | ;SAVE EAX                             |
| ...                      |                                       |
| MOV EBP, ESP             | ;SAVE ESP in EBP                      |
| SUB ESP, 512             | ;ALLOCATE 512 BYTES                   |
| AND ESP, 0ffffff0h       | ;MAKE THE ADDRESS 16-BYTE ALIGNED     |
| FXSAVE [ESP]             | ;SAVE FP, MMX, AND SIMD FP STATE      |
| PUSH [EBP+EFLAGS_OFFSET] | ;COPY OLD EFLAGS TO STACK TOP         |
| POPFD                    | ;RESTORE THE INTERRUPT ENABLE FLAG IF |
|                          | ;TO VALUE BEFORE SIMD FP EXCEPTION    |

;BODY

;APPLICATION-DEPENDENT EXCEPTION HANDLING CODE GOES HERE

|                     |                                   |
|---------------------|-----------------------------------|
| LDMXCSR LOCAL_MXCSR | ;LOAD LOCAL MXCSR VALUE IF NEEDED |
| ...                 |                                   |
| ...                 |                                   |

;EPILOGUE

|               |                                    |
|---------------|------------------------------------|
| FXRSTOR [ESP] | ;RESTORE MODIFIED STATE IMAGE      |
| MOV ESP, EBP  | ;DE-ALLOCATE STACK SPACE           |
| ...           |                                    |
| POP EAX       | ;RESTORE EAX                       |
| POP EBP       | ;RESTORE EBP                       |
| IRET          | ;RETURN TO INTERRUPTED CALCULATION |

SIMD\_FP\_EXC\_HANDLER ENDP

## D.3 EXCEPTION SYNCHRONIZATION

An SSE/SSE2/SSE3 instruction can execute in parallel with other similar instructions, with integer instructions, and with floating-point or MMX instructions. Unlike for x87 instructions, special precaution for exception synchronization is not necessary in this case. This is because floating-point exceptions for SSE/SSE2/SSE3 instructions occur immediately and are not delayed until a subsequent floating-point instruction is executed. However, floating-point emulation may be necessary when unmasked floating-point exceptions are generated.

## D.4 SIMD FLOATING-POINT EXCEPTIONS AND THE IEEE STANDARD 754

SSE/SSE2/SSE3 extensions are 100% compatible with the IEEE Standard 754 for Floating-Point Arithmetic, satisfying all of its mandatory requirements (when the flush-to-zero or denormals-are-zeros modes are not enabled). But a programming environment that includes SSE/SSE2/SSE3 instructions will comply with both the obligatory and the strongly recommended requirements of the IEEE Standard 754 regarding floating-point exception handling, only as a combination of hardware and software (which is acceptable). The standard states that a user should be able to request a trap on any of the five floating-point exceptions (note that the denormal exception is an IA-32 addition), and it also specifies the values (operands or result) to be delivered to the exception handler.

The main issue is that for SSE/SSE2/SSE3 instructions that raise post-computation exceptions (traps: overflow, underflow, or inexact), unlike for x87 FPU instructions, the processor does not provide the result recommended by IEEE Standard 754 to the user handler. If a user program needs the result of an instruction that generated a post-computation exception, it is the responsibility of the software to produce this result by emulating the faulting SSE/SSE2/SSE3 instruction. Another issue is that the standard does not specify explicitly how to handle multiple floating-point exceptions that occur simultaneously. For packed operations, a logical OR of the flags that would be set by each sub-operation is used to set the exception flags in the MXCSR. The following subsections present one possible way to solve these problems.

### D.4.1 Floating-Point Emulation

Every operating system must provide a kernel level floating-point exception handler (a template was presented in Section D.2, “Software Exception Handling,” above). In the following discussion, assume that a user mode floating-point exception filter is supplied for SIMD floating-point exceptions (for example as part of a library of C functions), that a user program can invoke in order to handle unmasked exceptions. The user mode floating-point exception filter (not shown here) has to be able to emulate the subset of Intel SSE, SSE2, and SSE3 instructions that can generate numeric exceptions, and has to be able to invoke a user provided floating-point exception handler for floating-point exceptions. When a floating-point exception that is not masked is raised by an Intel SSE, SSE2, and SSE3 instruction, the low-level floating-point exception handler will be called. This low-level handler may in turn call the user mode floating-point exception filter. The filter function receives the original operands of the excepting instruction as no results are provided by the hardware, whether a pre-computation or a post-computation exception has occurred. The filter will unpack the operands into up to four sets of sub-operands, and will submit them one set at a time to an emulation function (See Example D-2 in Section D.4.3, “Example SIMD Floating-Point Emulation Implementation.”) The emulation function will examine the sub-operands, and will possibly redo the necessary calculation.

Two cases are possible:

- If an unmasked (enabled) exception would occur in this process, the emulation function will return to its caller (the filter function) with the appropriate information. The filter will invoke a (previously registered) user floating-point exception handler for this set of sub-operands, and will record the result upon return from the user handler (provided the user handler allows continuation of the execution).
- If no unmasked (enabled) exception would occur, the emulation function will determine and will return to its caller the result of the operation for the current set of sub-operands (it has to be IEEE Standard 754 compliant). The filter function will record the result (plus any new flag settings).

The user level filter function will then call the emulation function for the next set of sub-operands (if any). When done with all the operand sets, the partial results will be packed (if the excepting instruction has a packed floating-point result, which is true for most SSE/SSE2/SSE3 numeric instructions) and the filter will return to the low-level exception handler, which in turn will return from the interruption, allowing execution to continue. Note that the

instruction pointer (EIP) has to be altered to point to the instruction following the excepting instruction, in order to continue execution correctly.

If a user mode floating-point exception filter is not provided, then all the work for decoding the excepting instruction, reading its operands, emulating the instruction for the components of the result that do not correspond to unmasked floating-point exceptions, and providing the compounded result will have to be performed by the user-provided floating-point exception handler.

Actual emulation might have to take place for one operand or pair of operands for scalar operations, and for all sub-operands or pairs of sub-operands for packed operations. The steps to perform are the following:

- The excepting instruction has to be decoded and the operands have to be read from the saved context.
- The instruction has to be emulated for each (pair of) sub-operand(s); if no floating-point exception occurs, the partial result has to be saved; if a masked floating-point exception occurs, the masked result has to be produced through emulation and saved, and the appropriate status flags have to be set; if an unmasked floating-point exception occurs, the result has to be generated by the user provided floating-point exception handler, and the appropriate status flags have to be set.
- The partial results have to be combined and written to the context that will be restored upon application program resumption.

A diagram of the control flow in handling an unmasked floating-point exception is presented below.

![A flowchart showing the control flow for handling unmasked floating-point exceptions. It consists of four rectangular boxes stacked vertically, connected by double-headed arrows. The boxes are labeled: 'User Application' at the top, followed by 'Low-Level Floating-Point Exception Handler', then 'User Level Floating-Point Exception Filter', and finally 'User Floating-Point Exception Handler' at the bottom.](62040663728a6cf721953152ce085937_img.jpg)

```

graph TD
    UA[User Application] <--> LLFPEH[Low-Level Floating-Point Exception Handler]
    LLFPEH <--> ULFPEF[User Level Floating-Point Exception Filter]
    ULFPEF <--> UFPEH[User Floating-Point Exception Handler]
  
```

A flowchart showing the control flow for handling unmasked floating-point exceptions. It consists of four rectangular boxes stacked vertically, connected by double-headed arrows. The boxes are labeled: 'User Application' at the top, followed by 'Low-Level Floating-Point Exception Handler', then 'User Level Floating-Point Exception Filter', and finally 'User Floating-Point Exception Handler' at the bottom.

**Figure D-1. Control Flow for Handling Unmasked Floating-Point Exceptions**

From the user-level floating-point filter, Example D-2 in Section D.4.3, “Example SIMD Floating-Point Emulation Implementation,” presents only the floating-point emulation part. In order to understand the actions involved, the expected response to exceptions has to be known for all Intel SSE, SSE2, and SSE3 numeric instructions in two situations: with exceptions enabled (unmasked result), and with exceptions disabled (masked result). The latter can be found in Section 6.5, “Interrupts and Exceptions.” The response to NaN operands that do not raise an exception is specified in Section 4.8.3.4, “NaNs.” Operations on NaNs are explained in the same source. This response is also discussed in more detail in the next subsection, along with the unmasked and masked responses to floating-point exceptions.

## D.4.2 Intel® SSE, SSE2, and SSE3 Response To Floating-Point Exceptions

This subsection specifies the unmasked response expected from the Intel SSE, SSE2, and SSE3 instructions that raise floating-point exceptions. The masked response is given in parallel, as it is necessary in the emulation process

of the instructions that raise unmasked floating-point exceptions. The response to NaN operands is also included in more detail than in Section 4.8.3.4, “NaNs.” For floating-point exception priority, refer to “Priority Among Simultaneous Exceptions and Interrupts” in Chapter 7, “Interrupt and Exception Handling,” of the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3A.

### D.4.2.1 Numeric Exceptions

There are six classes of numeric (floating-point) exception conditions that can occur: Invalid operation (#I), Divide-by-Zero (#Z), Denormal Operand (#D), Numeric Overflow (#O), Numeric Underflow (#U), and Inexact Result (precision) (#P). #I, #Z, #D are pre-computation exceptions (floating-point faults), detected before the arithmetic operation. #O, #U, #P are post-computation exceptions (floating-point traps).

Users can control how the Intel SSE, SSE2, and SSE3 floating-point exceptions are handled by setting the mask/unmask bits in MXCSR. Masked exceptions are handled by the processor, or by software if they are combined with unmasked exceptions occurring in the same instruction. Unmasked exceptions are usually handled by the low-level exception handler, in conjunction with user-level software.

### D.4.2.2 Results of Operations with NaN Operands or a NaN Result for Intel® SSE, SSE2, and SSE3 Numeric Instructions

The tables below (E-1 through E-10) specify the response of Intel SSE, SSE2, and SSE3 instructions to NaN inputs, or to other inputs that lead to NaN results.

These results will be referenced by subsequent tables (e.g., E-10). Most operations do not raise an invalid exception for quiet NaN operands, but even so, they will have higher precedence over raising floating-point exceptions other than invalid operation.

Note that the single precision QNaN Indefinite value is FFC00000H, the double precision QNaN Indefinite value is FFF8000000000000H, and the Integer Indefinite value is 80000000H (not a floating-point number, but it can be the result of a conversion instruction from floating-point to integer).

For an unmasked exception, no result will be provided by the hardware to the user handler. If a user registered floating-point exception handler is invoked, it may provide a result for the excepting instruction, that will be used if execution of the application code is continued after returning from the interruption.

In Tables D-1 through Table D-12, the specified operands cause an invalid exception, unless the unmasked result is marked with “not an exception”. In this latter case, the unmasked and masked results are the same.

**Table D-1. ADDPS, ADDSS, SUBPS, SUBSS, MULPS, MULSS, DIVPS, DIVSS, ADDPD, ADDSD, SUBPD, SUBSD, MULPD, MULSD, DIVPD, DIVSD, ADDSUBPS, ADDSUBPD, HADDPS, HADDPD, HSUBPS, and HSUBPD**

| Source Operands             | Masked Result                                                  | Unmasked Result          |
|-----------------------------|----------------------------------------------------------------|--------------------------|
| SNaN1 op <sup>1</sup> SNaN2 | SNaN1   00400000H or<br>SNaN1   0008000000000000H <sup>2</sup> | None                     |
| SNaN1 op QNaN2              | SNaN1   00400000H or<br>SNaN1   0008000000000000H <sup>2</sup> | None                     |
| QNaN1 op SNaN2              | QNaN1                                                          | None                     |
| QNaN1 op QNaN2              | QNaN1                                                          | QNaN1 (not an exception) |
| SNaN op real value          | SNaN   00400000H or<br>SNaN1   0008000000000000H <sup>2</sup>  | None                     |
| Real value op SNaN          | SNaN   00400000H or<br>SNaN1   0008000000000000H <sup>2</sup>  | None                     |
| QNaN op real value          | QNaN                                                           | QNaN (not an exception)  |
| Real value op QNaN          | QNaN                                                           | QNaN (not an exception)  |

**Table D-1. ADDPS, ADDSS, SUBPS, SUBSS, MULPS, MULSS, DIVPS, DIVSS, ADDPD, ADDSD, SUBPD, SUBSD, MULPD, MULSD, DIVPD, DIVSD, ADDSUBPS, ADDSUBPD, HADDPS, HADDPD, HSUBPS, and HSUBPD (Contd.)**

| Source Operands                                                                                   | Masked Result                                        | Unmasked Result |
|---------------------------------------------------------------------------------------------------|------------------------------------------------------|-----------------|
| Neither source operand is SNaN, but #I is signaled (e.g., for Inf - Inf, Inf * 0, Inf / Inf, 0/0) | Single precision or double precision QNaN Indefinite | None            |

**NOTES:**

1. For Tables E-1 to E-12: op denotes the operation to be performed.
2. SNaN | 00400000H is a quiet NaN in single precision format (if SNaN is in single precision) and SNaN | 0008000000000000H is a quiet NaN in double precision format (if SNaN is in double precision), obtained from the signaling NaN given as input.
3. Operations involving only quiet NaNs do not raise floating-point exceptions.

**Table D-2. CMPPS.EQ, CMPSS.EQ, CMPPS.ORD, CMPSS.ORD, CMPPD.EQ, CMPSD.EQ, CMPPD.ORD, and CMPSD.ORD**

| Source Operands        | Masked Result                               | Unmasked Result                                                |
|------------------------|---------------------------------------------|----------------------------------------------------------------|
| NaN op Opd2 (any Opd2) | 00000000H or 0000000000000000H <sup>1</sup> | 00000000H or 0000000000000000H <sup>1</sup> (not an exception) |
| Opd1 op NaN (any Opd1) | 00000000H or 0000000000000000H <sup>1</sup> | 00000000H or 0000000000000000H <sup>1</sup> (not an exception) |

**NOTE:**

1. 32-bit results are for single, and 64-bit results for double precision operations.

**Table D-3. CMPPS.NEQ, CMPSS.NEQ, CMPPS.UNORD, CMPSS.UNORD, CMPPD.NEQ, CMPSD.NEQ, CMPPD.UNORD, and CMPSD.UNORD**

| Source Operands        | Masked Result                               | Unmasked Result                                                |
|------------------------|---------------------------------------------|----------------------------------------------------------------|
| NaN op Opd2 (any Opd2) | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> (not an exception) |
| Opd1 op NaN (any Opd1) | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> (not an exception) |

**NOTE:**

1. 32-bit results are for single, and 64-bit results for double precision operations.

**Table D-4. CMPPS.LT, CMPSS.LT, CMPPS.LE, CMPSS.LE, CMPPD.LT, CMPSD.LT, CMPPD.LE, and CMPSD.LE**

| Source Operands        | Masked Result                               | Unmasked Result |
|------------------------|---------------------------------------------|-----------------|
| NaN op Opd2 (any Opd2) | 00000000H or 0000000000000000H <sup>1</sup> | None            |
| Opd1 op NaN (any Opd1) | 00000000H or 0000000000000000H <sup>1</sup> | None            |

**NOTE:**

1. 32-bit results are for single, and 64-bit results for double precision operations.

**Table D-5. CMPPS.NLT, CMPSS.NLT, CMPPS.NLE, CMPSS.NLE, CMPPD.NLT, CMPSD.NLT, CMPPD.NLE, and CMPSD.NLE**

| Source Operands        | Masked Result                               | Unmasked Result |
|------------------------|---------------------------------------------|-----------------|
| NaN op Opd2 (any Opd2) | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> | None            |
| Opd1 op NaN (any Opd1) | FFFFFFFFH or FFFFFFFFFFFFFFFFH <sup>1</sup> | None            |

**NOTE:**

1. 32-bit results are for single, and 64-bit results for double precision operations.

**Table D-6. COMISS and COMISD**

| Source Operands         | Masked Result                        | Unmasked Result |
|-------------------------|--------------------------------------|-----------------|
| SNaN op Opd2 (any Opd2) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None            |
| Opd1 op SNaN (any Opd1) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None            |
| QNaN op Opd2 (any Opd2) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None            |
| Opd1 op QNaN (any Opd1) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None            |

**Table D-7. UCOMISS and UCOMISD**

| Source Operands                   | Masked Result                        | Unmasked Result                                         |
|-----------------------------------|--------------------------------------|---------------------------------------------------------|
| SNaN op Opd2 (any Opd2)           | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None                                                    |
| Opd1 op SNaN (any Opd1)           | OF, SF, AF = 000<br>ZF, PF, CF = 111 | None                                                    |
| QNaN op Opd2<br>(any Opd2 ≠ SNaN) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | OF, SF, AF = 000<br>ZF, PF, CF = 111 (not an exception) |
| Opd1 op QNaN<br>(any Opd1 ≠ SNaN) | OF, SF, AF = 000<br>ZF, PF, CF = 111 | OF, SF, AF = 000<br>ZF, PF, CF = 111 (not an exception) |

**Table D-8. CVTPS2PI, CVTSS2SI, CVTTPS2PI, CVTTSS2SI, CVTPD2PI, CVTSD2SI, CVTTPD2PI, CVTTSD2SI, CVTPS2DQ, CVTTPS2DQ, CVTPD2DQ, and CVTTPD2DQ**

| Source Operand | Masked Result                                                      | Unmasked Result |
|----------------|--------------------------------------------------------------------|-----------------|
| SNaN           | 80000000H or 8000000000000000 <sup>1</sup><br>(Integer Indefinite) | None            |
| QNaN           | 80000000H or 8000000000000000 <sup>1</sup><br>(Integer Indefinite) | None            |

**NOTE:**

1. 32-bit results are for single, and 64-bit results for double precision operations.

Table D-9. MAXPS, MAXSS, MINPS, MINSS, MAXPD, MAXSD, MINPD, and MINSD

| Source Operands         | Masked Result | Unmasked Result |
|-------------------------|---------------|-----------------|
| Opd1 op NaN2 (any Opd1) | NaN2          | None            |
| NaN1 op Opd2 (any Opd2) | Opd2          | None            |

**NOTE:**  
1. SNaN and QNaN operands raise an Invalid Operation fault.

Table D-10. SQRTPS, SQRTPS, SQRTSS, SQRTSD, and SQRTSD

| Source Operand                                                               | Masked Result                                                | Unmasked Result         |
|------------------------------------------------------------------------------|--------------------------------------------------------------|-------------------------|
| QNaN                                                                         | QNaN                                                         | QNaN (not an exception) |
| SNaN                                                                         | SNaN   00400000H or<br>SNaN   0008000000000000H <sup>1</sup> | None                    |
| Source operand is not SNaN;<br>but #I is signaled (e.g., for<br>sqrt (-1.0)) | Single precision or<br>double precision QNaN Indefinite      | None                    |

**NOTE:**  
1. SNaN | 00400000H is a quiet NaN in single precision format (if SNaN is in single precision) and SNaN | 0008000000000000H is a quiet NaN in double precision format (if SNaN is in double precision), obtained from the signaling NaN given as input.

Table D-11. CVTPS2PD and CVTSS2SD

| Source Operands | Masked Result     | Unmasked Result                      |
|-----------------|-------------------|--------------------------------------|
| QNaN            | QNaN <sup>1</sup> | QNaN <sup>1</sup> (not an exception) |
| SNaN            | QNaN <sup>2</sup> | None                                 |

**NOTES:**  
1. The double precision output QNaN1 is created from the single precision input QNaN as follows: the sign bit is preserved, the 8-bit exponent FFH is replaced by the 11-bit exponent 7FFH, and the 24-bit significand is extended to a 53-bit significand by appending 29 bits equal to 0.  
2. The double precision output QNaN1 is created from the single precision input SNaN as follows: the sign bit is preserved, the 8-bit exponent FFH is replaced by the 11-bit exponent 7FFH, and the 24-bit significand is extended to a 53-bit significand by pending 29 bits equal to 0. The second most significant bit of the significand is changed from 0 to 1 to convert the signaling NaN into a quiet NaN.

Table D-12. CVTPD2PS and CVTSD2SS

| Source Operands | Masked Result     | Unmasked Result                      |
|-----------------|-------------------|--------------------------------------|
| QNaN            | QNaN <sup>1</sup> | QNaN <sup>1</sup> (not an exception) |
| SNaN            | QNaN <sup>2</sup> | None                                 |

**NOTES:**  
1. The single precision output QNaN1 is created from the double precision input QNaN as follows: the sign bit is preserved, the 11-bit exponent 7FFH is replaced by the 8-bit exponent FFH, and the 53-bit significand is truncated to a 24-bit significand by removing its 29 least significant bits.  
2. The single precision output QNaN1 is created from the double precision input SNaN as follows: the sign bit is preserved, the 11-bit exponent 7FFH is replaced by the 8-bit exponent FFH, and the 53-bit significand is truncated to a 24-bit significand by removing its 29 least significant bits. The second most significant bit of the significand is changed from 0 to 1 to convert the signaling NaN into a quiet NaN.

### D.4.2.3 Condition Codes, Exception Flags, and Response for Masked and Unmasked Numeric Exceptions

In the following, the masked response is what the processor provides when a masked exception is raised by an Intel SSE, SSE2, or SSE3 numeric instruction. The same response is provided by the floating-point emulator for Intel SSE, SSE2, and SSE3 numeric instructions, when certain components of the quadruple input operands generate exceptions that are masked (the emulator also generates the correct answer, as specified by IEEE Standard 754 wherever applicable, in the case when no floating-point exception occurs). The unmasked response is what the emulator provides to the user handler for those components of the packed operands of Intel SSE, SSE2, and SSE3 instructions that raise unmasked exceptions. Note that for pre-computation exceptions (floating-point faults), no result is provided to the user handler. For post-computation exceptions (floating-point traps), a result is provided to the user handler, as specified below.

In the following tables, the result is denoted by 'res', with the understanding that for the actual instruction, the destination coincides with the first source operand (except for COMISS, UCOMISS, COMISD, and UCOMISD, whose destination is the EFLAGS register).

**Table D-13. #I - Invalid Operations**

| Instruction                                                                  | Condition                                               | Masked Response                               | Unmasked Response and Exception Code |
|------------------------------------------------------------------------------|---------------------------------------------------------|-----------------------------------------------|--------------------------------------|
| ADDPS<br>ADDPD<br>ADDSS<br>ADDSD<br>HADDPS<br>HADDPD                         | src1 or src2 <sup>1</sup> = SNaN                        | Refer to Table D-1 for NaN operands, #IA = 1  | src1, src2 unchanged; #IA = 1        |
| ADDSUBPS (the addition component)<br>ADDSUBPD (the addition component)       | src1 = +Inf, src2 = -Inf or<br>src1 = -Inf, src2 = +Inf | res <sup>1</sup> = QNaN Indefinite, #IA = 1   |                                      |
| SUBPS<br>SUBPD<br>SUBSS<br>SUBSD<br>HSUBPS<br>HSUBPD                         | src1 or src2 = SNaN                                     | Refer to Table D-1 for NaN operands, #IA = 1  | src1, src2 unchanged; #IA = 1        |
| ADDSUBPS (the subtraction component)<br>ADDSUBPD (the subtraction component) | src1 = +Inf, src2 = +Inf or<br>src1 = -Inf, src2 = -Inf | res = QNaN Indefinite, #IA = 1                |                                      |
| MULPS<br>MULPD                                                               | src1 or src2 = SNaN                                     | Refer to Table D-1 for NaN operands, #IA = 1  | src1, src2 unchanged; #IA = 1        |
| MULSS<br>MULSD                                                               | src1 = ±Inf, src2 = ±0 or<br>src1 = ±0, src2 = ±Inf     | res = QNaN Indefinite, #IA = 1                |                                      |
| DIVPS<br>DIVPD                                                               | src1 or src2 = SNaN                                     | Refer to Table D-1 for NaN operands, #IA = 1  | src1, src2 unchanged; #IA = 1        |
| DIVSS<br>DIVSD                                                               | src1 = ±Inf, src2 = ±Inf or<br>src1 = ±0, src2 = ±0     | res = QNaN Indefinite, #IA = 1                |                                      |
| SQRTPS<br>SQRTPD<br>SQRTPD<br>SQRTSD                                         | src = SNaN                                              | Refer to Table D-10 for NaN operands, #IA = 1 | src unchanged, #IA = 1               |
|                                                                              | src < 0<br>(note that -0 < 0 is false)                  | res = QNaN Indefinite, #IA = 1                |                                      |

Table D-13. #I - Invalid Operations (Contd.)

| Instruction                                                                                                                                                                                          | Condition                                                                                                                                                                                      | Masked Response                                            | Unmasked Response and Exception Code  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|---------------------------------------|
| MAXPS<br>MAXSS<br>MAXPD<br>MAXSD                                                                                                                                                                     | src1 = NaN or src2 = NaN                                                                                                                                                                       | res = src2, #IA = 1                                        | src1, src2 unchanged; #IA = 1         |
| MINPS<br>MINSS<br>MINPD<br>MINSD                                                                                                                                                                     | src1 = NaN or src2 = NaN                                                                                                                                                                       | res = src2, #IA = 1                                        | src1, src2 unchanged; #IA = 1         |
| CMPPS.LT<br>CMPPS.LE<br>CMPPS.NLT<br>CMPPS.NLE<br>CMPSS.LT<br>CMPSS.LE<br>CMPSS.NLT<br>CMPSS.NLE<br>CMPPD.LT<br>CMPPD.LE<br>CMPPD.NLT<br>CMPPD.NLE<br>CMPSD.LT<br>CMPSD.LE<br>CMPSD.NLT<br>CMPSD.NLE | src1 = NaN or src2 = NaN                                                                                                                                                                       | Refer to Table D-4 and Table D-5 for NaN operands; #IA = 1 | src1, src2 unchanged; #IA = 1         |
| COMISS<br>COMISD                                                                                                                                                                                     | src1 = NaN or src2 = NaN                                                                                                                                                                       | Refer to Table D-6 for NaN operands                        | src1, src2, EFLAGS unchanged; #IA = 1 |
| UCOMISS<br>UCOMISD                                                                                                                                                                                   | src1 = SNaN or src2 = SNaN                                                                                                                                                                     | Refer to Table D-7 for NaN operands                        | src1, src2, EFLAGS unchanged; #IA = 1 |
| CVTPS2PI<br>CVTSS2SI<br>CVTPD2PI<br>CVTSD2SI<br>CVTPS2DQ<br>CVTPD2DQ                                                                                                                                 | src = NaN, $\pm\text{Inf}$ , or<br>$ (\text{src})_{\text{rnd}}  > 7\text{FFFFFFFH}$ and $(\text{src})_{\text{rnd}} \neq 80000000\text{H}$<br><br>See Note <sup>2</sup> for information on rnd. | res = Integer Indefinite, #IA = 1                          | src unchanged, #IA = 1                |
| CVTTPS2PI<br>CVTTSS2SI<br>CVTTPD2PI<br>CVTTSD2SI<br>CVTTPS2DQ<br>CVTTPD2DQ                                                                                                                           | src = NaN, $\pm\text{Inf}$ , or<br>$ (\text{src})_{\text{rz}}  > 7\text{FFFFFFFH}$ and $(\text{src})_{\text{rz}} \neq 80000000\text{H}$<br><br>See Note <sup>2</sup> for information on rz.    | res = Integer Indefinite, #IA = 1                          | src unchanged, #IA = 1                |

**Table D-13. #I - Invalid Operations (Contd.)**

| Instruction          | Condition  | Masked Response                      | Unmasked Response and Exception Code |
|----------------------|------------|--------------------------------------|--------------------------------------|
| CVTPS2PD<br>CVTSS2SD | src = SNAN | Refer to Table D-11 for NaN operands | src unchanged,<br>#IA = 1            |
| CVTPD2PS<br>CVTSD2SS | src = SNAN | Refer to Table D-12 for NaN operands | src unchanged,<br>#IA = 1            |

**NOTES:**

- For Tables E-13 to E-18:
  - src denotes the single source operand of a unary operation.
  - src1, src2 denote the first and second source operand of a binary operation.
  - res denotes the numerical result of an operation.
- rnd signifies the user rounding mode from MXCSR, and rz signifies the rounding mode toward zero. (truncate), when rounding a floating-point value to an integer. For more information, refer to Table 4-9.
- For NAN encodings, see Table 4-3.

**Table D-14. #Z - Divide-by-Zero**

| Instruction                      | Condition                                                      | Masked Response                     | Unmasked Response and Exception Code |
|----------------------------------|----------------------------------------------------------------|-------------------------------------|--------------------------------------|
| DIVPS<br>DIVSS<br>DIVPD<br>DIVPS | src1 = finite non-zero (normal, or denormal)<br>src2 = $\pm 0$ | res = $\pm \text{Inf}$ ,<br>#ZE = 1 | src1, src2 unchanged;<br>#ZE = 1     |

Table D-15. #D - Denormal Operand

| Instruction                                                                                                                                                                                                                                                                                                                                                                  | Condition                                                                                | Masked Response                                                                                                                                                      | Unmasked Response and Exception Code                                                                                  |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| ADDPS<br>ADDPD<br>ADDSUBPS<br>ADDSUBPD<br>HADDPS<br>HADDPD<br>SUBPS<br>SUBPD<br>HSUBPS<br>HSUBPD<br>MULPS<br>MULPD<br>DIVPS<br>DIVPD<br>SQRTPS<br>SQRTPD<br>MAXPS<br>MAXPD<br>MINPS<br>MINPD<br>ADDSS<br>ADDSD<br>SUBSS<br>SUBSD<br>MULSS<br>MULSD<br>DIVSS<br>DIVSD<br>SQRTSS<br>SQRTSD<br>MAXSS<br>MAXSD<br>MINSS<br>MINSD<br>CVTPS2PD<br>CVTSS2SD<br>CVTPD2PS<br>CVTSD2SS | src1 = denormal <sup>1</sup> or<br>src2 = denormal (and<br>the DAZ bit in MXCSR<br>is 0) | res = Result rounded to the<br>destination precision and using the<br>bounded exponent, but only if no<br>unmasked post-computation<br>exception occurs;<br>#DE = 1. | src1, src2 unchanged;<br>#DE = 1<br><br>Note that SQRT, CVTPS2PD,<br>CVTSS2SD, CVTPD2PS, CVTSD2SS<br>have only 1 src. |
| CMPPS<br>CMPPD<br>CMPSS<br>CMPSD                                                                                                                                                                                                                                                                                                                                             | src1 = denormal <sup>1</sup> or<br>src2 = denormal (and<br>the DAZ bit in MXCSR<br>is 0) | Comparison result, stored in the<br>destination register;<br>#DE = 1                                                                                                 | src1, src2 unchanged;<br>#DE = 1                                                                                      |
| COMISS<br>COMISD<br>UCOMISS<br>UCOMISD                                                                                                                                                                                                                                                                                                                                       | src1 = denormal <sup>1</sup> or<br>src2 = denormal (and<br>the DAZ bit in MXCSR<br>is 0) | Comparison result, stored in the<br>EFLAGS register;<br>#DE = 1                                                                                                      | src1, src2 unchanged;<br>#DE = 1                                                                                      |

**NOTE:**

1. For denormal encodings, see Section 4.8.3.2, “Normalized and Denormalized Finite Numbers.”

**Table D-16. #O - Numeric Overflow**

| Instruction                                                                                                                  | Condition                                                     | Masked Response  |        |                                                                                 | Unmasked Response and Exception Code                                                                                                                       |
|------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|------------------|--------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
|                                                                                                                              |                                                               | Rounding         | Sign   | Result & Status Flags                                                           |                                                                                                                                                            |
| ADDPS<br>ADDSUBPS<br>HADDPS<br>SUBPS<br>HSUBPS<br>MULPS<br>DIVPS<br>ADDSS<br>SUBSS<br>MULSS<br>DIVSS<br>CVTPD2PS<br>CVTSD2SS | Rounded result > largest single precision finite normal value | To nearest       | +<br>- | #OE = 1, #PE = 1<br>res = $+\infty$<br>res = $-\infty$                          | res = (result calculated with unbounded exponent and rounded to the destination precision) / $2^{192}$<br>#OE = 1<br>#PE = 1 if the result is inexact      |
|                                                                                                                              |                                                               | Toward $-\infty$ | +<br>- | #OE = 1, #PE = 1<br>res = $1.11...1 * 2^{127}$<br>res = $-\infty$               |                                                                                                                                                            |
|                                                                                                                              |                                                               | Toward $+\infty$ | +<br>- | #OE = 1, #PE = 1<br>res = $+\infty$<br>res = $-1.11...1 * 2^{127}$              |                                                                                                                                                            |
|                                                                                                                              |                                                               | Toward 0         | +<br>- | #OE = 1, #PE = 1<br>res = $1.11...1 * 2^{127}$<br>res = $-1.11...1 * 2^{127}$   |                                                                                                                                                            |
| ADDPD<br>ADDSUBPD<br>HADDPD<br>SUBPD<br>HSUBPD<br>MULPD<br>DIVPD<br>ADDSD<br>SUBSD<br>MULSD<br>DIVSD                         | Rounded result > largest double precision finite normal value | To nearest       | +<br>- | #OE = 1, #PE = 1<br>res = $+\infty$<br>res = $-\infty$                          | res = (result calculated with unbounded exponent and rounded to the destination precision) / $2^{1536}$<br>▪ #OE = 1<br>▪ #PE = 1 if the result is inexact |
|                                                                                                                              |                                                               | Toward $-\infty$ | +<br>- | #OE = 1, #PE = 1<br>res = $1.11...1 * 2^{1023}$<br>res = $-\infty$              |                                                                                                                                                            |
|                                                                                                                              |                                                               | Toward $+\infty$ | +<br>- | #OE = 1, #PE = 1<br>res = $+\infty$<br>res = $-1.11...1 * 2^{1023}$             |                                                                                                                                                            |
|                                                                                                                              |                                                               | Toward 0         | +<br>- | #OE = 1, #PE = 1<br>res = $1.11...1 * 2^{1023}$<br>res = $-1.11...1 * 2^{1023}$ |                                                                                                                                                            |

Table D-17. #U - Numeric Underflow

| Instruction                                                                                                                  | Condition                                                                                                                           | Masked Response                                                                                   | Unmasked Response and Exception Code                                                                                                                       |
|------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ADDPS<br>ADDSUBPS<br>HADDPS<br>SUBPS<br>HSUBPS<br>MULPS<br>DIVPS<br>ADDSS<br>SUBSS<br>MULSS<br>DIVSS<br>CVTPD2PS<br>CVTSD2SS | Result calculated with unbounded exponent and rounded to the destination precision < smallest single precision finite normal value. | res = $\pm 0$ , denormal, or normal<br><br>#UE = 1 and #PE = 1, but only if the result is inexact | res = (result calculated with unbounded exponent and rounded to the destination precision) * $2^{192}$<br>▪ #UE = 1<br>▪ #PE = 1 if the result is inexact  |
| ADDPD<br>ADDSUBPD<br>HADDPD<br>SUBPD<br>HSUBPD<br>MULPD<br>DIVPD<br>ADDSD<br>SUBSD<br>MULSD<br>DIVSD                         | Result calculated with unbounded exponent and rounded to the destination precision < smallest double precision finite normal value. | res = $\pm 0$ , denormal or normal<br><br>#UE = 1 and #PE = 1, but only if the result is inexact  | res = (result calculated with unbounded exponent and rounded to the destination precision) * $2^{1536}$<br>▪ #UE = 1<br>▪ #PE = 1 if the result is inexact |

Table D-18. #P - Inexact Result (Precision)

| Instruction                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Condition                                                          | Masked Response                                                                                                                                                                                                                         | Unmasked Response and Exception Code                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ADDPS<br>ADDPD<br>ADDSUBPS<br>ADDSUBPD<br>HADDPS<br>HADDPD<br>SUBPS<br>SUBPD<br>HSUBPS<br>HSUBPD<br>MULPS<br>MULPD<br>DIVPS<br>DIVPD<br>SQRTPS<br>SQRTPD<br>CVTDQ2PS<br>CVTPI2PS<br>CVTPI2DQ<br>CVTSD2PS<br>CVTSD2DQ<br>CVTSD2SI<br>CVTSD2SS<br>CVTSS2PS<br>CVTSS2DQ<br>CVTSS2SI<br>CVTSS2SS<br>ADDSS<br>ADDSD<br>SUBSS<br>SUBSD<br>MULSS<br>MULSD<br>DIVSS<br>DIVSD<br>SQRTSS<br>SQRTSD<br>CVTSS2SI<br>CVTSS2SS<br>CVTSD2SI<br>CVTSD2SS<br>CVTSS2SI<br>CVTSS2SS | The result is not exactly representable in the destination format. | res = Result rounded to the destination precision and using the bounded exponent, but only if no unmasked underflow or overflow conditions occur (this exception can occur in the presence of a masked underflow or overflow); #PE = 1. | Only if no underflow/overflow condition occurred, or if the corresponding exceptions are masked: <ul style="list-style-type: none"> <li>Set #OE if masked overflow and set result as described above for masked overflow.</li> <li>Set #UE if masked underflow and set result as described above for masked underflow.</li> </ul> If neither underflow nor overflow, res equals the result rounded to the destination precision and using the bounded exponent set #PE = 1. |

### D.4.3 Example SIMD Floating-Point Emulation Implementation

The sample code listed below may be considered as being part of a user-level floating-point exception filter for the intel SSE, SSE2, and SSE3 numeric instructions. It is assumed that the filter function is invoked by a low-level exception handler (invoked for exception 19 when an unmasked floating-point exception occurs), and that it operates as explained in Section D.4.1, "Floating-Point Emulation." The sample code does the emulation only for the SSE instructions for addition, subtraction, multiplication, and division. For this, it uses C code and x87 FPU operations. Operations corresponding to other Intel SSE, SSE2, and SSE3 numeric instructions can be emulated similarly. The example assumes that the emulation function receives a pointer to a data structure specifying a number of input parameters: the operation that caused the exception, a set of sub-operands (unpacked, of type float), the

rounding mode (the precision is always single), exception masks (having the same relative bit positions as in the MXCSR but starting from bit 0 in an unsigned integer), and flush-to-zero and denormals-are-zeros indicators.

The output parameters are a floating-point result (of type float), the cause of the exception (identified by constants not explicitly defined below), and the exception status flags. The corresponding C definition is:

```
typedef struct {
    unsigned int operation;           //SSE or SSE2 operation: ADDPS, ADDSS, ...
    unsigned int operand1_uint32; //first operand value
    unsigned int operand2_uint32; //second operand value (if any)
    float result_fval; // result value (if any)
    unsigned int rounding_mode; //rounding mode
    unsigned int exc_masks; //exception masks, in the order P,U,O,Z,D,I
    unsigned int exception_cause; //exception cause
    unsigned int status_flag_inexact; //inexact status flag
    unsigned int status_flag_underflow; //underflow status flag
    unsigned int status_flag_overflow; //overflow status flag
    unsigned int status_flag_divide_by_zero;
                                   //divide by zero status flag
    unsigned int status_flag_denormal_operand;
                                   //denormal operand status flag
    unsigned int status_flag_invalid_operation;
                                   //invalid operation status flag
    unsigned int ftz; // flush-to-zero flag
    unsigned int daz; // denormals-are-zeros flag
} EXC_ENV;
```

The arithmetic operations exemplified are emulated as follows:

1. If the denormals-are-zeros mode is enabled (the DAZ bit in MXCSR is set to 1), replace all the denormal inputs with zeroes of the same sign (the denormal flag is not affected by this change).
2. Perform the operation using x87 FPU instructions, with exceptions disabled, the original user rounding mode, and single precision. This reveals invalid, denormal, or divide-by-zero exceptions (if there are any) and stores the result in memory as a double precision value (whose exponent range is large enough to look like “unbounded” to the result of the single precision computation).
3. If no unmasked exceptions were detected, determine if the magnitude of the result is less than the smallest normal number that can be represented in single precision format, or greater than the largest normal number that can be represented in single precision format (huge). If an unmasked overflow or underflow occurs, calculate the scaled result that will be handed to the user exception handler, as specified by IEEE Standard 754.
4. If no exception was raised, calculate the result with a “bounded” exponent. If the result is tiny, it requires denormalization (shifting the significand right while incrementing the exponent to bring it into the admissible range of [-126,+127] for single precision floating-point numbers).

The result obtained in step 2 cannot be used because it might incur a double rounding error (it was rounded to 24 bits in step 2, and might have to be rounded again in the denormalization process). To overcome this is, calculate the result as a double precision value, and store it to memory in single precision format.

Rounding first to 53 bits in the significand, and then to 24 never causes a double rounding error (exact properties exist that state when double-rounding error occurs, but for the elementary arithmetic operations, the rule of thumb is that if an infinitely precise result is rounded to  $2p+1$  bits and then again to  $p$  bits, the result is the same as when rounding directly to  $p$  bits, which means that no double-rounding error occurs).

5. If the result is inexact and the inexact exceptions are unmasked, the calculated result will be delivered to the user floating-point exception handler.
6. The flush-to-zero case is dealt with if the result is tiny.

7. The emulation function returns RAISE\_EXCEPTION to the filter function if an exception has to be raised (the exception\_cause field indicates the cause). Otherwise, the emulation function returns DO\_NOT\_RAISE\_EXCEPTION. In the first case, the result is provided by the user exception handler called by the filter function. In the second case, it is provided by the emulation function. The filter function has to collect all the partial results, and to assemble the scalar or packed result that is used if execution is to continue.

### Example D-2. SIMD Floating-Point Emulation

```
// masks for individual status word bits
#define PRECISION_MASK 20H
#define UNDERFLOW_MASK 10H
#define OVERFLOW_MASK 08H
#define ZERODIVIDE_MASK 04H
#define DENORMAL_MASK 02H
#define INVALID_MASK 01H

// 32-bit constants
static unsigned ZERO_ARRAY[] = {00000000H};
#define ZERO *(float *) ZERO_ARRAY
// +0.0
static unsigned NZERO_ARRAY[] = {80000000H};
#define NZERO *(float *) NZERO_ARRAY
// -0.0
static unsigned POSINFF_ARRAY[] = {7f800000H};
#define POSINFF *(float *) POSINFF_ARRAY
// +Inf
static unsigned NEGINFF_ARRAY[] = {ff800000H};
#define NEGINFF *(float *) NEGINFF_ARRAY
// -Inf

// 64-bit constants
static unsigned MIN_SINGLE_NORMAL_ARRAY [] = {00000000H, 38100000H};
#define MIN_SINGLE_NORMAL *(double *) MIN_SINGLE_NORMAL_ARRAY
// +1.0 * 2^-126
static unsigned MAX_SINGLE_NORMAL_ARRAY [] = {70000000H, 47efffffH};
#define MAX_SINGLE_NORMAL *(double *) MAX_SINGLE_NORMAL_ARRAY
// +1.1...1*2^127
static unsigned TWO_TO_192_ARRAY[] = {00000000H, 4bf00000H};
#define TWO_TO_192 *(double *) TWO_TO_192_ARRAY
// +1.0 * 2^192
static unsigned TWO_TO_M192_ARRAY[] = {00000000H, 33f00000H};
#define TWO_TO_M192 *(double *) TWO_TO_M192_ARRAY
// +1.0 * 2^-192

// auxiliary functions
static int isnanf (unsigned int ); // returns 1 if f is a NaN, and 0 otherwise
static float quietf (unsigned int ); // converts a signaling NaN to a quiet
// NaN, and leaves a quiet NaN unchanged
static unsigned int check_for_daz (unsigned int ); // converts denormals
// to zeros of the same sign;
// does not affect any status flags

// emulation of SSE and SSE2 instructions using
// C code and x87 FPU instructions

unsigned int
simd_fp_emulate (EXC_ENV *exc_env)
{
    int uiopd1; // first operand of the add, subtract, multiply, or divide
    int uiopd2; // second operand of the add, subtract, multiply, or divide
    float res; // result of the add, subtract, multiply, or divide
    double dbl_res24; // result with 24-bit significand, but "unbounded" exponent
```

## GUIDELINES FOR WRITING SIMD FLOATING-POINT EXCEPTION HANDLERS

```
// (needed to check tininess, to provide a scaled result to
// an underflow/overflow trap handler, and in flush-to-zero mode)
double dbl_res; // result in double precision format (needed to avoid a
// double rounding error when denormalizing)
unsigned int result_tiny;
unsigned int result_huge;
unsigned short int sw; // 16 bits
unsigned short int cw; // 16 bits

// have to check first for faults (V, D, Z), and then for traps (O, U, I)

// initialize x87 FPU (floating-point exceptions are masked)
__asm {
    fninit;
}

result_tiny = 0;
result_huge = 0;

switch (exc_env->operation) {

    case ADDPS:
    case ADDSS:
    case SUBPS:
    case SUBSS:
    case MULPS:
    case MULSS:
    case DIVPS:
    case DIVSS:

        uiopd1 = exc_env->operand1_uint32; // copy as unsigned int
        // do not copy as float to avoid conversion
        // of SNaN to QNaN by compiled code
        uiopd2 = exc_env->operand2_uint32;
        // do not copy as float to avoid conversion of SNaN
        // to QNaN by compiled code
        uiopd1 = check_for_daz (uiopd1); // operand1 = +0.0 * operand1 if it is
        // denormal and DAZ=1
        uiopd2 = check_for_daz (uiopd2); // operand2 = +0.0 * operand2 if it is
        // denormal and DAZ=1

        // execute the operation and check whether the invalid, denormal, or
        // divide by zero flags are set and the respective exceptions enabled

        // set control word with rounding mode set to exc_env->rounding_mode,
        // single precision, and all exceptions disabled
        switch (exc_env->rounding_mode) {
            case ROUND_TO_NEAREST:
                cw = 003fH; // round to nearest, single precision, exceptions masked
                break;
            case ROUND_DOWN:
                cw = 043fH; // round down, single precision, exceptions masked
                break;
            case ROUND_UP:
                cw = 083fH; // round up, single precision, exceptions masked
                break;
            case ROUND_TO_ZERO:
                cw = 0c3fH; // round to zero, single precision, exceptions masked
                break;
            default:
                ;
        }
        __asm {
            fldcw WORD PTR cw;
        }
    }
}
```

```

}

// compute result and round to the destination precision, with
// "unbounded" exponent (first IEEE rounding)
switch (exc_env->operation) {

case ADDPS:
case ADDSS:
    // perform the addition
    __asm {
        fnclex;
        // load input operands
        fld DWORD PTR uiopd1; // may set denormal or invalid status flags
        fld DWORD PTR uiopd2; // may set denormal or invalid status flags
        faddp st(1), st(0); // may set inexact or invalid status flags
        // store result
        fstp QWORD PTR dbl_res24; // exact
    }
    break;

case SUBPS:
case SUBSS:
    // perform the subtraction
    __asm {
        fnclex;
        // load input operands
        fld DWORD PTR uiopd1; // may set denormal or invalid status flags
        fld DWORD PTR uiopd2; // may set denormal or invalid status flags
        fsubp st(1), st(0); // may set the inexact or invalid status flags

        // store result
        fstp QWORD PTR dbl_res24; // exact
    }
    break;

case MULPS:
case MULSS:
    // perform the multiplication
    __asm {
        fnclex;
        // load input operands
        fld DWORD PTR uiopd1; // may set denormal or invalid status flags
        fld DWORD PTR uiopd2; // may set denormal or invalid status flags
        fmulp st(1), st(0); // may set inexact or invalid status flags

        // store result
        fstp QWORD PTR dbl_res24; // exact
    }
    break;

case DIVPS:
case DIVSS:
    // perform the division
    __asm {
        fnclex;
        // load input operands
        fld DWORD PTR uiopd1; // may set denormal or invalid status flags
        fld DWORD PTR uiopd2; // may set denormal or invalid status flags
        fdivp st(1), st(0); // may set the inexact, divide by zero, or
                            // invalid status flags

        // store result
        fstp QWORD PTR dbl_res24; // exact
    }
    break;

```

## GUIDELINES FOR WRITING SIMD FLOATING-POINT EXCEPTION HANDLERS

```
        default:
            ; // will never occur

    }

    // read status word
    __asm {
        fstsw WORD PTR sw;
    }

    if (sw & ZERODIVIDE_MASK)
    sw = sw & ~DENORMAL_MASK; // clear D flag for (denormal / 0)

    // if invalid flag is set, and invalid exceptions are enabled, take trap
    if (!(exc_env->exc_masks & INVALID_MASK) && (sw & INVALID_MASK)) {
        exc_env->status_flag_invalid_operation = 1;
        exc_env->exception_cause = INVALID_OPERATION;
        return (RAISE_EXCEPTION);
    }

    // checking for NaN operands has priority over denormal exceptions;
    // also fix for the SSE and SSE2
    // differences in treating two NaN inputs between the
    // instructions and other IA-32 instructions
    if (isnanf (uiopd1) || isnanf (uiopd2)) {

        if (isnanf (uiopd1) && isnanf (uiopd2))
            exc_env->result_fval = quietf (uiopd1);
        else
            exc_env->result_fval = (float)dbl_res24; // exact

        if (sw & INVALID_MASK) exc_env->status_flag_invalid_operation = 1;
        return (DO_NOT_RAISE_EXCEPTION);
    }

    // if denormal flag set, and denormal exceptions are enabled, take trap
    if (!(exc_env->exc_masks & DENORMAL_MASK) && (sw & DENORMAL_MASK)) {
        exc_env->status_flag_denormal_operand = 1;
        exc_env->exception_cause = DENORMAL_OPERAND;
        return (RAISE_EXCEPTION);
    }

    // if divide by zero flag set, and divide by zero exceptions are
    // enabled, take trap (for divide only)
    if (!(exc_env->exc_masks & ZERODIVIDE_MASK) && (sw & ZERODIVIDE_MASK)) {
        exc_env->status_flag_divide_by_zero = 1;
        exc_env->exception_cause = DIVIDE_BY_ZERO;
        return (RAISE_EXCEPTION);
    }

    // done if the result is a NaN (QNaN Indefinite)
    res = (float)dbl_res24;
    if (isnanf (*(unsigned int *)&res)) {
        exc_env->result_fval = res; // exact
        exc_env->status_flag_invalid_operation = 1;
        return (DO_NOT_RAISE_EXCEPTION);
    }

    // dbl_res24 is not a NaN at this point

    if (sw & DENORMAL_MASK) exc_env->status_flag_denormal_operand = 1;

    // Note: (dbl_res24 == 0.0 && sw & PRECISION_MASK) cannot occur
    if (-MIN_SINGLE_NORMAL < dbl_res24 && dbl_res24 < 0.0 ||
        0.0 < dbl_res24 && dbl_res24 < MIN_SINGLE_NORMAL) {
```

```

    result_tiny = 1;
}

// check if the result is huge
if (NEG_INFINITY < dbl_res24 && dbl_res24 < -MAX_SINGLE_NORMAL ||
    MAX_SINGLE_NORMAL < dbl_res24 && dbl_res24 < POS_INFINITY) {
    result_huge = 1;
}

// at this point, there are no enabled I,D, or Z exceptions
// to take; the instr.
// might lead to an enabled underflow, enabled underflow and inexact,
// enabled overflow, enabled overflow and inexact, enabled inexact, or
// none of these; if there are no U or O enabled exceptions, re-execute
// the instruction using IA-32 double precision format, and the
// user's rounding mode; exceptions must have
// been disabled before calling
// this function; an inexact exception may be reported on the 53-bit
// fsubp, fmulp, or on both the 53-bit and 24-bit conversions, while an
// overflow or underflow (with traps disabled) may be reported on the
// conversion from dbl_res to res

// check whether there is an underflow, overflow,
// or inexact trap to be taken
// if the underflow traps are enabled and the result is
// tiny, take underflow trap

if (!(exc_env->exc_masks & UNDERFLOW_MASK) && result_tiny) {
    dbl_res24 = TWO_TO_192 * dbl_res24; // exact
    exc_env->status_flag_underflow = 1;
    exc_env->exception_cause = UNDERFLOW;
    exc_env->result_fval = (float)dbl_res24; // exact
    if (sw & PRECISION_MASK) exc_env->status_flag_inexact = 1;
    return (RAISE_EXCEPTION);
}

// if overflow traps are enabled and the result is huge, take
// overflow trap
if (!(exc_env->exc_masks & OVERFLOW_MASK) && result_huge) {
    dbl_res24 = TWO_TO_M192 * dbl_res24; // exact
    exc_env->status_flag_overflow = 1;
    exc_env->exception_cause = OVERFLOW;
    exc_env->result_fval = (float)dbl_res24; // exact
    if (sw & PRECISION_MASK) exc_env->status_flag_inexact = 1;
    return (RAISE_EXCEPTION);
}

// set control word with rounding mode set to exc_env->rounding_mode,
// double precision, and all exceptions disabled
cw = cw | 0200H; // set precision to double
__asm {
    fldcw WORD PTR cw;
}

switch (exc_env->operation) {

    case ADDPS:
    case ADDSS:
        // perform the addition
        __asm {
            // load input operands
            fld DWORD PTR uiopd1; // may set the denormal status flag
            fld DWORD PTR uiopd2; // may set the denormal status flag
            faddp st(1), st(0); // rounded to 53 bits, may set the inexact
                                // status flag

```

## GUIDELINES FOR WRITING SIMD FLOATING-POINT EXCEPTION HANDLERS

```

        // store result
        fstp QWORD PTR dbl_res; // exact, will not set any flag
    }
    break;

case SUBPS:
case SUBSS:
    // perform the subtraction
    __asm {
        // load input operands
        fld DWORD PTR uiopd1; // may set the denormal status flag
        fld DWORD PTR uiopd2; // may set the denormal status flag
        fsubp st(1), st(0);    // rounded to 53 bits, may set the inexact
                                // status flag

        // store result
        fstp QWORD PTR dbl_res; // exact, will not set any flag
    }
    break;

case MULPS:
case MULSS:
    // perform the multiplication
    __asm {
        // load input operands
        fld DWORD PTR uiopd1; // may set the denormal status flag
        fld DWORD PTR uiopd2; // may set the denormal status flag
        fmulp st(1), st(0);    // rounded to 53 bits, exact

        // store result
        fstp QWORD PTR dbl_res; // exact, will not set any flag
    }
    break;

case DIVPS:
case DIVSS:
    // perform the division
    __asm {
        // load input operands
        fld DWORD PTR uiopd1; // may set the denormal status flag
        fld DWORD PTR uiopd2; // may set the denormal status flag
        fdivp st(1), st(0);    // rounded to 53 bits, may set the inexact
                                // status flag

        // store result
        fstp QWORD PTR dbl_res; // exact, will not set any flag
    }
    break;

default:
    ; // will never occur

}

// calculate result for the case an inexact trap has to be taken, or
// when no trap occurs (second IEEE rounding)
res = (float)dbl_res;
    // may set P, U or O; may also involve denormalizing the result

// read status word
__asm {
    fstsw WORD PTR sw;
}

// if inexact traps are enabled and result is inexact, take inexact trap
if (!(exc_env->exc_masks & PRECISION_MASK) &&
    ((sw & PRECISION_MASK) || (exc_env->ftz && result_tiny))) {
    exc_env->status_flag_inexact = 1;
}

```

```

exc_env->exception_cause = INEXACT;
if (result_tiny) {
    exc_env->status_flag_underflow = 1;

    // if ftz = 1 and result is tiny, result = 0.0
    // (no need to check for underflow traps disabled: result tiny and
    // underflow traps enabled would have caused taking an underflow
    // trap above)
    if (exc_env->ftz) {
        if (res > 0.0)
            res = ZEROF;
        else if (res < 0.0)
            res = NZEROF;
        // else leave res unchanged
    }
}
if (result_huge) exc_env->status_flag_overflow = 1;
exc_env->result_fval = res;
return (RAISE_EXCEPTION);
}

// if it got here, then there is no trap to be taken; the following must
// hold: ((the MXCSR U exceptions are disabled or
//
// the MXCSR underflow exceptions are enabled and the underflow flag is
// clear and (the inexact flag is set or the inexact flag is clear and
// the 24-bit result with unbounded exponent is not tiny))
// and (the MXCSR overflow traps are disabled or the overflow flag is
// clear) and (the MXCSR inexact traps are disabled or the inexact flag
// is clear)
//
// in this case, the result has to be delivered (the status flags are
// sticky, so they are all set correctly already)

// read status word to see if result is inexact
__asm {
    fstsw WORD PTR sw;
}

if (sw & UNDERFLOW_MASK) exc_env->status_flag_underflow = 1;
if (sw & OVERFLOW_MASK) exc_env->status_flag_overflow = 1;
if (sw & PRECISION_MASK) exc_env->status_flag_inexact = 1;

// if ftz = 1, and result is tiny (underflow traps must be disabled),
// result = 0.0
if (exc_env->ftz && result_tiny) {
    if (res > 0.0)
        res = ZEROF;
    else if (res < 0.0)
        res = NZEROF;
    // else leave res unchanged

    exc_env->status_flag_inexact = 1;
    exc_env->status_flag_underflow = 1;
}

exc_env->result_fval = res;
if (sw & ZERODIVIDE_MASK) exc_env->status_flag_divide_by_zero = 1;
if (sw & DENORMAL_MASK) exc_env->status_flag_denormal = 1;
if (sw & INVALID_MASK) exc_env->status_flag_invalid_operation = 1;
return (DO_NOT_RAISE_EXCEPTION);

break;

case CMPPS:

```

## GUIDELINES FOR WRITING SIMD FLOATING-POINT EXCEPTION HANDLERS

```
    case CMPSS:

        ...

        break;

    case COMISS:
    case UCOMISS:

        ...

        break;

    case CVTPI2PS:
    case CVTSI2SS:

        ...

        break;

    case CVTPS2PI:
    case CVTSS2SI:
    case CVTTPS2PI:
    case CVTTSS2SI:

        ...

        break;

    case MAXPS:
    case MAXSS:
    case MINPS:
    case MINSS:

        ...

        break;

    case SQRTPS:
    case SQRTSS:

        ...

        break;

    ...

case UNSPEC:

    ...

    break;

default:
    ...

}

}
```

### NOTE

Intel® MPX has been deprecated and will not be available on any future processors.

## E.1 INTEL® MEMORY PROTECTION EXTENSIONS (INTEL® MPX)

Intel® Memory Protection Extensions (Intel® MPX) is a new capability introduced into Intel Architecture. Intel MPX can increase the robustness of software when it is used in conjunction with compiler changes to check memory references, for those references whose compile-time normal intentions are usurped at runtime due to buffer overflow or underflow. Two of the most important goals of Intel MPX are to provide this capability at low performance overhead for newly compiled code, and to provide compatibility mechanisms with legacy software components. A direct benefit Intel MPX provides is hardening software against malicious attacks designed to cause or exploit buffer overruns. This chapter describes the software visible interfaces of this extension.

## E.2 INTRODUCTION

Intel MPX is designed to allow a system (i.e., the logical processor(s) and the OS software) to run both Intel MPX enabled software and legacy software (written for processors without Intel MPX). When executing software containing a mixture of Intel MPX-unaware code (legacy code) and Intel MPX-enabled code, the legacy code does not benefit from Intel MPX, but it also does not experience any change in functionality or reduction in performance. The performance of Intel MPX-enabled code running on processors that do not support Intel MPX may be similar to the use of embedding NOPs in the instruction stream.

Intel MPX is designed such that an Intel MPX enabled application can link with, call into, or be called from legacy software (libraries, etc.) while maintaining existing application binary interfaces (ABIs). And in most cases, the benefit of Intel MPX requires minimal changes to the source code at the application programming interfaces (APIs) to legacy library/applications. As described later, Intel MPX associates **bounds** with pointers in a novel manner, and the Intel MPX hardware uses **bounds** to check that the pointer based accesses are suitably constrained. Intel MPX enabled software is not required to uniformly or universally utilize the new hardware capabilities over all memory references. Specifically, programmers can selectively use Intel MPX to protect a subset of pointers.

The code enabled for Intel MPX benefits from memory protection against vulnerability such as buffer overrun. Therefore there is a heightened incentive for software vendors to adopt this technology. At the same time, the security benefit of Intel MPX-protection can be implemented according to the business priorities of software vendors. A software vendor can choose to adopt Intel MPX in some modules to realize partial benefit from Intel MPX quickly, and introduce Intel MPX in other modules in phases (e.g., some programmer intervention might be required at the interface to legacy calls). This adaptive property of Intel MPX is designed to give software vendors control on their schedule and modularity of adoption. It also allows a software vendor to secure defense for higher priority or more attack-prone software first; and allows the use of Intel MPX features in one phase of software engineering (e.g., testing) and not in another (e.g., general release) as dictated by business realities.

The initial goal of Intel MPX is twofold: (1) provide means to defend a system against attacks that originate external to some trust perimeter where the trust perimeter subsumes the system memory and integral data repositories, and (2) provide means to pinpoint accidental logic defects in pointer usage, by undergirding memory references with hardware based pointer validation.

As with any instruction set extensions, Intel MPX can be used by application developers beyond detecting buffer overflow, the processor does not limit the use of Intel MPX for buffer overflow detection.

## E.3 INTEL MPX PROGRAMMING ENVIRONMENT

Intel MPX introduces new **bounds registers** and new instructions that operate on bounds registers. Intel MPX allows an OS to support user mode software (operating at CPL=3) and supervisor mode software (CPL < 3) to add memory protection capability against buffer overrun. It provides controls to enable Intel MPX extensions for user mode and supervisor mode independently. Intel MPX extensions are designed to allow software to associate bounds with pointers, and allow software to check memory references against the bounds associated with the pointer to prevent out of bound memory access (thus preventing buffer overflow). The bounds registers hold lower bound and upper bound that can be checked when referencing memory. An out-of-bounds memory reference then causes a #BR exception. Intel MPX also introduces configuration facilities that the OS must manage to support enabling of user-mode (and/or supervisor-mode) software operations using bounds registers.

### E.3.1 Detection and Enumeration of Intel MPX Interfaces

Detection of hardware support for processor extended state component is provided by the main CPUID.0DH.00H. Specifically, the return value in EDX:EAX of CPUID.0DH.00H provides a 64-bit wide bit vector of hardware support of processor state components.

If CPUID.07H.00H:EBX.MPX[14] = 1 (the processor supports Intel MPX), CPUID.0DH.00H:EAX[4:3] will enumerate the XSAVE state components associated with Intel MPX. These two component states of Intel MPX are the following:

- **BNDREGS:** CPUID.0DH.00H:EAX[3] indicates XCR0.BNDREGS[bit 3] is supported. This bit indicates bound register component of Intel MPX state, comprised of four bounds registers, BND0-BND3 (see Appendix E.3.2).
- **BNDCSR:** CPUID.0DH.00H:EAX[4] indicates XCR0.BNDCSR[bit 4] is supported. This bit indicates bounds configuration and status component of Intel MPX comprised of BNDCFGU and BNDSTATUS. OS must enable both BNDCSR and BNDREGS bits in XCR0 to ensure full Intel MPX support to applications.
- The size of the processor state component, enabled by XCR0.BNDREGS, is enumerated by CPUID.0DH.03H:EAX[31:0] and the byte offset of this component relative to the beginning of the XSAVE/XRSTOR area is reported by CPUID.0DH.03H:EBX[31:0].
- The size of the processor state component, enabled by XCR0.BNDCSR, is enumerated by CPUID.0DH.04H:EAX[31:0] and the byte offset of this component relative to the beginning of the XSAVE/XRSTOR area is reported by CPUID.0DH.04H:EBX[31:0].

On processors that support Intel MPX, CPUID.0DH.00H:EAX[3] and CPUID.0DH.00H:EAX[4] will both be 1. On processors that do not support Intel MPX, CPUID.0DH.00H:EAX[3] and CPUID.0DH.00H:EAX[4] will both be 0.

The layout of XCR0 for extended processor state components defined in Intel Architecture is shown in Figure 2-8 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A.

Enabling Intel MPX requires an OS to manage bits [4:3] of XCR0; see Section 13.5.

The BNDLDX and BNDSTX instructions (Appendix E.4.3) each take an operand whose bits are used to traverse data structures in memory. In 64-bit mode, these instructions operate only on the lower bits in the supplied 64-bit addresses. The number of bits used is 48 plus a value called the **MPX address-width adjust (MAWA)**. The MAWA value depends on CPL:

- If CPL < 3, the supervisor MAWA (**MAWAS**) is used. This value is 0.
- If CPL = 3, the user MAWA (**MAWAU**) is used. The value of MAWAU is enumerated in CPUID.07H.00H:ECX.MPX\_MAWAU[21:17].

(Outside of 64-bit mode, BNDLDX, and BNDSTX use the entire 32 bits of the supplied linear-address operands.)

### E.3.2 Bounds Registers

Intel MPX Architecture defines four new registers, BND0-BND3, which Intel MPX instructions operate on. Each bounds register stores a pair of 64-bit values which are the lower bound (LB) and upper bound (UB) of a buffer, see Figure E-1.

![Figure E-1: Layout of the Bounds Registers BND0-BND3. A 128-bit register divided into two 64-bit fields. Bits 127-64 are labeled 'Upper Bound (UB)'. Bits 63-0 are labeled 'Lower Bound (LB)'.](c0b77897a978d729dc8c21573062ed2f_img.jpg)

|                  |  |                  |  |   |
|------------------|--|------------------|--|---|
| 127              |  | 64 63            |  | 0 |
| Upper Bound (UB) |  | Lower Bound (LB) |  |   |

Figure E-1: Layout of the Bounds Registers BND0-BND3. A 128-bit register divided into two 64-bit fields. Bits 127-64 are labeled 'Upper Bound (UB)'. Bits 63-0 are labeled 'Lower Bound (LB)'.

**Figure E-1. Layout of the Bounds Registers BND0-BND3**

The bounds are unsigned effective addresses, and are inclusive. The upper bounds are architecturally represented in 1's complement form. Lower bound = 0, and upper bound = 0 (1's complement of all 1s) will allow access to the entire address space. The bounds are considered as INIT when both lower and upper bounds are 0 (cover the entire address space). The two Intel MPX instructions which operate on the upper bound (BNDMK and BNDCU) account for the 1's complement representation of the upper bounds.

The instruction set does not impose any conventions on the use of bounds registers. Software has full flexibility associating pointers to bounds registers including sharing them for multiple pointers.

RESET or INIT# will initialize (write zero to) BND0–BND3.

### E.3.3 Configuration and Status Registers

Intel MPX defines two configuration registers and one status register. The two configuration registers are defined for user mode (CPL = 3) and supervisor mode (CPL < 3). The user-mode configuration register BNDCFGU is accessible only with the XSAVE feature set instructions.

The supervisor mode configuration register is an MSR, referred to as IA32\_BNDCFGS (MSR 0D90H). Because both configuration registers share a common layout (see Figure E-2), when describing the common behavior, these configuration registers are often denoted as BNDCFGx, where x can be U or S, for user and supervisor mode respectively.

![Figure E-2: Common Layout of the Bound Configuration Registers BNDCFGU and BNDCFGS. A 64-bit register layout. Bits 63-12 contain the Base of Bound Directory (Linear Address). Bits 11-2 are Reserved (must be zero). Bit 1 is Bprv (BNDPRESERVE). Bit 0 is En (Enable).](b83e1a52fd0a217eb5bd0b65d25b1a00_img.jpg)

|                                          |                         |   |      |    |
|------------------------------------------|-------------------------|---|------|----|
| 63                                       | 12 11                   | 2 | 1    | 0  |
| Base of Bound Directory (Linear Address) | Reserved (must be zero) |   | Bprv | En |

Bprv: BNDPRESERVE  
 En: Enable

Figure E-2: Common Layout of the Bound Configuration Registers BNDCFGU and BNDCFGS. A 64-bit register layout. Bits 63-12 contain the Base of Bound Directory (Linear Address). Bits 11-2 are Reserved (must be zero). Bit 1 is Bprv (BNDPRESERVE). Bit 0 is En (Enable).

**Figure E-2. Common Layout of the Bound Configuration Registers BNDCFGU and BNDCFGS**

The Enable bit in BNDCFGU enables Intel MPX in user mode (CPL = 3), and the Enable bit in BNDCFGS enables Intel MPX in supervisor mode (CPL < 3). The BNDPRESERVE bit controls the initialization behavior of CALL/RET/JMP/Jcc instructions without the BND (F2H) prefix; see Appendix E.5.3.

WRMSR to BNDCFGS will #GP if any of the reserved bits of BNDCFGS is not zero or if the base address of the bound directory is not canonical. XRSTOR of BNDCFGU ignores the reserved bits and does not fault if any is non-zero; similarly, it ignores the upper bits of the base address of the bound directory and sign-extends the highest implemented bit of the linear address to guarantee the canonicity of this address.

Intel MPX also defines a status register (BNDSTATUS) primarily used to communicate status information for #BR exception. The layout of the status register is shown in Figure E-3.

![Figure E-3. Layout of the Bound Status Register BNDSTATUS. The diagram shows a 64-bit register layout. The top part is a box labeled 'ABD: Address Bound Directory Entry - Linear Address' spanning from bit 63 down to bit 2. The bottom part is a box labeled 'EC: Error Code' spanning from bit 1 down to bit 0. Bit positions 63, 2, 1, and 0 are indicated at the top of the diagram.](bb60fda45a6112f42bf6892a1d8209ad_img.jpg)

63 2 1 0

ABD: Address Bound Directory Entry - Linear Address

EC: Error Code

Figure E-3. Layout of the Bound Status Register BNDSTATUS. The diagram shows a 64-bit register layout. The top part is a box labeled 'ABD: Address Bound Directory Entry - Linear Address' spanning from bit 63 down to bit 2. The bottom part is a box labeled 'EC: Error Code' spanning from bit 1 down to bit 0. Bit positions 63, 2, 1, and 0 are indicated at the top of the diagram.

Figure E-3. Layout of the Bound Status Register BNDSTATUS

The BNDSTATUS register provides two fields to communicate the status of Intel MPX operations:

- EC (bits 1:0): The error code field communicates status information of a bound range exception #BR or operation involving bound directory.
- ABD: (bits 63:2): The address field of a bound directory entry can provide information when operation on the bound directory caused a #BR.

The valid error codes are defined in Table E-1.

Table E-1. Error Code Definition of BNDSTATUS

| EC               | Description            | Meaning                                                                                                                 |
|------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------|
| 00b <sup>1</sup> | No Intel MPX exception | No exception caused by Intel MPX operations.                                                                            |
| 01b              | Bounds violation       | #BR caused by BNDCL, BNDCU or BNDCN instructions; ABD is 0.                                                             |
| 10b              | Invalid BD entry       | #BR caused by BNDLDX or BNDSTX instructions, ABD will be set to the linear address of the invalid bound-directory entry |
| 11b              | Reserved               | Reserved                                                                                                                |

NOTES:

1. When legacy BOUND instruction cause a #BR with Intel MPX enabled (see Appendix E.5.4), EC is written with Zero.

RESET or INIT# will set BNDCFGx and BNDSTATUS registers to zero.

E.3.4 Read and Write of IA32\_BNDCFGS

The RDMSR and WRMSR instructions can be used to read and write the IA32\_BNDCFGS MSR. (The XSAVE state does not include IA32\_BNDCFGS, and instructions in the XSAVE feature set do not access that register). Attempts to write to IA32\_BNDCFGS check for canonicity of the addresses being loaded into IA32\_BNDCFGS (regardless of mode at the time of execution) and will #GP if the address is not canonical or if reserved bits would be set.

Software can use RDMSR and WRMSR to read and write IA32\_BNDCFGS as long as the processor implements Intel MPX, i.e., CPUID.07H.00H:EBX.MPX = 1. The states of CR4 and XCR0 have no impact on the ability to access IA32\_BNDCFGS.

E.4 INTEL MPX INSTRUCTION SUMMARY

When Intel MPX is not enabled or not present, all Intel MPX instructions behave as NOP. There are eight Intel MPX instructions, Table E-2 provides a summary.

A C/C++ compiler can implement intrinsic support for Intel MPX instructions to facilitate pointer operation with capability of checking for valid bounds on pointers. Typically, Intel MPX intrinsics are implemented by compiler via inline code generation where bounds register allocations are handled by the compiler without requiring the

programmer to directly manipulate any bounds registers. Therefore no new data type for a bounds register is needed in the syntax of Intel MPX intrinsics.

**Table E-2. Intel® MPX Instruction Summary**

| Intel MPX Instruction | Description                                                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| BNDMK b, m            | Create LowerBound (LB) and UpperBound (UB) in the bounds register b                                         |
| BNDCL b, r/m          | Checks the address of a memory reference or address in r against the lower bound                            |
| BNDUC b, r/m          | Checks the address of a memory reference or address in r against the upper bound in 1's complement form     |
| BNDNC b, r/m          | Checks the address of a memory reference or address in r against the upper bound not in 1's complement form |
| BNDMOV b, b/m         | Copy/load LB and UB bounds from memory or a bounds register                                                 |
| BNDMOV b/m, b         | Store LB and UB bounds in a bounds register to memory or another register                                   |
| BNDLDX b, mib         | Load bounds using address translation using an sib-addressing expression mib                                |
| BNDSTX mib, b         | Store bounds using address translation using an sib-addressing expression mib                               |

### E.4.1 Instruction Encoding

All Intel MPX instructions are NOP on processors that report CPUID.07H.00H:EBX.MPX[14] = 0, or if Intel MPX is not enabled by the operating system (see Section 13.5). Applications can selectively opt-in to use Intel MPX instructions.

All Intel MPX opcodes encoded to operate on BND0-BND3 are valid Intel MPX instructions. All Intel MPX opcodes encoded to operate on bound registers beyond BND3 will #UD if Intel MPX is enabled.

BNDLDX/BNDSTX opcodes require 66H as a mandatory prefix with its operand size tied to the address size attribute of the supported operating modes. Attempt to override operand size attribute with 66H or with REX.W in 64-bit mode is ignored.

### E.4.2 Usage and Examples

BNDMK is typically used after memory is allocated for a buffer, e.g., by functions such as malloc, calloc, or when the memory is allocated on the stack. However, many other usages are possible such as when accessing an array member of a structure.

#### Example E-1. BNDMK Example Usage in Application and Library Code

|                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <pre>//assume the array A is allocated on the stack at 'offset' // from RBP. int A[100];  // the instruction to store starting address of array will be: LEA RAX, [RBP+offset]  // the instruction to create the bounds for array A will be: BNDMK BND0, [RAX+399]  // Store RAX into BND0.LB, and ~(RAX+399) into BND0.UB.</pre> | <pre>// similarly, for a library implementation of dynamic allocated // memory int * k = malloc(100);  // assuming that malloc returns pointer k in RAX and holds // (size - 1) in RCX, the malloc implementation will execute the // following instruction before returning: BNDMK BND0, [RAX+RCX]  // BND0.LB stores RAX, and BND0.UB stores ~(RAX+RCX)</pre> |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

BNDMOV is typically used to copy bounds from one bound register to another when a pointer is copied from one general purpose register to another, or to spill/fill bounds into memory corresponding to a spill/fill of a pointer.

**Example E-2. BNDMOV Example**

Spilling or caller save of bound register would use BNDMOV [RBP+ offset], BNDx.

Assuming that the calling convention is that bound of first pointer is passed in BND0, and that bound happens to be in BND3 before the call, the software will add instruction BNDMOV BND0, BND3 prior to the call.

BNDCL/BNDUCU/BNDNCN are typically used before writing to a buffer but can be used in other instances as well. If there are no bounds violations as a result of bound check instruction, the processor will proceed to execute the next instruction. However, if the bound check fails, it will signal #BR exception (fault).

Typically, the pointer used to write to memory will be compared against lower bound. However, for upper bound check, the software must add the (operand size - 1) to the pointer before upper bound checking.

For example, the software intend to write 32-bit integer in 64-bit mode into a buffer at address specified in RAX, and the bounds are in register BND0, the instruction sequence will be:

```
BNDCL BND0, [RAX]
```

```
BNDUCU BND0, [RAX+3] ; operand size is 4
```

```
MOV Dword ptr [RAX], RBX ; RBX has the data to be written to the buffer.
```

Software may move one of the two bound checks out of a loop if it can determine that memory is accessed strictly in ascending or descending order. For string instructions of the form REP MOVSB, the software may choose to do check lower bound against first access and upper bound against last access to memory. However, if software wants to also check for wrap around conditions as part of address computation, it should check for both upper and lower bound for first and last instructions (total of four bound checks).

BNDSTX is used to store the bounds associated with a buffer and the “pointer value” of the pointer to that buffer onto a bound table entry via address translation using a two-level structure, see Appendix E.4.3.

For example, the software has a buffer with bounds stored in BND0, the pointer to the buffer is in ESI, the following sequence will store the “pointer value” (the buffer) and the bounds into a configured bound table entry using address translation from the linear address associated with the base of a SIB-addressing form consisting of a base register and a index register:

```
MOV ECX, Dword ptr [ESI] ; store the pointer value in the index register ECX
```

```
MOV EAX, ESI ; store the pointer in the base register EAX
```

```
BNDSTX Dword ptr [EAX+ECX], BND0 ; perform address translation from the linear address of the base EAX and store bounds and pointer value ECX onto a bound table entry.
```

Similarly to retrieve a buffer and its associated bounds from a bound table entry:

```
MOV EAX, dword ptr [EBX] ;
```

```
BNDLDX BND0, dword ptr [EBX+EAX]; perform address translation from the linear address of the base EBX, and loads bounds and pointer value from a bound table entry
```

**E.4.3 Loading and Storing Bounds in Memory**

Intel MPX defines two instructions to load and store of the linear address of a pointer to a buffer, along with the bounds of the buffer into a data structure of extended bounds. When storing these extended bounds, the processor parses the address of the pointer (where it is stored) to locate an entry in a **bound table** in which to store the extended bounds. Loading of an extended bounds performs the reverse sequence.

The memory representation of an extended bound is a 4-tuple consisting of lower bound, upper bound, pointer value and a reserved field (for use by future versions of Intel MPX; software must not use this field). Accesses to these extended bounds use 32-bit or 64-bit operands according to the current paging mode. Thus, a bound table entry is 4\*64 bits (32 bytes) in 64-bit mode and 4\*32 bits (16 bytes) outside 64-bit mode. The linear address of a bound table is stored in a bound-directory entry (BDE). The linear address of the **bound directory** is derived from either BNDCFGU (CPL = 3) or BNDCFGS (CPL < 3).

The bound directory and bound tables are stored in application memory and are allocated by the application (in case of kernel use, the structures will be in kernel memory). The bound directory and each bound table are in contiguous linear memory.

Software should take care to allocate sufficient memory for the bound directory and the bound tables. The amount of memory required depends on the current operating mode and, in some cases, on CPL:

- In 64-bit mode:
  - Each bound table comprises  $2^{17}$  32-byte entries thus, the size of a bound table in 64-bit mode is 4 MBytes.
  - The size of the bound directory depends on the value of MAWA. Specifically, the bound directory comprises  $2^{28+MAWA}$  64-bit entries; thus, the size of a bound directory in 64-bit mode is  $2^{1+MAWA}$  GBytes. The value of MAWA depends on CPL:
    - If  $CPL < 3$ , the supervisor MAWA (MAWAS) is used. This value is 0. Thus, when  $CPL < 3$ , a bound directory comprises  $2^{28}$  64-bit entries and the size of a bound directory is 2 GBytes.
    - If  $CPL = 3$ , the user MAWA (MAWAU) is used. The value of MAWAU is enumerated in CPUID.07H.00H:ECX.MPX\_MAWAU[21:17]. When  $CPL = 3$ , a bound directory comprises  $2^{28+MAWAU}$  64-bit entries and the size of a bound directory is  $2^{1+MAWAU}$  GBytes.

### NOTE

Software operating with  $CPL = 3$  in 64-bit mode should use CPUID to determine the proper amount of memory to allocate for the bound directory.

- Outside 64-bit mode:
  - Each bound table comprises  $2^{10}$  16-byte entries; thus, the size of a bound table outside 64-bit mode is 16 KBytes.
  - The bound directory comprises  $2^{20}$  32-bit entries; thus, the size of a bound directory outside 64-bit mode is 4 MBytes. This size is independent of MAWA and CPL.

Bounds in memory are associated with the memory address where the pointer is stored, i.e., Ap. A linear address LAp is computed by adding the appropriate segment base to Ap. (Note: for these instructions, the segment override applies only to the computation.) Appendix E.4.3.1 and Appendix E.4.3.2 describe how BNDLDX and BNDSTX parse LAp to locate a bound-directory entry (BDE), which contains the address of a bound table, and then a bound-table entry (BTE), which contains the extended bounds for the pointer.

#### E.4.3.1 BNDLDX and BNDSTX in 64-Bit Mode

Figure E-4 shows the two-level structures for address translation of extended bounds in 64-bit mode.

![Figure E-4: Bound Paging Structure and Address Translation in 64-Bit Mode. The diagram illustrates the hierarchical structure of bound directories and tables. At the top, the BNDCFGU/BNDCFGS register (bits 63:0) contains the Base of Bound Directory (Linear Address) in bits 63:12. This points to a BNDCFGx[63:12] register (bits 63:12). The Linear Address of 'pointer' (LAp) is split into two parts: bits 63:20 (LAp[63:20]) and bits 19:3 (LAp[19:3]). The LAp[63:20] part is used to select a Bound Directory Entry (BDE) in the Bound Directory (2^{1+MAWA} GBytes). The LAp[19:3] part is used to select a Bound Table Entry (BTE) in the Bound Table (4 MBytes). A detailed view of a BTE shows it contains a Pointer Value (bits 24:16), an Upper Bound (bits 8:0), and a Lower Bound (bits 0:0).](4c8f66d76c44fe270bbd24b1b122a434_img.jpg)

The diagram illustrates the Bound Paging Structure and Address Translation in 64-Bit Mode. It shows the flow from the BNDCFGU/BNDCFGS register to the Base of Bound Directory (Linear Address), then to the BNDCFGx[63:12] register. The Linear Address of 'pointer' (LAp) is split into two parts: LAp[63:20] and LAp[19:3]. LAp[63:20] is used to select a Bound Directory Entry (BDE) in the Bound Directory (2^{1+MAWA} GBytes). LAp[19:3] is used to select a Bound Table Entry (BTE) in the Bound Table (4 MBytes). A detailed view of a BTE shows it contains a Pointer Value (bits 24:16), an Upper Bound (bits 8:0), and a Lower Bound (bits 0:0).

Figure E-4: Bound Paging Structure and Address Translation in 64-Bit Mode. The diagram illustrates the hierarchical structure of bound directories and tables. At the top, the BNDCFGU/BNDCFGS register (bits 63:0) contains the Base of Bound Directory (Linear Address) in bits 63:12. This points to a BNDCFGx[63:12] register (bits 63:12). The Linear Address of 'pointer' (LAp) is split into two parts: bits 63:20 (LAp[63:20]) and bits 19:3 (LAp[19:3]). The LAp[63:20] part is used to select a Bound Directory Entry (BDE) in the Bound Directory (2^{1+MAWA} GBytes). The LAp[19:3] part is used to select a Bound Table Entry (BTE) in the Bound Table (4 MBytes). A detailed view of a BTE shows it contains a Pointer Value (bits 24:16), an Upper Bound (bits 8:0), and a Lower Bound (bits 0:0).

**Figure E-4. Bound Paging Structure and Address Translation in 64-Bit Mode**

As noted earlier, the linear address of the bound directory is derived from either BNDCFGU (CPL = 3) or BNDCFGS (CPL < 3). In 64-bit mode, each bound-directory entry (BDE) is 8 bytes. The number of entries in the bound directory is determined by the MPX address-width adjust (MAWA; see Appendix E.3.1). Specifically, the number of entries is  $2^{28+MAWA}$ .

In 64-bit mode, the processor uses the two-level structures to access extended bounds as follows:

- A bound directory is located at the 4-KByte aligned linear address specified in bits 63:12 of BNDCFGx (see Figure E-2). A bound directory comprises  $2^{28+MAWA}$  64-bit entries (BDEs); thus, the size of a bound directory in 64-bit mode is  $2^{1+MAWA}$  GBytes. A BDE is selected using the LAp (linear address of pointer to a buffer) to construct a 64-bit offset as follows:

- bits 63:31+MAWA are 0;
- bits 30+MAWA:3 are LAp[47+MAWA:20]; and
- bits 2:0 are 0.

The address of the BDE is the sum of the bound-directory base address (from BNDCFGx) plus this 64-bit offset.

- Bit 0 of a BDE is a valid bit. If this bit is 0, use of the BDE by BNDLDX or BNDSTX causes #BR, sets BNDSTATUS[1:0] to 10b (the error code), and loads BNDSTATUS[63:2] with bits 63:2 of the linear address of the BDE. Otherwise, the processor uses bits 63:3 of the BDE as the 8-byte aligned address of a bound table (BT); the processor ignores bits 2:1 of a BDE.

A bound table comprises  $2^{17}$  32-byte entries (BTEs); thus, the size of a bound table in 64-bit mode is 4 MBytes. A BTE is selected using the LAp (linear address of pointer to a buffer) to construct an offset as follows:

- bits 21:5 are LAp[19:3]; and
- bits 4:0 are 0.

The address of the BTE is the sum of the bound-table base address (from the BDE) plus this offset.

- Each BTE comprises the following:

- a 64-bit lower bound (LB) field;
- a 64-bit upper bound (UB) field;
- a 64-bit pointer value; and
- a 64-bit reserved field. This field is reserved for future Intel MPX; software must not use it.

### E.4.3.2 BNDLDX and BNDSTX Outside 64-Bit Mode

Figure E-5 shows the two-level structures for address translation of extended bounds outside 64-bit mode.

As noted earlier, the linear address of the bound directory is derived from either BNDCFGU (CPL = 3) or BNDCFGS (CPL < 3). Outside 64-bit mode, each bound-directory entry (BDE) is 4 bytes. The number of entries in the bound directory is  $2^{20}$ .

Outside 64-bit mode, the processor uses the two-level structures to access extended bounds as follows:

- A bound directory is located at the 4-KByte aligned linear address specified in bits 31:12 of BNDCFGx (see Figure E-2). A bound directory comprises  $2^{20}$  32-bit entries (BDEs); thus, the size of a bound directory outside 64-bit mode is 4 MBytes. A BDE is selected using the LAp (linear address of pointer to a buffer) to construct an offset as follows:
  - bits 21:2 are LAp[31:12]; and
  - bits 1:0 are 0.

The address of the BDE is the sum of the bound-directory base address (from BNDCFGx) plus this offset.

- Bit 0 of a BDE is a valid bit. If this bit is 0, use of the BDE by BNDLDX or BNDSTX causes #BR, sets BNDSTATUS[1:0] to 10b (the error code), and loads BNDSTATUS[31:2] with bits 31:2 of the linear address of the BDE. Otherwise, the processor uses bits 31:2 of the BDE as the 4-byte aligned address of a bound table (BT); the processor ignores bit 1 of a BDE.

![Diagram illustrating the Bound Paging Structure and Address Translation Outside 64-Bit Mode. The diagram shows the flow from BNDCFGU/BNDCFGS to the Base of Bound Directory, then to the Bound Directory Entries, and finally to the Bound Table Entries.](8f344dcec24b1c85105f3b329b8a5061_img.jpg)

The diagram illustrates the address translation process for extended bounds outside 64-bit mode. It shows the following components and their interactions:

- BNDCFGU/BNDCFGS:** A 32-bit register. Bits 31:12 are used to determine the **Base of Bound Directory (Linear Address)**. Bits 12:11 are used to determine the **Linear Address of "pointer" (LAp)**.
- Base of Bound Directory (Linear Address):** A 32-bit linear address. Bits 31:12 are used to determine the **Linear Address of "pointer" (LAp)**.
- Linear Address of "pointer" (LAp):** A 32-bit linear address. Bits 31:12 are used to determine the **Linear Address of "pointer" (LAp)**. Bits 12:11 are used to determine the **Linear Address of "pointer" (LAp)**.
- Bound Directory (4 MBytes):** A 4-MByte structure containing **Bound Directory Entries**. Each entry is 32 bits wide. The address of a specific entry is calculated as the base address plus the offset derived from LAp[31:12].
- Bound Table (16 KBytes):** A 16-KByte structure containing **Bound Table Entries**. Each entry is 14 bytes wide. The address of a specific entry is calculated as the base address plus the offset derived from LAp[11:2].
- Bound Table Entry Structure:** A 14-byte structure. The first 4 bytes are the **Reserved** field. The next 4 bytes are the **Pointer Value**. The next 4 bytes are the **Upper Bound**. The last 2 bytes are the **Lower Bound**.

Diagram illustrating the Bound Paging Structure and Address Translation Outside 64-Bit Mode. The diagram shows the flow from BNDCFGU/BNDCFGS to the Base of Bound Directory, then to the Bound Directory Entries, and finally to the Bound Table Entries.

Figure E-5. Bound Paging Structure and Address Translation Outside 64-Bit Mode

- A bound table comprises  $2^{10}$  16-byte entries (BTEs); thus, the size of a bound table outside 64-bit mode is 16 KBytes. A BTE is selected using the LAp (linear address of pointer to a buffer) to construct an offset as follows:
- bits 13:4 are LAp[11:2]; and
  - bits 3:0 are 0.
- The address of the BTE is the sum of the bound-table base address (from the BDE) plus this offset. This address is use as an offset into the DS segment to determine the linear address of the BTE.
- Each BTE comprises the following:
    - a 32-bit lower bound (LB) field;
    - a 32-bit upper bound (UB) field;
    - a 32-bit pointer value; and
    - a 32-bit reserved field. This field is reserved for future Intel MPX; software must not use it.

E.5 INTERACTIONS WITH INTEL MPX

E.5.1 Intel® MPX and Operating Modes

In 64-bit Mode, all Intel MPX instructions use 64-bit operands for bounds and 64 bit addressing, i.e., REX.W & 67H have no effect on data or address size.

XSAVE, XSAVEOPT, and XRSTOR load/store 64-bit values in all modes, as these state-management instructions are not Intel MPX instructions.

In compatibility and legacy modes (including 16-bit code segments, real and virtual 8086 modes) all Intel MPX instructions use 32-bit operands for bounds and 32 bit addressing. The upper 32-bits of destination bound register are cleared (consistent with behavior of integer registers)

In 32-bit and compatibility mode, the bounds are 32-bit, and are treated same as 32-bit integer registers. Therefore, when 32-bit bound is updated in a bound register, the upper 32-bits are undefined. When switching from 64-bit, the behavior of content of bounds register will be similar to that of general purpose registers.

Table E-3 describes the impact of 67H prefix on memory forms of Intel MPX instructions (register-only forms ignore 67H prefix) when Intel MPX is enabled:

Table E-3. Effective Address Size of Intel® MPX Instructions with 67H Prefix

| Addressing Mode | 67H Prefix | Effective Address Size used for Intel MPX instructions when Intel MPX is enabled |
|-----------------|------------|----------------------------------------------------------------------------------|
| 64-bit Mode     | Y          | 64 bit addressing used                                                           |
| 64-bit Mode     | N          | 64 bit addressing used                                                           |
| 32-bit Mode     | Y          | #UD                                                                              |
| 32-bit Mode     | N          | 32 bit addressing used                                                           |
| 16-bit Mode     | Y          | 32 bit addressing used                                                           |
| 16-bit Mode     | N          | #UD                                                                              |

E.5.2 Intel® MPX Support for Pointer Operations with Branching

- Intel MPX provides flexibility in supporting pointer operation across control flow changes. Intel MPX allows
- compatibility with legacy code that may perform pointer operation across control flow changes and are unaware of Intel MPX, along with
  - Intel MPX-aware code that adds bounds checking protection to pointer operation across control flow changes.

The interface to provide such flexibility consists of:

- Using a prefix, referred to as BND prefix, to relevant branch instructions: CALL, RET, JMP, and Jcc.
- BNDCFGU and BNDCFGS provides the bit field, BNDPRESERVE (bit 1).

The value of BNDPRESERVE in conjunction with the presence/absence the BND prefix with those branching instruction will determine whether the values in BND0-BND3 will be initialized or unchanged.

### E.5.3 CALL, RET, JMP, and All Jcc

An application compiled to use Intel MPX will use the REPNE (F2H) prefix (denoted by BND) for all forms of near CALL, near RET, near JMP, short & near Jcc instructions (BND+CALL, BND+RET, BND+JMP, BND+Jcc). See Table E-4 for specific opcodes. All far CALL, RET, and JMP instructions plus short JMP (JMP rel 8, opcode EB) instructions will never cause bound registers to be initialized.

If BNDPRESERVE bit is one, above instructions will NOT INIT the bounds registers when BND prefix is not present for above instructions (legacy behavior). However, If BNDPRESERVE is zero, above instructions will INIT ALL bound registers (BND0-BND3) when BND prefix is not present for above instructions. If BND prefix is present for above instructions, the BND registers will NOT INIT any bound registers (BND0-BND3).

The legacy code will continue to use non-prefixed forms of these instructions, so if BNDPRESERVE is zero, all the bound registers will INIT by legacy code. This allows the legacy function to execute and return to callee with all bound registers initialized (legacy code by definition cannot make or load bounds in bound registers because it does not have Intel MPX instructions). This will eliminate compatibility concerns when legacy function might have changed the pointer in registers but did not update the value of the bounds registers associated with these pointers.

If BNDCFGx.BNDPRESERVE is clear then non-prefixed forms of these instructions will initialize all the bound registers. If this bit is set then non-prefixed and prefixed forms of these instructions will preserve the contents of bound registers as shown in Table E-4.

**Table E-4. Bounds Register INIT Behavior Due to BND Prefix with Branch Instructions**

| Instruction | Branch Instruction Opcodes                        | BNDPRESERVE = 0     | BNDPRESERVE = 1     |
|-------------|---------------------------------------------------|---------------------|---------------------|
| CALL        | E8, FF/2                                          | Init BND0-BND3      | BND0-BND3 unchanged |
| BND + CALL  | F2 E8, F2 FF/2                                    | BND0-BND3 unchanged | BND0-BND3 unchanged |
| RET         | C2, C3                                            | Init BND0-BND3      | BND0-BND3 unchanged |
| BND + RET   | F2 C2, F2 C3                                      | BND0-BND3 unchanged | BND0-BND3 unchanged |
| JMP         | E9, FF/4                                          | Init BND0-BND3      | BND0-BND3 unchanged |
| BND + JMP   | F2 E9, F2 FF/4                                    | BND0-BND3 unchanged | BND0-BND3 unchanged |
| Jcc         | 70 through 7F,<br>0F 80 through 0F 8F             | Init BND0-BND3      | BND0-BND3 unchanged |
| BND + Jcc   | F2 70 through F2 7F,<br>F2 0F 80 through F2 0F 8F | BND0-BND3 unchanged | BND0-BND3 unchanged |

### E.5.4 BOUND Instruction and Intel MPX

If Intel MPX is enabled (see Section 13.5) and a #BR was caused due to a BOUND instruction, then BOUND instruction will write zero to the BNDSTATUS register. In all other situations, BOUND instruction will not modify BNDSTATUS. Specifically, the operation of the BOUND instruction can be described as:

```

IF ( ( BOUND instruction caused #BR) AND ( CR4.OXSAVE = 1 AND XCR0.BNDREGS = 1 AND XCR0.BNDCSR = 1) AND
    ( (CPL= 3 AND BNDCFGU.ENABLE = 1) OR (CPL < 3 AND BNDCFGS.ENABLE = 1) ) ) THEN
    BNDSTATUS := 0;
ELSE
    BNDSTATUS is not modified;
FI;

```

## E.5.5 Programming Considerations

Intel MPX instruction set does not dictate any calling convention, but allows the calling convention extensions to be interoperable with legacy code by making use of the of the bound registers and the bound tables to convey arguments and return values.

## E.5.6 Intel MPX and System Management Mode

Upon delivery of an SMI to a processor supporting Intel MPX, the contents of IA32\_BNDCFGS is saved to SMM state save map (at offset 7ED0H) and the register is then cleared when entering into SMM. RSM restores IA32\_BNDCFGS from the SMM state save map. The instruction forces the reserved bits (11:2) to 0 and sign-extends the highest implemented bit of the linear address to guarantee the canonicity of this address (regardless of what is in SMM state save map).

The content of IA32\_BNDCFGS is cleared after entering into SMM. Thus, Intel MPX is disabled inside an SMM handler until SMM code enables it explicitly. This will prevent initialization of the bound registers by execution of CALL, RET, JMP, or Jcc in SMM code.

## E.5.7 Support of Intel MPX in VMCS

A new guest-state field for IA32\_BNDCFGS is added to the VMCS. In addition, two new controls are added:

- a VM-exit control called “clear BNDCFGS”
- a VM-entry control called “load BNDCFGS.”

VM exits always save IA32\_BNDCFGS into BNDCFGS field of VMCS; if “clear BNDCFGS” is 1, VM exits clear IA32\_BNDCFGS. If “load BNDCFGS” is 1, VM entry loads IA32\_BNDCFGS from VMCS. If loading IA32\_BNDCFGS, VM entry should check the value of that register in the guest-state area of the VMCS and cause the VM entry to fail (late) if the value is one that would causes WRMSR to fault if executed in ring 0.

## E.5.8 Support of Intel MPX in Intel TSX

For some processor implementations, the following Intel MPX instructions may always cause transactional aborts:

- An Intel TSX transaction abort will occur in case of legacy branch (that causes bounds registers INIT) when at least one bounds register was in a NON-INIT state.
- An Intel TSX transaction abort will occur in case of a BNDLDX & BNDSTX instruction on non-flat segment.

Intel MPX Instructions (including BND prefix + branch instructions) not enumerated above as causing transactional abort when used inside a transaction will typically not cause an Intel TSX transaction to abort.

## Numerics

- 128-bit
  - packed byte integers data type, 4-10
  - packed double precision floating-point data type, 4-10
  - packed doubleword integers data type, 4-10
  - packed quadword integers data type, 4-10
  - packed SIMD data types, 4-9
  - packed single precision floating-point data type, 4-10, 10-5
  - packed word integers data type, 4-10
- 16-bit
  - address size, 3-9
  - operand size, 3-9
- 286 processor, 2-1
- 32-bit
  - address size, 3-9
  - operand size, 3-9
- 64-bit
  - packed byte integers data type, 4-9, 9-3
  - packed doubleword integers data type, 4-9
  - packed doubleword integers data types, 9-3
  - packed word integers data type, 4-9, 9-3
- 64-bit mode
  - sub-mode of IA-32e, 3-1
  - address calculation, 3-10
  - address size, 3-19
  - address space, 3-5
  - BOUND instruction, 7-18
  - branch behavior, 6-12
  - byte register limitation, 3-13
  - CALL instruction, 6-12, 7-17
  - canonical address, 3-10
  - CMPS instruction, 7-20
  - CMPXCHG16B instruction, 7-5
  - data types, 7-2
  - DEC instruction, 7-8
  - decimal arithmetic instructions, 7-10
  - default operand and address sizes, 3-2
  - exceptions, 6-19
  - far pointer, 4-8
  - feature list, 2-20
  - GDTR register, 3-6
  - IDTR register, 3-6
  - INC instruction, 7-8
  - instruction pointer, 3-10, 3-18
  - instructions introduced, 5-38
  - interrupts, 6-19
  - introduction, 2-20, 3-1, 7-1
  - IRET instruction, 7-18
  - I/O instructions, 7-20
  - JCC instruction, 6-12, 7-17
  - JCXZ instruction, 6-12, 7-17
  - JMP instruction, 6-12, 7-17
  - LAHF instruction, 7-22
  - LDTR register, 3-6
  - legacy modes, 2-20
  - LODS instruction, 7-20
  - LOOP instruction, 6-12, 7-17
  - memory models, 3-9
  - memory operands, 3-21
  - MMX technology, 9-2
  - MOVS instruction, 7-20
  - MOVSLD instruction, 7-8
  - near pointer, 4-8
  - operand addressing, 3-23
  - operand size, 3-19
  - operands, 3-20, 3-21
  - POPF instruction, 7-22
  - promoted instructions, 3-2
  - PUSHA, PUSHAD, POPA, POPAD, 7-7
  - PUSHF instruction, 7-22
  - PUSHFD instruction, 7-22
  - real address mode, 3-9
  - register operands, 3-20
  - REP prefix, 7-20
  - RET instruction, 6-12, 7-17
  - REX prefix, 3-2, 3-12, 3-19
  - RFLAGS register, 7-22
  - RIP register, 3-10
  - RIP-relative addressing, 3-18, 3-24
  - SAHF instruction, 7-22
  - SCAS instruction, 7-20
  - segment registers, 3-15
  - segmentation, 3-9, 3-22
  - SSE extensions, 10-3
  - SSE2 extensions, 11-3
  - SSE3 extensions, 12-1
  - SSSE3 extensions, 12-1
  - stack behavior, 6-4
  - STOS instruction, 7-20
  - TR register, 3-6
  - x87 FPU, 8-1
  - See also: IA-32e mode, compatibility mode
- 8086 processor, 2-1
- 8088 processor, 2-1

## A

- AAA instruction, 7-9
- AAD instruction, 7-10
- AAM instruction, 7-10
- AAS instruction, 7-10
- AC (alignment check) flag, EFLAGS register, 3-17
- Access rights, segment descriptor, 6-8, 6-13
- ADC instruction, 7-8
- ADD instruction, 7-8
- ADDPD instruction, 11-6
- ADDPS instruction, 10-8
- Address size attribute
  - code segment, 3-18
  - description of, 3-18
  - of stack, 6-3
- Address sizes, 3-9
- Address space
  - 64-bit mode, 3-1, 3-5
  - compatibility mode, 3-1
  - overview of, 3-2
  - physical, 3-6
- Addressing modes
  - assembler, 3-24
  - base, 3-22, 3-23, 3-24

## INDEX

- base plus displacement, 3-23
- base plus index plus displacement, 3-23
- base plus index time scale plus displacement, 3-23, 3-24
- canonical address, 3-10
- displacement, 3-22, 3-23
- effective address, 3-22
- immediate operands, 3-20
- index, 3-22, 3-24
- index times scale plus displacement, 3-23
- memory operands, 3-21
- register operands, 3-20
- RIP-relative addressing, 3-18, 3-24
- scale factor, 3-22, 3-24
- specifying a segment selector, 3-21
- specifying an offset, 3-22
- specifying offsets in 64-bit mode, 3-23
- ADDSD instruction, 11-6
- ADDSS instruction, 10-8
- ADDSUBPD instruction, 5-24, 12-4
- ADDSUBPS instruction, 5-24, 12-4
- Advanced media boost, 2-11
- advanced smart cache, 2-10
- AF (adjust) flag, EFLAGS register, 3-16, A-1
- AH register, 3-12
- AL register, 3-12
- Alignment
  - words, doublewords, quadwords, 4-2
- AND instruction, 7-10
- ANDNPD instruction, 11-7
- ANDNPS instruction, 10-9
- ANDPD instruction, 11-7
- ANDPS instruction, 10-9
- Arctangent, x87 FPU operation, 8-20
- Arithmetic instructions, x87 FPU, 8-25
- Assembler, addressing modes, 3-24
- Asymmetric processing model, 12-1
- AX register, 3-12

## B

- B (default size) flag, segment descriptor, 3-18
- Base (operand addressing), 3-22, 3-23, 3-24
- Basic execution environment, 3-2
- Basic programming environment, 7-1
- B-bit, x87 FPU status word, 8-5
- BCD integers
  - packed, 4-11
  - relationship to status flags, 3-17
  - unpacked, 4-10, 7-9
  - x87 FPU encoding, 4-11
- BH register, 3-12
- Bias value
  - numeric overflow, 8-29
  - numeric underflow, 8-30
- Biased exponent, 4-14
- Biassing constant, for floating-point numbers, 4-6
- Binary numbers, 1-7
- Binary-coded decimal (see BCD)
- Bit field, 4-8
- Bit order, 1-6
- BL register, 3-12
- BOUND instruction, 6-18, 7-18, 7-23
- BOUND range exceeded exception (#BR), 6-19
- BP register, 3-12
- Branch

- control transfer instructions, 7-14
- hints, 11-13
- on EFLAGS register status flags, 7-15, 8-6
- on x87 FPU condition codes, 8-6, 8-20
- prediction, 2-8
- Brand information
  - processor brand index, 21-5
  - processor brand string, 21-4
- BSF instruction, 7-14
- BSR instruction, 7-14
- BSWAP instruction, 7-4
- BT instruction, 3-15, 3-16, 7-14
- BTC instruction, 3-15, 3-16, 7-14
- BTR instruction, 3-15, 3-16, 7-14
- BTS instruction, 3-15, 3-16, 7-14
- BX register, 3-12
- Byte, 4-1
- Byte order, 1-6

## C

- C1 flag, x87 FPU status word, 8-4, 8-26, 8-29, 8-30
- C2 flag, x87 FPU status word, 8-5
- cache, smart, 2-4
- Call gate, 6-8
- CALL instruction, 3-18, 6-3, 6-4, 6-8, 7-15, 7-22
- Calls (see Procedure calls)
- Canonical address, 3-10
- CBW instruction, 7-7
- CDQ instruction, 7-7
- Celeron processor
  - description of, 2-2
- CF (carry) flag, EFLAGS register, 3-16, A-1
- CH register, 3-12
- CL register, 3-12
- CLC instruction, 3-16, 7-21
- CLD instruction, 3-17, 7-21
- CLFLUSH instruction, 11-12
- CLI instruction, 20-4
- CMC instruction, 3-16, 7-21
- CMOVcc instructions, 7-3, 7-4
- CMP instruction, 7-8
- CMPPD instruction, 11-7
- CMPPS instruction, 10-9
- CMPS instruction, 3-17, 7-18
- CMPSD instruction, 11-7
- CMPSS instruction, 10-9
- CMPXCHG instruction, 7-4
- CMPXCHG16B instruction, 7-5
- CMPXCHG8B instruction, 7-4
- Code segment, 3-14
- COMISD instruction, 11-7
- COMISS instruction, 10-9
- Compare
  - compare and exchange, 7-4
  - integers, 7-8
  - real numbers, x87 FPU, 8-19
  - strings, 7-18
- Compatibility mode
  - address space, 3-1
  - branch functions, 6-12
  - call gate descriptors, 6-12
  - introduction, 2-20, 3-1
  - memory models, 3-9
  - MMX technology, 9-2

- segmentation, 3-22
- SSE extensions, 10-3
- SSE2 extensions, 11-3
- SSE3 extensions, 12-1
- SSSE3 extensions, 12-1
- x87 FPU, 8-1
- See also: IA-32e mode, 64-bit mode
- Compatibility, software, 1-7
- Condition code flags, x87 FPU status word
  - branching on, 8-6
  - conditional moves on, 8-6
  - description of, 8-4
  - interpretation of, 8-5
  - use of, 8-19
- Conditional moves, x87 FPU condition codes, 8-6
- Constants (floating point), 8-17
- Control registers
  - 64-bit mode, 3-5
  - overview of, 3-4
- Core microarchitecture, 2-10, 2-12, 2-13
- core microarchitecture, 2-10, 2-12
- Core Solo and Core Duo, 2-4
- Cosine, x87 FPU operation, 8-20
- CPUID instruction
  - CLFLUSH flag, 11-12
  - CMOVcc feature flag, 7-3
  - determine support for, 3-17
  - earlier processors, 21-1
  - FXSAVE-FXRSTOR flag, 10-14
  - MMX feature flag, 9-8
  - processor brand index, 21-4
  - processor brand string, 21-4
  - serializing use, 20-5
  - SSE feature flag, 10-1, 10-6
  - SSE2 feature flag, 11-1, 12-5
  - SSE3 feature flag, 12-5
  - SSSE2 feature flag, 12-9, 12-19, 12-24
  - summary of, 7-23
- CS register, 3-13, 3-14
- CTI instruction, 7-22
- Current privilege level (see CPL)
- Current stack, 6-1, 6-3
- CVTDQ2PD instruction, 11-10
- CVTDQ2PS instruction, 11-10
- CVTPD2DQ instruction, 11-10
- CVTPD2PI instruction, 11-10
- CVTPD2PS instruction, 11-9
- CVTPI2PD instruction, 11-10
- CVTPI2PS instruction, 10-11
- CVTPS2DQ instruction, 11-10
- CVTPS2PD instruction, 11-9
- CVTPS2PI instruction, 10-11
- CVTSD2SI instruction, 11-10
- CVTSD2SS instruction, 11-9
- CVTSI2SD instruction, 11-10
- CVTSI2SS instruction, 10-11
- CVTSS2SD instruction, 11-9
- CVTSS2SI instruction, 10-11
- CVTTPD2DQ instruction, 11-10
- CVTTPD2PI instruction, 11-10
- CVTTPS2DQ instruction, 11-10
- CVTTPS2PI instruction, 10-11
- CVTTSD2SI instruction, 11-10
- CVTTSS2SI instruction, 10-11
- CWD instruction, 7-7

- CWDE instruction, 7-7
- CX register, 3-12

## D

- D (default size) flag, segment descriptor, 6-2, 6-3
- DAA instruction, 7-9
- DAS instruction, 7-9
- Data movement instructions, 7-2
- Data pointer, x87 FPU, 8-9
- Data registers, x87 FPU, 8-1
- Data segment, 3-14
- Data types
  - 128-bit packed SIMD, 4-9
  - 64-bit mode, 7-2
  - 64-bit packed SIMD, 4-9
  - alignment, 4-2
  - BCD integers, 4-10, 7-9
  - bit field, 4-8
  - byte, 4-1
  - doubleword, 4-1
  - floating-point, 4-4
  - fundamental, 4-1
  - integers, 4-3
  - numeric, 4-2
  - operated on by GP instructions, 7-1, 7-2
  - operated on by MMX technology, 9-3
  - operated on by SSE extensions, 10-5
  - operated on by SSE2 extensions, 11-3
  - operated on by x87 FPU, 8-13
  - operated on in 64-bit mode, 4-8
  - packed bytes, 9-3
  - packed doublewords, 9-3
  - packed SIMD, 4-9
  - packed words, 9-3
  - pointers, 4-7
  - quadword, 4-1, 9-3
  - signed integers, 4-4
  - strings, 4-9
  - unsigned integers, 4-3
  - word, 4-1
- DAZ (denormals-are-zeros) flag
  - MXCSR register, 10-5
- DE (denormal operand exception) flag
  - MXCSR register, 11-15
  - x87 FPU status word, 8-5, 8-28
- Debug registers
  - 64-bit mode, 3-5
  - legacy modes, 3-4
- DEC instruction, 7-8
- Decimal integers, x87 FPU, 4-11
- Deeper sleep, 2-4
- Denormal number (see Denormalized finite number)
- Denormal operand exception (#D)
  - overview of, 4-21
  - SSE and SSE2 extensions, 11-15
  - x87 FPU, 8-27
- Denormalization process, 4-16
- Denormalized finite number, 4-5, 4-15
- Denormals-are-zero
  - DAZ flag, MXCSR register, 10-5, 11-2, 11-3, 11-20
  - mode, 10-5, 11-20
- DF (direction) flag, EFLAGS register, 3-17, A-1
- DH register, 3-12
- DI register, 3-12

## INDEX

- Digital media boost, 2-4
- Displacement (operand addressing), 3-22, 3-23, 3-24
- DIV instruction, 7-9
- Divide, 4-22
- Divide by zero exception (#Z)
  - SSE and SSE2 extensions, 11-15
  - x87 FPU, 8-28
- DIVPD instruction, 11-6
- DIVPS instruction, 10-8
- DIVSD instruction, 11-6
- DIVSS instruction, 10-8
- DL register, 3-12
- DM (denormal operand exception) mask bit
  - MXCSR register, 11-15
  - x87 FPU, 8-28
  - x87 FPU control word, 8-7
- Double-extended-precision FP format, 4-4
- Doubleword, 4-1
- DS register, 3-13, 3-14
- Dual-core technology
  - introduction, 2-18
- DX register, 3-12
- Dynamic data flow analysis, 2-8
- Dynamic execution, 2-7, 2-10, 2-12, 2-13

## E

- EAX register, 3-11, 3-12
- EBP register, 3-11, 3-12, 6-3, 6-7
- EBX register, 3-11, 3-12
- ECX register, 3-11, 3-12
- EDI register, 3-11, 3-12
- EDX register, 3-11, 3-12
- Effective address, 3-22
- EFLAGS register
  - 64-bit mode, 7-2
  - condition codes, B-1
  - cross-reference with instructions, A-1
  - description of, 3-15
  - instructions that operate on, 7-21
  - overview, 3-11
  - part of basic programming environment, 7-1
  - restoring from stack, 6-7
  - saving on a procedure call, 6-7
  - status flags, 8-6, 8-7, 8-19
  - use with CMOVcc instructions, 7-3
- EIP register
  - description of, 3-18
  - overview, 3-11
  - part of basic programming environment, 7-1
  - relationship to CS register, 3-14
- EMMS instruction, 9-8, 9-9
- Enhanced Intel Deeper Sleep, 2-4
- ENTER instruction, 6-20, 7-21
- GETSEC, 5-40
- ES register, 3-13, 3-14
- ES (exception summary) flag
  - x87 FPU status word, 8-31
- ESC instructions, x87 FPU, 8-15
- ESI register, 3-11, 3-12
- ESP register, 3-12
- ESP register (stack pointer), 3-11, 6-3
- Exception flags, x87 FPU status word, 8-5
- Exception handlers
  - overview of, 6-12

- SIMD floating-point exceptions, D-1
- SSE and SSE2 extensions, 11-18
  - typical actions of a FP exception handler, 4-25
  - x87 FPU, 8-32
- Exception priority, floating-point exceptions, 4-24
- Exception-flag masks, x87 FPU control word, 8-7
- Exceptions
  - 64-bit mode, 6-19
  - description of, 6-12
  - handler, 6-12
  - implicit call to handler, 6-1
  - in real-address mode, 6-18
  - notation, 1-8
- Exponent, floating-point number, 4-12

## F

- F2XM1 instruction, 8-21
- FABS instruction, 8-17
- FADD instruction, 8-17
- FADDP instruction, 8-17
- Far call
  - description of, 6-4
  - operation, 6-5
- Far pointer
  - 16-bit addressing, 3-9
  - 32-bit addressing, 3-9
  - 64-bit mode, 4-8
  - description of, 3-7, 4-7
  - legacy modes, 4-7
- Far return operation, 6-5
- FBLD instruction, 8-16
- FBSTP instruction, 8-16
- FCHS instruction, 8-17
- FCLEX/FNCLEX instructions, 8-5
- FCMOVcc instructions, 8-7, 8-16
- FCOM instruction, 8-6, 8-18
- FCOMI instruction, 8-7, 8-18
- FCOMIP instruction, 8-7, 8-18
- FCOMP instruction, 8-6, 8-18
- FCOMPP instruction, 8-6, 8-18
- FCOS instruction, 8-5, 8-20
- FDIV instruction, 8-17
- FDIVP instruction, 8-17
- FDIVR instruction, 8-17
- FDIVRP instruction, 8-17
- Feature determination, of processor, 21-1
- FIADD instruction, 8-17
- FICOM instruction, 8-6, 8-18
- FICOMP instruction, 8-6, 8-18
- FIDIV instruction, 8-17
- FIDIVR instruction, 8-17
- FILD instruction, 8-16
- FIMUL instruction, 8-17
- FINIT/FNINIT instructions, 8-5, 8-7, 8-8, 8-23
- FIST instruction, 8-16
- FISTP instruction, 8-16
- FISTTP instruction, 5-24, 12-3
- FISUB instruction, 8-17
- FISUBR instruction, 8-17
- Flags
  - cross-reference with instructions, A-1
- Flat memory model, 3-7, 3-13
- FLD instruction, 8-16
- FLD1 instruction, 8-17

- FLDCW instruction, 8-7, 8-23
  - FLDENV instruction, 8-5, 8-9, 8-11, 8-23
  - FLDL2E instruction, 8-17
  - FLDL2T instruction, 8-17
  - FLDLG2 instruction, 8-17
  - FLDLN2 instruction, 8-17
  - FLDPI instruction, 8-17
  - FLDSW instruction, 8-23
  - FLDZ instruction, 8-17
  - Floating-point data types
    - biasing constant, 4-6
    - denormalized finite number, 4-5
    - description of, 4-4
    - double extended precision format, 4-4, 4-5
    - double precision format, 4-4, 4-5
    - half precision format, 4-5
    - infinities, 4-5
    - normalized finite number, 4-5
    - single precision format, 4-4, 4-5
    - SSE extensions, 10-5
    - SSE2 extensions, 11-3
    - storing in memory, 4-6
    - x87 FPU, 8-13
    - zeros, 4-5
  - Floating-point exception handlers
    - SSE and SSE2 extensions, 11-18
    - typical actions, 4-25
    - x87 FPU, 8-32
  - Floating-point exceptions
    - denormal operand exception (#D), 4-21, 8-28, 11-15, C-1
    - divide by zero exception (#Z), 4-22, 8-28, 11-15, C-1
    - exception conditions, 4-21
    - exception priority, 4-24
    - inexact result (precision) exception (#P), 4-23, 8-30, 11-16, C-1
    - invalid operation exception (#I), 4-21, 8-26, 11-14
    - invalid-operation exception (#IA), C-1
    - invalid-operation exception (#IS), C-1
    - invalid-operation exception (#I), C-1
    - numeric overflow exception (#O), 4-22, 8-28, 11-15, C-1
    - numeric underflow exception (#U), 4-23, 8-29, 11-16, C-1
    - summary of, 4-20, C-1
    - typical handler actions, 4-25
  - Floating-point format
    - biased exponent, 4-14
    - description of, 8-13
    - exponent, 4-12
    - fraction, 4-12
    - indefinite, 4-5
    - QNaN floating-point indefinite, 4-18
    - real number system, 4-12
    - sign, 4-12
    - significand, 4-12
  - Floating-point numbers
    - defined, 4-12
    - encoding, 4-5
  - Flush-to-zero
    - FTZ flag, MXCSR register, 10-4, 11-2
    - mode, 10-4
  - FMA operation, 14-22, 14-23
  - FMUL instruction, 8-17
  - FMULP instruction, 8-17
  - FNOP instruction, 8-23
  - Fopcode compatibility mode, 8-10
  - FPATAN instruction, 8-20, 8-21
  - FPREM instruction, 8-5, 8-18, 8-21
  - FPREM1 instruction, 8-5, 8-18, 8-21
  - FPTAN instruction, 8-5
  - Fraction, floating-point number, 4-12
  - FRNDINT instruction, 8-18
  - FRSTOR instruction, 8-5, 8-9, 8-11, 8-23
  - FS register, 3-13, 3-14
  - FSAVE/FNSAVE instructions, 8-4, 8-5, 8-9, 8-11, 8-23
  - FSCALE instruction, 8-21
  - FSIN instruction, 8-5, 8-20
  - FSINCOS instruction, 8-5, 8-20
  - FSQRT instruction, 8-18
  - FST instruction, 8-16
  - FSTCW/FNSTCW instructions, 8-7, 8-23
  - FSTENV/FNSTENV instructions, 8-4, 8-9, 8-11, 8-23
  - FSTP instruction, 8-16
  - FSTSW/FNSTSW instructions, 8-4, 8-23
  - FSUB instruction, 8-17
  - FSUBP instruction, 8-17
  - FSUBR instruction, 8-17
  - FSUBRP instruction, 8-17
  - FTST instruction, 8-6, 8-18
  - FUCOM instruction, 8-18
  - FUCOMI instruction, 8-7, 8-18
  - FUCOMIP instruction, 8-7, 8-18
  - FUCOMP instruction, 8-18
  - FUCOMPP instruction, 8-6, 8-18
  - FXAM instruction, 8-4, 8-19
  - FXCH instruction, 8-16
  - FXRSTOR instruction, 5-15, 8-12, 10-14, 11-23
  - FXSAVE instruction, 5-15, 8-12, 10-14, 11-23
  - FXTRACT instruction, 8-18
  - FYL2X instruction, 8-21
  - FYL2XP1 instruction, 8-21
- ## G
- GDTR register, 3-4, 3-6
  - General purpose registers
    - 64-bit mode, 3-5, 3-13
    - description of, 3-11
    - overview of, 3-2, 3-5
    - parameter passing, 6-7
    - part of basic programming environment, 7-1
    - using REX prefix, 3-13
  - General-purpose instructions
    - 64-bit mode, 7-1
    - basic programming environment, 7-1
    - data types operated on, 7-1, 7-2
    - description of, 7-1
    - origin of, 7-1
    - programming with, 7-1
    - summary of, 5-6, 7-2
  - GS register, 3-13, 3-14
- ## H
- HADDPD instruction, 5-25, 12-4
  - HADDPS instruction, 5-24, 12-4
  - Hardware Lock Elision (HLE), 17-2
  - Hexadecimal numbers, 1-7
  - Horizontal processing model, 12-1
  - HSUBPD instruction, 5-25, 12-5
  - HSUBPS instruction, 5-24, 12-4
  - HT Technology
    - first processor, 2-3

- implementing, 2-17
  - introduction, 2-16
- ## I
- IA-32 architecture
    - history of, 2-1
    - introduction to, 2-1
  - IA-32e mode
    - introduction, 2-20
    - segmentation, 3-22
    - See also: 64-bit mode, compatibility mode
  - IA32\_MISC\_ENABLE MSR, 8-10
  - ID (identification) flag, EFLAGS register, 3-17
  - IDIV instruction, 7-9
  - IDTR register, 3-4, 3-6
  - IE (invalid operation exception) flag
    - MXCSR register, 11-14
    - x87 FPU status word, 8-5, 8-26, 8-27
  - IEEE Standard 754, 4-4, 4-12, 8-1
  - IF (interrupt enable) flag
    - EFLAGS register, 3-17, 6-13, 20-4, A-1
  - IM (invalid operation exception) mask bit
    - MXCSR register, 11-14
    - x87 FPU control word, 8-7
  - Immediate operands, 3-20
  - IMUL instruction, 7-9
  - IN instruction, 5-10, 7-20, 20-3
  - INC instruction, 7-8
  - Indefinite
    - description of, 4-18, 14-18
    - floating-point format, 4-5, 4-14
    - integer, 4-4, 8-14
    - packed BCD integer, 4-12
    - QNaN floating-point, 4-18
  - Index (operand addressing), 3-22, 3-23, 3-24
  - Inexact result (precision)
    - exception (#P), overview, 4-23
    - exception (#P), SSE-SSE2 extensions, 11-16
    - exception (#P), x87 FPU, 8-30
    - on floating-point operations, 4-19
  - Infinity control flag, x87 FPU control word, 8-8
  - Infinity, floating-point format, 4-5, 4-16
  - INIT pin, 3-15
  - Input/output (see I/O)
  - INS instruction, 5-10, 7-20, 20-3
  - Instruction operands, 1-7
  - Instruction pointer
    - 64-bit mode, 7-2
    - EIP register, 3-11, 3-18
    - RIP register, 3-18
    - RIP, EIP, IP compared, 3-10
    - x87 FPU, 8-9
  - Instruction prefixes
    - effect on SSE and SSE2 instructions, 11-25
    - REX prefix, 3-2, 3-12
  - Instruction set
    - binary arithmetic instructions, 7-8
    - bit scan instructions, 7-14
    - bit test and modify instructions, 7-14
    - byte-set-on-condition instructions, 7-14
    - cacheability control instructions, 5-20, 5-23
    - comparison and sign change instruction, 7-8
    - control transfer instructions, 7-14
    - data movement instructions, 7-2
    - decimal arithmetic instructions, 7-9
    - EFLAGS cross-reference, A-1
    - EFLAGS instructions, 7-21
    - exchange instructions, 7-4
    - FXSAVE and FXRSTOR instructions, 5-15
    - general-purpose instructions, 5-6
    - grouped by processor, 5-2
    - increment and decrement instructions, 7-8
    - instruction ordering instructions, 5-20, 5-23
    - I/O instructions, 5-10, 7-20
    - logical instructions, 7-10
    - MMX instructions, 5-16, 9-5
    - multiply and divide instructions, 7-9
    - processor identification instruction, 7-23
    - repeating string operations, 7-19
    - rotate instructions, 7-13
    - segment register instructions, 7-22
    - shift instructions, 7-10
    - SIMD instructions, introduction to, 2-14
    - software interrupt instructions, 7-17
    - SSE instructions, 5-18
    - SSE2 instructions, 5-20
    - stack manipulation instructions, 7-5
    - string operation instructions, 7-18
    - summary, 5-1
    - system instructions, 5-32, 5-37
    - test instruction, 7-14
    - type conversion instructions, 7-7
    - x87 FPU and SIMD state management instructions, 5-15
    - x87 FPU instructions, 5-13
  - INT instruction, 6-18, 7-23
  - Integers
    - description of, 4-3
    - indefinite, 4-4, 8-14
    - signed integer encodings, 4-4
    - signed, description of, 4-4
    - unsigned integer encodings, 4-3
    - unsigned, description of, 4-3
  - Intel 64 architecture
    - 64-bit mode, 3-1
    - 64-bit mode instructions, 5-38
    - address space, 3-6
    - compatibility mode, 3-1
    - data types, 4-1
    - executing calls, 6-1
    - general purpose instructions, 7-1
    - generations, 2-20
    - history of, 2-1
    - IA32e mode, 3-1
    - introduction, 2-20
    - memory organization, 3-6, 3-8
    - See also: IA-32e mode
  - Intel Advanced Digital Media Boost, 2-4, 2-11
  - Intel Advanced Smart Cache, 2-10
  - Intel Advanced Thermal Manager, 2-4
  - Intel Core 2 Extreme processor family, 2-4, 2-18
  - Intel Core Duo processor, 2-4, 2-18
  - Intel Core microarchitecture, 2-4, 2-10, 2-12, 2-13, 2-18
  - Intel Core Solo processor, 2-4
  - Intel Dynamic Power Coordination, 2-4
  - Intel NetBurst microarchitecture, 1-3
    - description of, 2-8
    - introduction, 2-8
  - Intel Pentium D processor, 2-18
  - Intel Pentium processor Extreme Edition, 2-18

- Intel Smart Cache, 2-4
- Intel Smart Memory Access, 2-4, 2-11
- Intel software network link, 1-9
- Intel Transactional Synchronization, 15-3, 17-1
- Intel VTune Performance Analyzer
  - related information, 1-9
- Intel Wide Dynamic Execution, 2-4, 2-10, 2-12, 2-13
- Intel Xeon processor, 1-1
  - description of, 2-3
- Intel Xeon processor 5100 series, 2-4, 2-18
- Intel386 processor, 2-1
- Intel486 processor
  - history of, 2-1
- Inter-privilege level call
  - description of, 6-7
  - operation, 6-9
- Inter-privilege level return
  - description of, 6-7
  - operation, 6-9
- Interrupt gate, 6-13
- Interrupt handler, 6-12
- Interrupts
  - 64-bit mode, 6-19
  - description of, 6-12
  - handler, 6-12
  - implicit call to an interrupt handler
    - procedure, 6-13
  - implicit call to an interrupt handler task, 6-18
  - implicit call to interrupt handler procedure, 6-13
  - implicit call to interrupt handler task, 6-18
  - in real-address mode, 6-18
  - maskable, 6-13
- INTn instruction, 7-17
- INTO instruction, 6-18, 7-18, 7-23
- Invalid arithmetic operand exception (#IA)
  - description of, 8-27
  - masked response to, 8-27
- Invalid operation exception (#I)
  - overview, 4-21
  - SSE and SSE2 extensions, 11-14
  - x87 FPU, 8-26
- IOPL (I/O privilege level) field
  - EFLAGS register, 3-17, 20-3
- IRET instruction, 3-18, 6-17, 6-18, 7-15, 7-23, 20-4
- I/O
  - address space, 20-1
  - instruction serialization, 20-5
  - instructions, 5-10, 7-20, 20-3
  - I/O privilege level (see IOPL)
  - map base, 20-4
  - permission bit map, 20-4
  - ports, 3-4, 20-1, 20-2, 20-3, 20-5
  - sensitive instructions, 20-3

## J

- J-bit, 4-12
- Jcc instructions, 3-17, 3-18, 7-15
- JMP instruction, 3-18, 7-15, 7-22

## L

- L1 (level 1) cache, 2-7, 2-9
- L2 (level 2) cache, 2-7, 2-9
- LAHF instruction, 3-15, 7-21

- Last instruction opcode, x87 FPU, 8-10
- LDDQU instruction, 5-24, 12-3
- LDMXCSR instruction, 10-12, 11-24
- LDS instruction, 7-23
- LDTR register, 3-4, 3-6
- LEA instruction, 7-23
- LEAVE instruction, 6-20, 6-24, 7-21
- LES instruction, 7-23
- LFENCE instruction, 11-12
- LGS instruction, 7-23
- Linear address, 3-7
- Linear address space
  - defined, 3-7
  - maximum size, 3-7
- LOCK signal, 7-4
- LODS instruction, 3-17, 7-18
- Log epsilon, x87 FPU operation, 8-21
- Logical address, 3-7
- LOOP instructions, 7-16
- LOOPcc instructions, 3-17, 7-16
- LSS instruction, 7-23

## M

- Machine check registers, 3-4
- Maskable interrupts, 6-13
- Masked responses
  - denormal operand exception (#D), 4-21, 8-28
  - divide by zero exception (#Z), 4-22, 8-28
  - inexact result (precision) exception (#P), 4-24, 8-30
  - invalid arithmetic operation (#IA), 8-27
  - invalid operation exception (#I), 4-21
  - numeric overflow exception (#O), 4-22, 8-29
  - numeric underflow exception (#U), 4-23, 8-29
  - stack overflow or underflow
    - exception (#IS), 8-27
- MASKMOVDQU instruction, 11-12, 11-25
- MASKMOVQ instruction, 10-12, 11-25
- Masks, exception-flags
  - MXCSR register, 10-4
  - x87 FPU control word, 8-7
- MAXPD instruction, 11-6
- MAXPS instruction, 10-8
- MAXSD instruction, 11-6
- MAXSS instruction, 10-9
- Memory
  - flat memory model, 3-7
  - management registers, 3-4
  - memory type range registers (MTRRs), 3-4
  - modes of operation, 3-9
  - organization, 3-6, 3-7
  - physical, 3-6
  - real address mode memory model, 3-7, 3-8
  - segmented memory model, 3-7
  - virtual-8086 mode memory model, 3-7, 3-8
- Memory operands
  - 64-bit mode, 3-21
  - legacy modes, 3-21
- Memory-mapped I/O, 20-2
- MFENCE instruction, 11-12, 11-25
- Microarchitecture
  - (see Intel NetBurst microarchitecture)
  - (see P6 family microarchitecture)
- MINPD instruction, 11-6
- MINPS instruction, 10-9

## INDEX

- MINSD instruction, 11-7
  - MINSS instruction, 10-9
  - MMX instruction set
    - arithmetic instructions, 9-6
    - comparison instructions, 9-7
    - conversion instructions, 9-7
    - data transfer instructions, 9-6
    - EMMS instruction, 9-8
    - logical instructions, 9-7
    - overview, 9-5
    - shift instructions, 9-8
  - MMX registers
    - description of, 9-2
    - overview of, 3-2
  - MMX technology
    - 64-bit mode, 9-2
    - 64-bit packed SIMD data types, 4-9
    - compatibility mode, 9-2
    - compatibility with FPU architecture, 9-8
    - data types, 9-3
    - detecting MMX technology with CPUID instruction, 9-8
    - effect of instruction prefixes on MMX instructions, 9-11
    - exception handling in MMX code, 9-11
    - IA-32e mode, 9-2
    - instruction set, 5-16, 9-5
    - interfacing with MMX code, 9-10
    - introduction to, 9-1
    - memory data formats, 9-3
    - mixing MMX and floating-point instructions, 9-10
    - MMX registers, 9-2
    - programming environment (overview), 9-1
    - register mapping, 9-11
    - saturation arithmetic, 9-4
    - SIMD execution environment, 9-4
    - transitions between x87 FPU - MMX code, 9-9
    - updating MMX technology routines using 128-bit SIMD integer instructions, 11-24
    - using MMX code in a multitasking operating system environment, 9-10
    - using the EMMS instruction, 9-9
    - wraparound mode, 9-4
  - Model-specific registers (see MSRs)
  - Modes of operation
    - 64-bit mode, 3-1
    - compatibility mode, 3-1
    - memory models used with, 3-9
    - overview, 3-1, 3-5
    - protected mode, 3-1
    - real address mode, 3-1
    - system management mode (SMM), 3-1
  - MONITOR instruction, 5-25, 12-5
  - Moore's law, 2-20
  - MOV instruction, 7-3, 7-22
  - MOVAPD instruction, 11-5, 11-23
  - MOVAPS instruction, 10-7, 11-23
  - MOVD instruction, 9-6
  - MOVDDUP instruction, 5-25, 12-3
  - MOVQ2Q instruction, 11-11
  - MOVQ2DQ instruction, 11-11
  - MOVQ instruction, 9-6
  - MOVQ2DQ instruction, 11-11
  - MOVS instruction, 3-17, 7-18
  - MOVSD instruction, 11-6, 11-23
  - MOVSHDUP instruction, 5-25, 12-3
  - MOVSLDUP instruction, 5-25, 12-3
  - MOVSS instruction, 10-7, 11-23
  - MOVSB instruction, 7-8
  - MOVSD instruction, 11-6, 11-23
  - MOVUPS instruction, 10-6, 10-7, 11-23
  - MOVZX instruction, 7-8
  - MS-DOS compatibility mode, 8-32
  - MSRs, 3-4
  - MTRRs, 3-4
  - MUL instruction, 7-9
  - MULPD instruction, 11-6
  - MULPS instruction, 10-8
  - MULSD instruction, 11-6
  - MULSS instruction, 10-8
  - Multi-core technology, 2-18
  - Multi-threading capability, 2-18
  - MWAIT instruction, 5-25, 12-5
  - MXCSR register, 11-16
    - denormals-are-zero (DAZ) flag, 10-5, 11-2, 11-3
    - description, 10-3
    - flush-to-zero flag (FTZ), 10-4
    - FXSAVE and FXRSTOR instructions, 11-23
    - LDMXCSR instruction, 11-24
    - load and store instructions, 10-12
    - RC field, 4-19
    - saving on a procedure or function call, 11-23
    - SIMD floating-point mask and flag bits, 10-4
    - SIMD floating-point rounding control field, 10-4
    - state management instructions, 5-20, 10-12
    - STMXCSR instruction, 11-24
    - writing to while preventing general-protection exceptions (#GP), 11-21
- ## N
- NaNs
    - description of, 4-14, 4-16
    - encoding of, 4-5, 4-15
    - SNaNs vs. QNaNs, 4-16
  - Near call
    - description of, 6-4
    - operation, 6-4
  - Near pointer
    - 64-bit mode, 4-8
    - legacy modes, 4-7
  - Near return operation, 6-4
  - NEG instruction, 7-8
  - NetBurst microarchitecture (see Intel NetBurst microarchitecture)
  - Non-arithmetic instructions, x87 FPU, 8-25
  - Non-number encodings, floating-point format, 4-14
  - Non-temporal data

- caching of, 10-12
  - description, 10-12
  - temporal vs. non-temporal data, 10-12
- Non-waiting instructions, x87 FPU, 8-24, 8-32
- NOP instruction, 7-23
- Normalized finite number, 4-5, 4-14, 4-15
- NOT instruction, 7-10
- Notation
  - bit and byte order, 1-6
  - exceptions, 1-8
  - hexadecimal and binary numbers, 1-7
  - instruction operands, 1-7
  - notational conventions, 1-6
  - reserved bits, 1-7
  - segmented addressing, 1-8
- NT (nested task) flag, EFLAGS register, 3-17, A-1
- Numeric overflow exception (#O)
  - overview, 4-22
  - SSE and SSE2 extensions, 11-15
  - x87 FPU, 8-4, 8-28
- Numeric underflow exception (#U)
  - overview, 4-23
  - SSE and SSE2 extensions, 11-16
  - x87 FPU, 8-4, 8-29

## O

- OE (numeric overflow exception) flag
  - MXCSR register, 11-16
  - x87 FPU status word, 8-5, 8-29
- OF (overflow) flag
  - EFLAGS register, 3-16, 6-18
- OF (overflow) flag, EFLAGS register, A-1
- Offset (operand addressing, 64-bit mode), 3-23
- Offset (operand addressing), 3-22
- OM (numeric overflow exception) mask bit
  - MXCSR register, 11-16
  - x87 FPU control word, 8-7, 8-29
- Operand
  - addressing, modes, 3-19
  - instruction, 1-7
  - size attribute, 3-18
  - sizes, 3-9, 3-19
  - x87 FPU instructions, 8-15
- OR instruction, 7-10
- Ordering I/O, 20-5
- ORPD instruction, 11-7
- ORPS instruction, 10-9
- OSXMMEXCPT flag
  - control register CR4, 11-18
- OUT instruction, 5-10, 7-20, 20-3
- OUTS instruction, 5-10, 7-20, 20-3
- Overflow exception (#OF), 6-18
- Overflow, x87 FPU stack, 8-26

## P

- P6 family microarchitecture
  - description of, 2-7
  - history of, 2-2
- P6 family processors
  - description of, 1-1
  - history of, 2-2
  - P6 family microarchitecture, 2-7
- PABSB instruction, 5-26, 12-7
- PABSD instruction, 12-8
- PABSW instruction, 5-26, 12-8
- Packed
  - BCD integer indefinite, 4-12
  - BCD integers, 4-11
  - bytes, 9-3
  - doublewords, 9-3
  - SIMD data types, 4-9
  - SIMD floating-point values, 4-9
  - SIMD integers, 4-9
  - words, 9-3
- PACKSSWB instruction, 9-7
- PACKUSWB instruction, 9-7
- PADDB instruction, 9-6
- PADDD instruction, 9-6
- PADDQ instruction, 11-11
- PADDSB instruction, 9-7
- PADDSW instruction, 9-7
- PADDUSB instruction, 9-7
- PADDUSW instruction, 9-7
- PADDW instruction, 9-6
- PALIGNR instruction, 5-27, 12-8
- PAND instruction, 9-7
- PANDN instruction, 9-7
- Parameter passing
  - argument list, 6-7
  - on stack, 6-7
  - on the stack, 6-7
  - through general-purpose registers, 6-7
  - x87 FPU register stack, 8-3
  - XMM registers, 11-23
- PAUSE instruction, 11-12
- PAVGB instruction, 10-11
- PC (precision) field, x87 FPU control word, 8-7
- PCMPEQB instruction, 9-7
- PCMPEQD instruction, 9-7
- PCMPEQW instruction, 9-7
- PCMPGTB instruction, 9-7
- PCMPGTD instruction, 9-7
- PCMPGTW instruction, 9-7
- PE (inexact result exception) flag, 11-16
  - MXCSR register, 4-19
  - x87 FPU status word, 4-19, 8-4, 8-5, 8-30
- Pentium 4 processor, 1-1
  - description of, 2-3, 2-4
- Pentium 4 processor supporting Hyper-Threading Technology
  - description of, 2-3, 2-4
- Pentium II processor, 1-3
  - description of, 2-2
  - P6 family microarchitecture, 2-7
- Pentium II Xeon processor
  - description of, 2-2
- Pentium III processor, 1-3
  - description of, 2-2
  - P6 family microarchitecture, 2-7
- Pentium III Xeon processor
  - description of, 2-3
- Pentium M processor
  - description of, 2-3
  - instructions supported, 2-3
- Pentium Pro processor, 1-3
  - description of, 2-2
  - P6 family microarchitecture, 2-7
- Pentium processor, 1-1
  - history of, 2-2

## INDEX

- Pentium processor Extreme Edition
  - introduction, 2-4
- Pentium processor with MMX technology, 2-2
- Performance monitoring counters, 3-4
- PEXTRW instruction, 10-11
- PF (parity) flag, EFLAGS register, 3-16, A-1
- PHADD instruction, 5-26, 12-7
- PHADDSW instruction, 5-25, 12-7
- PHADDW instruction, 5-25, 12-7
- PHSUBD instruction, 5-26, 12-7
- PHSUBSW instruction, 5-26, 12-7
- PHSUBW instruction, 5-26, 12-7
- Physical
  - address space, 3-6
  - memory, 3-6
- PINSRW instruction, 10-11
- Pi, x87 FPU constant, 8-21
- PM (inexact result exception) mask bit
  - MXCSR register, 11-16
  - x87 FPU control word, 8-7, 8-30
- PMADDUBSW instruction, 5-26, 12-8
- PMADDWD instruction, 9-7
- PMAXSW instruction, 10-11
- PMAXUB instruction, 10-11
- PMINSW instruction, 10-11
- PMINUB instruction, 10-11
- PMOVMASKB instruction, 10-11
- PMULHRWS instruction, 5-26, 12-8
- PMULHUW instruction, 10-12
- PMULUDQ instruction, 11-11
- Pointer data types, 4-7, 4-8
- Pointers
  - 64-bit mode, 4-8
  - far pointer, 4-7
  - near pointer, 4-7
- POP instruction, 6-1, 6-2, 7-6, 7-22
- POPA instruction, 6-7, 7-6
- POPF instruction, 3-15, 6-7, 7-21, 20-4
- POPCD instruction, 3-15, 6-7, 7-21
- POR instruction, 9-7
- Power coordination, 2-4
- PREFETCHH instructions, 10-13, 11-25
- Privilege levels
  - description of, 6-8
  - inter-privilege level calls, 6-7
  - protection rings, 6-8
  - stack switching, 6-14
- Procedure calls
  - description of, 6-4
  - far call, 6-4
  - for block-structured languages, 6-20
  - inter-privilege level call, 6-9
  - linking, 6-3
  - near call, 6-4
  - overview, 6-1
  - return instruction pointer (EIP register), 6-3
  - saving procedure state information, 6-7
  - stack, 6-1
  - stack switching, 6-8
  - to exception handler procedure, 6-13
  - to exception task, 6-18
  - to interrupt handler procedure, 6-13
  - to interrupt task, 6-18
  - to other privilege levels, 6-7
  - types of, 6-1

- Processor identification
  - earlier Intel architecture processors, 21-1
  - early processors, 21-1
  - using CPUID instruction, 21-1
- Processor state information, saving, 6-7
- Protected mode
  - I/O, 20-3
  - memory models used, 3-9
  - overview, 3-1
- Protection rings, 6-8
- PSADBW instruction, 10-12
- PSHUFB instruction, 5-26, 12-8
- PSHUFD instruction, 11-11
- PSHUFHW instruction, 11-11
- PSHUFLW instruction, 11-11
- PSHUFW instruction, 10-12, 11-11
- PSIGNB/W/D instruction, 5-26, 12-8
- PSLLD instruction, 9-8
- PSLLDQ instruction, 11-11
- PSLLQ instruction, 9-8
- PSLLW instruction, 9-8
- PSRLDQ instruction, 11-11
- PSUBB instruction, 9-6
- PSUBD instruction, 9-6
- PSUBQ instruction, 11-11
- PSUBSB instruction, 9-7
- PSUBSW instruction, 9-7
- PSUBUSB instruction, 9-7
- PSUBUSW instruction, 9-7
- PSUBW instruction, 9-6
- PUNPCKHBW instruction, 9-7
- PUNPCKHDQ instruction, 9-7
- PUNPCKHQDQ instruction, 11-11
- PUNPCKHWD instruction, 9-7
- PUNPCKLBW instruction, 9-7
- PUNPCKLDQ instruction, 9-7
- PUNPCKLQDQ instruction, 11-11
- PUNPCKLWD instruction, 9-7
- PUSH instruction, 6-1, 6-2, 7-5, 7-22
- PUSHA instruction, 6-7, 7-5
- PUSHF instruction, 3-15, 6-7, 7-21
- PUSHFD instruction, 3-15, 6-7, 7-21
- PXOR instruction, 9-7

## Q

- QNaN floating-point indefinite, 4-5, 4-18, 8-14
- QNaNs
  - description of, 4-16
  - effect on COMISD and UCOMISD, 11-7
  - encodings, 4-5
  - operating on, 4-17
  - rules for generating, 4-17
  - using in applications, 4-17
- Quadword, 4-1, 9-3
- Quiet NaN (see QNaN)

## R

- R8D-R15D registers, 3-12
- R8-R15 registers, 3-12
- RAX register, 3-12
- RBP register, 3-12, 6-4
- RBX register, 3-12
- RC (rounding control) field

- MXCSR register, 4-19, 10-4
  - x87 FPU control word, 4-19, 8-8
  - RCL instruction, 7-13
  - RCPPS instruction, 10-8
  - RCPSS instruction, 10-8
  - RCR instruction, 7-13
  - RCX register, 3-12
  - RDI register, 3-12
  - RDRAND, 7-24
  - RDX register, 3-12
  - Real address mode
    - handling exceptions in, 6-18
    - handling interrupts in, 6-18
    - memory model, 3-7, 3-8
    - memory model used, 3-9
    - not in 64-bit mode, 3-9
    - overview, 3-1
  - Real numbers
    - continuum, 4-12
    - encoding, 4-14, 4-15
    - notation, 4-13, 14-18
    - system, 4-12
  - Register operands
    - 64-bit mode, 3-20
    - legacy modes, 3-20
  - Register stack, x87 FPU, 8-1
  - Registers
    - 64-bit mode, 3-12, 3-15
    - control registers, 3-4
    - CR in 64-bit mode, 3-5
    - debug registers, 3-4
    - EFLAGS register, 3-11, 3-15
    - EIP register, 3-11, 3-18
    - general purpose registers, 3-11
    - instruction pointer, 3-11
    - machine check registers, 3-4
    - memory management registers, 3-4
    - MMX registers, 3-2, 9-2
    - MSRs, 3-4
    - MTRRs, 3-4
    - MXCSR register, 10-4
    - performance monitoring counters, 3-4
    - REX prefix, 3-12
    - segment registers, 3-11, 3-13
    - x87 FPU registers, 8-1
    - XMM registers, 3-2, 10-3
  - Related literature, 1-9
  - REP/REPE/REPZ/REPNE/REPNZ
    - prefixes, 7-19, 20-3
  - Reserved bits, 1-7
  - RESET pin, 3-15
  - RET instruction, 3-18, 6-3, 6-4, 7-15, 7-22
  - Return instruction pointer, 6-3
  - Returns, from procedure calls
    - exception handler, return from, 6-13
    - far return, 6-5
    - inter-privilege level return, 6-9
    - interrupt handler, return from, 6-13
    - near return, 6-4
  - REX prefixes, 3-2, 3-12, 3-19
  - RF (resume) flag, EFLAGS register, 3-17, A-1
  - RFLAGS, 3-18
  - RFLAGS register, 7-22
    - See EFLAGS register
  - RIP register, 6-4
    - 64-bit mode, 7-2
    - description of, 3-18
    - relation to EIP, 7-2
  - ROL instruction, 7-13
  - ROR instruction, 7-13
  - Rounding
    - modes, floating-point operations, 4-19
    - modes, x87 FPU, 8-8
    - toward zero (truncation), 4-19
  - Rounding control (RC) field
    - MXCSR register, 4-19, 10-4
    - x87 FPU control word, 4-19, 8-8
  - RSI register, 3-12
  - RSP register, 3-12, 6-4
  - RSQRTPS instruction, 10-8
  - RSQRTSS instruction, 10-8
- ## S
- SAHF instruction, 3-15, 7-21
  - SAL instruction, 7-10
  - SAR instruction, 7-11
  - Saturation arithmetic (MMX instructions), 9-4
  - SBB instruction, 7-8
  - Scalar operations
    - defined, 10-7, 11-5
    - scalar double precision FP operands, 11-5
    - scalar single precision FP operands, 10-7
  - Scale (operand addressing), 3-22, 3-23, 3-24
  - Scale, x87 FPU operation, 8-21
  - Scaling bias value, 8-29, 8-30
  - SCAS instruction, 3-17, 7-18
  - Segment
    - defined, 3-7
    - maximum number, 3-7
  - Segment override prefixes, 3-21
  - Segment registers
    - 64-bit mode, 3-15, 3-22, 7-2
    - default usage rules, 3-21
    - description of, 3-11, 3-13
    - part of basic programming environment, 7-1
  - Segment selector
    - description of, 3-7, 3-13
    - segment override prefixes, 3-21
    - specifying, 3-21
  - Segmented memory model, 1-8, 3-7, 3-13
  - Serialization of I/O instructions, 20-5
  - Serializing instructions, 20-5
  - SETcc instructions, 3-17, 7-14
  - SF (sign) flag, EFLAGS register, 3-16, A-1
  - SF (stack fault) flag, x87 FPU status word, 8-6, 8-26
  - SFENCE instruction, 10-14, 11-12, 11-25
  - SHL instruction, 7-10
  - SHLD instruction, 7-12
  - SHR instruction, 7-11
  - SHRD instruction, 7-12
  - Shuffle instructions
    - SSE extensions, 10-9
    - SSE2 extensions, 11-7
  - SHUFPD instruction, 11-7
  - SI register, 3-12
  - Signaling NaN (see SNaN)
  - Signed
    - infinity, 4-16
    - integers, description of, 4-4

## INDEX

- integers, encodings, 4-4
- zero, 4-15
- Significand, of floating-point number, 4-12
- Sign, floating-point number, 4-12
- SIMD floating-point exception (#XM), 11-18
- SIMD floating-point exceptions
  - denormal operand exception (#D), 11-15
  - divide-by-zero (#Z), 11-15
  - exception conditions, 11-14
  - exception handlers, D-1
  - inexact result exception (#P), 11-16
  - invalid operation exception (#I), 11-14
  - list of, 11-13
  - numeric overflow exception (#O), 11-15
  - numeric underflow exception (#U), 11-16
  - precision exception (#P), 11-16
  - software handling, 11-18
  - summary of, C-1
  - writing exception handlers for, D-1
- SIMD floating-point flag bits, 10-4
- SIMD floating-point mask bits, 10-4
- SIMD floating-point rounding control field, 10-4
- SIMD (single instruction, multiple-data)
  - operations, on packed double precision floating-point operands, 11-4
- SIMD (single-instruction, multiple-data)
  - execution model, 2-2, 9-4
  - instructions, 2-14, 5-20, 10-7
  - MMX instructions, 5-16
  - operations, on packed single precision floating-point operands, 10-6
  - packed data types, 4-9
  - SSE instructions, 5-18
  - SSE2 instructions, 11-4, 12-2, 12-6
- Sine, x87 FPU operation, 8-20
- Single precision floating-point format, 4-4
- Sleep, 2-4
- Smart cache, 2-4
- Smart memory access, 2-11
- smart memory access, 2-4
- SMM
  - memory model used, 3-9
  - overview, 3-1
- SNaNs
  - description of, 4-16
  - effect on COMISD and UCOMISD, 11-7
  - encodings, 4-5
  - operating on, 4-17
  - typical uses of, 4-16
  - using in applications, 4-17
- Software compatibility, 1-7
- SP register, 3-12
- Speculative execution, 2-7, 2-9
- Spin-wait loops
  - programming with PAUSE instruction, 11-12
- SQRTPD instruction, 11-6
- SQRTPS instruction, 10-8
- SQRTSD instruction, 11-6
- SQRTSS instruction, 10-8
- SS register, 3-13, 3-14, 6-1
- SSE extensions
  - 128-bit packed single precision data type, 10-5
  - 64-bit mode, 10-3
  - 64-bit SIMD integer instructions, 10-11
  - branching on arithmetic operations, 11-24
  - cacheability control instructions, 10-12
  - cacheability hint instructions, 11-25
  - caller-save requirement for procedure and function calls, 11-24
  - checking for SSE and SSE2 support, 11-19
  - comparison instructions, 10-9
  - compatibility mode, 10-3
  - compatibility of SIMD and x87 FPU floating-point data types, 11-22
  - conversion instructions, 10-11
  - data movement instructions, 10-7
  - data types, 10-5, 12-1
  - denormal operand exception (#D), 11-15
  - denormals-are-zeros mode, 10-5
  - divide by zero exception (#Z), 11-15
  - exceptions, 11-13
  - floating-point format, 4-12
  - flush-to-zero mode, 10-4
  - generating SIMD FP exceptions, 11-16
  - handling combinations of masked and unmasked exceptions, 11-18
  - handling masked exceptions, 11-17
  - handling SIMD floating-point exceptions in software, 11-18
  - handling unmasked exceptions, 11-18
  - inexact result exception (#P), 11-16
  - instruction prefixes, effect on SSE and SSE2 instructions, 11-25
  - instruction set, 5-18, 10-6
  - interaction of SIMD and x87 FPU floating-point exceptions, 11-18
  - interaction of SSE and SSE2 instructions with x87 FPU and MMX instructions, 11-22
  - interfacing with SSE and SSE2 procedures and functions, 11-23
  - intermixing packed and scalar floating-point and 128-bit SIMD integer instructions and data, 11-22
  - introduction, 2-2
  - invalid operation exception (#I), 11-14
  - logical instructions, 10-9
  - masked responses to invalid arithmetic operations, 11-14
  - memory ordering instruction, 10-14
  - MMX technology compatibility, 10-5
  - MXCSR register, 10-3
  - MXCSR state management instructions, 10-12
  - non-temporal data, operating on, 10-12
  - numeric overflow exception (#O), 11-15
  - numeric underflow exception (#U), 11-16
  - packed 128-Bit SIMD data types, 4-9
  - packed and scalar floating-point instructions, 10-6
  - programming environment, 10-2
  - QNaN floating-point indefinite, 4-18
  - restoring SSE and SSE2 state, 11-21
  - REX prefixes, 10-3
  - saving SSE and SSE2 state, 11-21
  - saving XMM register state on a procedure or function call, 11-23
  - shuffle instructions, 10-9
  - SIMD floating-point exception conditions, 11-14
  - SIMD floating-point exception cross reference, C-3
  - SIMD floating-point exception (#XM), 11-18
  - SIMD floating-point exceptions, 11-13
  - SIMD floating-point mask and flag bits, 10-4
  - SIMD floating-point rounding control field, 10-4
  - SSE and SSE2 conversion instruction chart, 11-9
  - SSE feature flag, CPUID instruction, 11-20
  - SSE2 compatibility, 10-5
  - system programming, 13-23

- unpack instructions, 10-9
- updating MMX technology routines
  - using 128-bit SIMD integer instructions, 11-24
- x87 FPU compatibility, 10-5
- XMM registers, 10-3
- SSE feature flag, CPUID instruction, 11-20, 12-5
- SSE instructions
  - descriptions of, 10-6
  - SIMD floating-point exception cross-reference, C-3
  - summary of, 5-18
- SSE2 extensions
  - 128-bit packed single precision
    - data type, 11-3
  - 128-bit packed single precision data type, 12-1
  - 128-bit SIMD integer instruction
    - extensions, 11-11
  - 64-bit and 128-bit SIMD integer instructions, 11-11
  - 64-bit mode, 11-3
  - arithmetic instructions, 11-6
  - branch hints, 11-13
  - branching on arithmetic operations, 11-24
  - cacheability control instructions, 11-12
  - cacheability hint instructions, 11-25
  - caller-save requirement for procedure and function calls, 11-24
  - checking for SSE and SSE2 support, 11-19
  - comparison instructions, 11-7
  - compatibility mode, 11-3
  - compatibility of SIMD and x87 FPU floating-point data types, 11-22
  - conversion instructions, 11-9
  - data movement instructions, 11-5
  - data types, 11-3, 12-1
  - denormal operand exception (#D), 11-15
  - denormals-are-zero mode, 11-3
  - divide by zero exception (#Z), 11-15
  - exceptions, 11-13
  - floating-point format, 4-12
  - generating SIMD floating-point exceptions, 11-16
  - handling combinations of masked and unmasked exceptions, 11-18
  - handling masked exceptions, 11-17
  - handling SIMD floating-point exceptions in software, 11-18
  - handling unmasked exceptions, 11-18
  - inexact result exception (#P), 11-16
  - instruction prefixes, effect on SSE and SSE2 instructions, 11-25
  - instruction set, 5-20
  - instructions, 11-4, 12-2, 12-6
  - interaction of SIMD and x87 FPU floating-point exceptions, 11-18
  - interaction of SSE and SSE2 instructions with x87 FPU and MMX instructions, 11-22
  - interfacing with SSE and SSE2 procedures and functions, 11-23
  - intermixing packed and scalar floating-point and 128-bit SIMD integer instructions and data, 11-22
  - invalid operation exception (#I), 11-14
  - logical instructions, 11-7
  - masked responses to invalid arithmetic operations, 11-14
  - memory ordering instructions, 11-12
  - MMX technology compatibility, 11-3
  - numeric overflow exception (#O), 11-15
  - numeric underflow exception (#U), 11-16
  - packed 128-Bit SIMD data types, 4-9
  - packed and scalar floating-point instructions, 11-4
  - programming environment, 11-2
  - QNaN floating-point indefinite, 4-18
  - restoring SSE and SSE2 state, 11-21
  - REX prefixes, 11-3
  - saving SSE and SSE2 state, 11-21
  - saving XMM register state on a procedure or function call, 11-23
  - shuffle instructions, 11-7
  - SIMD floating-point exception conditions, 11-14
  - SIMD floating-point exception cross reference, C-5
  - SIMD floating-point exception (#XM), 11-18
  - SIMD floating-point exceptions, 11-13
  - SSE and SSE2 conversion instruction chart, 11-9
  - SSE compatibility, 11-3
  - SSE2 feature flag, CPUID instruction, 11-20
  - system programming, 13-23
  - unpack instructions, 11-7
  - updating MMX technology routines using 128-bit SIMD integer instructions, 11-24
  - x87 FPU compatibility, 11-3
  - SSE2 feature flag, CPUID instruction, 11-20, 12-5
  - SSE2 instructions
    - descriptions of, 11-4, 12-2, 12-6
    - SIMD floating-point exception cross-reference, C-5
    - summary of, 5-20
  - SSE3 extensions
    - 64-bit mode, 12-1
    - asymmetric processing, 12-1
    - compatibility mode, 12-1
    - DNA exceptions, 12-9
    - emulation, 12-10
    - enabling support in a system executive, 12-5, 12-18
    - exceptions, 12-9
    - guideline for packed addition/subtraction instructions, 12-6
    - horizontal addition/subtraction instructions, 12-4
    - horizontal processing, 12-1
    - instruction that addresses cache line splits, 5-24
    - instruction that improves X87-FP integer conversion, 5-24
    - instructions for horizontal addition/subtraction, 5-24
    - instructions for packed addition/subtraction, 5-24
    - instructions that enhance LOAD/MOVE/DUPLICATE, 5-25
    - instructions that improve synchronization between agents, 5-25
    - LOAD/MOVE/DUPLICATE enhancement instructions, 12-3
    - MMX technology compatibility, 12-1
    - numeric error flag and IGNNE#, 12-9
    - packed addition/subtraction instructions, 12-4
    - programming environment, 12-1
    - REX prefixes, 12-1
    - SIMD floating-point exception cross reference, C-7, C-8
    - specialized 120-bit load instruction, 12-3
    - SSE compatibility, 12-1
    - SSE2 compatibility, 12-1
    - system programming, 13-23
    - x87 FPU compatibility, 12-1
  - SSE3 instructions
    - descriptions of, 12-2
    - SIMD floating-point exception
      - cross-reference, C-7, C-8
    - summary of, 5-24
  - SSSE3 extensions
    - 64-bit mode, 12-1
    - asymmetric processing, 12-1
    - checking for support, 12-9
    - compatibility mode, 12-1
    - data types, 12-1
    - DNA exceptions, 12-9

- emulation, 12-10
- enabling support in a system executive, 12-9
- exceptions, 12-9
- horizontal add/subtract instructions, 12-7
- horizontal processing, 12-1
- multiply and add packed instructions, 12-8
- numeric error flag and IGNE#, 12-9
- packed absolute value instructions, 12-7
- packed align instruction, 12-8
- packed multiply high instructions, 12-8
- packed shuffle instruction, 12-8
- programming environment, 12-1
- SSSE3 instructions
  - descriptions of, 12-6
  - summary of, 5-25
- Stack
  - 64-bit mode, 3-5, 6-4
  - 64-bit mode behavior, 6-19
  - address-size attribute, 6-3
  - alignment, 6-2
  - alignment of stack pointer, 6-2
  - current stack, 6-1, 6-3
  - description of, 6-1
  - EIP register (return instruction pointer), 6-3
  - maximum size, 6-1
  - number allowed, 6-1
  - overview of, 3-4
  - passing parameters on, 6-7
  - popping values from, 6-1
  - procedure linking information, 6-3
  - pushing values on, 6-1
  - return instruction pointer, 6-3
  - SS register, 6-1
  - stack segment, 3-14, 6-1
  - stack-frame base pointer, EBP register, 6-3
  - switching
    - on calls to interrupt and exception handlers, 6-14
    - on inter-privilege level calls, 6-10, 6-17
    - privilege levels, 6-8
  - width, 6-2
- Stack, x87 FPU
  - stack fault, 8-6
  - stack overflow and underflow exception (#IS), 8-4, 8-26
- Status flags
  - EFLAGS register, 3-16, 8-6, 8-7, 8-19
- STC instruction, 3-16, 7-21
- STD instruction, 3-17, 7-21
- STI instruction, 7-22, 20-4
- Sticky bits, 8-5
- STMXCSR instruction, 10-12, 11-24
- STOS instruction, 3-17, 7-19
- Streaming SIMD extensions 2 (see SSE2 extensions)
- Streaming SIMD extensions (see SSE extensions)
- String data type, 4-9
- ST(0), top-of-stack register, 8-3
- SUB instruction, 7-8
- Superscalar microarchitecture
  - P6 family microarchitecture, 2-2
  - P6 family processors, 2-7
  - Pentium 4 processor, 2-9
  - Pentium Pro processor, 2-2
  - Pentium processor, 2-2
- System management mode (see SMM)
- System programming
  - SSE/SSE2/SSE3 extensions, 13-23

## T

- Tangent, x87 FPU operation, 8-20
- Task gate, 6-18
- Task register, 3-4
- Task state segment (see TSS)
- Tasks
  - exception handler, 6-18
  - interrupt handler, 6-18
- Temporal data, 10-12
- TEST instruction, 7-14
- TF (trap) flag, EFLAGS register, 3-17, A-1
- Thermal Monitor, 2-4
- TOP (stack TOP) field
  - x87 FPU status word, 8-2, 9-9
- TR register, 3-6
- Trace cache, 2-9
- Transcendental instruction accuracy, 8-21
- Trap gate, 6-13
- Truncation
  - description of, 4-19
  - with SSE-SSE2 conversion instructions, 4-19
- TSS
  - I/O map base, 20-4
  - I/O permission bit map, 20-4
  - saving state of EFLAGS register, 3-15

## U

- UCOMISD instruction, 11-7
- UCOMISS instruction, 10-9
- UD2 instruction, 7-24
- UE (numeric underflow exception) flag
  - MXCSR register, 11-16
  - x87 FPU status word, 8-5, 8-29
- UM (numeric underflow exception) mask bit
  - MXCSR register, 11-16
  - x87 FPU control word, 8-7, 8-29
- Underflow
  - FPU exception
    - (see Numeric underflow exception)
  - numeric, floating-point, 4-15
  - x87 FPU stack, 8-26
- Underflow, x87 FPU stack, 8-26
- Unpack instructions
  - SSE extensions, 10-9
  - SSE2 extensions, 11-7
- UNPCKHPD instruction, 11-8
- UNPCKHPS instruction, 10-10
- UNPCKLPD instruction, 11-8
- UNPCKLPS instruction, 10-10
- Unsigned integers
  - description of, 4-3
  - range of, 4-3
  - types, 4-3
- Unsupported, 8-14
  - floating-point formats, x87 FPU, 8-14
  - x87 FPU instructions, 8-24

## V

- VIF (virtual interrupt) flag, EFLAGS register, 3-17
- VIP (virtual interrupt pending) flag
  - EFLAGS register, 3-17
- Virtual 8086 mode
  - description of, 3-17

- memory model, 3-7, 3-8
- VM (virtual 8086 mode) flag, EFLAGS register, 3-17
- VMCALL instruction, 5-39, 5-40
- VMCLEAR instruction, 5-39, 5-40
- VMLAUNCH instruction, 5-39, 5-40
- VMPTSLD instruction, 5-39, 5-40
- VMPTST instruction, 5-39, 5-40
- VMREAD instruction, 5-39, 5-40
- VMRESUME instruction, 5-39, 5-40
- VMWRITE instruction, 5-39, 5-40
- VMX
  - instruction set, 5-39
  - introduction, 2-20
  - Virtual machine monitor (VMM), 2-20
  - virtualization, 2-20
- VMXOFF instruction, 5-39
- VMXON instruction, 5-39

## W

- Waiting instructions, x87 FPU, 8-24
- WAIT/FWAIT instructions, 8-23, 8-31
- WC memory type, 10-12
- wide dynamic execution, 2-4
- Word, 4-1
- Wraparound mode (MMX instructions), 9-4

## X

- x87 FPU
  - 64-bit mode, 8-1
  - compatibility mode, 8-1
  - control word, 8-7
  - data pointer, 8-9
  - data registers, 8-1
  - execution environment, 8-1
  - floating-point data types, 8-13
  - floating-point format, 4-12
  - fopcode compatibility mode, 8-10
  - FXSAVE and FXRSTOR instructions, 11-23
  - IEEE Standard 754, 8-1
  - instruction pointer, 8-9
  - instruction set, 8-15
  - last instruction opcode, 8-10
  - overview of registers, 3-2
  - programming, 8-1
  - QNaN floating-point indefinite, 4-18
  - register stack, 8-1
  - register stack, parameter passing, 8-3
  - registers, 8-1
  - save and restore state instructions, 5-15
  - saving registers, 11-23
  - state, 8-11
  - state, image, 8-11, 8-12
  - state, saving, 8-11, 8-12
  - status register, 8-4
  - tag word, 8-8
  - transcendental instruction accuracy, 8-21
- x87 FPU control word
  - description of, 8-7
  - exception-flag mask bits, 8-7
  - infinity control flag, 8-8
  - precision control (PC) field, 8-7
  - rounding control (RC) field, 4-19, 8-8
- x87 FPU exception handling
  - description of, 8-32
  - floating-point exception summary, C-1
  - MS-DOS compatibility mode, 8-32
  - native mode, 8-32
- x87 FPU floating-point exceptions
  - denormal operand exception, 8-28
  - division-by-zero, 8-28
  - exception conditions, 8-26
  - exception summary, C-1
  - inexact-result (precision), 8-30
  - interaction of SIMD and x87 FPU floating-point exceptions, 11-18
  - invalid arithmetic operand, 8-26, 8-27
  - numeric overflow, 8-28
  - numeric underflow, 8-29
  - software handling, 8-32
  - stack overflow, 8-4, 8-26
  - stack underflow, 8-4, 8-26
  - summary of, 8-24
  - synchronization, 8-31
- x87 FPU instructions
  - arithmetic vs. non-arithmetic instructions, 8-25
  - basic arithmetic, 8-17
  - comparison and classification, 8-18
  - control, 8-23
  - data transfer, 8-15
  - exponential, 8-21
  - instruction set, 8-15
  - load constant, 8-17
  - logarithmic, 8-21
  - operands, 8-15
  - overview, 8-15
  - save and restore state, 8-23
  - scale, 8-21
  - transcendental, 8-21
  - transitions between x87 FPU and MMX code, 9-9
  - trigonometric, 8-20
  - unsupported, 8-24
- x87 FPU status word
  - condition code flags, 8-4
  - DE flag, 8-28
  - description of, 8-4
  - exception flags, 8-5
  - OE flag, 8-28
  - PE flag, 8-4
  - stack fault flag, 8-6
  - TOP field, 8-2
  - top of stack (TOP) pointer, 8-4
- x87 FPU tag word, 8-8, 9-9
- XADD instruction, 7-4
- XCHG instruction, 7-4
- XCRO, 14-15
- XLAT/XLATB instruction, 7-23
- XMM registers
  - 64-bit mode, 3-5
  - description, 10-3
  - FXSAVE and FXRSTOR instructions, 11-23
  - overview of, 3-2
  - parameters passing in, 11-23
  - saving on a procedure or function call, 11-23
- XOR instruction, 7-10
- XORPD instruction, 11-7
- XORPS instruction, 10-9
- XRSTOR, 14-15, 15-1, 15-4
- XSAVE, 14-15, 14-20, 14-25, 14-31, 14-32, 15-1, 15-4, 15-8

## INDEX

### Z

- ZE (divide by zero exception) flag
  - x87 FPU status word, 8-5, 8-28
- ZE (divide by zero exception) flag bit
  - MXCSR register, 11-15
- Zero, floating-point format, 4-5, 4-15
- ZF (zero) flag, EFLAGS register, 3-16, A-1
- ZM (divide by zero exception) mask bit
  - MXCSR register, 11-15
  - x87 FPU control word, 8-7, 8-28