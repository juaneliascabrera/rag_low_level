import pytest
from chunker.markdown import MarkdownChunker
import tempfile
import os


class TestMarkdownChunker:
    def test_basic_chunking(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("# Title\nIntro\n## Section 1\nContent 1\n## Section 2\nContent 2")
            
            chunker = MarkdownChunker(overlap_lines=0)
            chunks = chunker.chunk(md_file)
            
            assert len(chunks) >= 2

    def test_frontmatter_extraction(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("---\narchitecture: x86_32\ncomponent: GDT\n---\n# Title\nContent")
            
            chunker = MarkdownChunker(overlap_lines=0)
            chunks = chunker.chunk(md_file)
            
            assert chunks[0]["metadata"]["architecture"] == "x86_32"
            assert chunks[0]["metadata"]["component"] == "GDT"

    def test_code_block_separation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("## Section\nExplanation\n```nasm\nmov eax, 1\n```\nMore text")
            
            chunker = MarkdownChunker(overlap_lines=0)
            chunks = chunker.chunk(md_file)
            
            code_chunks = [c for c in chunks if c["metadata"].get("type") == "code"]
            text_chunks = [c for c in chunks if c["metadata"].get("type") == "explanation"]
            
            assert len(code_chunks) >= 1
            assert len(text_chunks) >= 1

    def test_overlap(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("## Section 1\nLine 1\nLine 2\nLine 3\n## Section 2\nContent")
            
            chunker = MarkdownChunker(overlap_lines=2)
            chunks = chunker.chunk(md_file)
            
            if len(chunks) >= 2:
                assert "Line 2" in chunks[1]["text"] or "Line 3" in chunks[1]["text"]

    def test_filter_irrelevant(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            md_file = os.path.join(tmpdir, "test.md")
            with open(md_file, 'w') as f:
                f.write("# Title\nShort\n## Section\nLonger content here with more text")
            
            chunker = MarkdownChunker(overlap_lines=0)
            chunks = chunker.chunk(md_file)
            
            for chunk in chunks:
                assert len(chunk["text"]) >= 50
