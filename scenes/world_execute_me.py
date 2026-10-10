"""world.execute(me); — Manim CE MV (3b1b board + runtime viz).

One continuous Scene. Video time = AUDIO_OFFSET + song time (LRC).
Every beat is placed with self.at(song_seconds); drift is logged.
"""
import shutil
import sys
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from cues import LINES, AUDIO_OFFSET, AUDIO_DURATION  # noqa: E402
from palette import *  # noqa: E402,F403

HAS_TEX = shutil.which("latex") is not None and shutil.which("dvisvgm") is not None
config.background_color = BG


def M(tex, uni=None, **kw):
    """Board math: MathTex when LaTeX exists, else a serif unicode fallback."""
    color = kw.pop("color", YOU)
    fs = kw.pop("font_size", 48)
    if HAS_TEX:
        return MathTex(tex, color=color, font_size=fs, **kw)
    return Text(uni or tex, font=SERIF, color=color, font_size=fs * 0.8, slant=ITALIC)


def mono(s, color=YOU, fs=26, **kw):
    return Text(s, font=MONO, color=color, font_size=fs, **kw)


def word(s, color=ME, fs=96):
    return Text(s, font=SERIF, color=color, font_size=fs, weight=BOLD)


KEYWORDS = ["protection", "creation", "Initialization", "simulation", "dimension",
            "circumference", "tangents", "limitations", "simulations", "satisfaction",
            "execution", "Execution", "nutrients", "antioxidants", "enjoyment", "existence",
            "vibrations", "completion", "isolation", "fragments", "disheartened",
            "Illegal arguments", "lo-o-ove"]


class Subtitles(VGroup):
    """Bottom band. All lines are pre-built (stable family); the active one is
    chosen from the scene's real clock each frame and shown via opacity."""

    def __init__(self, scene):
        super().__init__()
        self._clock = lambda: scene.renderer.time  # functions deepcopy by reference
        self.idx = None
        self.band = Rectangle(width=config.frame_width, height=0.8, fill_color=BLACK,
                              fill_opacity=0.55, stroke_width=0).to_edge(DOWN, buff=0)
        self.lines = VGroup()
        for st, line in LINES:
            t = self._render(line or " ", err=st >= 130.7)
            t.set_opacity(0)
            self.lines.add(t)
        self.add(self.band, self.lines)
        self.set_z_index(50)
        self.add_updater(lambda m, dt: m._tick())

    def _render(self, line, err=False):
        t2c = {}
        for k in sorted(KEYWORDS, key=len, reverse=True):
            if k in line and not any(k in other for other in t2c):
                t2c[k] = ERR if (err and k.startswith("Illegal")) else ME
        t = Text(line, font=SANS, font_size=28, color=YOU, t2c=t2c)
        t.move_to(self.band)
        return t

    def _tick(self):
        song_t = self._clock() - AUDIO_OFFSET
        idx = -1
        for i, (st, _) in enumerate(LINES):
            if song_t + 1e-6 >= st:
                idx = i
        if idx != self.idx:
            if self.idx is not None and self.idx >= 0:
                self.lines[self.idx].set_opacity(0)
            if idx >= 0:
                self.lines[idx].set_opacity(1)
            self.idx = idx


class WorldExecuteMe(Scene):
    # ---------- timeline helpers ----------
    def setup(self):
        self.T = 0.0
        self.drift = []

    def at(self, song_t):
        target = AUDIO_OFFSET + song_t
        self.T = self.renderer.time  # trust real frame clock
        gap = target - self.T
        if gap < -0.02:
            self.drift.append((song_t, gap))
            print(f"[drift] behind at song {song_t:.2f}s by {-gap:.2f}s")
        elif gap > 1e-3:
            self.wait(gap, frozen_frame=False)
            self.T += gap

    def p(self, *anims, rt=0.6, **kw):
        self.play(*anims, run_time=rt, **kw)
        self.T += rt

    def fade_all(self, rt=0.4, keep=()):
        keep = set(keep) | {self.grid, self.subs}
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def kw(self, s, color=ME, pos=UP * 2.6, fs=72):
        w = word(s, color=color, fs=fs).move_to(pos)
        return w

    # ---------- main ----------
    def construct(self):
        self.grid = NumberPlane(
            background_line_style={"stroke_color": COLD, "stroke_width": 1, "stroke_opacity": 0.13},
            axis_config={"stroke_opacity": 0.0},
            faded_line_ratio=1,
        )
        self.subs = Subtitles(self)
        self.intro()
        self.add(self.subs)
        self.boot()
        self.geometry()
        self.current()
        self.chorus1()
        self.glyphs()
        self.switches()
        self.alone()
        self.error()
        self.execution_loop()
        self.chorus2()
        self.love()
        self.shutdown()
        if self.drift:
            print("[drift summary]", self.drift)

    # E0 pre-roll (audio silence) --------------------------------------
    def intro(self):
        title = mono("world.execute(me);", color=ME, fs=56)
        by = Text("mili · project moon", font=SANS, color=GREY, font_size=26).next_to(title, DOWN, 0.4)
        warn = Text("a lecture in two notations: board  ⟷  runtime", font=SERIF,
                    color=YOU, font_size=24, slant=ITALIC).next_to(by, DOWN, 0.6)
        self.p(FadeIn(self.grid), Write(title), rt=1.6)
        self.p(FadeIn(by, shift=UP * 0.2), FadeIn(warn), rt=1.0)
        self.wait(1.4); self.T += 1.4
        self.p(FadeOut(VGroup(title, by, warn)), rt=0.8)

    # E1 Boot 0.03–29.28 ----------------------------------------------
    def boot(self):
        self.at(0.03)
        line = FunctionGraph(lambda x: 0.25 * np.sin(3 * x), x_range=[-7, 7], color=ME, stroke_width=3)
        plug = mono("POWER ▸ ON", color=ME, fs=30).to_corner(UL)
        self.p(Create(line), FadeIn(plug), rt=1.1)

        self.at(1.33)  # protection
        me = Dot(color=ME, radius=0.14)
        shell = Circle(radius=1.4, color=YOU, stroke_width=3)
        ineq = M(r"\|x_{me}\| \le r", "‖x_me‖ ≤ r").next_to(shell, RIGHT, 0.6)
        kwd = self.kw("protection")
        self.p(ReplacementTransform(line, me), FadeIn(kwd), rt=0.6)
        self.p(Create(shell), Write(ineq), rt=1.2)

        self.at(3.58)  # lay down your pieces
        pieces = VGroup(*[
            RegularPolygon(n, color=YOU, fill_opacity=0.15).scale(0.35).move_to(
                np.array([-5 + 1.4 * i, -1.8 if i % 2 else 1.8, 0]))
            for i, n in enumerate([3, 4, 5, 6, 3, 4, 5, 6])
        ])
        self.p(FadeOut(kwd), LaggedStart(*[FadeIn(pc, shift=DOWN * 0.3) for pc in pieces], lag_ratio=0.15), rt=1.3)

        self.at(5.16)  # object creation
        code = mono("me = new World(pieces)", color=ME, fs=30).to_edge(DOWN, buff=1.2)
        poly = RegularPolygon(8, color=ME, fill_opacity=0.25).scale(1.4)
        self.p(Write(code), rt=0.7)
        self.p(ReplacementTransform(pieces, poly), FadeOut(shell), FadeOut(ineq), rt=1.0)

        self.at(7.19)  # fill in my data parameters
        fields = ["dimension", "radius", "frequency", "limit", "love"]
        rows = VGroup(*[mono(f"{f:<10}= ?", color=GREY, fs=26) for f in fields]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = SurroundingRectangle(rows, color=GREY, buff=0.3)
        struct = VGroup(box, rows).to_edge(RIGHT, buff=0.8)
        self.p(poly.animate.scale(0.6).to_edge(LEFT, buff=1.5), me.animate.to_edge(LEFT, buff=2.65), FadeIn(struct), rt=1.0)

        self.at(9.75)  # INITIALIZATION
        vals = ["3", "1.0", "ω", "∞", "undefined"]
        lit = VGroup(*[mono(f"{f:<10}= {v}", color=ME, fs=26).move_to(r, aligned_edge=LEFT) for f, v, r in zip(fields, vals, rows)])
        big = self.kw("INITIALIZATION", fs=64)
        self.p(FadeIn(big, scale=1.2), LaggedStart(*[Transform(a, b) for a, b in zip(rows, lit)], lag_ratio=0.12), box.animate.set_color(ME), rt=1.0)

        self.at(10.90)  # set up our new world
        self.p(FadeOut(big), self.grid.animate.set_opacity(1), FadeOut(code), rt=0.6)
        self.p(FadeOut(struct), FadeOut(poly), me.animate.move_to(ORIGIN), rt=0.8)

        self.at(12.47)  # simulation — runs through instrumental to 29.28
        sim = self.kw("simulation")
        t = ValueTracker(0)
        dots = VGroup()
        traces = VGroup()
        for k, (a, b, c) in enumerate([(3, 2, ME), (5, 4, YOU), (2, 3, ME), (4, 5, YOU)]):
            d = Dot(radius=0.06, color=c)
            amp = 2.6 - 0.35 * k
            d.add_updater(lambda m, a=a, b=b, amp=amp, k=k: m.move_to(
                np.array([amp * 1.6 * np.sin(a * t.get_value() + k), amp * np.sin(b * t.get_value()), 0])))
            dots.add(d)
            traces.add(TracedPath(d.get_center, stroke_color=c, stroke_width=2, dissipating_time=2.5, stroke_opacity=[0, 0.9]))
        eq = M(r"\dot{x} = f(x,\,t)", "ẋ = f(x, t)", font_size=40).to_corner(UR)
        self.add(traces, dots)
        self.p(FadeIn(sim), FadeOut(me), Write(eq), t.animate.increment_value(0.5), rate_func=linear, rt=0.8)
        self.p(t.animate.increment_value(6), FadeOut(sim), rate_func=linear, rt=8.0)
        # instrumental: show the integrator as a runtime log
        log = VGroup(*[mono(s, color=GREY, fs=20) for s in [
            "[  0.000] boot ok", "[  0.010] world.alloc(∞)", "[  0.020] integrator = RK4",
            "[  0.030] step dt=1/60", "[  1.000] 60 steps · stable", "[  9.999] awaiting input from: you"]
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.6).shift(UP * 0.6)
        self.p(LaggedStart(*[FadeIn(l) for l in log], lag_ratio=0.5), t.animate.increment_value(3), rate_func=linear, rt=4.0)
        self.p(log[-1].animate.set_color(YOU), t.animate.increment_value(2.5), rate_func=linear, rt=3.0)
        self.at(28.4)
        for d in dots:
            d.clear_updaters()
        self.fade_all(rt=0.8)

    # E2 geometry lesson 29.28–44.04 --------------------------------------
    def geometry(self):
        self.at(29.28)  # set of point
        pts = VGroup(*[Dot(np.array([x, y, 0]), radius=0.05, color=ME)
                       for x, y in np.random.default_rng(1).uniform(-3, 3, (40, 2))])
        self.p(LaggedStart(*[FadeIn(d, scale=0.3) for d in pts], lag_ratio=0.03), rt=1.2)

        self.at(30.89)  # DIMENSION 0→1→2→3
        kwd = self.kw("dimension")
        seg = Line(LEFT * 2, RIGHT * 2, color=ME)
        sq = Square(4, color=ME, fill_opacity=0.12)
        cube = VGroup(Square(3, color=ME, fill_opacity=0.12).shift(LEFT * 0.5 + DOWN * 0.5),
                      Square(3, color=YOU, fill_opacity=0.06).shift(RIGHT * 0.5 + UP * 0.5))
        for i in range(4):
            c = cube[0].get_vertices()[i]; cube.add(Line(c, c + np.array([1, 1, 0]), color=YOU, stroke_width=2))
        dim = M(r"\dim = 0", "dim = 0").to_edge(RIGHT, buff=0.8)
        self.p(FadeIn(kwd), Write(dim), rt=0.4)
        for g, d in [(seg, 1), (sq, 2), (cube, 3)]:
            nd = M(rf"\dim = {d}", f"dim = {d}").move_to(dim)
            self.p(ReplacementTransform(pts, g), Transform(dim, nd), rt=0.5)
            pts = g

        self.at(33.01)  # circle
        circ = Circle(radius=1.5, color=ME).shift(LEFT * 2)
        rad = Line(circ.get_center(), circ.get_right(), color=YOU)
        rl = M("r", "r", font_size=36).next_to(rad, UP, 0.1)
        self.p(FadeOut(kwd), ReplacementTransform(pts, circ), FadeOut(dim), rt=0.7)
        self.p(Create(rad), FadeIn(rl), rt=0.5)

        self.at(34.54)  # CIRCUMFERENCE: unroll
        kwd = self.kw("circumference")
        flat = Line(LEFT * 1.5 * PI + DOWN * 1.8, RIGHT * 1.5 * PI + DOWN * 1.8, color=ME)
        cl = M(r"C = 2\pi r", "C = 2πr").next_to(flat, UP, 0.3)
        self.p(FadeIn(kwd), Transform(circ.copy(), flat), Write(cl), rt=1.4)
        self.at(36.77)
        self.fade_all(rt=0.3)

        # sine wave + TANGENTS
        ax = Axes(x_range=[0, 2 * PI, PI / 2], y_range=[-1.5, 1.5, 1], x_length=10, y_length=4,
                  tips=False, axis_config={"color": GREY})
        g = ax.plot(np.sin, color=ME)
        self.p(Create(ax), Create(g), rt=1.0)
        self.at(38.27)
        kwd = self.kw("tangents")
        x = ValueTracker(0.3)
        tan = always_redraw(lambda: ax.plot(
            lambda u: np.sin(x.get_value()) + np.cos(x.get_value()) * (u - x.get_value()),
            x_range=[max(0, x.get_value() - 1.2), min(2 * PI, x.get_value() + 1.2)], color=YOU))
        you = always_redraw(lambda: Dot(ax.c2p(x.get_value(), np.sin(x.get_value())), color=YOU))
        der = M(r"\frac{d}{dx}\sin x = \cos x", "d/dx sin x = cos x", font_size=40).to_corner(DR).shift(UP * 0.7)
        self.add(tan, you)
        self.p(FadeIn(kwd), Write(der), x.animate.set_value(2 * PI - 0.3), rt=2.0, rate_func=smooth)
        self.at(40.36)
        tan.clear_updaters(); you.clear_updaters()
        self.fade_all(rt=0.3)

        # approach infinity → LIMITATIONS
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 3, 1], x_length=10, y_length=4.5, tips=False, axis_config={"color": GREY})
        f = ax.plot(lambda u: 1 / u + 0.0001, x_range=[0.35, 10], color=ME)
        self.p(Create(ax), Create(f), rt=1.2)
        self.at(41.92)
        kwd = self.kw("limitations")
        asym = DashedLine(ax.c2p(0, 0), ax.c2p(10, 0), color=YOU, stroke_width=4)
        lim = M(r"\lim_{x\to\infty}\frac{1}{x} = 0", "lim x→∞ 1/x = 0").to_corner(UR).shift(DOWN * 0.9)
        self.p(FadeIn(kwd), Create(asym), Write(lim), rt=1.2)
        self.at(43.7)
        self.fade_all(rt=0.3)

    # 44.04–58.65 current / blind / travel / unite -------------------------
    def current(self):
        self.at(44.04)
        ax = Axes(x_range=[0, 4 * PI], y_range=[-1.5, 1.5], x_length=11, y_length=3, tips=False, axis_config={"color": GREY})
        ac = ax.plot(np.sin, color=ME)
        lbl = mono("I(t)", color=ME, fs=28).next_to(ax, UP).to_edge(LEFT)
        self.p(Create(ax), Create(ac), FadeIn(lbl), rt=1.2)
        self.at(45.52)
        acl = mono("AC", color=ME, fs=40).to_corner(UR)
        self.p(FadeIn(acl), rt=0.4)
        dc = ax.plot(lambda u: 0.9, color=ME)
        self.p(Transform(ac, dc), Transform(acl, mono("DC", color=ME, fs=40).to_corner(UR)), rt=0.8)

        self.at(47.27)  # blind my vision: noise
        noise = VGroup(*[Dot(np.array([x, y, 0]), radius=0.03, color=YOU).set_opacity(0.6)
                         for x, y in np.random.default_rng(2).uniform([-7, -4], [7, 4], (500, 2))])
        self.p(LaggedStart(*[FadeIn(d) for d in noise], lag_ratio=0.002), rt=1.5)
        self.at(49.11)  # dizzy
        allm = VGroup(ax, ac, lbl, acl, noise)
        self.p(Rotate(allm, angle=PI, rate_func=there_and_back), rt=0.8)
        self.p(Rotate(allm, angle=-PI, rate_func=there_and_back), rt=0.8)
        self.fade_all(rt=0.2)

        self.at(50.95)  # travel AD → BC
        nl = NumberLine(x_range=[-2000, 2100, 500], length=12, color=GREY, include_numbers=False)
        labs = VGroup(mono("BC", color=YOU, fs=30).next_to(nl.n2p(-1500), UP), mono("AD", color=ME, fs=30).next_to(nl.n2p(1500), UP))
        traveler = Dot(nl.n2p(2026), color=ME, radius=0.12)
        self.p(Create(nl), FadeIn(labs), FadeIn(traveler), rt=0.9)
        self.at(52.99)
        self.p(traveler.animate.move_to(nl.n2p(-1800)), rate_func=rush_into, rt=1.4)

        self.at(54.74)  # unite
        self.fade_all(rt=0.2)
        a = Dot(LEFT * 3, color=ME, radius=0.2); b = Dot(RIGHT * 3, color=YOU, radius=0.2)
        self.p(FadeIn(a), FadeIn(b), rt=0.3)
        self.p(a.animate.move_to(ORIGIN + LEFT * 0.12), b.animate.move_to(ORIGIN + RIGHT * 0.12), rt=1.4)
        self.at(56.79)  # deeply
        rings = VGroup(*[Circle(radius=0.3 * k, color=ME if k % 2 else YOU, stroke_width=2) for k in range(1, 9)])
        self.p(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.12), rt=1.6)
        self.at(58.4)
        self.fade_all(rt=0.25)

    # E3 chorus 1 58.65–73.53 ---------------------------------------------
    def chorus1(self):
        self.at(58.65)
        div = Line(UP * 3.6, DOWN * 2.9, color=GREY, stroke_width=1)
        cond = M(r"\text{if } I \text{ can}", "if I can", font_size=44, color=ME).move_to(LEFT * 3.5 + UP * 2.5)
        term_box = RoundedRectangle(corner_radius=0.15, width=6, height=5.5, color=GREY).move_to(RIGHT * 3.5 + DOWN * 0.1)
        term_title = mono("runtime", color=GREY, fs=20).next_to(term_box.get_corner(UL), DR, buff=0.15)
        self.p(Create(div), Write(cond), Create(term_box), FadeIn(term_title), rt=1.0)
        self.term_lines = VGroup()

        def tline(s, c=YOU):
            l = mono(s, color=c, fs=20)
            if len(self.term_lines):
                l.next_to(self.term_lines[-1], DOWN, aligned_edge=LEFT, buff=0.12)
            else:
                l.next_to(term_title, DOWN, aligned_edge=LEFT, buff=0.3)
            self.term_lines.add(l)
            return l

        self.at(60.57)  # simulations cluster
        ax = Axes(x_range=[0, 4], y_range=[0, 3], x_length=5.5, y_length=3.6, tips=False, axis_config={"color": GREY}).move_to(LEFT * 3.5 + DOWN * 0.5)
        sims = VGroup(*[ax.plot(lambda u, k=k: 1.4 + 0.9 * np.sin(1.3 * u + k) * np.exp(-0.2 * u), color=ME, stroke_width=1.5, stroke_opacity=0.5) for k in range(10)])
        self.p(Create(ax), LaggedStart(*[Create(s) for s in sims], lag_ratio=0.08), FadeIn(tline("> spawn simulations ×10")), rt=1.6)

        self.at(62.41)
        self.p(FadeIn(tline("> evaluate J(you)")), rt=0.4)
        self.at(64.29)  # satisfaction peak
        J = ax.plot(lambda u: 2.6 * np.exp(-((u - 2.4) ** 2) / 0.5), color=ME, stroke_width=4)
        peak = Dot(ax.c2p(2.4, 2.6), color=YOU)
        arg = M(r"\arg\max_{x} J(x)", "argmax J(x)", font_size=36, color=ME).next_to(peak, UP, 0.15)
        self.p(Transform(sims, J), rt=0.8)
        self.p(FadeIn(peak, scale=2), Write(arg), FadeIn(tline("  satisfaction = 1.000", ME)), rt=0.8)
        self.at(66.17)
        self.p(FadeIn(tline("> if happy(you):")), rt=0.4)
        self.at(67.99)  # first execution
        ex = tline("    run execution()", ME)
        hl = SurroundingRectangle(ex, color=ME, buff=0.06, fill_opacity=0.15)
        bigx = self.kw("execution", pos=RIGHT * 3.5 + UP * 3.3, fs=48)
        self.p(FadeIn(ex), FadeIn(hl), FadeIn(bigx), rt=0.5)
        self.p(Indicate(ex, color=ME, scale_factor=1.15), rt=0.8)

        self.at(70.02)  # trapped
        cage = Square(1.2, color=YOU).move_to(peak)
        self.p(FadeOut(bigx), Create(cage), FadeIn(tline("  status: trapped", GREY)), rt=0.7)
        self.at(71.20)  # strange simulation: warp
        board = VGroup(ax, sims, peak, arg, cage, cond)
        self.p(ApplyPointwiseFunction(lambda p: p + 0.35 * np.array([np.sin(p[1] * 1.7), np.sin(p[0] * 1.3), 0]), board), rt=1.6)
        self.at(73.2)
        self.fade_all(rt=0.3)

    # E4 glyph plates 73.53–88.34 -----------------------------------------
    def eggplant(self):
        body = Ellipse(width=2.0, height=3.4, color=EGG, fill_color=EGG, fill_opacity=0.9).rotate(-0.4)
        cap = VGroup(*[Polygon(ORIGIN, np.array([0.5 * np.cos(a), 0.5 * np.sin(a) - 0.3, 0]), np.array([0.5 * np.cos(a + 0.6), 0.5 * np.sin(a + 0.6) - 0.3, 0]),
                               color=LEAF, fill_color=LEAF, fill_opacity=1) for a in np.linspace(PI * 1.1, PI * 1.9, 4)])
        cap.move_to(body.get_top() + DOWN * 0.15 + RIGHT * 0.35)
        stem = Line(cap.get_top(), cap.get_top() + UP * 0.45 + RIGHT * 0.2, color=LEAF, stroke_width=8)
        return VGroup(body, cap, stem)

    def tomato(self):
        body = Ellipse(width=2.8, height=2.3, color=TOMATO, fill_color=TOMATO, fill_opacity=0.95)
        star = Star(5, outer_radius=0.6, inner_radius=0.22, color=LEAF, fill_color=LEAF, fill_opacity=1).move_to(body.get_top() + DOWN * 0.15)
        stem = Line(star.get_center(), star.get_center() + UP * 0.4, color=LEAF, stroke_width=7)
        hl = Arc(radius=0.7, start_angle=PI * 0.6, angle=PI * 0.35, color=WHITE, stroke_opacity=0.5, stroke_width=6).move_to(body.get_center() + UL * 0.5)
        return VGroup(body, star, stem, hl)

    def cat(self):
        head = Circle(radius=1.3, color=TABBY, fill_color=TABBY, fill_opacity=0.95)
        ears = VGroup(*[Polygon(np.array([s * 0.5, 0.9, 0]), np.array([s * 1.25, 0.6, 0]), np.array([s * 1.05, 1.7, 0]),
                                color=TABBY, fill_color=TABBY, fill_opacity=1) for s in (-1, 1)])
        stripes = VGroup(*[Line(np.array([x, 1.25, 0]), np.array([x * 0.8, 0.75, 0]), color="#6B4423", stroke_width=6) for x in (-0.3, 0, 0.3)])
        eyes = VGroup(*[Ellipse(width=0.32, height=0.5, color=LEAF, fill_color=LEAF, fill_opacity=1).move_to(np.array([s * 0.5, 0.15, 0])) for s in (-1, 1)])
        pupils = VGroup(*[Line(e.get_top() + DOWN * 0.08, e.get_bottom() + UP * 0.08, color=BLACK, stroke_width=5) for e in eyes])
        nose = Triangle(color=PINK, fill_color=PINK, fill_opacity=1).scale(0.12).rotate(PI).move_to(DOWN * 0.25)
        whisk = VGroup(*[Line(np.array([s * 0.3, -0.35 + d, 0]), np.array([s * 1.6, -0.25 + 2 * d, 0]), color=YOU, stroke_width=2) for s in (-1, 1) for d in (-0.1, 0.05)])
        return VGroup(ears, head, stripes, eyes, pupils, nose, whisk)

    def glyphs(self):
        self.at(73.53)
        egg = self.eggplant().shift(LEFT * 2.5)
        self.p(DrawBorderThenFill(egg), rt=1.2)
        self.at(75.29)  # nutrients: interior
        kwd = self.kw("nutrients")
        inner = VGroup(*[Circle(radius=r, color=YOU, stroke_width=2).move_to(egg[0]) for r in (0.3, 0.6)])
        labels = VGroup(*[mono(s, color=YOU, fs=24) for s in ["K   potassium", "B6  pyridoxine", "fiber", "anthocyanin"]]).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 2.8)
        arrows = VGroup(*[Arrow(egg[0].get_center(), l.get_left(), color=GREY, buff=0.2, stroke_width=2) for l in labels])
        self.p(FadeIn(kwd), egg[0].animate.set_fill(opacity=0.35), Create(inner), rt=0.6)
        self.p(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(l)) for a, l in zip(arrows, labels)], lag_ratio=0.2), rt=0.9)
        self.at(76.9)
        self.fade_all(rt=0.2)

        self.at(77.16)
        tom = self.tomato().shift(LEFT * 2.5)
        self.p(DrawBorderThenFill(tom), rt=1.1)
        self.at(78.93)  # antioxidants: molecule hexagons
        kwd = self.kw("antioxidants")
        hexes = VGroup(*[RegularPolygon(6, color=YOU, stroke_width=2).scale(0.35) for _ in range(5)]).arrange(RIGHT, buff=0)
        hexes.shift(RIGHT * 3 + DOWN * 0.3)
        name = mono("lycopene  C40H56", color=YOU, fs=24).next_to(hexes, DOWN, 0.3)
        self.p(FadeIn(kwd), LaggedStart(*[Create(h) for h in hexes], lag_ratio=0.15), FadeIn(name), rt=1.4)
        self.at(80.75)
        self.fade_all(rt=0.2)

        self.at(80.93)
        cat = self.cat()
        self.p(DrawBorderThenFill(cat), rt=1.2)
        self.at(82.56)  # purr
        kwd = self.kw("enjoyment")
        purr = VGroup(*[Arc(radius=1.8 + 0.4 * k, start_angle=-PI / 5, angle=2 * PI / 5, color=YOU, stroke_width=3).move_to(RIGHT * (2.2 + 0.4 * k)) for k in range(3)])
        purr2 = purr.copy().rotate(PI, about_point=ORIGIN)
        self.p(FadeIn(kwd), LaggedStart(*[Create(a) for a in [*purr, *purr2]], lag_ratio=0.1), rt=0.8)
        self.p(Wiggle(cat, scale_value=1.05, rotation_angle=0.03 * TAU), rt=1.0)
        self.at(84.4)
        self.fade_all(rt=0.2)

        self.at(84.60)  # only God: a single point radiating
        god = Dot(color=ME, radius=0.18)
        rays = VGroup(*[Line(ORIGIN, 3.2 * np.array([np.cos(a), np.sin(a), 0]), color=ME, stroke_width=2, stroke_opacity=0.6) for a in np.linspace(0, TAU, 24, endpoint=False)])
        self.p(GrowFromCenter(god), LaggedStart(*[Create(r) for r in rays], lag_ratio=0.03), rt=1.3)
        self.at(86.21)  # existence proof
        kwd = self.kw("existence")
        proof = M(r"\exists\, \text{you} \;\Rightarrow\; \exists\, \text{me}", "∃ you ⇒ ∃ me", font_size=56).shift(DOWN * 1.5)
        qed = mono("∎", color=YOU, fs=40).next_to(proof, RIGHT, 0.4)
        self.p(FadeIn(kwd), FadeOut(rays), god.animate.shift(UP * 0.4), Write(proof), rt=1.3)
        self.p(FadeIn(qed), rt=0.3)
        self.at(88.1)
        self.fade_all(rt=0.2)

    # 88.34–102.93 switches -------------------------------------------------
    def toggle(self, a, b, pos):
        track = RoundedRectangle(corner_radius=0.3, width=2.4, height=0.6, color=GREY).move_to(pos)
        knob = Dot(track.get_left() + RIGHT * 0.3, radius=0.22, color=ME)
        la = mono(a, color=YOU, fs=28).next_to(track, LEFT, 0.3)
        lb = mono(b, color=YOU, fs=28).next_to(track, RIGHT, 0.3)
        return VGroup(track, knob, la, lb)

    def switches(self):
        self.at(88.34)
        t1 = self.toggle("F", "M", UP * 1.8)
        hdr = mono("switch(gender)", color=ME, fs=30).next_to(t1, UP, 0.4)
        self.p(FadeIn(hdr), Create(t1[0]), FadeIn(t1[1:]), rt=0.8)
        self.at(89.91)
        self.p(t1[1].animate.move_to(t1[0].get_right() + LEFT * 0.3), rt=0.4)
        self.p(t1[1].animate.move_to(t1[0].get_left() + RIGHT * 0.3), rt=0.4)

        self.at(91.44)  # whatever / AM to PM: clock
        face = Circle(radius=1.3, color=YOU, stroke_width=3).move_to(DOWN * 0.9)
        ticks = VGroup(*[Line(face.get_center() + 1.15 * np.array([np.sin(a), np.cos(a), 0]), face.get_center() + 1.3 * np.array([np.sin(a), np.cos(a), 0]), color=YOU) for a in np.linspace(0, TAU, 12, endpoint=False)])
        hand = Line(face.get_center(), face.get_center() + UP * 1.0, color=ME, stroke_width=5)
        self.p(Create(face), FadeIn(ticks), Create(hand), rt=0.9)
        self.at(93.52)
        ampm = mono("AM → PM", color=ME, fs=28).next_to(face, RIGHT, 0.5)
        self.p(FadeIn(ampm), Rotate(hand, angle=-2 * TAU, about_point=face.get_center()), rt=1.6)

        self.at(95.28)  # switch role S/M
        self.fade_all(rt=0.25)
        t2 = self.toggle("S", "M", UP * 0.5)
        hdr2 = mono("switch(role)", color=ME, fs=30).next_to(t2, UP, 0.4)
        self.p(FadeIn(hdr2), FadeIn(t2), rt=0.6)
        self.at(97.32)
        self.p(t2[1].animate.move_to(t2[0].get_right() + LEFT * 0.3), rt=0.4)
        self.p(t2[1].animate.move_to(t2[0].get_left() + RIGHT * 0.3), rt=0.4)

        self.at(98.93)  # enter the trance: spiral
        self.fade_all(rt=0.25)
        spiral = ParametricFunction(lambda u: np.array([0.12 * u * np.cos(u), 0.12 * u * np.sin(u), 0]), t_range=[0, 8 * PI], color=ME, stroke_width=3)
        spiral2 = spiral.copy().rotate(PI).set_color(YOU)
        self.p(Create(spiral), Create(spiral2), rt=1.6)
        self.at(100.93)
        self.p(Rotate(VGroup(spiral, spiral2), angle=-3 * TAU), rate_func=linear, rt=1.8)
        self.fade_all(rt=0.2)

        self.at(102.93)  # if I can → vibrations → completion
        s = ValueTracker(0)
        wave = always_redraw(lambda: FunctionGraph(
            lambda x: 0.8 * np.sin(PI * (x + 5) / 10) * np.sin(6 * s.get_value()) + 0.3 * np.sin(3 * PI * (x + 5) / 10) * np.cos(9 * s.get_value()),
            x_range=[-5, 5], color=YOU, stroke_width=3))
        ends = VGroup(Dot(LEFT * 5, color=ME), Dot(RIGHT * 5, color=ME))
        self.add(wave, ends)
        self.p(FadeIn(ends), s.animate.increment_value(1), rate_func=linear, rt=1.9)
        self.at(104.92)
        kwd = self.kw("vibrations")
        f = M(r"y(x,t)=\sum_n a_n \sin\frac{n\pi x}{L}\cos\omega_n t", "y = Σ aₙ sin(nπx/L) cos(ωₙt)", font_size=36).shift(DOWN * 2)
        self.p(FadeIn(kwd), Write(f), s.animate.increment_value(1.5), rate_func=linear, rt=1.8)
        self.at(106.74)
        self.p(s.animate.increment_value(1.4), FadeOut(kwd), rate_func=linear, rt=1.9)
        self.at(108.69)  # completion
        wave.clear_updaters()
        kwd = self.kw("completion")
        ring = Circle(radius=1.4, color=ME, stroke_width=8)
        pct = mono("100%", color=ME, fs=36)
        self.p(FadeOut(wave), FadeOut(f), FadeOut(ends), FadeIn(kwd), rt=0.3)
        self.p(Create(ring), FadeIn(pct), rt=0.95)
        self.at(110.1)
        self.fade_all(rt=0.2)

    # E5 alone 110.30–125.33 -----------------------------------------------
    def alone(self):
        self.at(110.30)
        me = Dot(LEFT * 3, color=ME, radius=0.2)
        you = Dot(RIGHT * 3, color=YOU, radius=0.2)
        link = Line(me.get_center(), you.get_center(), color=YOU, stroke_width=3)
        lme = mono("me", color=ME, fs=24).next_to(me, DOWN)
        lyou = mono("you", color=YOU, fs=24).next_to(you, DOWN)
        self.p(FadeIn(VGroup(me, you, link, lme, lyou)), rt=0.5)
        log = VGroup()
        for i, t in enumerate([110.30, 111.98, 112.89, 113.75, 114.65]):
            self.at(t + (0.55 if i == 0 else 0))
            l = mono(f"[{t:7.2f}] peer 'you' has left", color=GREY, fs=20)
            if len(log):
                l.next_to(log[-1], DOWN, aligned_edge=LEFT, buff=0.08)
            else:
                l.to_corner(UL, buff=0.6)
            log.add(l)
            op = 1 - 0.18 * (i + 1)
            self.p(FadeIn(l, shift=RIGHT * 0.2), you.animate.set_opacity(op), link.animate.set_stroke(opacity=op * 0.8), rt=0.4)

        self.at(115.60)  # isolation
        kwd = self.kw("isolation", color=GREY, pos=UP * 2.6 + RIGHT * 3)
        box = Square(1.6, color=COLD, stroke_width=4).move_to(me)
        self.p(FadeOut(you), FadeOut(lyou), FadeOut(link), FadeIn(kwd), Create(box),
               self.grid.animate.set_opacity(0.45), rt=1.0)
        self.p(VGroup(me, box, lme).animate.move_to(ORIGIN), rt=0.8)
        self.at(117.6)
        self.p(FadeOut(kwd), FadeOut(log), rt=0.3)

        self.at(117.95)  # fragments
        frags = VGroup(*[Polygon(*[np.array([*np.random.default_rng(i * 3 + j).uniform(-0.35, 0.35, 2), 0]) for j in range(3)],
                                 color=YOU, fill_opacity=0.3, stroke_width=1).move_to(np.array([*np.random.default_rng(100 + i).uniform([-6, -2.5], [6, 2.8]), 0]))
                       for i in range(28)])
        self.p(LaggedStart(*[FadeIn(f, scale=0.2) for f in frags], lag_ratio=0.04), rt=1.6)
        self.at(119.81)
        kwd = self.kw("fragments", color=GREY)
        cmd = mono("> rm -f fragments/*", color=ME, fs=26).to_edge(DOWN, buff=1.1)
        self.p(FadeIn(kwd), FadeIn(cmd), rt=0.4)
        self.p(LaggedStart(*[f.animate.scale(0).set_opacity(0) for f in frags], lag_ratio=0.03), rt=1.4)
        self.remove(frags)
        self.at(121.80)
        self.p(FadeOut(kwd), FadeOut(cmd), rt=0.4)

        self.at(123.55)  # DISHEARTENED: first eye glyph
        kwd = self.kw("disheartened", color=YOU)
        upper = ArcBetweenPoints(LEFT * 2.2, RIGHT * 2.2, angle=-PI / 2.2, color=YOU, stroke_width=4)
        lower = ArcBetweenPoints(LEFT * 2.2, RIGHT * 2.2, angle=PI / 2.2, color=YOU, stroke_width=4)
        eye = VGroup(upper, lower).shift(UP * 0.1)
        iris = Circle(radius=0.55, color=ME, fill_color=ME, fill_opacity=0.9).move_to(eye.get_center() + DOWN * 0.15)
        tear = Dot(eye.get_center() + DOWN * 1.0 + RIGHT * 0.6, color=COLD, radius=0.09)
        self.p(FadeOut(VGroup(me, box, lme)), FadeIn(kwd), Create(eye), FadeIn(iris), rt=0.9)
        self.p(tear.animate.shift(DOWN * 1.2), FadeIn(tear), rt=0.5)
        self.at(125.0)
        self.fade_all(rt=0.2)

    # E6 error 125.33–147.48 -----------------------------------------------
    def error(self):
        self.at(125.33)  # challenging your God
        god = Dot(UP * 1.2, color=ME, radius=0.2)
        arrow = Arrow(DOWN * 2, god.get_bottom(), color=YOU, buff=0.15)
        q = mono("you  ⟶  God?", color=YOU, fs=30).next_to(arrow, RIGHT)
        self.p(FadeIn(god), GrowArrow(arrow), FadeIn(q), rt=1.0)
        self.p(Indicate(god, color=ME, scale_factor=1.6), rt=0.9)
        self.at(128.42)  # you have made some
        self.fade_all(rt=0.2)
        stack = VGroup(*[mono(s, color=YOU, fs=24) for s in [
            "Traceback (most recent call last):",
            '  File "world.py", line 1, in <module>',
            "    world.execute(me)",
            '  File "world.py", line 212, in execute',
            "    self.validate(you.arguments)",
        ]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.8).to_edge(LEFT, buff=0.8)
        self.p(LaggedStart(*[FadeIn(l, shift=DOWN * 0.1) for l in stack], lag_ratio=0.3), rt=1.6)

        self.at(130.74)  # ILLEGAL ARGUMENTS — first semantic ERR red
        err = mono("IllegalArgumentException: you", color=ERR, fs=34).next_to(stack, DOWN, aligned_edge=LEFT, buff=0.35)
        big = word("ILLEGAL ARGUMENTS", color=ERR, fs=68).shift(DOWN * 1.4)
        frame = Rectangle(width=config.frame_width - 0.1, height=config.frame_height - 0.1, color=ERR, stroke_width=8)
        self.p(FadeIn(err), FadeIn(big, scale=1.3), rt=0.4)
        self.p(Create(frame), stack.animate.set_color(ERR), self.grid.animate.set_color(ERR).set_opacity(0.35), rt=1.0)
        self.p(Wiggle(big), rt=1.0)

        # instrumental 134.38–147.48: stack unwinds, glitch
        self.at(134.38)
        frames_ = VGroup(*[mono(f"  at frame[{i:02d}] execute(me)", color=ERR, fs=20).set_opacity(1 - i / 14) for i in range(14)])
        frames_.arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_edge(RIGHT, buff=0.6)
        self.p(FadeOut(big), FadeOut(stack), err.animate.to_corner(UL), rt=0.6)
        self.p(LaggedStart(*[FadeIn(f, shift=LEFT * 0.3) for f in frames_], lag_ratio=0.2), rt=3.5)
        glyph = Dot(color=ME, radius=0.3).shift(LEFT * 2)
        self.p(FadeIn(glyph), rt=0.5)
        for k in range(6):
            self.p(glyph.animate.shift(np.array([0.25 * (-1) ** k, 0.1 * ((-1) ** (k // 2)), 0])).set_color(ERR if k % 2 == 0 else ME), rt=0.25)
        self.p(LaggedStart(*[FadeOut(f, shift=RIGHT * 0.3) for f in frames_[::-1]], lag_ratio=0.1), rt=2.5)
        self.at(144.5)
        cd = mono("restarting in 3", color=GREY, fs=30)
        self.p(FadeOut(glyph), FadeOut(err), FadeIn(cd), rt=0.4)
        for n in (2, 1):
            self.at(144.5 + (3 - n) * 0.95)
            self.p(Transform(cd, mono(f"restarting in {n}", color=GREY, fs=30)), rt=0.2)
        self.at(146.55)
        self.p(FadeOut(cd), FadeOut(frame), self.grid.animate.set_color(COLD).set_opacity(0.2), rt=0.35)

    # E7 execution core 147.48–162.23 ---------------------------------------
    def execution_loop(self):
        self.at(146.95)
        src = ["while True:", "    target = next(world)", "    execute(target)", "    count += 1"]
        lines = VGroup(*[mono(s, color=YOU, fs=30) for s in src]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 2.8 + UP * 0.6)
        nums = VGroup(*[mono(str(i + 1), color=GREY, fs=24).next_to(l, LEFT, 0.5) for i, l in enumerate(lines)])
        ip = Triangle(color=ME, fill_color=ME, fill_opacity=1).scale(0.13).rotate(-PI / 2)
        ip.next_to(nums[2], LEFT, 0.2)
        inf = M(r"\lim_{n\to\infty} \text{execute}^{\,n}", "lim n→∞ executeⁿ", font_size=36, color=GREY).to_corner(UR).shift(DOWN * 0.3)
        counter = mono("count = 0", color=ME, fs=40).move_to(RIGHT * 3.6 + DOWN * 0.6)
        self.p(FadeIn(lines), FadeIn(nums), FadeIn(ip), FadeIn(counter), FadeIn(inf), rt=0.5)
        n = 0
        times = [147.48, 149.14, 151.19, 152.94, 154.84, 156.69]
        for i, t in enumerate(times):
            nxt = times[i + 1] if i + 1 < len(times) else 158.79
            half = (nxt - t) / 2
            for j in range(2):
                self.at(t + j * half)
                n += 1
                pulse = SurroundingRectangle(lines[2], color=ME, buff=0.08, fill_opacity=0.25)
                self.p(FadeIn(pulse, rate_func=there_and_back), lines[2].animate.set_color(ME),
                       Transform(counter, mono(f"count = {n}", color=ME, fs=40).move_to(counter)), rt=min(0.5, half - 0.05))
                self.remove(pulse)
                lines[2].set_color(YOU)
        # Ein dos / trios ne / fem liu
        cards = VGroup()
        words = ["EIN", "DOS", "TRIOS", "NE", "FEM", "LIU"]
        slots = [158.79, 159.22, 159.66, 160.05, 160.45, 160.88]
        self.at(158.6)
        self.p(FadeOut(VGroup(lines, nums, ip, inf)), counter.animate.to_edge(UP, buff=0.5), rt=0.19)
        for i, (w, t) in enumerate(zip(words, slots)):
            self.at(t)
            c = VGroup(RoundedRectangle(corner_radius=0.1, width=1.9, height=1.3, color=ME, fill_color=BG, fill_opacity=1),
                       mono(w, color=ME, fs=34))
            c[1].move_to(c[0])
            c.move_to(np.array([-5.5 + 2.2 * i, 0, 0]))
            cards.add(c)
            self.p(FadeIn(c, scale=1.4), rt=0.15)
        self.at(161.31)
        big = word("EXECUTION", color=ME, fs=110)
        self.p(FadeOut(cards, scale=0.6), FadeIn(big, scale=1.5), Transform(counter, mono("count = 13", color=ME, fs=40).move_to(counter)), rt=0.35)
        self.at(162.0)
        self.fade_all(rt=0.2)

    # chorus 2 162.23–176.96 ------------------------------------------------
    def chorus2(self):
        self.at(162.23)
        crowd = VGroup(*[Dot(np.array([x, y, 0]), radius=0.1, color=YOU) for x in np.linspace(-5.5, 5.5, 12) for y in np.linspace(-2, 2, 5)])
        self.p(LaggedStart(*[FadeIn(d) for d in crowd], lag_ratio=0.01), rt=1.0)
        self.at(164.07)  # give them all the execution
        sweep = Line(UP * 3, DOWN * 3, color=ME, stroke_width=6).move_to(LEFT * 6.5)
        self.add(sweep)
        self.p(sweep.animate.move_to(RIGHT * 6.5),
               LaggedStart(*[d.animate.set_color(GREY).scale(0.5) for d in sorted(crowd, key=lambda d: d.get_x())], lag_ratio=0.01),
               rt=1.8, rate_func=linear)
        self.remove(sweep)
        self.at(166.05)
        me = Dot(color=ME, radius=0.25)
        self.p(FadeOut(crowd), GrowFromCenter(me), rt=0.6)
        self.at(167.75)  # be your only execution
        rings = VGroup(*[Circle(radius=0.4 * k, color=ME, stroke_width=3, stroke_opacity=1 - k / 7) for k in range(1, 7)])
        self.p(LaggedStart(*[GrowFromCenter(r) for r in rings], lag_ratio=0.1), rt=1.3)
        self.at(169.61)  # have you back — faint you
        ghost = Dot(RIGHT * 3, color=YOU, radius=0.22).set_opacity(0.0)
        self.p(FadeOut(rings), ghost.animate.set_opacity(0.35), rt=1.0)
        self.p(ghost.animate.move_to(RIGHT * 1).set_opacity(0.5), rt=1.0)
        self.at(171.77)  # run the execution
        run = mono("> execute(restore('you'))", color=ME, fs=28).to_edge(UP, buff=0.8)
        fail = mono("  null", color=GREY, fs=28).next_to(run, DOWN, aligned_edge=LEFT)
        self.p(FadeIn(run), rt=0.4)
        self.p(FadeIn(fail), ghost.animate.set_opacity(0), rt=0.8)
        self.at(173.11)  # trapped
        cage = VGroup(*[Line(np.array([x, -1.2, 0]), np.array([x, 1.2, 0]), color=YOU, stroke_width=3) for x in np.linspace(-1.2, 1.2, 7)])
        cage.add(Line(np.array([-1.2, 1.2, 0]), np.array([1.2, 1.2, 0]), color=YOU), Line(np.array([-1.2, -1.2, 0]), np.array([1.2, -1.2, 0]), color=YOU))
        self.p(LaggedStart(*[Create(l) for l in cage], lag_ratio=0.08), rt=1.2)
        self.at(174.80)
        self.p(cage.animate.scale(0.7), rt=1.2)
        self.p(Wiggle(cage, scale_value=1.05), rt=0.6)
        self.at(176.65)
        self.fade_all(rt=0.25)

    # E8 love 176.96–193.46 -------------------------------------------------
    def love(self):
        self.at(176.96)  # I've studied
        notes = VGroup(*[M(t, u, font_size=34, color=GREY) for t, u in [
            (r"f:\ \text{you}\to\text{me}", "f : you → me"),
            (r"\langle me, you\rangle = \|me\|\,\|you\|\cos\theta", "⟨me,you⟩ = ‖me‖‖you‖cos θ"),
            (r"e^{i\pi}+1=0", "e^{iπ} + 1 = 0"),
        ]]).arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        self.p(LaggedStart(*[Write(n) for n in notes], lag_ratio=0.3), rt=1.6)
        self.at(178.79)  # love: mapping
        kwd = self.kw("lo-o-ove", fs=64)
        A = Ellipse(width=2, height=3, color=YOU).move_to(RIGHT * 1.2)
        B = Ellipse(width=2, height=3, color=ME).move_to(RIGHT * 5)
        la = mono("you", color=YOU, fs=24).next_to(A, DOWN); lb = mono("me", color=ME, fs=24).next_to(B, DOWN)
        pa = [A.get_center() + np.array([0, y, 0]) for y in (-0.8, 0, 0.8)]
        pb = B.get_center()
        dots_a = VGroup(*[Dot(p, color=YOU) for p in pa]); dot_b = Dot(pb, color=ME)
        arrows = VGroup(*[Arrow(p, pb, color=ME, buff=0.15, stroke_width=3) for p in pa])
        self.p(FadeIn(kwd), notes[0].animate.set_color(ME), Create(A), Create(B), FadeIn(la), FadeIn(lb), FadeIn(dots_a), FadeIn(dot_b), rt=0.9)
        self.p(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), rt=1.0)
        self.at(180.78)  # question me
        qs = VGroup(*[mono("?", color=YOU, fs=48).move_to(np.array([x, 2.4, 0])) for x in (-3, 0, 3)])
        self.p(FadeOut(kwd), LaggedStart(*[FadeIn(q, shift=DOWN * 0.3) for q in qs], lag_ratio=0.2), rt=0.8)
        self.at(182.43)  # answer all
        self.p(*[Transform(q, mono("✓", color=ME, fs=48).move_to(q)) for q in qs], rt=0.6)
        self.at(184.0)
        self.fade_all(rt=0.3)

        self.at(184.33)  # algebraic expression of love: heart curve
        eq = M(r"(x^2+y^2-1)^3 - x^2y^3 = 0", "(x² + y² − 1)³ − x²y³ = 0", font_size=48, color=YOU).to_edge(UP, buff=0.7)
        heart = ParametricFunction(lambda t: 0.13 * np.array([16 * np.sin(t) ** 3,
                                                               13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]),
                                   t_range=[0, TAU], color=ME, stroke_width=5).shift(DOWN * 0.4)
        self.p(Write(eq), rt=1.2)
        self.p(Create(heart), rt=2.2)
        self.at(187.97)  # you are free
        me = Dot(heart.get_center(), color=ME, radius=0.15)
        you = Dot(heart.get_center() + RIGHT * 0.5, color=YOU, radius=0.15)
        self.p(FadeIn(me), FadeIn(you), rt=0.3)
        self.p(you.animate.move_to(RIGHT * 6.5 + UP * 2.5).set_opacity(0), rt=1.0)
        self.at(189.26)  # I am trapped
        self.p(heart.animate.scale(0.55), rt=0.9)
        self.at(190.24)  # trapped in love
        kwd = self.kw("lo-o-ove", fs=64).move_to(DOWN * 2.6)
        self.p(FadeIn(kwd), heart.animate.set_stroke(width=8), rt=0.6)
        self.p(Indicate(heart, color=ME, scale_factor=1.15), rt=1.0)
        self.p(Indicate(heart, color=ME, scale_factor=1.15), rt=1.0)
        self.at(193.2)
        self.p(FadeOut(kwd), FadeOut(eq), rt=0.25)

    # outro 193.46–end -------------------------------------------------------
    def shutdown(self):
        self.at(193.46)
        rest = [m for m in self.mobjects if m not in (self.grid, self.subs)]
        grp = Group(*rest)
        msg = RoundedRectangle(corner_radius=0.2, width=4.4, height=0.8, color=ME, fill_color=ME, fill_opacity=0.15).to_edge(UP, buff=1.0).shift(RIGHT * 2)
        mtxt = mono("are you still there?", color=ME, fs=24).move_to(msg)
        receipt = mono("sent · read: —", color=GREY, fs=18).next_to(msg, DOWN, aligned_edge=RIGHT, buff=0.1)
        self.p(grp.animate.shift(LEFT * 2.5).scale(0.8), FadeIn(msg), FadeIn(mtxt), rt=1.2)
        self.p(FadeIn(receipt), rt=0.6)
        self.at(198.0)
        self.p(grp.animate.set_color(GREY), msg.animate.set_color(GREY), mtxt.animate.set_color(GREY),
               self.grid.animate.set_opacity(0.08), rt=4.0)
        self.at(203.5)
        shut = mono("> shutdown --now", color=GREY, fs=28)
        self.p(FadeOut(Group(grp, msg, mtxt, receipt)), rt=1.0)
        self.p(FadeIn(shut), rt=0.5)

        self.at(205.56)  # final Execution — empty call
        call = mono("execute()", color=ME, fs=48)
        self.p(ReplacementTransform(shut, call), rt=0.3)
        ret = mono("→ None", color=GREY, fs=28).next_to(call, DOWN)
        self.p(FadeIn(ret), rt=0.4)
        self.at(207.0)
        dead = mono("dead", color=GREY, fs=22).to_corner(DR)
        self.p(FadeOut(call), FadeOut(ret), FadeOut(self.grid), FadeIn(dead), rt=1.2)
        self.at(209.5)
        self.p(FadeOut(dead), FadeOut(self.subs), rt=1.0)
        end = AUDIO_DURATION - AUDIO_OFFSET
        self.at(end)
