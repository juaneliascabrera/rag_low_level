---
architecture: x86_32
component: GDT
mode: protected
tags: [segmentation, memory, descriptors]
---

# GDT - Global Descriptor Table

La Global Descriptor Table (GDT) es una estructura de datos utilizada por la arquitectura x86 en Modo Protegido para definir las características de los segmentos de memoria.

## Estructura General de la GDT

La GDT es una tabla de descriptores de segmento. Cada descriptor tiene exactamente 8 bytes (64 bits). La primera entrada de la GDT (índice 0) debe ser siempre un descriptor nulo (todos los bits en 0) y no puede ser utilizada.

El registro GDTR contiene:
- **Base:** Dirección lineal de 32 bits donde comienza la GDT
- **Límite:** Tamaño de la GDT en bytes menos 1 (máximo 65535 bytes = 8192 descriptores)

La instrucción `lgdt` carga el registro GDTR con la dirección y tamaño de la GDT.

## Descriptor de Segmento

Un descriptor de segmento tiene 8 bytes con la siguiente estructura:

```
Bytes 0-1: Límite [15:0]
Bytes 2-3: Base [15:0]
Byte 4:    Base [23:16]
Byte 5:    Access Byte
Byte 6:    Flags (4 bits) + Límite [19:16] (4 bits)
Byte 7:    Base [31:24]
```

Los campos principales son:
- **Base (32 bits):** Dirección lineal donde comienza el segmento
- **Límite (20 bits):** Tamaño del segmento
- **Access Byte:** Permisos y tipo de segmento
- **Flags:** Granularidad, tamaño de operación, y otras opciones

## Access Byte

El Access Byte (byte 5) tiene la siguiente estructura de bits:

```
Bit 7:   Present (P) - Debe ser 1 para descriptores válidos
Bits 6-5: Descriptor Privilege Level (DPL) - Nivel de privilegio (0-3)
Bit 4:   Descriptor Type (S) - 1 para código/datos, 0 para sistema
Bits 3-0: Type - Tipo específico de segmento
```

Para segmentos de código ejecutables:
- **Type = 1010 (0xA):** Código, solo ejecución
- **Type = 1011 (0xB):** Código, ejecución y lectura

Para segmentos de datos:
- **Type = 0010 (0x2):** Datos, solo lectura
- **Type = 0011 (0x3):** Datos, lectura y escritura

## Flags y Límite Extendido

El byte 6 contiene:
- **Bits 7-4 (Flags):**
  - **G (Granularity):** 0 = límite en bytes, 1 = límite en páginas de 4KB
  - **D/B (Default operation size):** 0 = 16-bit, 1 = 32-bit
  - **L (Long mode):** 0 para modo protegido de 32 bits
  - **AVL:** Disponible para uso del sistema operativo

- **Bits 3-0:** Límite [19:16] (bits altos del límite de 20 bits)

## Descriptor de Segmento de Código

Un descriptor típico para segmento de código en kernel (Ring 0):

```
Base:     0x00000000
Límite:   0xFFFFF (con G=1, esto es 4GB)
Access:   0x9A (Present=1, DPL=0, S=1, Type=1010)
Flags:    0xC (G=1, D=1)
```

En ensamblador NASM:
```nasm
; Descriptor de código kernel
dw 0xFFFF       ; Límite [15:0]
dw 0x0000       ; Base [15:0]
db 0x00         ; Base [23:16]
db 10011010b    ; Access: Present, DPL=0, Code, Execute/Read
db 11001111b    ; Flags (G=1, D=1) + Límite [19:16]
db 0x00         ; Base [31:24]
```

## Descriptor de Segmento de Datos

Un descriptor típico para segmento de datos en kernel (Ring 0):

```
Base:     0x00000000
Límite:   0xFFFFF (con G=1, esto es 4GB)
Access:   0x92 (Present=1, DPL=0, S=1, Type=0010)
Flags:    0xC (G=1, D=1)
```

En ensamblador NASM:
```nasm
; Descriptor de datos kernel
dw 0xFFFF       ; Límite [15:0]
dw 0x0000       ; Base [15:0]
db 0x00         ; Base [23:16]
db 10010010b    ; Access: Present, DPL=0, Data, Read/Write
db 11001111b    ; Flags (G=1, D=1) + Límite [19:16]
db 0x00         ; Base [31:24]
```

## Selectores de Segmento

Un selector de segmento es un valor de 16 bits que indexa la GDT:

```
Bits 15-3: Índice en la GDT (desplazamiento / 8)
Bit 2:     Table Indicator (0 = GDT, 1 = LDT)
Bits 1-0:  Requested Privilege Level (RPL)
```

Ejemplos comunes:
- **0x08:** Índice 1, GDT, RPL 0 (primer descriptor después del nulo)
- **0x10:** Índice 2, GDT, RPL 0 (segundo descriptor)

## Carga de la GDT

Para cargar la GDT en modo protegido:

```nasm
; Estructura GDTR
gdt_pointer:
    dw gdt_end - gdt_start - 1    ; Límite (tamaño - 1)
    dd gdt_start                   ; Base (dirección lineal)

; Cargar GDT
lgdt [gdt_pointer]

; Habilitar modo protegido
mov eax, cr0
or eax, 1
mov cr0, eax

; Salto lejano para cargar CS con selector de código
jmp 0x08:protected_mode_entry

protected_mode_entry:
    ; Cargar selectores de datos
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
```

## Descriptor de TSS

El Task State Segment (TSS) descriptor es especial y tiene una estructura diferente:

```
Base:     Dirección del TSS
Límite:   Tamaño del TSS (mínimo 104 bytes para 32-bit)
Access:   0x89 (Present=1, DPL=0, S=0, Type=1001 = TSS disponible)
Flags:    0x0
```

El TSS se utiliza para cambios de contexto y manejo de interrupciones con cambio de privilegio.
