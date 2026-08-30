from __future__ import annotations

import csv
import html
import re
import ssl
import textwrap
import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[2]
CORPUS_DIR = ROOT / "docs" / "final_benchmark_corpus"
RAW_DIR = CORPUS_DIR / "raw"


PDF_SOURCES = [
    {
        "source_id": "D1",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/pdf/2005.11401",
        "output": "D1_RAG_Lewis_2020.pdf",
        "type": "downloaded_pdf",
    },
    {
        "source_id": "D3",
        "title": "NIST AI Risk Management Framework 1.0",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
        "output": "D3_NIST_AI_RMF_1_0.pdf",
        "type": "downloaded_pdf",
    },
]


TEXT_SOURCES = [
    {
        "source_id": "D2",
        "title": "llama.cpp README",
        "url": "https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md",
        "raw_output": "D2_llama_cpp_README.md",
        "pdf_output": "D2_llama_cpp_README.pdf",
        "type": "generated_pdf_from_markdown",
    }
]


ICO_PAGES = [
    (
        "ICO AI and Data Protection - Guidance Overview",
        "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/",
    ),
    (
        "ICO AI and Data Protection - Transparency",
        "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-transparency-in-ai/",
    ),
    (
        "ICO AI and Data Protection - Lawfulness",
        "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-do-we-ensure-lawfulness-in-ai/",
    ),
    (
        "ICO AI and Data Protection - Accuracy",
        "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/what-do-we-need-to-know-about-accuracy-and-statistical-accuracy/",
    ),
    (
        "ICO AI and Data Protection - Security and Data Minimisation",
        "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/artificial-intelligence/guidance-on-ai-and-data-protection/how-should-we-assess-security-and-data-minimisation-in-ai/",
    ),
]


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "nav", "footer"}:
            self.skip_depth += 1
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "p", "li", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer"} and self.skip_depth:
            self.skip_depth -= 1
        if not self.skip_depth and tag in {"h1", "h2", "h3", "p", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            text = data.strip()
            if text:
                self.parts.append(text)

    def get_text(self) -> str:
        text = html.unescape(" ".join(self.parts))
        text = re.sub(r"\s+\n", "\n", text)
        text = re.sub(r"\n\s+", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return response.read()
    except URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" not in str(exc):
            raise
        # The Codex bundled Python may not have a populated CA bundle on Windows.
        # Fallback is limited to public benchmark sources and is recorded in README.
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=60, context=context) as response:
            return response.read()


def write_wrapped_pdf(title: str, source_url: str, body_text: str, output_path: Path) -> None:
    styles = getSampleStyleSheet()
    story = [
        Paragraph(title, styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Source URL: {source_url}", styles["Normal"]),
        Spacer(1, 12),
    ]

    for block in body_text.splitlines():
        block = block.strip()
        if not block:
            story.append(Spacer(1, 6))
            continue
        if len(block) < 80 and not block.endswith("."):
            story.append(Paragraph(block, styles["Heading3"]))
        else:
            safe = html.escape(block)
            story.append(Paragraph(safe, styles["BodyText"]))
            story.append(Spacer(1, 4))

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=42,
        leftMargin=42,
        topMargin=42,
        bottomMargin=42,
        title=title,
    )
    doc.build(story)


def markdown_to_text(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        line = re.sub(r"<[^>]+>", " ", line)
        line = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = re.sub(r"`([^`]+)`", r"\1", line)
        line = line.replace("#", "").strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def html_to_text(page_html: str) -> str:
    extractor = TextExtractor()
    extractor.feed(page_html)
    text = extractor.get_text()
    drop_patterns = [
        "The Data (Use and Access) Act 2026 got Royal Assent",
        "Follow us",
        "Print this page",
    ]
    filtered = []
    for line in text.splitlines():
        if any(pattern in line for pattern in drop_patterns):
            continue
        filtered.append(line)
    return "\n".join(filtered)


def main() -> None:
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    manifest_rows = []

    for source in PDF_SOURCES:
        output_path = CORPUS_DIR / source["output"]
        output_path.write_bytes(download_bytes(source["url"]))
        manifest_rows.append({**source, "local_path": str(output_path.relative_to(ROOT))})

    for source in TEXT_SOURCES:
        raw_path = RAW_DIR / source["raw_output"]
        pdf_path = CORPUS_DIR / source["pdf_output"]
        markdown = download_bytes(source["url"]).decode("utf-8", errors="replace")
        raw_path.write_text(markdown, encoding="utf-8")
        write_wrapped_pdf(source["title"], source["url"], markdown_to_text(markdown), pdf_path)
        manifest_rows.append({**source, "output": source["pdf_output"], "local_path": str(pdf_path.relative_to(ROOT))})

    ico_sections = []
    ico_urls = []
    for title, url in ICO_PAGES:
        raw_html = download_bytes(url).decode("utf-8", errors="replace")
        raw_name = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_") + ".html"
        (RAW_DIR / raw_name).write_text(raw_html, encoding="utf-8")
        ico_sections.append(f"{title}\nURL: {url}\n\n{html_to_text(raw_html)}")
        ico_urls.append(url)

    ico_pdf = CORPUS_DIR / "D4_ICO_AI_Data_Protection_Guidance.pdf"
    write_wrapped_pdf(
        "ICO Guidance on AI and Data Protection - Selected Chapters",
        "; ".join(ico_urls),
        "\n\n".join(ico_sections),
        ico_pdf,
    )
    manifest_rows.append(
        {
            "source_id": "D4",
            "title": "ICO Guidance on AI and Data Protection - Selected Chapters",
            "url": " ; ".join(ico_urls),
            "output": ico_pdf.name,
            "type": "generated_pdf_from_html",
            "local_path": str(ico_pdf.relative_to(ROOT)),
        }
    )

    manifest_path = CORPUS_DIR / "corpus_manifest.csv"
    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["source_id", "title", "url", "output", "type", "local_path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in manifest_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})

    readme = CORPUS_DIR / "README.md"
    readme.write_text(
        textwrap.dedent(
            """\
            # Final Benchmark Corpus

            This folder contains the PDF files to upload into the local RAG app for the final benchmark.

            Use these four PDFs as the final source corpus:

            - `D1_RAG_Lewis_2020.pdf`
            - `D2_llama_cpp_README.pdf`
            - `D3_NIST_AI_RMF_1_0.pdf`
            - `D4_ICO_AI_Data_Protection_Guidance.pdf`

            `corpus_manifest.csv` records the source URL and local filename for each source.

            `raw/` stores downloaded raw HTML/Markdown used to generate the derived PDFs. The final RAG app only needs the four PDFs above.

            `Jackie_report.pdf` remains a pilot document only and is not part of this final benchmark corpus.

            Note: if Python certificate validation fails in the local runtime, the preparation script falls back to downloading these public sources with certificate verification disabled. This is only for public benchmark documents and should not be used for private or authenticated sources.
            """
        ),
        encoding="utf-8",
    )

    print(f"Wrote final corpus to {CORPUS_DIR}")


if __name__ == "__main__":
    main()
