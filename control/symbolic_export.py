from pathlib import Path
import re
import sympy as sp


def _split_latex_for_pages(latex_expr, max_chars_per_page=1800):
    """Split a long LaTeX expression into smaller chunks that fit one page each."""
    if len(latex_expr) <= max_chars_per_page:
        return [latex_expr]

    chunks = []
    current = []
    depth = 0
    for idx, char in enumerate(latex_expr):
        if char in '{[(':
            depth += 1
        elif char in '}])':
            depth = max(0, depth - 1)

        current.append(char)

        if depth == 0 and char in '+-' and idx > 0 and latex_expr[idx - 1] not in 'eE':
            segment = ''.join(current[:-1]).strip()
            if segment:
                chunks.append(segment)
                current = [char]

        if len(''.join(current)) >= max_chars_per_page:
            segment = ''.join(current).strip()
            if segment:
                chunks.append(segment)
                current = []

    tail = ''.join(current).strip()
    if tail:
        chunks.append(tail)

    if not chunks:
        return [latex_expr]

    return chunks


def export_symbolic_expression_to_pdf(expr, filename='symbolic_expression.pdf', output_dir='.', landscape=False, font_scale=1.0, max_chars_per_page=1800):
    """Export a SymPy expression or matrix to a multi-page PDF.

    The renderer uses Matplotlib directly so the page orientation and font scale
    are applied consistently, even for large symbolic expressions and matrices.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if not str(filename).lower().endswith('.pdf'):
        filename = f'{filename}.pdf'

    output_file = output_path / filename

    if isinstance(expr, (sp.MatrixBase, sp.Matrix)):
        expr = expr
    elif isinstance(expr, sp.Basic):
        expr = expr
    else:
        expr = sp.sympify(expr)

    latex_expr = sp.latex(expr)
    pages = _split_latex_for_pages(latex_expr, max_chars_per_page=max_chars_per_page)

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    import subprocess
    import tempfile
    import os

    fig_width = 11 if landscape else 8.5
    fig_height = 8.5 if landscape else 11

    text_length = max(1, len(latex_expr))
    base_font_size = max(8, min(36, int(12 * font_scale + 0.008 * text_length)))

    if isinstance(expr, (sp.MatrixBase, sp.Matrix)):
        if expr.rows * expr.cols > 25:
            base_font_size = max(8, base_font_size - 2)

    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = os.path.join(tmp_dir, 'expr.tex')
            with open(tmp_path, 'w', encoding='utf-8') as fh:
                fh.write(r'\documentclass[border=5pt]{standalone}' + '\n')
                fh.write(r'\usepackage{amsmath}' + '\n')
                fh.write(r'\begin{document}' + '\n')
                fh.write(r'$\displaystyle ' + latex_expr + r'$' + '\n')
                fh.write(r'\end{document}' + '\n')

            out_pdf = os.path.join(tmp_dir, 'expr.pdf')
            subprocess.run(['pdflatex', '-interaction', 'nonstopmode', '-halt-on-error', '-output-directory', tmp_dir, tmp_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if os.path.exists(out_pdf):
                import shutil
                shutil.copyfile(out_pdf, output_file)
                return str(output_file)
    except Exception:
        pass

    with PdfPages(str(output_file)) as pdf:
        for page_idx, page_text in enumerate(pages):
            fig = plt.figure(figsize=(fig_width, fig_height))
            ax = fig.add_axes([0.03, 0.03, 0.94, 0.94])
            ax.axis('off')

            font_size = max(8, base_font_size - max(0, len(pages) - 1) * 1)
            ax.text(0.01, 0.5, page_text, fontsize=font_size, ha='left', va='center', family='serif')

            pdf.savefig(fig, bbox_inches='tight', pad_inches=0.2)
            plt.close(fig)

    return str(output_file)
