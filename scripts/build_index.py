import csv, json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
RULE_JSON = os.path.join(ROOT, "RULE_PACKS.json")
CSV_PATH  = os.path.join(ROOT, "data", "index.csv")
OUT_MD    = os.path.join(ROOT, "docs", "index.md")

def val(d, k):
    """Safely get and normalize a value from a dict, handling None and empty strings."""
    return (d.get(k) or "").strip()

def load_rules():
    with open(RULE_JSON, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def read_rows():
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    # Skip fully-empty rows
    filtered = []
    for row in rows:
        if any(val(row, k) for k in ['id','title','drive_url','tags','summary','next_action','notes','source']):
            filtered.append(row)
    return filtered

def normalize_tags(s):
    if not s: return []
    return [t.strip() for t in s.split(";") if t.strip()]

def md_link(title, url):
    return f"[{title}]({url})" if url and url.strip() else title

def build_index(rows, rules):
    by_tag = defaultdict(list)
    for row in rows:
        for t in normalize_tags(val(row, "tags")):
            by_tag[t].append(row)

    tag_order = list(rules.keys()) + sorted([t for t in by_tag.keys() if t not in rules])

    lines = []
    lines.append("# Number-Theory Rule Index\n")
    lines.append("_Auto-generated from `data/index.csv`_\n")
    lines.append("## Rule Packs\n")
    for key in rules:
        lines.append(f"- **{key}** — {rules[key].get('title','')}: {rules[key].get('desc','')}")
    lines.append("\n---\n")

    for t in tag_order:
        if t not in by_tag: continue
        title = rules.get(t, {}).get("title", t)
        lines.append(f"## {title} ({t})\n")
        for row in sorted(by_tag[t], key=lambda r: val(r, "title").lower()):
            link = md_link(val(row, "title") or "(untitled)", val(row, "drive_url"))
            summary = val(row, "summary")
            next_action = val(row, "next_action")
            notes = val(row, "notes")
            meta = ", ".join([m for m in [val(row, "source"), val(row, "id")] if m])
            lines.append(f"- {link}  \n  _{meta}_  \n  {summary}")
            if next_action: lines.append(f"  \n  **Next:** {next_action}")
            if notes: lines.append(f"  \n  **Notes:** {notes}")
            lines.append("")
        lines.append("---\n")
    return "\n".join(lines).rstrip() + "\n"

if __name__ == "__main__":
    rules = load_rules()
    rows  = read_rows()
    os.makedirs(os.path.join(ROOT,"docs"), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(build_index(rows, rules))
    print(f"Wrote {OUT_MD}")
