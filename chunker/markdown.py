from pathlib import Path


class MarkdownChunker:
    def chunk(self, filepath: str) -> list[dict]:
        path = Path(filepath)
        content = path.read_text(encoding='utf-8')
        filename = path.name

        sections = content.split('\n## ')
        chunks = []

        for i, section in enumerate(sections):
            if i == 0:
                if section.strip():
                    chunks.append({
                        "text": section.strip(),
                        "metadata": {
                            "source": filename,
                            "section": "Introducción"
                        }
                    })
            else:
                lines = section.strip().split('\n')
                section_title = lines[0].strip()
                section_content = '\n'.join(lines[1:]).strip()

                if section_content:
                    chunks.append({
                        "text": f"## {section_title}\n{section_content}",
                        "metadata": {
                            "source": filename,
                            "section": section_title
                        }
                    })

        return chunks
