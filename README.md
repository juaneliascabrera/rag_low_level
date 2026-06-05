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
# Próximamente
python rag.py "¿Cómo configuro un descriptor de segmento en la GDT?"
```

## Estructura

```
.
├── data/
│   └── curated/       # Documentos Markdown curados manualmente
├── rag.py             # Script principal (próximamente)
├── requirements.txt   # Dependencias
└── CONTEXT.md         # Contexto detallado del proyecto
```

## Licencia

Open Source
