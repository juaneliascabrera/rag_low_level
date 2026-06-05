# Contexto del Proyecto: RAG Especializado en Bajo Nivel (Intel x86 32-bits)

> **Fecha:** 2026-06-05  
> **Objetivo:** Centralizar el contexto, desafíos técnicos, arquitectura sugerida y hoja de ruta para el desarrollo de un sistema RAG de código abierto enfocado en optimizar el rendimiento de LLMs en tareas de programación de bajo nivel, desarrollo de kernels monolíticos y sistemas embebidos.

---

## 1. Planteamiento del Problema

Los LLMs comerciales y genéricos demuestran un rendimiento deficiente al interactuar con el hardware o escribir código en Assembler debido a:

- **Escasez de Datos de Entrenamiento:** El volumen de código en ensamblador público y moderno en plataformas como GitHub es astronómicamente menor en comparación con lenguajes de alto nivel (Python, JavaScript, C++).
- **Ausencia de Contexto Físico:** Los modelos carecen de comprensión inherente sobre mapas de memoria, temporizaciones, estados de pines o la distribución exacta de registros de control específicos.
- **Dependencia Absoluta de la Arquitectura:** El código varía drásticamente según la arquitectura física (Intel x86, ARM, RISC-V, AVR). Mezclar convenciones sintácticas o registros inexistentes deriva en fallas críticas del sistema (Triple Faults, Kernel Panics).

> En el desarrollo de bajo nivel, la precisión es binaria: un bit incorrecto en un registro de control anula la viabilidad de todo el sistema operativo o firmware.

---

## 2. Alcance Inicial del Proyecto (MVP)

Para garantizar la viabilidad y precisión del sistema, el alcance inicial se delimita estrictamente a:

- **Arquitectura Objetivo:** Intel x86 de 32 bits (Arquitectura educativa/experimental clásica y desarrollo de kernels monolíticos en Modo Protegido).
- **Conceptos Críticos a Cubrir:**
  * Inicialización y estructuras del sistema: **GDT** (Global Descriptor Table), **IDT** (Interrupt Descriptor Table).
  * Gestión de Memoria: **Paginación básica**, Page Directory, Page Tables, registros de control (**CR0, CR2, CR3**).
  * Set de Instrucciones de Sistema: `lgdt`, `lidt`, `iret`, `cli`, `sti`, `in/out`, manipulación de **EFLAGS**.

---

## 3. Arquitectura del Sistema RAG

El sistema se compone de tres módulos core distribuidos localmente para garantizar la privacidad y el funcionamiento offline del desarrollador:

```
[ Manuales Técnicos / PDFs ] --> [ Parser de Ingesta ] --> [ Fragmentación Semántica ]
                                                                     │
                                                                     ▼
[ LLM Local via Ollama ] <-- [ Orquestador de Prompts ] <-- [ Base Vectorial (ChromaDB) ]
```

### 3.A. Módulo de Ingesta y Parser Especializado (`src/parser/`)

Los manuales técnicos oficiales (como el *Intel Architecture Software Developer's Manual, Volume 3*) presentan estructuras tabulares complejas que los extractores de texto plano rompen fácilmente.

- **Función:** Parsear páginas seleccionadas de la documentación oficial convirtiendo diagramas de bits y tablas de registros a formatos estructurados limpios (Markdown o JSON).
- **Herramientas sugeridas:** PyMuPDF, Marker, o modelos locales de visión de maquetación.

### 3.B. Base de Conocimiento Vectorial y Chunking (`src/embedder/`)

La fragmentación tradicional basada en conteo de caracteres destruye la semántica de bajo nivel.

- **Estrategia de Chunking:** Fragmentación semántica indivisible por estructuras de hardware. Por ejemplo, la descripción completa de un descriptor de segmento de la GDT (Base, Límite, Acceso, DPL) debe permanecer en un único chunk con sus metadatos asociados.
- **Estructura de Metadatos:** Cada vector se almacena con etiquetas explícitas:

```json
{
  "arquitectura": "x86_32",
  "componente": "IDT",
  "tipo_informacion": "estructura_byte",
  "modo": "protegido"
}
```

- **Almacenamiento:** Base de datos vectorial local y ligera como ChromaDB, FAISS o LanceDB.

### 3.C. Cliente de Orquestación e Inyección de Prompt (`src/llm_client/`)

Encargado de interceptar la consulta del desarrollador, realizar la búsqueda semántica e inyectar el contexto bajo reglas estrictas de control.

- **Prompt del Sistema Sugerido:**

> "Actúa como un ingeniero de firmware y arquitecto de sistemas operativos experto en Intel x86 de 32 bits en Modo Protegido. Se te proporciona un fragmento textual verificado del manual de referencia oficial. Utilizando únicamente las direcciones de memoria, estructuras y nombres de registros presentes en el contexto, genera el código solicitado. Si la información no es suficiente, indícalo explícitamente; está terminantemente prohibido alucinar o inventar registros de hardware."

---

## 4. Hoja de Ruta para Desarrollo Open-Source

### Fase 1: Preparación del Dataset Semilla
- Extraer y limpiar de forma manual/semi-asistida las secciones del manual de Intel correspondientes al establecimiento de la GDT, IDT y activación de la paginación. Crear el repositorio inicial con estos archivos estructurados.

### Fase 2: Pipeline de Vectores Local
- Desarrollar el script de Python para automatizar la generación de embeddings y el almacenamiento en ChromaDB.

### Fase 3: Interfaz de Usuario e Integración
- Diseñar una interfaz de línea de comandos (CLI) que permita realizar consultas directamente desde la terminal de desarrollo e interactuar con modelos locales de código a través de Ollama (ej. qwen2.5-coder, deepseek-coder).

### Fase 4: Agente con Bucle de Compilación (Futuro)
- Conectar el generador con herramientas como `nasm` o `gcc` para capturar errores de sintaxis en caliente, permitiendo que el LLM se autocorrija antes de entregar el código final.

---

## 5. Estructura de Directorios Sugerida

```
.
├── src/
│   ├── parser/          # Módulo de ingesta y parseo de documentación técnica
│   ├── embedder/        # Módulo de chunking semántico y generación de embeddings
│   └── llm_client/      # Módulo de orquestación de prompts y consulta a LLM local
├── data/
│   ├── raw/             # Manuales técnicos en PDF
│   └── processed/       # Texto estructurado extraído (Markdown/JSON)
├── chroma_db/           # Base de datos vectorial local
├── CONTEXT.md           # Este archivo
└── README.md            # Documentación del proyecto
```

---

*Documento generado a partir del análisis del contexto inicial del proyecto.*
