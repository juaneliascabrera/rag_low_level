# Project Context: RAG Specialized in Low-Level (Intel x86 32-bit)

> **Date:** 2026-06-05  
> **Goal:** Centralize the context, technical challenges, suggested architecture, and roadmap for developing an open-source RAG system focused on optimizing LLM performance in low-level programming tasks, monolithic kernel development, and embedded systems.

---

## 1. Problem Statement

Commercial and generic LLMs demonstrate poor performance when interacting with hardware or writing Assembler code due to:

- **Scarcity of Training Data:** The volume of modern, public assembler code on platforms like GitHub is astronomically smaller compared to high-level languages (Python, JavaScript, C++).
- **Absence of Physical Context:** The models lack inherent understanding of memory maps, timings, pin states, or the exact distribution of specific control registers.
- **Absolute Architecture Dependence:** Code varies drastically depending on the physical architecture (Intel x86, ARM, RISC-V, AVR). Mixing syntactic conventions or non-existent registers leads to critical system failures (Triple Faults, Kernel Panics).

> In low-level development, precision is binary: a single incorrect bit in a control register voids the viability of the entire operating system or firmware.

---

## 2. Initial Project Scope (MVP)

To guarantee the system's viability and accuracy, the initial scope is strictly limited to:

- **Target Architecture:** Intel x86 32-bit (Classic educational/experimental architecture and monolithic kernel development in Protected Mode).
- **Critical Concepts to Cover:**
  * System initialization and structures: **GDT** (Global Descriptor Table), **IDT** (Interrupt Descriptor Table).
  * Memory Management: **Basic Paging**, Page Directory, Page Tables, control registers (**CR0, CR2, CR3**).
  * System Instruction Set: `lgdt`, `lidt`, `iret`, `cli`, `sti`, `in/out`, **EFLAGS** manipulation.

---

## 3. RAG System Architecture

The system is composed of three core modules distributed locally to guarantee the developer's privacy and offline operation:

```
[ Technical Manuals / PDFs ] --> [ Ingestion Parser ] --> [ Semantic Fragmentation ]
                                                            │
                                                            ▼
[ Local LLM via Ollama ] <-- [ Prompt Orchestrator ] <-- [ Vector Database (ChromaDB) ]
```

### 3.A. Specialized Ingestion and Parser Module (`src/parser/`)

Official technical manuals (such as the *Intel Architecture Software Developer's Manual, Volume 3*) present complex tabular structures that plain text extractors break easily.

- **Function:** Parse selected pages of the official documentation, converting bit diagrams and register tables into clean structured formats (Markdown or JSON).
- **Suggested tools:** PyMuPDF, Marker, or local layout-vision models.

### 3.B. Vector Knowledge Base and Chunking (`src/embedder/`)

Traditional character-count-based fragmentation destroys low-level semantics.

- **Chunking Strategy:** Indivisible semantic fragmentation by hardware structures. For example, the complete description of a GDT segment descriptor (Base, Limit, Access, DPL) must remain in a single chunk with its associated metadata.
- **Metadata Structure:** Each vector is stored with explicit labels:

```json
{
  "architecture": "x86_32",
  "component": "IDT",
  "information_type": "byte_structure",
  "mode": "protected"
}
```

- **Storage:** Lightweight local vector database such as ChromaDB, FAISS, or LanceDB.

### 3.C. Orchestration Client and Prompt Injection (`src/llm_client/`)

Responsible for intercepting the developer's query, performing semantic search, and injecting context under strict control rules.

- **Suggested System Prompt:**

> "Act as an expert firmware engineer and operating system architect specialized in Intel x86 32-bit Protected Mode. You are provided with a verified textual fragment from the official reference manual. Using only the memory addresses, structures, and register names present in the context, generate the requested code. If the information is not sufficient, state so explicitly; it is strictly forbidden to hallucinate or invent hardware registers."

---

## 4. Open-Source Development Roadmap

### Phase 1: Seed Dataset Preparation
- Manually/semi-assisted extraction and cleaning of the Intel manual sections corresponding to the GDT, IDT setup, and paging activation. Create the initial repository with these structured files.

### Phase 2: Local Vector Pipeline
- Develop the Python script to automate embedding generation and storage in ChromaDB.

### Phase 3: User Interface and Integration
- Design a command-line interface (CLI) that allows queries directly from the development terminal and interacts with local code models through Ollama (e.g. qwen2.5-coder, deepseek-coder).

### Phase 4: Agent with Compilation Loop (Future)
- Connect the generator with tools like `nasm` or `gcc` to capture syntax errors in real-time, allowing the LLM to self-correct before delivering the final code.

---

## 5. Suggested Directory Structure

```
.
├── src/
│   ├── parser/          # Ingestion and parsing module for technical documentation
│   ├── embedder/        # Semantic chunking and embedding generation module
│   └── llm_client/      # Prompt orchestration and local LLM query module
├── data/
│   ├── raw/             # Technical manuals in PDF
│   └── processed/       # Extracted structured text (Markdown/JSON)
├── chroma_db/           # Local vector database
├── CONTEXT.md           # This file
└── README.md            # Project documentation
```

---

*Document generated from the analysis of the initial project context.*
