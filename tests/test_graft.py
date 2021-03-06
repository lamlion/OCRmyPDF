# © 2019 James R. Barlow: github.com/jbarlow83
#
# This file is part of OCRmyPDF.
#
# OCRmyPDF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OCRmyPDF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OCRmyPDF.  If not, see <http://www.gnu.org/licenses/>.

import os

import pytest

import ocrmypdf
import pikepdf

os_environ = pytest.helpers.os_environ


def test_no_glyphless_graft(resources, outdir):
    pdf = pikepdf.open(resources / 'francais.pdf')
    pdf_aspect = pikepdf.open(resources / 'aspect.pdf')
    pdf_cmyk = pikepdf.open(resources / 'cmyk.pdf')
    pdf.pages.extend(pdf_aspect.pages)
    pdf.pages.extend(pdf_cmyk.pages)
    pdf.save(outdir / 'test.pdf')

    env = os.environ.copy()
    env['_OCRMYPDF_MAX_REPLACE_PAGES'] = '2'
    with os_environ(env):
        ocrmypdf.ocr(
            outdir / 'test.pdf', outdir / 'out.pdf', deskew=True, tesseract_timeout=0
        )


def test_links(resources, outpdf):
    ocrmypdf.ocr(
        resources / 'link.pdf', outpdf, redo_ocr=True, oversample=200, output_type='pdf'
    )
    pdf = pikepdf.open(outpdf)
    p1 = pdf.pages[0]
    p2 = pdf.pages[1]
    assert p1.Annots[0].A.D[0].objgen == p2.objgen
    assert p2.Annots[0].A.D[0].objgen == p1.objgen
