import pandas as pd

INPUT_CSV = "C:\python\webapp-public.csv"
OUTPUT_MD = "C:\python\webapp-public.md"

df = pd.read_csv(INPUT_CSV)

lines = []

# --------------------------------------------------
# Title
# --------------------------------------------------
lines.append("# 🌐 Azure Web Applications – Public Access Report\n")
lines.append(
    "This document provides visibility into Azure Web Applications with a focus on "
    "**public network exposure, ownership, and access justification**.\n"
)

# --------------------------------------------------
# Normalize column names (defensive)
# --------------------------------------------------
df.columns = [c.strip() for c in df.columns]

# --------------------------------------------------
# Summary Section
# --------------------------------------------------
public_apps = df[
    (df["public_network_access"].str.lower() == "enabled") |
    (df["public_network_allowed_rule"].str.contains("public", case=False, na=False))
]

lines.append("## 🚨 Summary – Publicly Accessible Web Applications\n")

if public_apps.empty:
    lines.append("No web applications are publicly accessible.\n")
else:
    lines.append("The following web applications currently allow public access:\n")
    for app in sorted(public_apps["WebApp"].unique()):
        lines.append(f"- **{app}**")
    lines.append("")

# --------------------------------------------------
# Detailed Sections (One per WebApp)
# --------------------------------------------------
for _, row in df.iterrows():
    webapp = row["WebApp"]

    lines.append(f"\n## {webapp}\n")

    lines.append(f"- **Subscription:** {row['Subscription']}")
    lines.append(f"- **Hostname:** {row['Hostnames']}")
    lines.append(f"- **Public Network Access:** {row['public_network_access']}")
    lines.append(
        f"- **IP Restriction Default Action:** "
        f"{row['ip_security_restrictions_default_action']}"
    )

    if pd.notna(row.get("public_network_allowed_rule")):
        lines.append(
            f"- **Public Network Allowed Rule:** "
            f"{row['public_network_allowed_rule']}"
        )

    # Ownership
    owners = []
    if pd.notna(row.get("Owner-1")):
        owners.append(row["Owner-1"])
    if pd.notna(row.get("VP")):
        owners.append(row["VP"])

    if owners:
        lines.append(f"\n**Owners of {webapp}:** {', '.join(owners)}")

    if pd.notna(row.get("Infra_POC")):
        lines.append(f"**Infra POC:** {row['Infra_POC']}")

    # Public access requirement
    if pd.notna(row.get("Public-Access-Required (Yes/No)")):
        lines.append(
            f"**Public Access Required:** "
            f"{row['Public-Access-Required (Yes/No)']}"
        )

    # Justification
    if pd.notna(row.get("Justification")):
        lines.append(f"\n**Justification:** {row['Justification']}")

    # Jira / approval
    if pd.notna(row.get("JiraId_Approval")):
        lines.append(
            f"**Approval Reference:** {row['JiraId_Approval']}"
        )

    # Action
    if pd.notna(row.get("Action")):
        lines.append(f"\n**Recommended Action:** {row['Action']}")

    # Security assessment (generated)
    lines.append("\n**Security Assessment:**")
    if str(row["public_network_access"]).lower() == "enabled":
        lines.append(
            "This web application allows public network access and should be reviewed "
            "to ensure exposure is required and approved."
        )
    else:
        lines.append(
            "This web application does not allow public network access."
        )

# --------------------------------------------------
# Write file
# --------------------------------------------------
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Markdown report generated: {OUTPUT_MD}")
