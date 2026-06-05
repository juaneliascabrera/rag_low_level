import re
from pathlib import Path
import yaml
from logger import get_logger

logger = get_logger(__name__)


class MarkdownChunker:
    def __init__(self, overlap_lines: int = 3):
        self.overlap_lines = overlap_lines

    def chunk(self, filepath: str) -> list[dict]:
        path = Path(filepath)
        content = path.read_text(encoding='utf-8')
        filename = path.name

        frontmatter, body = self._extract_frontmatter(content)
        base_metadata = self._build_base_metadata(frontmatter, filename)

        sections = self._split_by_headings(body)
        chunks = []

        for i, section in enumerate(sections):
            section_chunks = self._process_section(section, base_metadata, i)
            chunks.extend(section_chunks)

        chunks = self._add_overlap(chunks)
        chunks = self._filter_irrelevant(chunks)

        logger.info(f"  {filename}: {len(chunks)} chunks generated")
        return chunks

    def _extract_frontmatter(self, content: str) -> tuple[dict, str]:
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2]
                    return frontmatter, body
                except yaml.YAMLError:
                    logger.warning("Error parseando YAML frontmatter, ignorando")
        return {}, content

    def _build_base_metadata(self, frontmatter: dict, filename: str) -> dict:
        metadata = {
            "source": filename,
            "architecture": frontmatter.get("architecture", "x86_32"),
            "component": frontmatter.get("component", filename.replace(".md", "")),
            "mode": frontmatter.get("mode", "protected"),
        }
        if "tags" in frontmatter:
            metadata["tags"] = frontmatter["tags"]
        return metadata

    def _split_by_headings(self, body: str) -> list[dict]:
        pattern = r'^(#{1,4})\s+(.+)$'
        lines = body.split('\n')
        sections = []
        current_section = {"heading": "Introduction", "level": 0, "content": []}
        in_code_block = False

        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                current_section["content"].append(line)
                continue

            if not in_code_block:
                match = re.match(pattern, line)
                if match:
                    if current_section["content"]:
                        current_section["content"] = '\n'.join(current_section["content"])
                        sections.append(current_section)

                    level = len(match.group(1))
                    heading = match.group(2).strip()
                    current_section = {"heading": heading, "level": level, "content": []}
                    continue

            current_section["content"].append(line)

        if current_section["content"]:
            current_section["content"] = '\n'.join(current_section["content"])
            sections.append(current_section)

        return sections

    def _process_section(self, section: dict, base_metadata: dict, index: int) -> list[dict]:
        heading = section["heading"]
        content = section["content"].strip()

        if not content:
            return []

        chunks = []
        code_blocks = self._extract_code_blocks(content)

        if code_blocks:
            text_without_code = self._remove_code_blocks(content)

            if text_without_code.strip():
                chunk_metadata = {**base_metadata, "section": heading, "type": "explanation"}
                chunks.append({
                    "text": f"## {heading}\n{text_without_code}",
                    "metadata": chunk_metadata
                })

            for i, (code, lang) in enumerate(code_blocks):
                code_metadata = {
                    **base_metadata,
                    "section": heading,
                    "type": "code",
                    "language": lang or "text"
                }
                chunks.append({
                    "text": f"## {heading} - Code\n```{lang}\n{code}\n```",
                    "metadata": code_metadata
                })
        else:
            chunk_metadata = {**base_metadata, "section": heading, "type": "explanation"}
            chunks.append({
                "text": f"## {heading}\n{content}",
                "metadata": chunk_metadata
            })

        return chunks

    def _extract_code_blocks(self, content: str) -> list[tuple[str, str]]:
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        return [(code.strip(), lang or "text") for lang, code in matches]

    def _remove_code_blocks(self, content: str) -> str:
        return re.sub(r'```(?:\w+)?\n.*?```', '', content, flags=re.DOTALL).strip()

    def _add_overlap(self, chunks: list[dict]) -> list[dict]:
        if len(chunks) <= 1 or self.overlap_lines == 0:
            return chunks

        result = [chunks[0]]

        for i in range(1, len(chunks)):
            prev_type = chunks[i-1]["metadata"].get("type")
            curr_type = chunks[i]["metadata"].get("type")

            if prev_type == curr_type:
                prev_lines = chunks[i-1]["text"].split('\n')
                overlap_text = '\n'.join(prev_lines[-self.overlap_lines:])
                new_text = f"{overlap_text}\n\n{chunks[i]['text']}"
            else:
                new_text = chunks[i]["text"]

            result.append({
                "text": new_text,
                "metadata": chunks[i]["metadata"]
            })

        return result

    def _filter_irrelevant(self, chunks: list[dict]) -> list[dict]:
        filtered = []
        for chunk in chunks:
            text = chunk["text"]

            if len(text) < 50:
                continue

            if chunk["metadata"].get("section") == "Introduction":
                lines = text.split('\n')
                if len(lines) <= 3 and not any('```' in line for line in lines):
                    continue

            filtered.append(chunk)

        return filtered
