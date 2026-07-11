"""PDF/X-1a post-processing via Ghostscript."""

import shutil
import subprocess
from pathlib import Path


def pdfx_available() -> bool:
    return shutil.which("gs") is not None


def convert_to_pdfx1a(input_pdf: Path, output_pdf: Path) -> Path:
    """
    Convert CMYK PDF to PDF/X-1a using Ghostscript.
    Requires Ghostscript installed on system.
    """
    if not pdfx_available():
        raise RuntimeError(
            "Ghostscript (gs) not found. Install ghostscript for PDF/X-1a export."
        )

    pdfx_def = _write_pdfx_def(output_pdf.parent)

    cmd = [
        "gs",
        "-dPDFX",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOOUTERSAVE",
        "-sDEVICE=pdfwrite",
        "-dPDFSETTINGS=/prepress",
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        "-sProcessColorModel=DeviceCMYK",
        "-sColorConversionStrategy=CMYK",
        f"-sOutputFile={output_pdf}",
        str(pdfx_def),
        str(input_pdf),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_pdf


def _write_pdfx_def(directory: Path) -> Path:
    """Write minimal PDFX definition file for Ghostscript."""
    path = directory / "PDFX_def.ps"
    path.write_text(
        """
%!PS
/Inch { 72 mul } def
/ISOCoatedRBv2.icc (ISO Coated v2 300%) def
[/_objdef {icc_PDFX} /type /stream /OBJ pdfmark
[/_objdef {OutputIntent_PDFX} /type /dict /OBJ pdfmark
[{OutputIntent_PDFX} <<
  /Type /OutputIntent
  /S /GTS_PDFX
  /OutputConditionIdentifier (FOGRA39)
  /Info (FOGRA39)
  /OutputCondition ()
  /RegistryName ()
>> /PUT pdfmark
""",
        encoding="utf-8",
    )
    return path
