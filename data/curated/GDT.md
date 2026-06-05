---
architecture: x86_32
component: GDT
mode: protected
tags: [segmentation, memory, descriptors]
---

# GDT - Global Descriptor Table

The Global Descriptor Table (GDT) is a data structure used by the x86 architecture in Protected Mode to define the characteristics of memory segments.

## General Structure of the GDT

The GDT is a table of segment descriptors. Each descriptor is exactly 8 bytes (64 bits). The first entry of the GDT (index 0) must always be a null descriptor (all bits set to 0) and cannot be used.

The GDTR register contains:
- **Base:** 32-bit linear address where the GDT begins
- **Limit:** Size of the GDT in bytes minus 1 (maximum 65535 bytes = 8192 descriptors)

The `lgdt` instruction loads the GDTR register with the GDT address and size.

## Segment Descriptor

A segment descriptor is 8 bytes with the following structure:

```
Bytes 0-1: Limit [15:0]
Bytes 2-3: Base [15:0]
Byte 4:    Base [23:16]
Byte 5:    Access Byte
Byte 6:    Flags (4 bits) + Limit [19:16] (4 bits)
Byte 7:    Base [31:24]
```

The main fields are:
- **Base (32 bits):** Linear address where the segment begins
- **Limit (20 bits):** Size of the segment
- **Access Byte:** Permissions and segment type
- **Flags:** Granularity, operation size, and other options

## Access Byte

The Access Byte (byte 5) has the following bit structure:

```
Bit 7:   Present (P) - Must be 1 for valid descriptors
Bits 6-5: Descriptor Privilege Level (DPL) - Privilege level (0-3)
Bit 4:   Descriptor Type (S) - 1 for code/data, 0 for system
Bits 3-0: Type - Specific segment type
```

For executable code segments:
- **Type = 1010 (0xA):** Code, execute-only
- **Type = 1011 (0xB):** Code, execute and read

For data segments:
- **Type = 0010 (0x2):** Data, read-only
- **Type = 0011 (0x3):** Data, read and write

## Flags and Extended Limit

Byte 6 contains:
- **Bits 7-4 (Flags):**
  - **G (Granularity):** 0 = limit in bytes, 1 = limit in 4KB pages
  - **D/B (Default operation size):** 0 = 16-bit, 1 = 32-bit
  - **L (Long mode):** 0 for 32-bit protected mode
  - **AVL:** Available for operating system use

- **Bits 3-0:** Limit [19:16] (high bits of the 20-bit limit)

## Code Segment Descriptor

A typical descriptor for a kernel code segment (Ring 0):

```
Base:     0x00000000
Limit:    0xFFFFF (with G=1, this is 4GB)
Access:   0x9A (Present=1, DPL=0, S=1, Type=1010)
Flags:    0xC (G=1, D=1)
```

In NASM assembly:
```nasm
; Kernel code descriptor
dw 0xFFFF       ; Limit [15:0]
dw 0x0000       ; Base [15:0]
db 0x00         ; Base [23:16]
db 10011010b    ; Access: Present, DPL=0, Code, Execute/Read
db 11001111b    ; Flags (G=1, D=1) + Limit [19:16]
db 0x00         ; Base [31:24]
```

## Data Segment Descriptor

A typical descriptor for a kernel data segment (Ring 0):

```
Base:     0x00000000
Limit:    0xFFFFF (with G=1, this is 4GB)
Access:   0x92 (Present=1, DPL=0, S=1, Type=0010)
Flags:    0xC (G=1, D=1)
```

In NASM assembly:
```nasm
; Kernel data descriptor
dw 0xFFFF       ; Limit [15:0]
dw 0x0000       ; Base [15:0]
db 0x00         ; Base [23:16]
db 10010010b    ; Access: Present, DPL=0, Data, Read/Write
db 11001111b    ; Flags (G=1, D=1) + Limit [19:16]
db 0x00         ; Base [31:24]
```

## Segment Selectors

A segment selector is a 16-bit value that indexes the GDT:

```
Bits 15-3: Index into the GDT (offset / 8)
Bit 2:     Table Indicator (0 = GDT, 1 = LDT)
Bits 1-0:  Requested Privilege Level (RPL)
```

Common examples:
- **0x08:** Index 1, GDT, RPL 0 (first descriptor after the null)
- **0x10:** Index 2, GDT, RPL 0 (second descriptor)

## Loading the GDT

To load the GDT in protected mode:

```nasm
; GDTR structure
gdt_pointer:
    dw gdt_end - gdt_start - 1    ; Limit (size - 1)
    dd gdt_start                   ; Base (linear address)

; Load GDT
lgdt [gdt_pointer]

; Enable protected mode
mov eax, cr0
or eax, 1
mov cr0, eax

; Far jump to load CS with code selector
jmp 0x08:protected_mode_entry

protected_mode_entry:
    ; Load data selectors
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
```

## TSS Descriptor

The Task State Segment (TSS) descriptor is special and has a different structure:

```
Base:     TSS address
Limit:    TSS size (minimum 104 bytes for 32-bit)
Access:   0x89 (Present=1, DPL=0, S=0, Type=1001 = available TSS)
Flags:    0x0
```

The TSS is used for context switches and interrupt handling with privilege level change.
