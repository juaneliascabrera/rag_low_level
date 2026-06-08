---
architecture: x86_32
component: procedures_interrupts_exceptions
mode: protected
tags: ['procedures', 'stack', 'interrupts', 'exceptions']
source: intel_sdm_vol1_chapter_6.md
---

# Intel SDM Volume 1 - Chapter 6

# PROCEDURE CALLS, INTERRUPTS, AND EXCEPTIONS

---

This chapter describes the facilities in the Intel 64 and IA-32 architectures for executing calls to procedures or subroutines. It also describes how interrupts and exceptions are handled from the perspective of an application programmer.

## 6.1 PROCEDURE CALL TYPES

The processor supports procedure calls in the following two different ways:

- CALL and RET instructions.
- ENTER and LEAVE instructions, in conjunction with the CALL and RET instructions.

Both of these procedure call mechanisms use the procedure stack, commonly referred to simply as “the stack,” to save the state of the calling procedure, pass parameters to the called procedure, and store local variables for the currently executing procedure.

The processor’s facilities for handling interrupts and exceptions are similar to those used by the CALL and RET instructions.

Processors that support Control-Flow Enforcement Technology (CET) support an additional stack referred to as “the shadow stack”. The CALL instruction, when shadow stacks are enabled, additionally saves the state of the calling procedure on the shadow stack; and the RET instruction restores the state of the calling procedure if the state on the stack and the shadow stack match.

## 6.2 STACKS

The stack (see Figure 6-1) is a contiguous array of memory locations. It is contained in a segment and identified by the segment selector in the SS register. When using the flat memory model, the stack can be located anywhere in the linear address space for the program. A stack can be up to 4 GBytes long, the maximum size of a segment.

Items are placed on the stack using the PUSH instruction and removed from the stack using the POP instruction. When an item is pushed onto the stack, the processor decrements the ESP register, then writes the item at the new top of stack. When an item is popped off the stack, the processor reads the item from the top of stack, then increments the ESP register. In this manner, the stack grows **down** in memory (towards lesser addresses) when items are pushed on the stack and shrinks **up** (towards greater addresses) when the items are popped from the stack.

A program or operating system/executive can set up many stacks. For example, in multitasking systems, each task can be given its own stack. The number of stacks in a system is limited by the maximum number of segments and the available physical memory.

When a system sets up many stacks, only one stack—the **current stack**—is available at a time. The current stack is the one contained in the segment referenced by the SS register.

![Diagram of Stack Structure showing the Stack Segment, Local Variables, Parameters, Return Instruction Pointer, and the ESP/EBP registers.](3abb87a27232fe2f2806b67f2e5e1390_img.jpg)

The diagram illustrates the stack structure within a memory segment. The stack grows downwards from higher memory addresses at the top to lower memory addresses at the bottom. The stack segment is bounded by the 'Bottom of Stack (Initial ESP Value)' at the top and the 'Top of Stack' at the bottom. The stack is divided into sections: 'Local Variables for Calling Procedure', 'Parameters Passed to Called Procedure', and the 'Return Instruction Pointer'. The 'EBP Register' (Base Pointer) typically points to the return instruction pointer, while the 'ESP Register' (Stack Pointer) points to the current top of the stack. The stack can be 16 or 32 bits wide. Arrows indicate that pushes move the top of the stack to lower addresses, while pops move it to higher addresses.

Diagram of Stack Structure showing the Stack Segment, Local Variables, Parameters, Return Instruction Pointer, and the ESP/EBP registers.

Figure 6-1. Stack Structure

The processor references the SS register automatically for all stack operations. For example, when the ESP register is used as a memory address, it automatically points to an address in the current stack. Also, the CALL, RET, PUSH, POP, ENTER, and LEAVE instructions all perform operations on the current stack.

### 6.2.1 Setting Up a Stack

To set a stack and establish it as the current stack, the program or operating system/executive must do the following:

1. Establish a stack segment.
2. Load the segment selector for the stack segment into the SS register using a MOV, POP, or LSS instruction.
3. Load the stack pointer for the stack into the ESP register using a MOV, POP, or LSS instruction. The LSS instruction can be used to load the SS and ESP registers in one operation.

See "Segment Descriptors" in Chapter 3, "Protected-Mode Memory Management," of the Intel<sup>®</sup> 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, for information on how to set up a segment descriptor and segment limits for a stack segment.

### 6.2.2 Stack Alignment

The stack pointer for a stack segment should be aligned on 16-bit (word) or 32-bit (double-word) boundaries, depending on the width of the stack segment. The D flag in the segment descriptor for the current code segment sets the stack-segment width (see "Segment Descriptors" in Chapter 3, "Protected-Mode Memory Management," of the Intel<sup>®</sup> 64 and IA-32 Architectures Software Developer's Manual, Volume 3A). The PUSH and POP instructions use the D flag to determine how much to decrement or increment the stack pointer on a push or pop operation, respectively. When the stack width is 16 bits, the stack pointer is incremented or decremented in 16-bit increments; when the width is 32 bits, the stack pointer is incremented or decremented in 32-bit increments. Pushing a 16-bit value onto a 32-bit wide stack can result in stack misaligned (that is, the stack pointer is not aligned on a double-

word boundary). One exception to this rule is when the contents of a segment register (a 16-bit segment selector) are pushed onto a 32-bit wide stack. Here, the processor automatically aligns the stack pointer to the next 32-bit boundary.

The processor does not check stack pointer alignment. It is the responsibility of the programs, tasks, and system procedures running on the processor to maintain proper alignment of stack pointers. Misaligning a stack pointer can cause serious performance degradation and in some instances program failures.

### 6.2.3 Address-Size Attributes for Stack Accesses

Instructions that use the stack implicitly (such as the PUSH and POP instructions) have two address-size attributes each of either 16 or 32 bits. This is because they always have the implicit address of the top of the stack, and they may also have an explicit memory address (for example, PUSH Array1[EBX]). The attribute of the explicit address is determined by the D flag of the current code segment and the presence or absence of the 67H address-size prefix.

The address-size attribute of the top of the stack determines whether SP or ESP is used for the stack access. Stack operations with an address-size attribute of 16 use the 16-bit SP stack pointer register and can use a maximum stack address of FFFFH; stack operations with an address-size attribute of 32 bits use the 32-bit ESP register and can use a maximum address of FFFFFFFFH. The default address-size attribute for data segments used as stacks is controlled by the B flag of the segment's descriptor. When this flag is clear, the default address-size attribute is 16; when the flag is set, the address-size attribute is 32.

### 6.2.4 Procedure Linking Information

The processor provides two pointers for linking of procedures: the stack-frame base pointer and the return instruction pointer. When used in conjunction with a standard software procedure-call technique, these pointers permit reliable and coherent linking of procedures.

#### 6.2.4.1 Stack-Frame Base Pointer

The stack is typically divided into frames. Each stack frame can then contain local variables, parameters to be passed to another procedure, and procedure linking information. The stack-frame base pointer (contained in the EBP register) identifies a fixed reference point within the stack frame for the called procedure. To use the stack-frame base pointer, the called procedure typically copies the contents of the ESP register into the EBP register prior to pushing any local variables on the stack. The stack-frame base pointer then permits easy access to data structures passed on the stack, to the return instruction pointer, and to local variables added to the stack by the called procedure.

Like the ESP register, the EBP register automatically points to an address in the current stack segment (that is, the segment specified by the current contents of the SS register).

#### 6.2.4.2 Return Instruction Pointer

Prior to branching to the first instruction of the called procedure, the CALL instruction pushes the address in the EIP register onto the current stack. This address is then called the return-instruction pointer and it points to the instruction where execution of the calling procedure should resume following a return from the called procedure. Upon returning from a called procedure, the RET instruction pops the return-instruction pointer from the stack back into the EIP register. Execution of the calling procedure then resumes.

The processor does not keep track of the location of the return-instruction pointer. It is thus up to the programmer to ensure that stack pointer is pointing to the return-instruction pointer on the stack, prior to issuing a RET instruction. A common way to reset the stack pointer to the point to the return-instruction pointer is to move the contents of the EBP register into the ESP register. If the EBP register is loaded with the stack pointer immediately following a procedure call, it should point to the return instruction pointer on the stack.

The processor does not require that the return instruction pointer point back to the calling procedure. Prior to executing the RET instruction, the return instruction pointer can be manipulated in software to point to any address

in the current code segment (near return) or another code segment (far return). Performing such an operation, however, should be undertaken very cautiously, using only well defined code entry points.

## 6.2.5 Stack Behavior in 64-Bit Mode

In 64-bit mode, address calculations that reference SS segments are treated as if the segment base is zero. Fields (base, limit, and attribute) in segment descriptor registers are ignored. SS DPL is modified such that it is always equal to CPL. This will be true even if it is the only field in the SS descriptor that is modified.

Registers E(SP), E(IP) and E(BP) are promoted to 64-bits and are re-named RSP, RIP, and RBP respectively. Some forms of segment load instructions are invalid (for example, LDS, POP ES).

PUSH/POP instructions increment/decrement the stack using a 64-bit width. When the contents of a segment register is pushed onto 64-bit stack, the pointer is automatically aligned to 64 bits (as with a stack that has a 32-bit width).

## 6.3 SHADOW STACKS

A shadow stack is a second stack used exclusively for control transfer operations. This stack is separate from the procedure stack. The shadow stack is not used to store data, hence is not explicitly writeable by software. Writes to the shadow stack are restricted to control transfer instructions and shadow stack management instructions. Shadow stacks can be enabled separately for privilege level 3 (user mode) or privilege levels less than 3 (supervisor mode).

Shadow stacks are active only in protected mode with paging enabled. Shadow stacks cannot be enabled for a program executing in virtual 8086 mode.

Processors that support shadow stacks have an architectural register called the shadow stack pointer (SSP) that points to the current top of the shadow stack. The SSP cannot be directly encoded as a source, destination, or memory operand in instructions. The width of the shadow stack is 32-bit in 32-bit/compatibility mode, and is 64-bit in 64-bit mode. The address-size attribute of the shadow stack is likewise 32-bit in 32-bit/compatibility mode, and 64-bit in 64-bit mode.

The size of the shadow stack pushes and pops for far CALL and call to interrupt/exception handlers is fixed at 64 bits, and the processor uses 8-byte, zero padded stores for these pushes in 32-bit/compatibility modes.

## 6.4 CALLING PROCEDURES USING CALL AND RET

The CALL instruction allows control transfers to procedures within the current code segment (**near call**) and in a different code segment (**far call**). Near calls usually provide access to local procedures within the currently running program or task. Far calls are usually used to access operating system procedures or procedures in a different task. See "CALL—Call Procedure" in Chapter 3, "Instruction Set Reference, A-L," of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 2A, for a detailed description of the CALL instruction.

The RET instruction also allows near and far returns to match the near and far versions of the CALL instruction. In addition, the RET instruction allows a program to increment the stack pointer on a return to release parameters from the stack. The number of bytes released from the stack is determined by an optional argument (*n*) to the RET instruction. See "RET—Return from Procedure" in Chapter 4, "Instruction Set Reference, M-U," of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 2B, for a detailed description of the RET instruction.

### 6.4.1 Near CALL and RET Operation

When executing a near call, the processor does the following (see Figure 6-2):

1. Pushes the current value of the EIP register on the stack.  
If shadow stack is enabled and the displacement value is not 0, pushes the current value of the EIP register on the shadow stack.

2. Loads the offset of the called procedure in the EIP register.
3. Begins execution of the called procedure.

When executing a near return, the processor performs these actions:

1. Pops the top-of-stack value (the return instruction pointer) into the EIP register.  
If shadow stack is enabled, pops the top-of-stack (the return instruction pointer) value from the shadow stack and if it's not the same as the return instruction pointer popped from the stack, then the processor causes a control protection exception with error code NEAR-RET (#CP(NEAR-RET)).
2. If the RET instruction has an optional *n* argument, increments the stack pointer by the number of bytes specified with the *n* operand to release parameters from the stack.
3. Resumes execution of the calling procedure.

## 6.4.2 Far CALL and RET Operation

When executing a far call, the processor performs these actions (see Figure 6-2):

1. Pushes the current value of the CS register on the stack.  
If shadow stack is enabled:
  - a. Temporarily saves the current value of the SSP register internally and aligns the SSP to the next 8 byte boundary.
  - b. Pushes the current value of the CS register on the shadow stack.
  - c. Pushes the current value of LIP (CS.base + EIP) on the shadow stack.
  - d. Pushes the internally saved value of the SSP register on the shadow stack.
2. Pushes the current value of the EIP register on the stack.
3. Loads the segment selector of the segment that contains the called procedure in the CS register.
4. Loads the offset of the called procedure in the EIP register.
5. Begins execution of the called procedure.

When executing a far return, the processor does the following:

1. Pops the top-of-stack value (the return instruction pointer) into the EIP register.
2. Pops the top-of-stack value (the segment selector for the code segment being returned to) into the CS register.  
If shadow stack is enabled:
  - a. Causes a control protection exception (#CP(FAR-RET/IRET)) if the SSP is not aligned to 8 bytes.
  - b. Compares the values on the shadow stack at address SSP+8 (the LIP) and SSP+16 (the CS) to the CS and (CS.base + EIP) popped from the stack, and causes a control protection exception (#CP(FAR-RET/IRET)) if they do not match.
  - c. Pops the top-of-stack value (the SSP of the procedure being returned to) from shadow stack into the SSP register.
3. If the RET instruction has an optional *n* argument, increments the stack pointer by the number of bytes specified with the *n* operand to release parameters from the stack.
4. Resumes execution of the calling procedure.

![Diagram showing stack states for Near and Far Calls and Returns.](42d1ffab6bbf720e8421aeace0808924_img.jpg)

The diagram illustrates the stack state during and after Near and Far Calls and Returns. It is divided into four quadrants:

- Stack During Near Call:** Shows a stack frame with parameters Param 1, Param 2, Param 3, and Calling EIP. Arrows indicate ESP Before Call at Param 3 and ESP After Call at Calling EIP. The stack frame after the call is shown below.
- Stack During Far Call:** Shows a stack frame with parameters Param 1, Param 2, Param 3, Calling CS, and Calling EIP. Arrows indicate ESP Before Call at Param 3 and ESP After Call at Calling EIP. The stack frame before the call is shown above, and the stack frame after the call is shown below.
- Stack During Near Return:** Shows the stack frame after the return, with Param 1, Param 2, Param 3, and Calling EIP. Arrows indicate ESP After Return at Param 1 and ESP Before Return at Calling EIP.
- Stack During Far Return:** Shows the stack frame after the return, with Param 1, Param 2, Param 3, Calling CS, and Calling EIP. Arrows indicate ESP After Return at Param 1 and ESP Before Return at Calling EIP.

Note: On a near or far return, parameters are released from the stack based on the optional *n* operand in the RET *n* instruction.

Diagram showing stack states for Near and Far Calls and Returns.

Figure 6-2. Stack on Near and Far Calls

![Diagram showing shadow stack states for Near and Far Calls and Returns.](9ef15a4afab1416db28b91184862a3a5_img.jpg)

The diagram illustrates the shadow stack state during and after Near and Far Calls and Returns. It is divided into four quadrants:

- Shadow Stack During Near Call:** Shows a shadow stack frame with Calling EIP. Arrows indicate SSP Before Call at the top and SSP After Call at Calling EIP.
- Shadow Stack During Far Call:** Shows a shadow stack frame with Calling CS, Calling LIP, and Calling SSP. Arrows indicate SSP Before Call at the top, SSP After Call at Calling SSP, and SSP Before Return at Calling SSP.
- Shadow Stack During Near Return:** Shows the shadow stack frame after the return, with Calling EIP. Arrows indicate SSP After Return at the top and SSP Before Return at Calling EIP.
- Shadow Stack During Far Return:** Shows the shadow stack frame after the return, with Calling CS, Calling LIP, and Calling SSP. Arrows indicate SSP After Return at the top, SSP Before Return at Calling SSP, and SSP Before Return at Calling SSP.

Note: There are no parameters on the shadow stack. RET and RET *n* operate identically on the shadow stack.

Diagram showing shadow stack states for Near and Far Calls and Returns.

Figure 6-3. Shadow Stack on Near and Far Calls

## 6.4.3 Parameter Passing

Parameters can be passed between procedures in any of three ways: through general-purpose registers, in an argument list, or on the stack.

### 6.4.3.1 Passing Parameters Through the General-Purpose Registers

The processor does not save the state of the general-purpose registers on procedure calls. A calling procedure can thus pass up to six parameters to the called procedure by copying the parameters into any of these registers (except the ESP and EBP registers) prior to executing the CALL instruction. The called procedure can likewise pass parameters back to the calling procedure through general-purpose registers.

### 6.4.3.2 Passing Parameters on the Stack

To pass a large number of parameters to the called procedure, the parameters can be placed on the stack, in the stack frame for the calling procedure. Here, it is useful to use the stack-frame base pointer (in the EBP register) to make a frame boundary for easy access to the parameters.

The stack can also be used to pass parameters back from the called procedure to the calling procedure.

### 6.4.3.3 Passing Parameters in an Argument List

An alternate method of passing a larger number of parameters (or a data structure) to the called procedure is to place the parameters in an argument list in one of the data segments in memory. A pointer to the argument list can then be passed to the called procedure through a general-purpose register or the stack. Parameters can also be passed back to the calling procedure in this same manner.

## 6.4.4 Saving Procedure State Information

The processor does not save the contents of the general-purpose registers, segment registers, or the EFLAGS register on a procedure call. A calling procedure should explicitly save the values in any of the general-purpose registers that it will need when it resumes execution after a return. These values can be saved on the stack or in memory in one of the data segments.

The PUSHA and POPA instructions facilitate saving and restoring the contents of the general-purpose registers. PUSHA pushes the values in all the general-purpose registers on the stack in the following order: EAX, ECX, EDX, EBX, ESP (the value prior to executing the PUSHA instruction), EBP, ESI, and EDI. The POPA instruction pops all the register values saved with a PUSHA instruction (except the ESP value) from the stack to their respective registers.

If a called procedure changes the state of any of the segment registers explicitly, it should restore them to their former values before executing a return to the calling procedure.

If a calling procedure needs to maintain the state of the EFLAGS register, it can save and restore all or part of the register using the PUSHF/PUSHFD and POPF/POPFD instructions. The PUSHF instruction pushes the lower word of the EFLAGS register on the stack, while the PUSHFD instruction pushes the entire register. The POPF instruction pops a word from the stack into the lower word of the EFLAGS register, while the POPFD instruction pops a double word from the stack into the register.

## 6.4.5 Calls to Other Privilege Levels

The IA-32 architecture's protection mechanism recognizes four privilege levels, numbered from 0 to 3, where a greater number mean less privilege. The reason to use privilege levels is to improve the reliability of operating systems. For example, Figure 6-4 shows how privilege levels can be interpreted as rings of protection.

![Diagram of Protection Rings showing four concentric circles labeled Level 0, Level 1, Level 2, and Level 3. Level 0 is the innermost circle, and Level 3 is the outermost. Arrows point from text labels to the rings: 'Operating System Kernel' points to Level 0, 'Operating System Services (Device Drivers, Etc.)' points to Level 1, and 'Applications' points to Level 2. Below the rings is a horizontal axis labeled 'Privilege Levels' with tick marks for 0, 1, 2, and 3. Above the axis, 'Highest' is above 0 and 'Lowest' is above 3.](f54b2e4444e410765295be668123f27a_img.jpg)

The diagram illustrates the Protection Rings architecture. It consists of four concentric circles representing privilege levels. The innermost circle is labeled 'Level 0', the next is 'Level 1', then 'Level 2', and the outermost is 'Level 3'. Arrows indicate the mapping of software components to these levels: 'Operating System Kernel' is associated with Level 0, 'Operating System Services (Device Drivers, Etc.)' with Level 1, and 'Applications' with Level 2. Below the rings, a horizontal axis labeled 'Privilege Levels' shows a scale from 0 to 3. Above this axis, 'Highest' is positioned above level 0 and 'Lowest' is positioned above level 3, indicating that privilege decreases as the level number increases.

Diagram of Protection Rings showing four concentric circles labeled Level 0, Level 1, Level 2, and Level 3. Level 0 is the innermost circle, and Level 3 is the outermost. Arrows point from text labels to the rings: 'Operating System Kernel' points to Level 0, 'Operating System Services (Device Drivers, Etc.)' points to Level 1, and 'Applications' points to Level 2. Below the rings is a horizontal axis labeled 'Privilege Levels' with tick marks for 0, 1, 2, and 3. Above the axis, 'Highest' is above 0 and 'Lowest' is above 3.

Figure 6-4. Protection Rings

In this example, the highest privilege level 0 (at the center of the diagram) is used for segments that contain the most critical code modules in the system, usually the kernel of an operating system. The outer rings (with progressively lower privileges) are used for segments that contain code modules for less critical software.

Code modules in lower privilege segments can only access modules operating at higher privilege segments by means of a tightly controlled and protected interface called a **gate**. Attempts to access higher privilege segments without going through a protection gate and without having sufficient access rights causes a general-protection exception (#GP) to be generated.

If an operating system or executive uses this multilevel protection mechanism, a call to a procedure that is in a more privileged protection level than the calling procedure is handled in a similar manner as a far call (see Section 6.4.2, "Far CALL and RET Operation"). The differences are as follows:

- The segment selector provided in the CALL instruction references a special data structure called a **call gate descriptor**. Among other things, the call gate descriptor provides the following:
  - Access rights information.
  - The segment selector for the code segment of the called procedure.
  - An offset into the code segment (that is, the instruction pointer for the called procedure).
- The processor switches to a new stack to execute the called procedure. Each privilege level has its own stack. The segment selector and stack pointer for the privilege level 3 stack are stored in the SS and ESP registers, respectively, and are automatically saved when a call to a more privileged level occurs. The segment selectors and stack pointers for the privilege level 2, 1, and 0 stacks are stored in a system segment called the task state segment (TSS).

The use of a call gate and the TSS during a stack switch are transparent to the calling procedure, except when a general-protection exception is raised.

Flexible return and event delivery (FRED) defines new mechanisms for changing privilege levels. See Chapter 8, "Flexible Return and Event Delivery (FRED)," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3. When FRED transitions are enabled, call gates cannot be used to change privilege level. An execution of CALL causes a general-protection exception (#GP) if it accesses a call gate. Similarly, an execution of RET causes a #GP if it would change privilege level. In any of these cases, the fault identifies the relevant selector in its error code.

## 6.4.6 CALL and RET Operation Between Privilege Levels

When making a call to a more privileged protection level, the processor does the following (see Figure 6-5):

1. Performs an access rights check (privilege check).
2. Temporarily saves (internally) the current contents of the SS, ESP, CS, and EIP registers.

![Diagram illustrating the stack switch on a call to a different privilege level. It shows two states: 'Before Call' and 'After Call'. In the 'Before Call' state, the 'Stack for Calling Procedure' contains parameters 1, 2, and 3, and the 'Stack for Called Procedure' contains the calling SS, ESP, CS, and EIP. The ESP Before Call points to the top of Param 3. In the 'After Call' state, the 'Stack for Calling Procedure' contains parameters 1, 2, and 3, and the 'Stack for Called Procedure' contains the calling SS, ESP, CS, and EIP. The ESP After Return points to the top of Param 3. The ESP After Call points to the top of the Calling EIP. A note at the bottom states: 'Note: On a return, parameters are released on both stacks based on the optional n operand in the RET n instruction.'](3adb4bad764bde2c7c001c4e7fed57ad_img.jpg)

The diagram illustrates the stack switch on a call to a different privilege level. It shows two states: "Before Call" and "After Call".

**Before Call:**

- Stack for Calling Procedure:** Contains Param 1, Param 2, and Param 3. The ESP Before Call points to the top of Param 3.
- Stack for Called Procedure:** Contains Calling SS, Calling ESP, Param 1, Param 2, Param 3, Calling CS, and Calling EIP. The ESP After Call points to the top of Calling EIP.

**After Call:**

- Stack for Calling Procedure:** Contains Param 1, Param 2, and Param 3. The ESP After Return points to the top of Param 3.
- Stack for Called Procedure:** Contains Calling SS, Calling ESP, Param 1, Param 2, Param 3, Calling CS, and Calling EIP. The ESP Before Return points to the top of Calling EIP.

Note: On a return, parameters are released on both stacks based on the optional *n* operand in the RET *n* instruction.

Diagram illustrating the stack switch on a call to a different privilege level. It shows two states: 'Before Call' and 'After Call'. In the 'Before Call' state, the 'Stack for Calling Procedure' contains parameters 1, 2, and 3, and the 'Stack for Called Procedure' contains the calling SS, ESP, CS, and EIP. The ESP Before Call points to the top of Param 3. In the 'After Call' state, the 'Stack for Calling Procedure' contains parameters 1, 2, and 3, and the 'Stack for Called Procedure' contains the calling SS, ESP, CS, and EIP. The ESP After Return points to the top of Param 3. The ESP After Call points to the top of the Calling EIP. A note at the bottom states: 'Note: On a return, parameters are released on both stacks based on the optional n operand in the RET n instruction.'

**Figure 6-5. Stack Switch on a Call to a Different Privilege Level**

![Diagram showing the shadow stack switch for a call from privilege level 3 to a higher privilege level. It depicts the 'Shadow Stack for Calling Procedure' and the 'Handler's Shadow Stack'. Arrows indicate the 'SSP Before Call and After Return' pointing to the top of the calling stack and the 'SSP After Call and Before Return' pointing to the 'Supervisor Shadow Stack Token' in the handler's stack. Diagram showing the shadow stack switch for a call from privilege level 2 or 1 to a higher privilege level. It depicts the 'Interrupted Procedure's Shadow Stack' and the 'Handler's Shadow Stack'. Arrows indicate the 'SSP Before Call and After Return' pointing to the top of the interrupted stack and the 'SSP After Call and Before Return' pointing to the 'SSP' field in the handler's stack. The handler's stack also shows 'Supervisor Shadow Stack Token', 'CS', and 'LIP' fields.](04963ae224a8e10b369dad650b0c57be_img.jpg)

**Calling to Procedure at Higher Privilege Level from Privilege Level 3**

**Calling to Procedure at Higher Privilege Level from Privilege Level 2 or 1**

Note: There are no parameters on the shadow stack. RET and RET n operate identically on the shadow stack.

Diagram showing the shadow stack switch for a call from privilege level 3 to a higher privilege level. It depicts the 'Shadow Stack for Calling Procedure' and the 'Handler's Shadow Stack'. Arrows indicate the 'SSP Before Call and After Return' pointing to the top of the calling stack and the 'SSP After Call and Before Return' pointing to the 'Supervisor Shadow Stack Token' in the handler's stack. Diagram showing the shadow stack switch for a call from privilege level 2 or 1 to a higher privilege level. It depicts the 'Interrupted Procedure's Shadow Stack' and the 'Handler's Shadow Stack'. Arrows indicate the 'SSP Before Call and After Return' pointing to the top of the interrupted stack and the 'SSP After Call and Before Return' pointing to the 'SSP' field in the handler's stack. The handler's stack also shows 'Supervisor Shadow Stack Token', 'CS', and 'LIP' fields.

**Figure 6-6. Shadow Stack Switch on a Call to a Different Privilege Level**

3. Loads the segment selector and stack pointer for the new stack (that is, the stack for the privilege level being called) from the TSS into the SS and ESP registers and switches to the new stack.
4. Pushes the temporarily saved SS and ESP values for the calling procedure's stack onto the new stack.
5. Copies the parameters from the calling procedure's stack to the new stack. A value in the call gate descriptor determines how many parameters to copy to the new stack.
6. Pushes the temporarily saved CS and EIP values for the calling procedure to the new stack.

If shadow stack is enabled at the privilege level of the calling procedure, then the processor temporarily saves the SSP of the calling procedure internally. If the calling procedure is at privilege level 3, the SSP of the calling procedure is also saved into the IA32\_PL3\_SSP MSR.

If shadow stack is enabled at the privilege level of the called procedure, then the SSP for the called procedure is obtained from one of the MSRs listed below, depending on the target privilege level. The SSP obtained is then verified to ensure it points to a valid supervisor shadow stack that is not currently active by verifying a supervisor shadow stack token at the address pointed to by the SSP. The operations performed to verify and acquire the supervisor shadow stack token by making it busy are as described in Section 18.2.3 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 1.

- IA32\_PL2\_SSP if transitioning to ring 2.
- IA32\_PL1\_SSP if transitioning to ring 1.
- IA32\_PL0\_SSP if transitioning to ring 0.

If shadow stack is enabled at the privilege level of the called procedure and the calling procedure was not at privilege level 3, then the processor pushes the temporarily saved CS, LIP (CS.base + EIP), and SSP of the calling procedure to the new shadow stack.<sup>1</sup>

7. Loads the segment selector for the new code segment and the new instruction pointer from the call gate into the CS and EIP registers, respectively.
8. Begins execution of the called procedure at the new privilege level.

When executing a return from the privileged procedure, the processor performs these actions:

1. Performs a privilege check.
2. Restores the CS and EIP registers to their values prior to the call.

If shadow stack is enabled at the current privilege level:

- Causes a control protection exception (#CP(FAR-RET/IRET)) if SSP is not aligned to 8 bytes.
  - If the privilege level of the procedure being returned to is less than 3 (returning to supervisor mode):
    - Compares the values on shadow stack at address SSP+8 (the LIP) and SSP+16 (the CS) to the CS and (CS.base + EIP) popped from the stack and causes a control protection exception (#CP(FAR-RET/IRET)) if they do not match.
    - Temporarily saves the top-of-stack value (the SSP of the procedure being returned to) internally.
  - If a busy supervisor shadow stack token is present at address SSP+24, then marks the token free using operations described in Section 18.2.3 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 1.
  - If the privilege level of the procedure being returned to is less than 3 (returning to supervisor mode), restores the SSP register from the internally saved value.
  - If the privilege level of the procedure being returned to is 3 (returning to user mode) and shadow stack is enabled at privilege level 3, then restores the SSP register with value of IA32\_PL3\_SSP MSR.
3. If the RET instruction has an optional *n* argument, increments the stack pointer by the number of bytes specified with the *n* operand to release parameters from the stack. If the call gate descriptor specifies that one or more parameters be copied from one stack to the other, a RET *n* instruction must be used to release the parameters from both stacks. Here, the *n* operand specifies the number of bytes occupied on each stack by the parameters. On a return, the processor increments ESP by *n* for each stack to step over (effectively remove) these parameters from the stacks.
  4. Restores the SS and ESP registers to their values prior to the call, which causes a switch back to the stack of the calling procedure.
  5. If the RET instruction has an optional *n* argument, increments the stack pointer by the number of bytes specified with the *n* operand to release parameters from the stack (see explanation in step 3).
  6. Resumes execution of the calling procedure.

See Chapter 6, "Protection," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, for detailed information on calls to privileged levels and the call gate descriptor.

---

1. If any of these pushes leads to an exception or a VM exit, the supervisor shadow-stack token remains busy.

## 6.4.7 Branch Functions in 64-Bit Mode

The 64-bit extensions expand branching mechanisms to accommodate branches in 64-bit linear-address space. These are:

- Near-branch semantics are redefined in 64-bit mode.
- In 64-bit mode and compatibility mode, 64-bit call-gate descriptors for far calls are available.

In 64-bit mode, the operand size for all near branches (CALL, RET, JCC, JCXZ, JMP, and LOOP) is forced to 64 bits. These instructions update the 64-bit RIP without the need for a REX operand-size prefix.

The following aspects of near branches are controlled by the effective operand size:

- Truncation of the size of the instruction pointer.
- Size of a stack pop or push, due to a CALL or RET.
- Size of a stack-pointer increment or decrement, due to a CALL or RET.
- Indirect-branch operand size.

In 64-bit mode, all of the above actions are forced to 64 bits regardless of operand size prefixes (operand size prefixes are silently ignored). However, the displacement field for relative branches is still limited to 32 bits and the address size for near branches is not forced in 64-bit mode.

Address sizes affect the size of RCX used for JCXZ and LOOP; they also impact the address calculation for memory indirect branches. Such addresses are 64 bits by default; but they can be overridden to 32 bits by an address size prefix.

Software typically uses far branches to change privilege levels. The legacy IA-32 architecture provides the call-gate mechanism to allow software to branch from one privilege level to another, although call gates can also be used for branches that do not change privilege levels. When call gates are used, the selector portion of the direct or indirect pointer references a gate descriptor (the offset in the instruction is ignored). The offset to the destination's code segment is taken from the call-gate descriptor.

64-bit mode redefines the type value of a 32-bit call-gate descriptor type to a 64-bit call gate descriptor and expands the size of the 64-bit descriptor to hold a 64-bit offset. The 64-bit mode call-gate descriptor allows far branches that reference any location in the supported linear-address space. These call gates also hold the target code selector (CS), allowing changes to privilege level and default size as a result of the gate transition.

Because immediates are generally specified up to 32 bits, the only way to specify a full 64-bit absolute RIP in 64-bit mode is with an indirect branch. For this reason, direct far branches are eliminated from the instruction set in 64-bit mode.

64-bit mode also expands the semantics of the SYSENTER and SYSEXIT instructions so that the instructions operate within a 64-bit memory space. The mode also introduces two new instructions: SYSCALL and SYSRET (which are valid only in 64-bit mode). For details, see "SYSENTER—Fast System Call," "SYSEXIT—Fast Return from Fast System Call," "SYSCALL—Fast System Call," and "SYSRET—Return From Fast System Call" in Chapter 4, "Instruction Set Reference, M-U," of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 2B.

## 6.5 INTERRUPTS AND EXCEPTIONS

The processor provides two mechanisms for interrupting program execution, interrupts, and exceptions:

- An **interrupt** is an asynchronous event that is typically triggered by an I/O device.
- An **exception** is a synchronous event that is generated when the processor detects one or more predefined conditions while executing an instruction. The IA-32 architecture specifies three classes of exceptions: faults, traps, and aborts.

The processor responds to interrupts and exceptions in essentially the same way. When an interrupt or exception is signaled, the processor halts execution of the current program or task and switches to a handler procedure that has been written specifically to handle the interrupt or exception condition. The processor accesses the handler procedure through an entry in the interrupt descriptor table (IDT) or through FRED event delivery. When the handler has completed handling the interrupt or exception, program control is returned to the interrupted program or task.

The operating system, executive, and/or device drivers normally handle interrupts and exceptions independently from application programs or tasks. Application programs can, however, access the interrupt and exception handlers incorporated in an operating system or executive through assembly-language calls. The remainder of this section gives a brief overview of the processor's interrupt and exception handling mechanism. See Chapter 7, "Interrupt and Exception Handling," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, for a description of this mechanism.

The IA-32 Architecture defines 18 predefined interrupts and exceptions and 224 user defined interrupts, which are associated with entries in the IDT. Each interrupt and exception in the IDT is identified with a number, called a **vector**. Table 6-1 lists the interrupts and exceptions with entries in the IDT and their respective vectors. Vectors 0 through 8, 10 through 14, and 16 through 19 are the predefined interrupts and exceptions; vectors 32 through 255 are for software-defined interrupts, which are for either **software interrupts** or **maskable hardware interrupts**.

When FRED transitions are enabled, the processor does not use the IDT. Instead, interrupts and exceptions are delivered using **FRED event delivery**. FRED event delivery saves an event's vector on the stack, along with the event type (e.g., interrupt or exception). The event type allows software to distinguish interrupts and exceptions with the same vector.

Note that the processor defines several additional interrupts that do not point to entries in the IDT and are not delivered using FRED event delivery; the most notable of these interrupts is the SMI interrupt. See Chapter 7, "Interrupt and Exception Handling," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, for more information about the interrupts and exceptions.

When the processor detects an interrupt or exception, it does one of the following things:

- Executes an implicit call to a handler procedure.
- Executes an implicit call to a handler task.

### 6.5.1 Call and Return Operation for Interrupt or Exception Handling Procedures

This section describes **IDT event delivery**, a method for calling OS handlers for interrupts and exceptions. When FRED transitions are enabled, FRED event delivery is used instead. FRED event delivery is detailed in Section 8.3, "FRED Event Delivery" in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3.

A call to an interrupt or exception handler procedure is similar to a procedure call to another protection level (see Section 6.4.6, "CALL and RET Operation Between Privilege Levels"). Here, the vector references one of two kinds of gates in the IDT: an **interrupt gate** or a **trap gate**. Interrupt and trap gates are similar to call gates in that they provide the following information:

- Access rights information
- The segment selector for the code segment that contains the handler procedure
- An offset into the code segment to the first instruction of the handler procedure

The difference between an interrupt gate and a trap gate is as follows. If an interrupt or exception handler is called through an interrupt gate, the processor clears the interrupt enable (IF) flag in the EFLAGS register to prevent subsequent interrupts from interfering with the execution of the handler. When a handler is called through a trap gate, the state of the IF flag is not changed.

**Table 6-1. Exceptions and Interrupts**

| Vector | Mnemonic | Description                       | Source                             |
|--------|----------|-----------------------------------|------------------------------------|
| 0      | #DE      | Divide Error                      | DIV and IDIV instructions.         |
| 1      | #DB      | Debug                             | Any code or data reference.        |
| 2      |          | NMI Interrupt                     | Non-maskable external interrupt.   |
| 3      | #BP      | Breakpoint                        | INT3 instruction.                  |
| 4      | #OF      | Overflow                          | INTO instruction.                  |
| 5      | #BR      | BOUND Range Exceeded              | BOUND instruction.                 |
| 6      | #UD      | Invalid Opcode (Undefined Opcode) | UD instruction or reserved opcode. |

**Table 6-1. Exceptions and Interrupts (Contd.)**

| Vector | Mnemonic | Description                                | Source                                                                                                                                                                                                                                          |
|--------|----------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 7      | #NM      | Device Not Available (No Math Coprocessor) | Floating-point or WAIT/FWAIT instruction.                                                                                                                                                                                                       |
| 8      | #DF      | Double Fault                               | Any instruction that can generate an exception, an NMI, or an INTR.                                                                                                                                                                             |
| 9      | #MF      | CoProcessor Segment Overrun (reserved)     | Floating-point instruction. <sup>1</sup>                                                                                                                                                                                                        |
| 10     | #TS      | Invalid TSS                                | Task switch or TSS access.                                                                                                                                                                                                                      |
| 11     | #NP      | Segment Not Present                        | Loading segment registers or accessing system segments.                                                                                                                                                                                         |
| 12     | #SS      | Stack Segment Fault                        | Stack operations and SS register loads.                                                                                                                                                                                                         |
| 13     | #GP      | General Protection                         | Any memory reference and other protection checks.                                                                                                                                                                                               |
| 14     | #PF      | Page Fault                                 | Any memory reference.                                                                                                                                                                                                                           |
| 15     |          | Reserved                                   |                                                                                                                                                                                                                                                 |
| 16     | #MF      | Floating-Point Error (Math Fault)          | Floating-point or WAIT/FWAIT instruction.                                                                                                                                                                                                       |
| 17     | #AC      | Alignment Check                            | Any data reference in memory. <sup>2</sup>                                                                                                                                                                                                      |
| 18     | #MC      | Machine Check                              | Error codes (if any) and source are model dependent. <sup>3</sup>                                                                                                                                                                               |
| 19     | #XM      | SIMD Floating-Point Exception              | SIMD Floating-Point Instruction <sup>4</sup>                                                                                                                                                                                                    |
| 20     | #VE      | Virtualization Exception                   | EPT violations <sup>5</sup>                                                                                                                                                                                                                     |
| 21     | #CP      | Control Protection Exception               | The RET, IRET, RSTORSSP, and SETSSBSY instructions can generate this exception. When CET indirect branch tracking is enabled, this exception can be generated due to a missing ENDBRANCH instruction at the target of an indirect call or jump. |
| 22-31  |          | Reserved                                   |                                                                                                                                                                                                                                                 |
| 32-255 |          | Maskable Interrupts                        | External interrupt from INTR pin or INT <i>n</i> instruction.                                                                                                                                                                                   |

**NOTES:**

1. IA-32 processors after the Intel386 processor do not generate this exception.
2. This exception was introduced in the Intel486 processor.
3. This exception was introduced in the Pentium processor and enhanced in the P6 family processors.
4. This exception was introduced in the Pentium III processor.
5. This exception can occur only on processors that support the 1-setting of the “EPT-violation #VE” VM-execution control.

If the code segment for the handler procedure has the same privilege level as the currently executing program or task, the handler procedure uses the current stack; if the handler executes at a more privileged level, the processor switches to the stack for the handler’s privilege level.

If no stack switch occurs, the processor does the following when calling an interrupt or exception handler (see Figure 6-7):

1. Pushes the current contents of the EFLAGS, CS, and EIP registers (in that order) on the stack.  
If shadow stack is enabled:
  - a. Temporarily saves the current value of the SSP register internally.
  - b. Pushes the current value of the CS register on the shadow stack.
  - c. Pushes the current value of LIP (CS.base + EIP) on the shadow stack.
  - d. Pushes the temporarily saved SSP value on the shadow stack.
2. Pushes an error code (if appropriate) on the stack.
3. Loads the segment selector for the new code segment and the new instruction pointer (from the interrupt gate or trap gate) into the CS and EIP registers, respectively.
4. If the call is through an interrupt gate, clears the IF flag in the EFLAGS register.

5. Begins execution of the handler procedure.

![Diagram showing stack usage with no privilege-level change. A single stack structure contains EFLAGS, CS, EIP, and Error Code. Arrows indicate ESP before and after the transfer to the handler. Diagram showing stack usage with a privilege-level change. Two separate stack structures are shown: one for the interrupted procedure and one for the handler. The handler's stack contains SS, ESP, EFLAGS, CS, EIP, and Error Code. Arrows indicate ESP before and after the transfer to the handler.](7fbdef79403f482e82031e3591c98bc2_img.jpg)

**Stack Usage with No Privilege-Level Change**

Interrupted Procedure's and Handler's Stack

The diagram shows a single stack structure. The top four slots are labeled EFLAGS, CS, EIP, and Error Code. An arrow points to the top of the stack with the text "ESP Before Transfer to Handler". Another arrow points to the bottom of the Error Code slot with the text "ESP After Transfer to Handler".

**Stack Usage with Privilege-Level Change**

Interrupted Procedure's Stack                      Handler's Stack

The diagram shows two separate stack structures. The left stack, labeled "Interrupted Procedure's Stack", has an arrow pointing to its top with the text "ESP Before Transfer to Handler". The right stack, labeled "Handler's Stack", contains six slots: SS, ESP, EFLAGS, CS, EIP, and Error Code. An arrow points to the top of the Error Code slot with the text "ESP After Transfer to Handler".

Diagram showing stack usage with no privilege-level change. A single stack structure contains EFLAGS, CS, EIP, and Error Code. Arrows indicate ESP before and after the transfer to the handler. Diagram showing stack usage with a privilege-level change. Two separate stack structures are shown: one for the interrupted procedure and one for the handler. The handler's stack contains SS, ESP, EFLAGS, CS, EIP, and Error Code. Arrows indicate ESP before and after the transfer to the handler.

**Figure 6-7. Stack Usage on Transfers to Interrupt and Exception Handling Routines**

![Diagram showing shadow stack usage with no privilege-level change. It depicts a single stack structure with CS, LIP, and SSP registers. Arrows indicate the SSP Before and After Transfer to Handler. Diagram showing shadow stack usage with privilege-level change from Level 3. It depicts two separate stack structures. The Interrupted Procedure's Shadow Stack has CS, LIP, and SSP registers. The Handler's Shadow Stack has a Supervisor Shadow Stack Token. Arrows indicate the SSP Before and After Transfer to Handler. Diagram showing shadow stack usage with privilege-level change from Level 2 or 1. It depicts two separate stack structures. The Interrupted Procedure's Shadow Stack has CS, LIP, and SSP registers. The Handler's Shadow Stack has a Supervisor Shadow Stack Token, CS, LIP, and SSP registers. Arrows indicate the SSP Before and After Transfer to Handler.](bb100d4069b5ff6f9ee2e366ca169c24_img.jpg)

**Shadow Stack Usage with No Privilege-Level Change**

Interrupted Procedure's  
and Handler's Shadow Stack

The diagram shows a single stack structure. The top section is labeled "Interrupted Procedure's and Handler's Shadow Stack". It contains three registers: CS, LIP, and SSP. Arrows point to the top of the stack (labeled "SSP Before Transfer to Handler") and to the SSP register (labeled "SSP After Transfer to Handler").

**Shadow Stack Usage with Privilege-Level Change from Level 3**

Interrupted Procedure's Shadow Stack                      Handler's Shadow Stack

The diagram shows two separate stack structures. The left stack is labeled "Interrupted Procedure's Shadow Stack" and contains CS, LIP, and SSP registers. The right stack is labeled "Handler's Shadow Stack" and contains a "Supervisor Shadow Stack Token". Arrows point to the top of the left stack (labeled "SSP Before Transfer to Handler") and to the top of the right stack (labeled "SSP After Transfer to Handler").

**Shadow Stack Usage with Privilege-Level Change from Level 2 or 1**

Interrupted Procedure's Shadow Stack                      Handler's Shadow Stack

The diagram shows two separate stack structures. The left stack is labeled "Interrupted Procedure's Shadow Stack" and contains CS, LIP, and SSP registers. The right stack is labeled "Handler's Shadow Stack" and contains a "Supervisor Shadow Stack Token", CS, LIP, and SSP registers. Arrows point to the top of the left stack (labeled "SSP Before Transfer to Handler") and to the top of the right stack (labeled "SSP After Transfer to Handler").

Diagram showing shadow stack usage with no privilege-level change. It depicts a single stack structure with CS, LIP, and SSP registers. Arrows indicate the SSP Before and After Transfer to Handler. Diagram showing shadow stack usage with privilege-level change from Level 3. It depicts two separate stack structures. The Interrupted Procedure's Shadow Stack has CS, LIP, and SSP registers. The Handler's Shadow Stack has a Supervisor Shadow Stack Token. Arrows indicate the SSP Before and After Transfer to Handler. Diagram showing shadow stack usage with privilege-level change from Level 2 or 1. It depicts two separate stack structures. The Interrupted Procedure's Shadow Stack has CS, LIP, and SSP registers. The Handler's Shadow Stack has a Supervisor Shadow Stack Token, CS, LIP, and SSP registers. Arrows indicate the SSP Before and After Transfer to Handler.

Figure 6-8. Shadow Stack Usage on Transfers to Interrupt and Exception Handling Routines

If a stack switch does occur, the processor does the following:

1. Temporarily saves (internally) the current contents of the SS, ESP, EFLAGS, CS, and EIP registers.
2. Loads the segment selector and stack pointer for the new stack (that is, the stack for the privilege level being called) from the TSS into the SS and ESP registers and switches to the new stack.
3. Pushes the temporarily saved SS, ESP, EFLAGS, CS, and EIP values for the interrupted procedure's stack onto the new stack.

If shadow stack is enabled at the privilege level of the interrupted procedure, then the processor temporarily saves the SSP of the interrupted procedure internally. If the interrupted procedure is at privilege level 3, the SSP of the interrupted procedure is also saved into the IA32\_PL3\_SSP MSR.

If shadow stack is enabled at the privilege level being called, then the SSP for the called privilege level is obtained from one of the MSRs listed below, depending on the target privilege level. The SSP obtained is then verified to ensure it points to a valid supervisor shadow stack that is not currently active by verifying a supervisor shadow stack token at the address pointed to by the SSP. The operations performed to verify and acquire the supervisor shadow stack token by making it busy are as described in Section 18.2.3 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 1.

- IA32\_PL2\_SSP if transitioning to ring 2.
- IA32\_PL1\_SSP if transitioning to ring 1.
- IA32\_PL0\_SSP if transitioning to ring 0.

If shadow stack is enabled at the privilege level being called and the interrupted procedure was not at privilege level 3, then the processor pushes the temporarily saved CS, LIP (CS.base + EIP), and SSP of the interrupted procedure to the new shadow stack.<sup>1</sup>

4. Pushes an error code on the new stack (if appropriate).
5. Loads the segment selector for the new code segment and the new instruction pointer (from the interrupt gate or trap gate) into the CS and EIP registers, respectively.
6. If the call is through an interrupt gate, clears the IF flag in the EFLAGS register.
7. Begins execution of the handler procedure at the new privilege level.

A return from an interrupt or exception handler is initiated with the IRET instruction. The IRET instruction is similar to the far RET instruction, except that it also restores the contents of the EFLAGS register for the interrupted procedure. When executing a return from an interrupt or exception handler from the same privilege level as the interrupted procedure, the processor performs these actions:

1. Restores the CS and EIP registers to their values prior to the interrupt or exception.

If shadow stack is enabled:

- a. Compares the values on the shadow stack at address SSP+8 (the LIP) and SSP+16 (the CS) to the CS and (CS.base + EIP) popped from the stack, and causes a control protection exception (#CP(FAR-RET/IRET)) if they do not match.
- b. Pops the top-of-stack value (the SSP prior to the interrupt or exception) from the shadow stack into the SSP register.

2. Restores the EFLAGS register.
3. Increments the stack pointer appropriately.
4. Resumes execution of the interrupted procedure.

When executing a return from an interrupt or exception handler from a different privilege level than the interrupted procedure, the processor performs these actions:

1. Performs a privilege check.
2. Restores the CS and EIP registers to their values prior to the interrupt or exception.
3. Restores the EFLAGS register.

---

1. If any of these pushes leads to an exception or a VM exit, the supervisor shadow-stack token remains busy.

If shadow stack is enabled at the current privilege level:

- If SSP is not aligned to 8 bytes, then causes a control protection exception (#CP(FAR-RET/IRET)).
  - If the privilege level of the procedure being returned to is less than 3 (returning to supervisor mode):
    - Compares the values on the shadow stack at address SSP+8 (the LIP) and SSP+16 (the CS) to the CS and (CS.base + EIP) popped from the stack, and causes a control protection exception (#CP(FAR-RET/IRET)) if they do not match.
    - Temporarily saves the top-of-stack value (the SSP of the procedure being returned to) internally.
  - If a busy supervisor shadow stack token is present at address SSP+24, then marks the token free using operations described in Section 18.2.3 of the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 1.
  - If the privilege level of the procedure being returned to is less than 3 (returning to supervisor mode), restores the SSP register from the internally saved value.
  - If the privilege level of the procedure being returned to is 3 (returning to user mode) and shadow stack is enabled at privilege level 3, then restores the SSP register with the value of the IA32\_PL3\_SSP MSR.
4. Restores the SS and ESP registers to their values prior to the interrupt or exception, resulting in a stack switch back to the stack of the interrupted procedure.
  5. Resumes execution of the interrupted procedure.

## 6.5.2 Calls to Interrupt or Exception Handler Tasks

Interrupt and exception handler routines can also be executed in a separate task. Here, an interrupt or exception causes a task switch to a handler task. The handler task is given its own address space and (optionally) can execute at a higher protection level than application programs or tasks.

The switch to the handler task is accomplished with an implicit task call that references a **task gate descriptor**. The task gate provides access to the address space for the handler task. As part of the task switch, the processor saves complete state information for the interrupted program or task. Upon returning from the handler task, the state of the interrupted program or task is restored and execution continues. See Chapter 7, "Interrupt and Exception Handling," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3A, for more information on handling interrupts and exceptions through handler tasks.

## 6.5.3 Interrupt and Exception Handling in Real-Address Mode

When operating in real-address mode, the processor responds to an interrupt or exception with an implicit far call to an interrupt or exception handler. The processor uses the interrupt or exception vector as an index into an interrupt table. The interrupt table contains instruction pointers to the interrupt and exception handler procedures.

The processor saves the state of the EFLAGS register, the EIP register, the CS register, and an optional error code on the stack before switching to the handler procedure.

A return from the interrupt or exception handler is carried out with the IRET instruction.

See Chapter 23, "8086 Emulation," in the Intel® 64 and IA-32 Architectures Software Developer's Manual, Volume 3B, for more information on handling interrupts and exceptions in real-address mode.

## 6.5.4 INT *n*, INTO, INT3, INT1, and BOUND Instructions

The INT *n*, INTO, INT3, and BOUND instructions allow a program or task to explicitly call an interrupt or exception handler. The INT *n* instruction (opcode CD) uses a vector as an argument, which allows a program to call any interrupt handler.

The INTO instruction (opcode CE) explicitly calls the overflow exception (#OF) handler if the overflow flag (OF) in the EFLAGS register is set. The OF flag indicates overflow on arithmetic instructions, but it does not automatically raise an overflow exception. An overflow exception can only be raised explicitly in either of the following ways:

- Execute the INTO instruction.
- Test the OF flag and execute the INT *n* instruction with an argument of 4 (the vector of the overflow exception) if the flag is set.

Both the methods of dealing with overflow conditions allow a program to test for overflow at specific places in the instruction stream.

The INT3 instruction (opcode CC) explicitly calls the breakpoint exception (#BP) handler. Similarly, the INT1 instruction (opcode F1) explicitly calls the debug exception (#DB) handler.<sup>1</sup>

The BOUND instruction explicitly calls the BOUND-range exceeded exception (#BR) handler if an operand is found to be not within predefined boundaries in memory. This instruction is provided for checking references to arrays and other data structures. Like the overflow exception, the BOUND-range exceeded exception can only be raised explicitly with the BOUND instruction or the INT *n* instruction with an argument of 5 (the vector of the bounds-check exception). The processor does not implicitly perform bounds checks and raise the BOUND-range exceeded exception.

### 6.5.5 Handling Floating-Point Exceptions

When operating on individual or packed floating-point values, the IA-32 architecture supports a set of six floating-point exceptions. These exceptions can be generated during operations performed by the x87 FPU instructions or by SSE/SSE2/SSE3 instructions. When an x87 FPU instruction (including the FISTTP instruction in SSE3) generates one or more of these exceptions, it in turn generates floating-point error exception (#MF); when an SSE/SSE2/SSE3 instruction generates a floating-point exception, it in turn generates SIMD floating-point exception (#XM).

See the following sections for further descriptions of the floating-point exceptions, how they are generated, and how they are handled:

- Section 4.9.1, “Floating-Point Exception Conditions,” and Section 4.9.3, “Typical Actions of a Floating-Point Exception Handler.”
- Section 8.4, “x87 FPU Floating-Point Exception Handling,” and Section 8.5, “x87 FPU Floating-Point Exception Conditions.”
- Section 11.5.1, “SIMD Floating-Point Exceptions.”
- Interrupt Behavior.

### 6.5.6 Interrupt and Exception Behavior in 64-Bit Mode

64-bit extensions expand the legacy IA-32 interrupt-processing and exception-processing mechanism to allow support for 64-bit operating systems and applications. Changes include:

- All interrupt handlers pointed to by the IDT are 64-bit code (does not apply to the SMI handler).
- The size of interrupt-stack pushes is fixed at 64 bits. The processor uses 8-byte, zero extended stores.
- The stack pointer (SS:RSP) is pushed unconditionally on interrupts. In legacy environments, this push is conditional and based on a change in current privilege level (CPL).
- The new SS is set to NULL if there is a change in CPL.
- IRET behavior changes.
- There is a new interrupt stack-switch mechanism and a new interrupt shadow stack-switch mechanism.
- The alignment of interrupt stack frame is different.

The above items apply to IDT event delivery. When FRED transitions are enabled, FRED event delivery is used instead. See Section 8.3, “FRED Event Delivery” in the Intel® 64 and IA-32 Architectures Software Developer’s Manual, Volume 3.

---

1. Hardware vendors may use the INT1 instruction for hardware debug. For that reason, Intel recommends software vendors instead use the INT3 instruction for software breakpoints.

## 6.6 PROCEDURE CALLS FOR BLOCK-STRUCTURED LANGUAGES

The IA-32 architecture supports an alternate method of performing procedure calls with the ENTER (enter procedure) and LEAVE (leave procedure) instructions. These instructions automatically create and release, respectively, stack frames for called procedures. The stack frames have predefined spaces for local variables and the necessary pointers to allow coherent returns from called procedures. They also allow scope rules to be implemented so that procedures can access their own local variables and some number of other variables located in other stack frames.

ENTER and LEAVE offer two benefits:

- They provide machine-language support for implementing block-structured languages, such as C and Pascal.
- They simplify procedure entry and exit in compiler-generated code.

### 6.6.1 ENTER Instruction

The ENTER instruction creates a stack frame compatible with the scope rules typically used in block-structured languages. In block-structured languages, the scope of a procedure is the set of variables to which it has access. The rules for scope vary among languages. They may be based on the nesting of procedures, the division of the program into separately compiled files, or some other modularization scheme.

ENTER has two operands. The first specifies the number of bytes to be reserved on the stack for dynamic storage for the procedure being called. Dynamic storage is the memory allocated for variables created when the procedure is called, also known as automatic variables. The second parameter is the lexical nesting level (from 0 to 31) of the procedure. The nesting level is the depth of a procedure in a hierarchy of procedure calls. The lexical level is unrelated to either the protection privilege level or to the I/O privilege level of the currently running program or task.

ENTER, in the following example, allocates 2 Kbytes of dynamic storage on the stack and sets up pointers to two previous stack frames in the stack frame for this procedure:

```
ENTER 2048,3
```

The lexical nesting level determines the number of stack frame pointers to copy into the new stack frame from the preceding frame. A stack frame pointer is a doubleword used to access the variables of a procedure. The set of stack frame pointers used by a procedure to access the variables of other procedures is called the display. The first doubleword in the display is a pointer to the previous stack frame. This pointer is used by a LEAVE instruction to undo the effect of an ENTER instruction by discarding the current stack frame.

After the ENTER instruction creates the display for a procedure, it allocates the dynamic local variables for the procedure by decrementing the contents of the ESP register by the number of bytes specified in the first parameter. This new value in the ESP register serves as the initial top-of-stack for all PUSH and POP operations within the procedure.

To allow a procedure to address its display, the ENTER instruction leaves the EBP register pointing to the first doubleword in the display. Because stacks grow down, this is actually the doubleword with the highest address in the display. Data manipulation instructions that specify the EBP register as a base register automatically address locations within the stack segment instead of the data segment.

The ENTER instruction can be used in two ways: nested and non-nested. If the lexical level is 0, the non-nested form is used. The non-nested form pushes the contents of the EBP register on the stack, copies the contents of the ESP register into the EBP register, and subtracts the first operand from the contents of the ESP register to allocate dynamic storage. The non-nested form differs from the nested form in that no stack frame pointers are copied. The nested form of the ENTER instruction occurs when the second parameter (lexical level) is not zero.

The following pseudo code shows the formal definition of the ENTER instruction. STORAGE is the number of bytes of dynamic storage to allocate for local variables, and LEVEL is the lexical nesting level.

```

PUSH EBP;
FRAME_PTR := ESP;
IF LEVEL > 0
  THEN
    DO (LEVEL - 1) times
      EBP := EBP - 4;
      PUSH Pointer(EBP); (* doubleword pointed to by EBP *)
    OD;
  PUSH FRAME_PTR;
FI;
EBP := FRAME_PTR;
ESP := ESP - STORAGE;

```

The main procedure (in which all other procedures are nested) operates at the highest lexical level, level 1. The first procedure it calls operates at the next deeper lexical level, level 2. A level 2 procedure can access the variables of the main program, which are at fixed locations specified by the compiler. In the case of level 1, the ENTER instruction allocates only the requested dynamic storage on the stack because there is no previous display to copy.

A procedure that calls another procedure at a lower lexical level gives the called procedure access to the variables of the caller. The ENTER instruction provides this access by placing a pointer to the calling procedure's stack frame in the display.

A procedure that calls another procedure at the same lexical level should not give access to its variables. In this case, the ENTER instruction copies only that part of the display from the calling procedure which refers to previously nested procedures operating at higher lexical levels. The new stack frame does not include the pointer for addressing the calling procedure's stack frame.

The ENTER instruction treats a re-entrant procedure as a call to a procedure at the same lexical level. In this case, each succeeding iteration of the re-entrant procedure can address only its own variables and the variables of the procedures within which it is nested. A re-entrant procedure always can address its own variables; it does not require pointers to the stack frames of previous iterations.

By copying only the stack frame pointers of procedures at higher lexical levels, the ENTER instruction makes certain that procedures access only those variables of higher lexical levels, not those at parallel lexical levels (see Figure 6-9).

![Diagram illustrating nested procedures. It shows a large rectangle labeled 'Main (Lexical Level 1)' containing two smaller rectangles. The first smaller rectangle is labeled 'Procedure A (Lexical Level 2)' and contains a rectangle labeled 'Procedure B (Lexical Level 3)'. The second smaller rectangle is labeled 'Procedure C (Lexical Level 3)' and contains a rectangle labeled 'Procedure D (Lexical Level 4)'. This visualizes that Procedure A and Procedure C are at the same lexical level (Level 3) and thus cannot access each other's variables, only those of Main (Level 1) and Procedure A (Level 2).](27fc71a666ffdf8fdc4ce84d9d585008_img.jpg)

Diagram illustrating nested procedures. It shows a large rectangle labeled 'Main (Lexical Level 1)' containing two smaller rectangles. The first smaller rectangle is labeled 'Procedure A (Lexical Level 2)' and contains a rectangle labeled 'Procedure B (Lexical Level 3)'. The second smaller rectangle is labeled 'Procedure C (Lexical Level 3)' and contains a rectangle labeled 'Procedure D (Lexical Level 4)'. This visualizes that Procedure A and Procedure C are at the same lexical level (Level 3) and thus cannot access each other's variables, only those of Main (Level 1) and Procedure A (Level 2).

**Figure 6-9. Nested Procedures**

Block-structured languages can use the lexical levels defined by ENTER to control access to the variables of nested procedures. In Figure 6-9, for example, if procedure A calls procedure B which, in turn, calls procedure C, then procedure C will have access to the variables of the MAIN procedure and procedure A, but not those of procedure B because they are at the same lexical level. The following definition describes the access to variables for the nested procedures in Figure 6-9.

1. MAIN has variables at fixed locations.
2. Procedure A can access only the variables of MAIN.

- 3. Procedure B can access only the variables of procedure A and MAIN. Procedure B cannot access the variables of procedure C or procedure D.
- 4. Procedure C can access only the variables of procedure A and MAIN. Procedure C cannot access the variables of procedure B or procedure D.
- 5. Procedure D can access the variables of procedure C, procedure A, and MAIN. Procedure D cannot access the variables of procedure B.

In Figure 6-10, an ENTER instruction at the beginning of the MAIN procedure creates three doublewords of dynamic storage for MAIN, but copies no pointers from other stack frames. The first doubleword in the display holds a copy of the last value in the EBP register before the ENTER instruction was executed. The second doubleword holds a copy of the contents of the EBP register following the ENTER instruction. After the instruction is executed, the EBP register points to the first doubleword pushed on the stack, and the ESP register points to the last doubleword in the stack frame.

When MAIN calls procedure A, the ENTER instruction creates a new display (see Figure 6-11). The first doubleword is the last value held in MAIN's EBP register. The second doubleword is a pointer to MAIN's stack frame which is copied from the second doubleword in MAIN's display. This happens to be another copy of the last value held in MAIN's EBP register. Procedure A can access variables in MAIN because MAIN is at level 1.

Therefore the base address for the dynamic storage used in MAIN is the current address in the EBP register, plus four bytes to account for the saved contents of MAIN's EBP register. All dynamic variables for MAIN are at fixed, positive offsets from this value.

![Diagram of the stack frame after entering the MAIN procedure. It shows a vertical stack of memory slots. The 'Display' section contains 'Old EBP' and 'Main's EBP'. The 'Dynamic Storage' section contains three empty slots. Arrows indicate EBP points to the 'Old EBP' slot and ESP points to the bottom of the 'Dynamic Storage' section.](8625b4a3b017d8bfae8fa0bb940cfc96_img.jpg)

The diagram illustrates the stack frame after entering the MAIN procedure. It shows a vertical stack of memory slots. The 'Display' section, indicated by a bracket on the left, contains two slots: 'Old EBP' and 'Main's EBP'. The 'Dynamic Storage' section, also indicated by a bracket on the left, contains three empty slots. An arrow labeled 'EBP' points to the 'Old EBP' slot, and an arrow labeled 'ESP' points to the bottom of the 'Dynamic Storage' section.

Diagram of the stack frame after entering the MAIN procedure. It shows a vertical stack of memory slots. The 'Display' section contains 'Old EBP' and 'Main's EBP'. The 'Dynamic Storage' section contains three empty slots. Arrows indicate EBP points to the 'Old EBP' slot and ESP points to the bottom of the 'Dynamic Storage' section.

Figure 6-10. Stack Frame After Entering the MAIN Procedure

![Diagram of the stack frame after entering Procedure A. It shows a vertical stack of memory slots. The 'Display' section contains 'Old EBP', 'Main's EBP', and 'Main's EBP'. The 'Dynamic Storage' section contains 'Procedure A's EBP' and two empty slots. Arrows indicate EBP points to the second 'Main's EBP' slot and ESP points to the bottom of the 'Dynamic Storage' section.](7faf16dab4a9596f24408c85ed8083db_img.jpg)

The diagram illustrates the stack frame after entering Procedure A. It shows a vertical stack of memory slots. The 'Display' section, indicated by a bracket on the left, contains three slots: 'Old EBP', 'Main's EBP', and 'Main's EBP'. The 'Dynamic Storage' section, also indicated by a bracket on the left, contains two slots: 'Procedure A's EBP' and one empty slot. An arrow labeled 'EBP' points to the second 'Main's EBP' slot, and an arrow labeled 'ESP' points to the bottom of the 'Dynamic Storage' section.

Diagram of the stack frame after entering Procedure A. It shows a vertical stack of memory slots. The 'Display' section contains 'Old EBP', 'Main's EBP', and 'Main's EBP'. The 'Dynamic Storage' section contains 'Procedure A's EBP' and two empty slots. Arrows indicate EBP points to the second 'Main's EBP' slot and ESP points to the bottom of the 'Dynamic Storage' section.

Figure 6-11. Stack Frame After Entering Procedure A

When procedure A calls procedure B, the ENTER instruction creates a new display (see Figure 6-12). The first doubleword holds a copy of the last value in procedure A's EBP register. The second and third doublewords are copies of the two stack frame pointers in procedure A's display. Procedure B can access variables in procedure A and MAIN by using the stack frame pointers in its display.

When procedure B calls procedure C, the ENTER instruction creates a new display for procedure C (see Figure 6-13). The first doubleword holds a copy of the last value in procedure B's EBP register. This is used by the LEAVE instruction to restore procedure B's stack frame. The second and third doublewords are copies of the two stack frame pointers in procedure A's display. If procedure C were at the next deeper lexical level from procedure B, a fourth doubleword would be copied, which would be the stack frame pointer to procedure B's local variables.

Note that procedure B and procedure C are at the same level, so procedure C is not intended to access procedure B's variables. This does not mean that procedure C is completely isolated from procedure B; procedure C is called by procedure B, so the pointer to the returning stack frame is a pointer to procedure B's stack frame. In addition, procedure B can pass parameters to procedure C either on the stack or through variables global to both procedures (that is, variables in the scope of both procedures).

![Diagram of the stack frame after entering Procedure B. The stack is shown as a vertical column of cells. From top to bottom, the labeled cells are: 'Old EBP', 'Main's EBP', three empty cells, 'Main's EBP', 'Main's EBP', 'Procedure A's EBP', and one empty cell. Below this is the 'Display' section containing: 'Procedure A's EBP', 'Main's EBP', 'Procedure A's EBP', and 'Procedure B's EBP'. Below the Display is the 'Dynamic Storage' section consisting of empty cells. An arrow labeled 'EBP' points to the 'Procedure A's EBP' cell at the top of the Display section. An arrow labeled 'ESP' points to the bottom of the Dynamic Storage section.](6ba19a99fb96f0139505f0992544a2cf_img.jpg)

Diagram of the stack frame after entering Procedure B. The stack is shown as a vertical column of cells. From top to bottom, the labeled cells are: 'Old EBP', 'Main's EBP', three empty cells, 'Main's EBP', 'Main's EBP', 'Procedure A's EBP', and one empty cell. Below this is the 'Display' section containing: 'Procedure A's EBP', 'Main's EBP', 'Procedure A's EBP', and 'Procedure B's EBP'. Below the Display is the 'Dynamic Storage' section consisting of empty cells. An arrow labeled 'EBP' points to the 'Procedure A's EBP' cell at the top of the Display section. An arrow labeled 'ESP' points to the bottom of the Dynamic Storage section.

**Figure 6-12. Stack Frame After Entering Procedure B**

![Diagram of a stack frame after entering Procedure C, showing nested frames for Main, Procedure A, Procedure B, and Procedure C.](ecb413c6a2e6e22d0413a5020854f529_img.jpg)

The diagram illustrates the stack layout after entering Procedure C. The stack grows downwards, with higher memory addresses at the top and lower addresses at the bottom. The stack is divided into several sections:

- Old EBP:** The topmost frame, representing the caller's frame.
- Main's EBP:** The frame for the main program, located below the Old EBP.
- Main's EBP:** A second instance of the main program's frame, located below the first Main's EBP.
- Procedure A's EBP:** The frame for Procedure A, located below the second Main's EBP.
- Procedure A's EBP:** A second instance of Procedure A's frame, located below the first Procedure A's EBP.
- Main's EBP:** A third instance of the main program's frame, located below the second Procedure A's EBP.
- Procedure A's EBP:** A third instance of Procedure A's frame, located below the third Main's EBP.
- Procedure B's EBP:** The frame for Procedure B, located below the third Procedure A's EBP.
- Procedure B's EBP:** A second instance of Procedure B's frame, located below the first Procedure B's EBP.
- Main's EBP:** A fourth instance of the main program's frame, located below the second Procedure B's EBP.
- Procedure A's EBP:** A fourth instance of Procedure A's frame, located below the fourth Main's EBP.
- Procedure C's EBP:** The frame for Procedure C, located below the fourth Procedure A's EBP.

On the left side, two brackets indicate the stack's growth:

- Display:** A bracket spanning from the top of the stack down to the top of the Procedure C's EBP frame.
- Dynamic Storage:** A bracket spanning from the top of the Procedure C's EBP frame down to the bottom of the stack.

On the right side, two arrows indicate the current values of the EBP and ESP registers:

- EBP:** An arrow pointing to the top of the Procedure B's EBP frame.
- ESP:** An arrow pointing to the bottom of the stack.

Diagram of a stack frame after entering Procedure C, showing nested frames for Main, Procedure A, Procedure B, and Procedure C.

Figure 6-13. Stack Frame After Entering Procedure C

6.6.2 LEAVE Instruction

The LEAVE instruction, which does not have any operands, reverses the action of the previous ENTER instruction. The LEAVE instruction copies the contents of the EBP register into the ESP register to release all stack space allocated to the procedure. Then it restores the old value of the EBP register from the stack. This simultaneously restores the ESP register to its original value. A subsequent RET instruction then can remove any arguments and the return address pushed on the stack by the calling program for use by the procedure.
