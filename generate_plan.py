#!/usr/bin/env python3
# Simple SVG floor plan generator for a 2-apartment-per-floor layout with a central core.
# Not construction-ready; schematic only.

def make_svg(width_m=16.0, depth_m=11.0, floors=3, core_w_m=4.0, scale=60, ext_wall_m=0.24, int_wall_m=0.115):
    W = int(width_m * scale)
    D = int(depth_m * scale)
    ext_w_px = ext_wall_m * scale
    int_w_px = int_wall_m * scale

    core_x1 = 6.0 * scale
    core_x2 = (6.0 + core_w_m) * scale
    left_x1, left_x2 = 0, 6.0*scale
    right_x1, right_x2 = core_x2, width_m*scale

    def rect(x,y,w,h, stroke="black", fill="none", stroke_width=2, dash=None):
        d = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"'
        if dash:
            d += f' stroke-dasharray="{dash}"'
        d += '/>'
        return d

    def label(text, x, y, size=16, anchor="middle"):
        return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" text-anchor="{anchor}">{text}</text>'

    svg_elems = []
    svg_elems.append(f'<rect x="0" y="0" width="{W}" height="{D}" fill="white"/>')
    svg_elems.append(rect(0, 0, W, D, stroke="black", stroke_width=ext_w_px))
    svg_elems.append(rect(core_x1, 0, core_w_m*scale, D, stroke="black", stroke_width=int_w_px))
    svg_elems.append(label("Kern: Treppe + Aufzug + Flur", (core_x1+core_x2)/2, 25, 16))
    svg_elems.append(rect(left_x1, 0, left_x2-left_x1, D, stroke="black", stroke_width=int_w_px, dash="6,4"))
    svg_elems.append(label("WE-L: ~66 m²", (left_x1+left_x2)/2, 25, 16))
    svg_elems.append(rect(right_x1, 0, right_x2-right_x1, D, stroke="black", stroke_width=int_w_px, dash="6,4"))
    svg_elems.append(label("WE-R: ~66 m²", (right_x1+right_x2)/2, 25, 16))

    # (weitere Raumaufteilungen wie im SVG möglich)

    title = f"QNG Mehrparteienhaus – Typischer Grundriss je Geschoss (EG/OG/DG)\\n" \
            f"Grundfläche: {width_m:.1f} × {depth_m:.1f} m = {width_m*depth_m:.0f} m², " \
            f"Geschossfläche gesamt: {floors*width_m*depth_m:.0f} m² (bei {floors} Ebenen)\\n" \
            f"2 WE à ~66 m² / Ebene + Gebäudekern (~{core_w_m*depth_m:.0f} m²)"
    svg_elems.append(label(title, W/2, D + 40, 18))

    svg = f'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\\n' \
          f'<svg width="{W}" height="{D+80}" viewBox="0 0 {W} {D+80}" xmlns="http://www.w3.org/2000/svg">\\n' \
          f'    {"".join(svg_elems)}\\n' \
          f'</svg>\\n'
    return svg

if __name__ == "__main__":
    svg = make_svg()
    with open("grundriss_qng_16x11_3x.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Wrote grundriss_qng_16x11_3x.svg")
