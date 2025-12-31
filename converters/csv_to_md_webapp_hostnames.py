import pandas as pd
import openpyxl

INPUT_CSV = "C:\\python\\Book1.xlsx"
OUTPUT_MD = "C:\\python\\hostnames.md"


def main():
    df = pd.read_excel(INPUT_CSV)

    # Normalize column names
    df.columns = [c.strip() for c in df.columns]

    required_cols = {"WebApp", "Hostnames"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    lines = []

    # --------------------------------------------------
    # Title
    # --------------------------------------------------
    lines.append("# 🌐 Azure Web Applications – Hostnames\n")
    lines.append(
        "This document lists Azure Web Applications and their associated hostnames. "
        "It is intended for internal reference and automated knowledge retrieval.\n"
    )

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    lines.append("## 📋 Summary\n")
    lines.append("The following web applications are currently registered:\n")

    for app in sorted(df["WebApp"].unique()):
        lines.append(f"- **{app}**")

    # --------------------------------------------------
    # Detailed Sections
    # --------------------------------------------------
    for _, row in df.iterrows():
        webapp = row["WebApp"]
        hostname = row["Hostnames"]

        lines.append(f"\n## {webapp}\n")
        lines.append(
            f"The web application **{webapp}** is accessible via the following hostname:\n"
        )
        lines.append(f"- `{hostname}`")

    # --------------------------------------------------
    # Write output
    # --------------------------------------------------
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Markdown README generated: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
