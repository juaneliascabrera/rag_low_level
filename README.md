# RAG Intel x86 32-bit

Sistema RAG (Retrieval-Augmented Generation) especializado en programación de bajo nivel para Intel x86 de 32 bits en Modo Protegido.

## Objetivo

Optimizar el rendimiento de LLMs locales en tareas de desarrollo de kernels monolíticos y sistemas embebidos, eliminando alucinaciones críticas de hardware mediante recuperación de contexto verificado.

## MVP - Alcance

- **Arquitectura:** Intel x86 32-bit, Modo Protegido
- **Conceptos:** GDT, IDT, Paginación, Registros de Control (CR0, CR2, CR3)
- **Instrucciones:** lgdt, lidt, iret, cli, sti, in/out, manipulación de EFLAGS

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
# 1. Configurar proveedor de embeddings en config.py
# EMBEDDING_PROVIDER = "local"  # o "ollama", "openai"

# 2. Indexar documentos (primera vez o cambio de modelo)
python rag.py index

# 3. Hacer consultas
python rag.py query "¿Cómo configuro un descriptor de segmento en la GDT?"
```

## Estructura

```
.
├── rag.py              # CLI principal y orquestador
├── config.py           # Configuración central
├── embedder/           # Proveedores de embeddings (local, ollama, openai)
├── vectorstore/        # Almacenamiento vectorial (NumPy + JSON)
├── chunker/            # Parser de Markdown por headings
├── llm/                # Clientes LLM (Ollama)
├── data/curated/       # Documentos Markdown curados manualmente
├── storage/            # Vectores persistidos (auto-generado)
├── requirements.txt    # Dependencias
└── CONTEXT.md          # Contexto detallado del proyecto
```

## Licencia

Open Source
