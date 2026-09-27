#!/usr/bin/env python3
"""Render one or more sentence structure overviews as an inline HTML fragment."""

import argparse
import html
import json
import re
import sys
from pathlib import Path


ROLE_COLORS = {
    "main": "light-dark(#0969da, #58a6ff)",
    "clause": "light-dark(#1a7f37, #3fb950)",
    "parallel": "light-dark(#9a6700, #d29922)",
    "nested": "light-dark(#8250df, #bc8cff)",
    "extra": "light-dark(#9a6700, #d29922)",
}


def safe_id(value):
    value = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    return value or "structure-overview"


def render_item(item):
    title = html.escape(item.get("title", "结构总览"))
    sentence_parts = []
    for segment in item.get("segments", []):
        raw_text = segment.get("text", "")
        role = segment.get("role")
        if role and raw_text.strip():
            leading = raw_text[: len(raw_text) - len(raw_text.lstrip())]
            trailing = raw_text[len(raw_text.rstrip()) :]
            core_end = len(raw_text) - len(trailing) if trailing else len(raw_text)
            core = raw_text[len(leading) : core_end]
            sentence_parts.append(
                '{0}<span class="syntax-segment role-{1}">{2}</span>{3}'.format(
                    html.escape(leading),
                    html.escape(role),
                    html.escape(core),
                    html.escape(trailing),
                )
            )
        else:
            sentence_parts.append(html.escape(raw_text))

    legend_rows = []
    for entry in item.get("legend", []):
        role = html.escape(entry.get("role", "extra"))
        label = html.escape(entry.get("label", ""))
        legend_rows.append(
            '<li><span class="legend-swatch role-{0}" aria-hidden="true"></span>'
            '<span>{1}</span></li>'.format(role, label)
        )

    relations = ""
    if item.get("relations"):
        relation_text = "\n".join(html.escape(x) for x in item["relations"])
        relations = (
            '<div class="relation-title">层级关系</div>'
            '<pre class="relations">{}</pre>'.format(relation_text)
        )

    legend = ""
    if legend_rows:
        legend = '<div class="legend-title">图例</div><ul class="legend">{}</ul>'.format(
            "".join(legend_rows)
        )

    return (
        '<section class="syntax-item card" aria-label="{0}">'
        '<header class="syntax-heading"><p class="eyebrow">Sentence structure</p>'
        '<h3>{0}</h3></header>'
        '<p class="sentence">{1}</p>'
        '{2}{3}'
        '</section>'
    ).format(title, "".join(sentence_parts), legend, relations)


def render(spec, root_id):
    color_rules = []
    for role, color in ROLE_COLORS.items():
        color_rules.append(
            "#{root} .role-{role}{{--syntax-color:{color};}}".format(
                root=root_id, role=role, color=color
            )
        )

    items = "".join(render_item(item) for item in spec.get("items", []))
    return """<div id="{root}" class="syntax-overview">
<style>
#{root}{{color-scheme:light dark;color:var(--foreground);font-size:var(--font-size-base);display:grid;gap:1.5rem;}}
#{root} .syntax-item{{display:grid;gap:1rem;}}
#{root} .syntax-heading{{display:grid;gap:.25rem;}}
#{root} .eyebrow{{margin:0;color:var(--muted-foreground);font-size:.72em;font-weight:650;letter-spacing:.08em;text-transform:uppercase;}}
#{root} h3{{margin:0;font-size:1.05em;font-weight:600;line-height:1.35;}}
#{root} .sentence{{margin:0;padding:.9rem 0;border-block:1px solid var(--border);line-height:2.05;font-size:1.02em;}}
#{root} .syntax-segment{{--syntax-soft:color-mix(in srgb,var(--syntax-color) 7%,transparent);color:inherit;padding:.08em .22em;border-radius:.22rem;background:var(--syntax-soft);box-decoration-break:clone;-webkit-box-decoration-break:clone;}}
#{root} .legend-title,#{root} .relation-title{{font-size:.82em;font-weight:650;letter-spacing:.02em;}}
#{root} .legend{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem 1rem;}}
#{root} .legend li{{display:flex;align-items:center;gap:.6rem;min-width:0;color:var(--muted-foreground);font-size:.92em;}}
#{root} .legend-swatch{{--syntax-soft:color-mix(in srgb,var(--syntax-color) 7%,transparent);width:2rem;height:1.05rem;border-radius:.22rem;background:var(--syntax-soft);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--syntax-color) 18%,transparent);flex:none;}}
#{root} .relations{{margin:0;padding:.15rem 0 .15rem .85rem;border-left:2px solid var(--border);background:transparent;color:var(--muted-foreground);white-space:pre-wrap;font:inherit;font-size:.92em;line-height:1.65;}}
@media(max-width:560px){{#{root} .legend{{grid-template-columns:1fr;}}}}
{color_rules}
</style>
{items}
</div>
""".format(root=root_id, color_rules="\n".join(color_rules), items=items)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="UTF-8 JSON specification; stdin when omitted")
    parser.add_argument("--json", help="JSON specification passed as one argument")
    parser.add_argument("--output", required=True, help="Destination .html fragment")
    args = parser.parse_args()

    if args.json:
        spec = json.loads(args.json)
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            spec = json.load(handle)
    else:
        spec = json.load(sys.stdin)

    if not isinstance(spec.get("items"), list) or not spec["items"]:
        raise ValueError("spec.items must contain at least one structure overview")

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    root_id = safe_id(output.stem)
    output.write_text(render(spec, root_id), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
