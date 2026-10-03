#!/usr/bin/env python3
"""Builds slides/index.html (three static slides) from data/results.json.

Run from the repository root:  python3 scripts/build_slides.py
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data" / "results.json").read_text())

AMBER, TEAL, GREY = "#F2B134", "#6FD6DC", "#8191AB"
TIER_COLOUR = {"tested": AMBER, "frontier": TEAL, "lower": GREY}
SANS = "'IBM Plex Sans', sans-serif"
MONO = "'IBM Plex Mono', monospace"
PIXEL = "'Press Start 2P', monospace"


def total(m):
    return sum(m["scores"].values())


def header(title, subtitle):
    return f"""<div style="display:flex;flex-direction:column;gap:14px">
<div style="font:400 11px/1.6 {PIXEL};color:#9FB0C6;letter-spacing:1px">PIXEL FISHING GAME / MODEL COMPARISON</div>
<h2 style="margin:0;font:400 28px/1.4 {PIXEL};color:#F2EBD9">{title}</h2>
<div style="font:400 16px/24px {SANS};color:#9FB0C6">{subtitle}</div>
</div>"""


def footer(note, page):
    return f"""<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:32px">
<div style="max-width:900px;font:400 13px/18px {SANS};color:#9FB0C6">{note}</div>
<div style="font:400 10px/1.6 {PIXEL};color:#9FB0C6;flex:none">{page} / 3</div>
</div>"""


def slide(inner):
    return f"""<section class="slide-wrap"><div class="slide" style="width:1280px;height:720px;box-sizing:border-box;padding:40px 56px;background:#0F1B2D;color:#F2EBD9;font-family:{SANS};display:flex;flex-direction:column;gap:24px">
{inner}
</div></section>"""


def fmt_cost(v):
    return str(float(f"{v:.3f}" if v < 1 else f"{v:.2f}")).rstrip("0").rstrip(".") if v else "0"


# ---------- slide 1: time taken
def slide1():
    px = 13
    rows = []
    items = [(m["name"], m["minutes"], "tested", m["id"] == "grok-4-7-high") for m in data["tested"]]
    items += [(f'{r["name"]} (est.)', r["minutes"], r["tier"], False) for r in data["references"]]
    # tested models keep the order of the data file; references go below
    for name, t, kind, open_end in items:
        c = TIER_COLOUR[kind]
        solid = kind == "tested"
        if solid:
            bar = f"width:{t*px}px;height:24px;flex:none;background:{c};box-shadow:4px 4px 0 rgba(0,0,0,.35)"
        else:
            bar = (f"width:{t*px}px;height:24px;flex:none;box-sizing:border-box;border:2px solid {c};"
                   f"background:repeating-linear-gradient(135deg,{c}55 0,{c}55 4px,transparent 4px,transparent 8px)")
        open_div = ""
        if open_end:
            open_div = (f'<div style="width:{520-t*px}px;height:24px;flex:none;box-sizing:border-box;border:2px dashed {AMBER};border-left:none;'
                        f'background:repeating-linear-gradient(135deg,rgba(242,177,52,.35) 0,rgba(242,177,52,.35) 4px,transparent 4px,transparent 8px)"></div>')
        label = f"{t}+ min" if open_end else (f"{t} min" if solid else f"~{t} min")
        rows.append(f"""<div style="position:relative;display:flex;align-items:center;gap:16px;height:40px">
<div style="width:190px;flex:none;font:600 15px/20px {SANS}">{name}</div>
<div style="width:520px;flex:none;display:flex;align-items:center"><div style="{bar}"></div>{open_div}</div>
<div style="width:90px;flex:none;font:500 16px/20px {MONO}">{label}</div>
</div>""")
    ticks = "".join(
        f'<div style="position:absolute;left:{i*130}px;top:0;transform:translateX(-50%);white-space:nowrap">{i*10}{" min" if i==4 else ""}</div>' for i in range(5))
    grid = "".join(
        f'<div style="position:absolute;top:0;bottom:0;left:{min(i*130,519)}px;width:1px;background:#243756"></div>' for i in range(5))

    def chips(items_, colour):
        return "".join(f'<div style="padding:6px 12px;border:2px solid {colour};font:600 14px/20px {SANS}">{n}</div>' for n in items_)

    frontier = [r["name"] for r in data["references"] if r["tier"] == "frontier"]
    lower = [r["name"] for r in data["references"] if r["tier"] == "lower"]
    panel = f"""<div style="flex:1;min-width:0;align-self:flex-start;box-sizing:border-box;padding:24px;background:#14263F;border:2px solid #2B3F5E;display:flex;flex-direction:column;gap:20px">
<div style="font:400 12px/1.6 {PIXEL}">Reference tiers</div>
<div style="display:flex;flex-direction:column;gap:10px"><div style="font:600 12px/16px {SANS};letter-spacing:1.5px;color:{TEAL}">FRONTIER</div><div style="display:flex;flex-wrap:wrap;gap:8px">{chips(frontier, TEAL)}</div></div>
<div style="display:flex;flex-direction:column;gap:10px"><div style="font:600 12px/16px {SANS};letter-spacing:1.5px;color:{AMBER}">THIS TEST</div><div style="padding:8px 12px;border:2px dashed {AMBER};font:400 14px/20px {SANS}">The six models you tested, drawn solid</div></div>
<div style="display:flex;flex-direction:column;gap:10px"><div style="font:600 12px/16px {SANS};letter-spacing:1.5px;color:#9AA9C0">LOWER TIER</div><div style="display:flex;flex-wrap:wrap;gap:8px">{chips(lower, GREY)}</div></div>
<div style="font:400 13px/18px {SANS};color:#9FB0C6">Reference times are illustrative estimates, drawn hatched.</div>
</div>"""
    body = f"""<div style="display:flex;gap:48px;flex:1;min-height:0">
<div style="display:flex;flex-direction:column;gap:12px;width:832px;flex:none">
<div style="display:flex;gap:16px"><div style="width:190px;flex:none"></div>
<div style="position:relative;width:520px;height:20px;flex:none;font:500 12px/16px {MONO};color:#9FB0C6">{ticks}</div></div>
<div style="position:relative;display:flex;flex-direction:column">
<div style="position:absolute;left:206px;top:0;bottom:0;width:520px">{grid}</div>
{"".join(rows)}
</div></div>{panel}</div>"""
    note = ("Grok 4.7 High looped for 32 minutes, needed steering, ran 6 more minutes, looped again and then hit the 5 hour usage cap. "
            "Its bar is a floor, and it is judged on what it produced.")
    return slide(header("How long each model took", "Wall-clock time to one-shot the same prompt. Shorter is faster, not better.") + body + footer(note, 1))


# ---------- slide 2: time against quality
def slide2():
    W, H, TMAX, QMAX = 620, 340, 40, 100
    dirs = {"luna-6-high": "b", "grok-4-6-high": "r", "minimax-m3-thinking": "r",
            "longcat-preview-2-5": "r", "glm-5-3-high": "t", "grok-4-7-high": "l"}
    dots = []
    for m in data["tested"]:
        x = round(m["minutes"] / TMAX * W)
        y = round(H - total(m) / QMAX * H)
        d = dirs[m["id"]]
        base = "position:absolute;display:flex;white-space:nowrap;"
        if d == "l":
            st = base + f"left:{x+8}px;top:{y-10}px;transform:translateX(-100%);flex-direction:row-reverse;align-items:center;gap:8px;"
        elif d == "t":
            st = base + f"left:{x-8}px;top:{y-36}px;flex-direction:column-reverse;align-items:flex-start;gap:4px;"
        elif d == "b":
            st = base + f"left:{x-8}px;top:{y-8}px;flex-direction:column;align-items:flex-start;gap:4px;"
        else:
            st = base + f"left:{x-8}px;top:{y-10}px;flex-direction:row;align-items:center;gap:8px;"
        dots.append(f'<div style="{st}"><div style="width:16px;height:16px;flex:none;background:{AMBER};box-shadow:3px 3px 0 rgba(0,0,0,.4)"></div>'
                    f'<span style="font:600 14px/20px {SANS}">{m["name"]}</span></div>')
    hlines = "".join(f'<div style="position:absolute;left:0;top:{i*68}px;width:{W}px;height:1px;background:#243756"></div>' for i in range(5))
    vlines = "".join(f'<div style="position:absolute;left:{min(i*155,619)}px;top:0;width:1px;height:{H}px;background:#243756"></div>' for i in range(1, 5))
    ylabels = "".join(f'<div style="position:absolute;right:0;top:{(-8 if i==0 else i*68-8)}px">{100-i*20}</div>' for i in range(6))
    xlabels = "".join(f'<div style="position:absolute;left:{i*155}px;top:2px;transform:translateX(-50%)">{i*10}</div>' for i in range(5))
    chart = f"""<div style="display:flex;flex-direction:column;gap:8px;width:692px;flex:none">
<div style="font:600 12px/16px {SANS};letter-spacing:1px;color:#9FB0C6">QUALITY SCORE OUT OF 100</div>
<div style="display:flex;gap:12px">
<div style="position:relative;width:40px;height:{H}px;flex:none;font:500 12px/16px {MONO};color:#9FB0C6;text-align:right">{ylabels}</div>
<div style="position:relative;width:{W}px;height:{H}px;flex:none;background:#14263F">{hlines}{vlines}
<div style="position:absolute;left:0;top:{H-2}px;width:{W}px;height:2px;background:#4A6491"></div>
<div style="position:absolute;left:0;top:0;width:2px;height:{H}px;background:#4A6491"></div>
<div style="position:absolute;left:0;top:0;width:155px;height:102px;box-sizing:border-box;border:2px dashed #3C8F95"></div>
<div style="position:absolute;left:12px;top:8px;font:600 12px/16px {SANS};color:{TEAL}">Fast and good</div>
{"".join(dots)}</div></div>
<div style="position:relative;width:{W}px;height:20px;margin-left:52px;font:500 12px/16px {MONO};color:#9FB0C6">{xlabels}</div>
<div style="margin-left:52px;width:{W}px;text-align:center;font:600 12px/16px {SANS};letter-spacing:1px;color:#9FB0C6">MINUTES TAKEN, SLOWER TO THE RIGHT</div>
</div>"""
    rows = []
    for m in sorted(data["tested"], key=total, reverse=True):
        t = total(m)
        r = m["minutes"] / t if t else None
        ratio = "n/a" if r is None else (f"{r:.2f}" if r < 1 else f"{r:.1f}")
        s = m["scores"]
        rows.append(f"""<div style="display:flex;align-items:center;gap:4px;padding:8px 0;border-bottom:1px solid #2B3F5E;font:500 14px/20px {MONO}">
<span style="flex:1;min-width:0;font:600 14px/20px {SANS}">{m["name"]}</span>
<span style="width:26px;text-align:right">{s["creativity"]}</span><span style="width:26px;text-align:right">{s["design"]}</span>
<span style="width:26px;text-align:right">{s["enjoyability"]}</span><span style="width:26px;text-align:right">{s["feature"]}</span>
<span style="width:44px;text-align:right;color:{AMBER}">{t}</span><span style="width:60px;text-align:right;color:#9FB0C6">{ratio}</span></div>""")
    panel = f"""<div style="flex:1;min-width:0;align-self:flex-start;box-sizing:border-box;padding:24px;background:#14263F;border:2px solid #2B3F5E;display:flex;flex-direction:column;gap:14px">
<div style="font:400 13px/1.6 {PIXEL}">Scores</div>
<div style="display:flex;flex-direction:column">
<div style="display:flex;align-items:flex-end;gap:4px;padding-bottom:6px;border-bottom:2px solid #2B3F5E;font:600 12px/16px {MONO};color:#9FB0C6">
<span style="flex:1;min-width:0"></span><span style="width:26px;text-align:right">C</span><span style="width:26px;text-align:right">D</span><span style="width:26px;text-align:right">E</span><span style="width:26px;text-align:right">F</span><span style="width:44px;text-align:right">Total</span><span style="width:60px;text-align:right">Min/pt</span></div>
{"".join(rows)}</div>
<div style="font:400 13px/18px {SANS};color:#9FB0C6">C creativity, D design and visuals, E enjoyability, F implemented feature, each out of 25. Min/pt is minutes per point, lower is better.</div>
</div>"""
    note = "Grok 4.7 High is plotted at 38 minutes and was cut short by the usage cap. GLM 5.3 High scored 0 because it did not run."
    return slide(header("Time against quality", "Each square is one model. Top left means fast and good.")
                 + f'<div style="display:flex;gap:48px;flex:1;min-height:0">{chart}{panel}</div>' + footer(note, 2))


# ---------- slide 3: cost
def slide3():
    W = 720
    items = [(m["name"], m["cost_usd"], "tested", m.get("cost_note")) for m in data["tested"]]
    items += [(f'{r["name"]} (reference)', r["cost_usd"], r["tier"], None) for r in data["references"]]
    mx = max(c for _, c, _, _ in items)
    pw = 10 ** math.floor(math.log10(mx))
    axis_max = next((s * pw for s in (1, 2, 2.5, 5, 10) if s * pw >= mx), pw * 10)
    rows = []
    for name, c, kind, note in items:
        colour = TIER_COLOUR[kind]
        w = max(6, round(c / axis_max * W)) if c else 6
        if c:
            label = ("" if kind == "tested" else "~") + "$" + fmt_cost(c)
        else:
            label = "$0 (free)"
        rows.append(f"""<div style="position:relative;display:flex;align-items:center;gap:16px;height:46px">
<div style="width:190px;flex:none;font:600 15px/20px {SANS}">{name}</div>
<div style="width:{W}px;flex:none;display:flex;align-items:center"><div style="width:{w}px;height:26px;flex:none;background:{colour};box-shadow:4px 4px 0 rgba(0,0,0,.35)"></div></div>
<div style="width:110px;flex:none;font:500 16px/20px {MONO}">{label}</div></div>""")
    ticks = "".join(f'<div style="position:absolute;top:0;left:{i*180}px;transform:translateX(-50%);font:500 12px/16px {MONO};color:#9FB0C6">${fmt_cost(axis_max*i/4)}</div>' for i in range(5))
    grid = "".join(f'<div style="position:absolute;top:0;bottom:0;left:{min(i*180,719)}px;width:1px;background:#243756"></div>' for i in range(5))
    body = f"""<div style="display:flex;flex-direction:column;gap:12px;flex:1;min-height:0">
<div style="display:flex;gap:16px"><div style="width:190px;flex:none"></div><div style="position:relative;width:{W}px;height:20px;flex:none">{ticks}</div></div>
<div style="position:relative;display:flex;flex-direction:column"><div style="position:absolute;left:206px;top:0;bottom:0;width:{W}px">{grid}</div>{"".join(rows)}</div></div>"""
    note = ("All six ran at the same time on OpenCode Go and together used 100% of the 5 hour allowance. Grok 4.7 High alone used about 12% of it. "
            "Tested-model costs come from the OpenCode request log. LongCat Preview 2.5 ran on a free tier. "
            "Reference bars are illustrative API-cost estimates, not measured.")
    return slide(header("What each run cost", "Spend for one attempt at the same prompt, in the same order as the time slide.") + body + footer(note, 3))


html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pixel Fishing Game: model comparison slides</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;600&family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 0; background: #0A121F; padding: 16px 0 48px; }}
  .slide-wrap {{ margin: 0 auto 24px; overflow: hidden; }}
  .slide {{ transform-origin: top left; }}
</style>
</head>
<body>
{slide1()}
{slide2()}
{slide3()}
<script>
  // Scale the fixed 1280x720 slides down to fit narrow screens.
  function fit() {{
    var s = Math.min(1, (window.innerWidth - 32) / 1280);
    document.querySelectorAll('.slide-wrap').forEach(function (w) {{
      w.style.width = 1280 * s + 'px';
      w.style.height = 720 * s + 'px';
      w.firstElementChild.style.transform = 'scale(' + s + ')';
    }});
  }}
  window.addEventListener('resize', fit);
  fit();
</script>
</body>
</html>
"""
(ROOT / "slides" / "index.html").write_text(html)
print("wrote slides/index.html")

# ---------- landing page (works with GitHub Pages)
cards = []
for m in sorted(data["tested"], key=total, reverse=True):
    cards.append(f'<li><a href="{m["file"]}"><strong>{m["name"]}</strong><span>{m["game_title"]}</span>'
                 f'<em>{total(m)}/100 &middot; {m["minutes"]} min</em></a></li>')
landing = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Model Comparison: Pixel Fishing Game</title>
<link rel="icon" href="assets/icon.svg">
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin: 0; background: #0F1B2D; color: #F2EBD9; font: 16px/1.6 system-ui, sans-serif; }}
  main {{ max-width: 720px; margin: 0 auto; padding: 48px 20px; }}
  h1 {{ font-size: 28px; margin: 0 0 8px; }}
  p {{ color: #9FB0C6; }}
  ul {{ list-style: none; padding: 0; display: grid; gap: 12px; }}
  li a {{ display: grid; grid-template-columns: 1fr auto; gap: 2px 16px; padding: 14px 16px; background: #14263F; border: 2px solid #2B3F5E; color: inherit; text-decoration: none; }}
  li a:hover {{ border-color: #F2B134; }}
  li span {{ color: #9FB0C6; }} li em {{ grid-row: 1 / span 2; grid-column: 2; align-self: center; color: #F2B134; font-style: normal; }}
  .slides {{ display: inline-block; margin: 8px 0 24px; padding: 10px 16px; background: #F2B134; color: #0F1B2D; font-weight: 600; text-decoration: none; }}
</style>
</head>
<body>
<main>
<h1>Model Comparison: Pixel Fishing Game</h1>
<p>Six models were given the same one-shot prompt to build a Stardew Valley style fishing game. Open each game below, ranked by my score out of 100.</p>
<a class="slides" href="slides/">View the comparison slides</a>
<ul>
{chr(10).join(cards)}
</ul>
</main>
</body>
</html>
"""
(ROOT / "index.html").write_text(landing)
print("wrote index.html")
