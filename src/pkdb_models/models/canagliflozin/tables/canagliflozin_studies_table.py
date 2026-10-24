"""Create the LaTeX table of the canagliflozin studies from `canagliflozin_studies.tsv`."""

from pathlib import Path

import pandas as pd
from sbmlutils.console import console


def create_latex_table(df: pd.DataFrame) -> str:
    """Create the rows of the LaTeX table of the studies.

    Every second row is shaded, the study cites its reference and the PK-DB and
    PubMed identifiers are links.

    Args:
        df: the studies, one row per study.

    Returns:
        The header and the rows of the table.
    """
    latex = ""

    columns_formated = ["\\textbf{" + c + "}" for c in df.columns]
    latex += " & ".join(columns_formated) + " \\\\\n"
    latex += "\n\\hline\n\n"

    for k, (_, row) in enumerate(df.iterrows()):
        if k % 2 == 0:
            latex += "\\rowcolor{Lightgrey}\n"
        values = [
            str(v).replace("TRUE", r"\checkmark").replace("-", "") for v in row.values
        ]

        # references
        values[0] = values[0] + r" \cite{" + values[0] + "}"

        # links
        values[1] = (
            r"\href{https://identifiers.org/pkdb:" + values[1] + "}{" + values[1] + "}"
        )
        values[2] = (
            r"\href{https://pubmed.ncbi.nlm.nih.gov/"
            + values[2]
            + "/}{"
            + values[2]
            + "}"
        )

        latex += " & ".join(values) + "\\\\\n"

    return latex


if __name__ == "__main__":
    tsv_path = Path(__file__).parent / "canagliflozin_studies.tsv"
    latex_path = Path(__file__).parent / "canagliflozin_studies.tex"

    df = pd.read_csv(tsv_path, sep="\t")
    console.print(df)
    latex_str = create_latex_table(df)
    console.rule(style="white")
    console.print(latex_str)
    console.rule(style="white")
    with latex_path.open("w") as f_tex:
        f_tex.write(latex_str)
