#!/usr/bin/env python3
"""Render one or more sentence structure overviews as an inline HTML fragment."""

import argparse
import html
import json
import re
import sys
from pathlib import Path


ROLE_COLORS = {
    "main": "var(--blue)",
    "clause": "var(--green)",
    "parallel": "var(--orange)",
    "nested": "var(--red)",
    "extra": "var(--purple)",
}


def safe_id(value):
    value = re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")
    return value or "structure-overview"


def render_item(item):
    title = html.escape(item.get("title", "结构总览"))
    sentence_parts = []
    for segment in item.get("segments", []):
        text = html.escape(segment.get("text", ""))
        role = segment.get("role")
        if role:
            sentence_parts.append(
                '<span class="syntax-segment role-{0}">{1}</span>'.format(
                    html.escape(role), text
                )
            )
        else:
            sentence_parts.append(text)

    legend_rows = []
    for entry in item.get("legend", []):
        role = html.escape(entry.get("role", "extra"))
        label = html.escape(entry.get("label", ""))
        legend_rows.append(
            '<li><span class="legend-line role-{0}" aria-hidden="true"></span>'
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
        '<section class="syntax-item" aria-label="{0}">'
        '<h3>{0}</h3>'
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
#{root}{{color:var(--foreground);font-size:var(--font-size-base);display:grid;gap:1.5rem;}}
#{root} .syntax-item{{display:grid;gap:.65rem;}}
#{root} h3{{margin:0;font-weight:500;}}
#{root} .sentence{{margin:0;line-height:1.9;font-size:1.02em;}}
#{root} .syntax-segment{{color:inherit;text-decoration-line:underline;text-decoration-color:var(--syntax-color);text-decoration-thickness:3px;text-underline-offset:5px;text-decoration-skip-ink:none;}}
#{root} .legend-title,#{root} .relation-title{{font-weight:500;margin-top:.15rem;}}
#{root} .legend{{list-style:none;padding:0;margin:0;display:grid;gap:.4rem;}}
#{root} .legend li{{display:flex;align-items:center;gap:.65rem;color:var(--muted-foreground);}}
#{root} .legend-line{{width:2.25rem;border-bottom:3px solid var(--syntax-color);flex:none;}}
#{root} .relations{{margin:0;padding:0;background:transparent;color:var(--muted-foreground);white-space:pre-wrap;font:inherit;line-height:1.65;}}
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
