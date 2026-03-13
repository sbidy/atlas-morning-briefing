# Copyright (c) 2026 Junjie Tang. MIT License. See LICENSE file for details.
"""Tests for pdf_generator module."""

import pytest
from scripts.pdf_generator import PDFGenerator


@pytest.fixture
def generator():
    return PDFGenerator(page_format="kindle", font_size=10, line_spacing=1.5)


class TestParseMarkdownLine:
    def test_h1(self, generator):
        assert generator.parse_markdown_line("# Title") == ("h1", "Title")

    def test_h2(self, generator):
        assert generator.parse_markdown_line("## Section") == ("h2", "Section")

    def test_h3(self, generator):
        assert generator.parse_markdown_line("### Subsection") == ("h3", "Subsection")

    def test_body(self, generator):
        assert generator.parse_markdown_line("Normal text") == ("body", "Normal text")

    def test_empty_line(self, generator):
        assert generator.parse_markdown_line("") == ("empty", "")

    def test_code_fence(self, generator):
        assert generator.parse_markdown_line("```python") == ("code_fence", "python")

    def test_unordered_list(self, generator):
        assert generator.parse_markdown_line("- Item") == ("body", "- Item")

    def test_ordered_list(self, generator):
        assert generator.parse_markdown_line("1. Item") == ("body", "1. Item")

    def test_whitespace_line(self, generator):
        assert generator.parse_markdown_line("   ") == ("empty", "")


class TestStripEmoji:
    def test_strips_emoji(self, generator):
        assert generator.strip_emoji("Hello World") == "Hello World"

    def test_strips_common_emoji(self, generator):
        result = generator.strip_emoji("Stock Watchlist")
        assert "Stock Watchlist" in result

    def test_preserves_text(self, generator):
        assert generator.strip_emoji("Plain text") == "Plain text"

    def test_empty_string(self, generator):
        assert generator.strip_emoji("") == ""


class TestMarkdownToFlowables:
    def test_generates_flowables(self, generator):
        md = "# Title\n\nSome text\n\n## Section\n\nMore text"
        flowables = generator.markdown_to_flowables(md)
        assert len(flowables) > 0

    def test_code_block(self, generator):
        md = "```python\nprint('hello')\n```"
        flowables = generator.markdown_to_flowables(md)
        assert len(flowables) > 0

    def test_empty_input(self, generator):
        flowables = generator.markdown_to_flowables("")
        assert isinstance(flowables, list)


class TestPageSizes:
    def test_kindle_size(self):
        gen = PDFGenerator(page_format="kindle")
        assert gen.page_size is not None

    def test_a4_size(self):
        gen = PDFGenerator(page_format="a4")
        assert gen.page_size is not None

    def test_letter_size(self):
        gen = PDFGenerator(page_format="letter")
        assert gen.page_size is not None

    def test_unknown_falls_back_to_kindle(self):
        gen = PDFGenerator(page_format="unknown")
        kindle_gen = PDFGenerator(page_format="kindle")
        assert gen.page_size == kindle_gen.page_size


class TestGeneratePdf:
    def test_generates_pdf_file(self, generator, tmp_path):
        md = "# Test Briefing\n\nThis is a test.\n\n## Section\n\n- Item 1\n- Item 2"
        output = str(tmp_path / "test.pdf")
        generator.generate_pdf(md, output)
        import os
        assert os.path.exists(output)
        assert os.path.getsize(output) > 0
