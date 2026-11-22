#!/usr/bin/env python3
"""Rectangular spiral NFC coil -> KiCad footprint.

Inductance uses the planar rectangular coil formula from NXP AN11276
(antenna design guide), which is what their antenna tool is based on.
It's good to roughly 10% for etched coils; the trim cap covers the rest.

By default it keeps trace and gap equal (even stripes, since the coil is
visible on the front) and solves their width for each turn count so the
coil resonates at --f-target, then picks the most turns that land in a
sensible width range.

    uv run tools/coil_gen.py -o hardware/libs/card.pretty
    uv run tools/coil_gen.py --width 0.3 --gap 0.3 --turns 6
"""

import argparse
import math
import pathlib
import uuid

MU0 = 4e-7 * math.pi


def inductance(a0, b0, n, w, g, t=0.035):
    """All dims in mm. a0/b0 are the outer coil dimensions. Returns henries."""
    a0, b0, w, g, t = (x * 1e-3 for x in (a0, b0, w, g, t))
    a = a0 - n * (g + w)
    b = b0 - n * (g + w)
    if a <= 0 or b <= 0:
        return float("nan")
    d = 2 * (t + w) / math.pi
    diag = math.hypot(a, b)
    x1 = a * math.log(2 * a * b / (d * (a + diag)))
    x2 = b * math.log(2 * a * b / (d * (b + diag)))
    x3 = 2 * (a + b - diag)
    x4 = (a + b) / 4
    # p = 1.8 for etched coils per the app note
    return MU0 / math.pi * (x1 + x2 - x3 + x4) * n ** 1.8


def resistance_dc(a0, b0, n, w, g, t=0.035, rho=1.72e-8):
    length = 0.0
    for i in range(n):
        inset = i * (w + g)
        length += 2 * (a0 - 2 * inset) + 2 * (b0 - 2 * inset)
    return rho * (length * 1e-3) / (w * 1e-3 * t * 1e-3)


def spiral_points(a0, b0, n, w, g):
    """Centre-line polyline, starting at the outer end, winding inward."""
    pitch = w + g
    x0, y0 = -a0 / 2 + w / 2, -b0 / 2 + w / 2
    x1, y1 = a0 / 2 - w / 2, b0 / 2 - w / 2
    # start a little in from the top-left corner so the lead-in has room
    pts = [(x0 + 3.0, y0)]
    for i in range(n):
        o = i * pitch
        pts += [
            (x1 - o, y0 + o),
            (x1 - o, y1 - o),
            (x0 + o, y1 - o),
            (x0 + o, y0 + o + pitch),
        ]
    # end the last turn partway along the top edge, inside the start
    last = pts[-1]
    pts.append((last[0] + 3.0, last[1]))
    return pts


def footprint(name, a0, b0, n, w, g, drill, l_uh, r_dc):
    pts = spiral_points(a0, b0, n, w, g)
    uid = lambda: str(uuid.uuid4())
    out = [
        f'(footprint "{name}"',
        '  (version 20241229)',
        '  (generator "coil_gen")',
        '  (layer "F.Cu")',
        f'  (descr "Rectangular NFC coil {a0:.2f}x{b0:.2f}mm, {n} turns, w={w} g={g}, '
        f'L~{l_uh:.2f}uH, Rdc~{r_dc:.2f}ohm")',
        '  (tags "NFC antenna coil 13.56MHz")',
        '  (attr board_only exclude_from_pos_files exclude_from_bom)',
        '  (net_tie_pad_groups "1,2")',
        f'  (property "Reference" "ANT1" (at 0 {-b0 / 2 - 1.5:.3f} 0) (layer "F.SilkS") (hide yes)',
        '    (effects (font (size 1 1) (thickness 0.15))))',
        f'  (property "Value" "{name}" (at 0 {b0 / 2 + 1.5:.3f} 0) (layer "F.Fab")',
        '    (effects (font (size 1 1) (thickness 0.15))))',
    ]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        out.append(
            f'  (fp_line (start {xa:.4f} {ya:.4f}) (end {xb:.4f} {yb:.4f}) '
            f'(stroke (width {w}) (type solid)) (layer "F.Cu") (uuid "{uid()}"))'
        )
    # exposed gold coil: mask opening follows the copper exactly
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        out.append(
            f'  (fp_line (start {xa:.4f} {ya:.4f}) (end {xb:.4f} {yb:.4f}) '
            f'(stroke (width {w}) (type solid)) (layer "F.Mask") (uuid "{uid()}"))'
        )
    pad = max(w + 0.1, drill + 0.2)
    for num, (x, y) in (("1", pts[0]), ("2", pts[-1])):
        out.append(
            f'  (pad "{num}" thru_hole circle (at {x:.4f} {y:.4f}) (size {pad:.3f} {pad:.3f}) '
            f'(drill {drill}) (layers "*.Cu") (remove_unused_layers no) (uuid "{uid()}"))'
        )
    out.append(
        f'  (fp_rect (start {-a0 / 2:.3f} {-b0 / 2:.3f}) (end {a0 / 2:.3f} {b0 / 2:.3f}) '
        f'(stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd") (uuid "{uid()}"))'
    )
    out.append(")")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--card", default="85.6x54", help="board outline WxH in mm")
    p.add_argument("--margin", type=float, default=1.2, help="outline to outer copper, mm")
    p.add_argument("--width", type=float, help="trace width, mm (default: solved, equal to the gap)")
    p.add_argument("--gap", type=float, help="trace gap, mm (default: equal to the width)")
    p.add_argument("--wmin", type=float, default=0.25, help="narrowest stripe the solver may pick, mm")
    p.add_argument("--wmax", type=float, default=0.60, help="widest stripe the solver may pick, mm")
    p.add_argument("--cu", type=float, default=0.018, help="copper thickness, mm (half-ounce flex)")
    p.add_argument("--drill", type=float, default=0.2)
    # NTAG X DNA datasheet Rev 3.2, Table 282: 18.4 pF and 1.5 kohm (parallel) at start of operation
    p.add_argument("--cin-pf", type=float, default=18.4, help="tag input capacitance")
    p.add_argument("--rchip-kohm", type=float, default=1.5, help="tag input resistance, parallel")
    p.add_argument("--cpar-pf", type=float, default=2.5, help="coil + layout parasitics")
    # the trim cap and the lamination can only pull f0 down, so start above 13.56
    p.add_argument("--f-target", type=float, default=14.0, help="untuned resonance to aim for, MHz")
    p.add_argument("--turns", type=int, help="force turn count")
    p.add_argument("-o", "--out", type=pathlib.Path)
    args = p.parse_args()

    cw, ch = (float(v) for v in args.card.lower().split("x"))
    a0, b0 = cw - 2 * args.margin, ch - 2 * args.margin
    c = (args.cin_pf + args.cpar_pf) * 1e-12
    w0 = 2 * math.pi * 13.56e6
    wt = 2 * math.pi * args.f_target * 1e6
    target = 1 / (wt * wt * c)
    f0_of = lambda l: 1 / (2 * math.pi * math.sqrt(l * c))
    L = lambda n, w, g: inductance(a0, b0, n, w, g, args.cu)

    print(f"coil {a0:.1f} x {b0:.1f} mm, copper {args.cu * 1000:.0f} um")
    print(f"target L = {target * 1e6:.2f} uH for {args.f_target} MHz (C = {c * 1e12:.1f} pF)")

    if args.width is not None:
        w, g = args.width, args.gap if args.gap is not None else args.width
        best = None
        for n in range(1, 20):
            l = L(n, w, g)
            if math.isnan(l):
                break
            print(f"  N={n:2d}  L={l * 1e6:6.2f} uH  f0={f0_of(l) / 1e6:6.2f} MHz")
            if l <= target:
                best = n
        n = args.turns or best
    else:
        # L falls as the stripes widen, so bisect the stripe width for each N
        fits = []
        for n in range(1, 20):
            lo, hi = 0.05, 2.0
            if math.isnan(L(n, hi, hi)) or L(n, lo, lo) < target:
                hi = lo  # no solution for this N
            for _ in range(60):
                if hi <= lo:
                    break
                mid = (lo + hi) / 2
                l = L(n, mid, mid)
                if math.isnan(l) or l < target:
                    hi = mid
                else:
                    lo = mid
            if hi > 0.05:
                wsol = round(lo, 2)
                ok = args.wmin <= wsol <= args.wmax
                print(f"  N={n:2d}  stripes {wsol:.2f} mm{'' if ok else '  (out of range)'}")
                if ok:
                    fits.append((n, wsol))
        if args.turns:
            fits = [f for f in fits if f[0] == args.turns]
        if not fits:
            raise SystemExit("no turn count fits the stripe range; widen --wmin/--wmax")
        n, w = max(fits)
        g = w

    l = L(n, w, g)
    r = resistance_dc(a0, b0, n, w, g, args.cu)
    f0 = f0_of(l)
    trim = 1 / (w0 * w0 * l) - c
    # the tag's input resistance, not the copper, sets the loaded Q
    x = 2 * math.pi * f0 * l
    rp = 1 / (1 / (args.rchip_kohm * 1e3) + 1 / ((x / r) ** 2 * r))
    print(f"\npicked N={n}, w={w} g={g}: L={l * 1e6:.2f} uH, Rdc={r:.2f} ohm, f0={f0 / 1e6:.2f} MHz")
    print(f"loaded Q ~ {rp / x:.1f}, trim cap to pull down to 13.56 MHz = {max(trim, 0) * 1e12:.1f} pF")

    if args.out:
        name = f"NFC_Coil_{a0:.0f}x{b0:.0f}_N{n}"
        args.out.mkdir(parents=True, exist_ok=True)
        path = args.out / f"{name}.kicad_mod"
        path.write_text(footprint(name, a0, b0, n, w, g, args.drill, l * 1e6, r))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
