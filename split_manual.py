#!/usr/bin/env python3
"""
Script para dividir el manual Intel Volume 1 en archivos markdown separados por capítulo.
Combina múltiples métodos para identificar los límites de cada capítulo.
"""

import re
from pathlib import Path

# Mapeo de capítulos a metadata
CHAPTER_METADATA = {
    1: {
        "component": "manual_overview",
        "tags": ["introduction", "conventions", "notation"]
    },
    2: {
        "component": "architecture_history",
        "tags": ["history", "processors", "microarchitecture"]
    },
    3: {
        "component": "basic_execution_environment",
        "tags": ["registers", "memory", "addressing", "segments"]
    },
    4: {
        "component": "data_types",
        "tags": ["data_types", "addressing_modes", "floating_point"]
    },
    5: {
        "component": "instruction_set_summary",
        "tags": ["instructions", "simd", "sse", "avx"]
    },
    6: {
        "component": "procedures_interrupts_exceptions",
        "tags": ["procedures", "stack", "interrupts", "exceptions"]
    },
    7: {
        "component": "general_purpose_instructions",
        "tags": ["instructions", "load_store", "arithmetic", "control_flow"]
    },
    8: {
        "component": "x87_fpu",
        "tags": ["fpu", "floating_point", "x87"]
    },
    9: {
        "component": "mmx_technology",
        "tags": ["mmx", "simd", "packed_data"]
    },
    10: {
        "component": "sse",
        "tags": ["sse", "xmm", "simd", "floating_point"]
    },
    11: {
        "component": "sse2",
        "tags": ["sse2", "xmm", "simd", "double_precision"]
    },
    12: {
        "component": "sse3_sse4_aesni",
        "tags": ["sse3", "ssse3", "sse4", "aesni"]
    },
    13: {
        "component": "xsave",
        "tags": ["xsave", "state_management"]
    },
    14: {
        "component": "avx_fma_avx2",
        "tags": ["avx", "fma", "ymm", "simd"]
    },
    15: {
        "component": "avx512",
        "tags": ["avx512", "zmm", "simd"]
    },
    16: {
        "component": "avx10",
        "tags": ["avx10", "simd"]
    },
    17: {
        "component": "tsx",
        "tags": ["transactional_synchronization", "lock_elision"]
    },
    18: {
        "component": "cet",
        "tags": ["control_flow_enforcement", "shadow_stack"]
    },
    19: {
        "component": "amx",
        "tags": ["advanced_matrix_extensions"]
    },
    20: {
        "component": "input_output",
        "tags": ["io", "ports", "in", "out"]
    },
    21: {
        "component": "processor_identification",
        "tags": ["cpuid", "feature_detection"]
    }
}


def split_manual(input_file: str, output_dir: str):
    """Divide el manual en archivos separados por capítulo."""
    
    # Leer el archivo completo
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Encontrar todos los límites de capítulos usando múltiples métodos
    chapter_starts = {}
    
    # Método 1: Buscar "## X.1" (primera sección de cada capítulo)
    section_pattern = re.compile(r'^## (\d+)\.1\s+')
    for i, line in enumerate(lines):
        match = section_pattern.match(line)
        if match:
            chapter_num = int(match.group(1))
            if chapter_num not in chapter_starts:
                # Retroceder para encontrar el encabezado del capítulo
                for j in range(i-1, max(0, i-50), -1):
                    if re.match(r'^#{1,2}\s+CHAPTER\s+\d+', lines[j], re.IGNORECASE):
                        chapter_starts[chapter_num] = j
                        break
                    elif lines[j].startswith('#') and not lines[j].startswith('##'):
                        chapter_starts[chapter_num] = j
                        break
                else:
                    chapter_starts[chapter_num] = i - 1
    
    # Método 2: Buscar "# CHAPTER X" o "## CHAPTER X" en el contenido real
    # (después de la línea 1059, que es donde termina la tabla de contenidos)
    chapter_pattern = re.compile(r'^#{1,2}\s+CHAPTER\s+(\d+)', re.IGNORECASE)
    for i in range(1059, len(lines)):
        match = chapter_pattern.match(lines[i])
        if match:
            chapter_num = int(match.group(1))
            if chapter_num not in chapter_starts:
                chapter_starts[chapter_num] = i
    
    # Ordenar los capítulos por posición
    sorted_chapters = sorted(chapter_starts.items(), key=lambda x: x[1])
    
    # Crear los capítulos con sus límites
    chapters = []
    for idx, (chapter_num, start) in enumerate(sorted_chapters):
        if idx + 1 < len(sorted_chapters):
            end = sorted_chapters[idx + 1][1]
        else:
            end = len(lines)
        
        chapters.append({
            'number': chapter_num,
            'start': start,
            'end': end
        })
    
    # Crear directorio de salida
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Procesar cada capítulo
    for chapter in chapters:
        chapter_num = chapter['number']
        chapter_lines = lines[chapter['start']:chapter['end']]
        chapter_content = '\n'.join(chapter_lines)
        
        # Obtener metadata para este capítulo
        metadata = CHAPTER_METADATA.get(chapter_num, {
            "component": f"chapter_{chapter_num}",
            "tags": []
        })
        
        # Crear frontmatter YAML
        frontmatter = f"""---
architecture: x86_32
component: {metadata['component']}
mode: protected
tags: {metadata['tags']}
source: intel_sdm_vol1_chapter_{chapter_num}.md
---

"""
        
        # Agregar título del documento
        title = f"# Intel SDM Volume 1 - Chapter {chapter_num}\n\n"
        
        # Escribir el archivo
        output_file = output_path / f"intel_sdm_vol1_chapter_{chapter_num:02d}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(title)
            f.write(chapter_content)
        
        print(f"✓ Chapter {chapter_num:02d}: {output_file.name} ({len(chapter_lines)} lines)")
    
    print(f"\n✓ {len(chapters)} capítulos extraídos en {output_dir}/")


if __name__ == "__main__":
    input_file = "pdf/datalab-output-vol1.pdf.md"
    output_dir = "data/curated"
    
    split_manual(input_file, output_dir)
