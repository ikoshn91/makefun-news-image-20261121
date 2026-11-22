#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news atlas (1024x1024 PNG).

A one-page "atlas dashboard", drawn programmatically with Pillow:
no downloaded images, no AI generation, every word is real text
rendered from the strings below. Deterministic: same input bytes
every run (Pillow writes no timestamps into the PNG).

Layout: masthead + date, three lead cards (Iran/Bahrain, COP31,
Peru quake), then 8 colour-coded region panels holding 27 more
stories — 34 dated stories in 8 regions — plus an "Also today"
ticker. Hierarchy is deliberate: masthead, date and lead headlines
are far bigger than panel text, so the structure reads at 300 px.

Stories (all reported on Saturday 21 November 2026; sources:
CNN, Reuters, AP, WSJ, OneTurn, Majik, AppiSToS):
 leads: Iran strikes Bahrain; COP31 overtime in Antalya;
        M6.7 Peru quake, 00:09 UTC.
 Middle East: Riyadh intercepts 3 Houthi missiles; two tankers
        hit near Hormuz; Basra power-station fire; Trump seeks Iran deal.
 Europe: Kryvyi Rih triple-tap; Sparta II ablaze; Finland
        helicopter incursion; Denmark expels Russian attache.
 Asia: Myanmar rejects ICJ ruling; Manipur toxic alcohol;
        Ladakh polls; EU-Indonesia trade deals.
 Americas: "El Chapo Isidro" captured; FBI database hacked;
        Palisades arson verdict; Trump's "Great Powers" post.
 Markets: AI sell-off correction; Anthropic debut; Canada retail.
 Science: Wolbachia dengue cut; Voyager one light-day out;
        UN autonomous-weapons progress.
 Africa: Ethiopia displacement; Bayelsa boat; TAZARA overhaul.
 Sport: Cavalry FC title; Harden 51, passes Kobe.
 Ticker: Estonia drone warning; Russian missiles in Poland;
        Haiti blast kills 3 Salvadoran soldiers.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
CARD = (255, 253, 246)
INK = (22, 19, 14)
MUTED = (107, 99, 85)
RED = (166, 30, 30)
NAVY = (31, 58, 95)
TEAL = (15, 118, 110)
AMBER = (146, 64, 14)
ORANGE = (180, 83, 9)
GREEN = (34, 110, 60)
BROWN = (120, 72, 20)
PURPLE = (90, 50, 140)
WHITE = (255, 255, 255)
GOLD = (255, 214, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r1, r2, fill):
    pts = []
    for i in range(24):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 12 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_missile(draw, x, y, s, color):
    draw.line([x, y + s, x + s * 0.55, y + s * 0.45], fill=color, width=4)
    pts = [(x + s * 0.55, y + s * 0.15), (x + s * 0.95, y + s * 0.05),
           (x + s * 0.75, y + s * 0.5), (x + s * 0.45, y + s * 0.55)]
    draw.polygon(pts, fill=color)
    burst(draw, x + s * 0.42, y + s * 0.62, 10, 4, ORANGE)


def icon_summit(draw, x, y, s, color):
    cols = [RED, NAVY, TEAL]
    for i, c in enumerate(cols):
        cx = x + 10 + i * (s - 20) / 2
        draw.ellipse([cx - 9, y + 6, cx + 9, y + 24], fill=c)
        draw.rectangle([cx - 9, y + 26, cx + 9, y + 40], fill=c)
    draw.line([x, y + s - 6, x + s, y + s - 6], fill=color, width=4)


def icon_quake(draw, x, y, s, color):
    """Seismograph zigzag in a frame."""
    draw.rectangle([x, y, x + s, y + s], outline=color, width=3)
    pts = []
    n = 9
    for i in range(n + 1):
        px = x + 4 + i * (s - 8) / n
        py = y + s / 2 + (0 if i % 2 == 0 else (-1 if i % 4 == 1 else 1)) * (s * 0.28 if i not in (0, n) else 0)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=4, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 32  # margin

    # ---------- masthead ----------
    d.line([M, 22, W - M, 22], fill=INK, width=3)
    d.line([M, 28, W - M, 28], fill=INK, width=1)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 52)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 36), title, font=tf, fill=INK)
    date = "SATURDAY  21  NOVEMBER  2026"
    df = font(SANS_B, 24)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 100), date, font=df, fill=RED)
    sub = "34 dated stories  ·  8 regions  ·  all times UTC"
    sf = font(SANS, 15)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 130), sub, font=sf, fill=MUTED)
    d.line([M, 152, W - M, 152], fill=INK, width=3)

    # ---------- lead cards ----------
    leads = [
        ("MIDDLE EAST", RED, icon_missile,
         "Iran strikes Bahrain, claims US bases hit",
         "IRGC claims two US bases hit; Bahrain says a site burned, "
         "no one hurt."),
        ("CLIMATE  ·  ANTALYA", TEAL, icon_summit,
         "COP31 talks run into overtime",
         "Draft drops fossil-fuel phase-out; ~200 nations deadlocked "
         "as a deal nears."),
        ("AMERICAS  ·  PERU", AMBER, icon_quake,
         "M6.7 quake shakes Peru at 00:09 UTC",
         "108 km deep near Junín; felt in Lima; 152 homes "
         "uninhabitable, no deaths."),
    ]
    lw, lh, lgap = 309, 160, 16
    ly = 164
    lkf = font(SANS_B, 15)
    lhf = font(SANS_B, 23)
    lbf = font(SANS, 13)
    for i, (kick, color, icon, head, body) in enumerate(leads):
        x = M + i * (lw + lgap)
        d.rectangle([x, ly, x + lw, ly + lh], fill=CARD, outline=INK, width=2)
        d.rectangle([x, ly, x + lw, ly + 6], fill=color)
        icon(d, x + lw - 58, ly + 14, 44, color)
        d.text((x + 14, ly + 12), kick, font=lkf, fill=color)
        hlines = wrap(d, head, lhf, lw - 28 - 52)
        y = text_block(d, x + 14, ly + 38, hlines, lhf, INK, 28)
        blines = wrap(d, body, lbf, lw - 28)
        text_block(d, x + 14, y + 4, blines, lbf, INK, 17)

    # ---------- region panels ----------
    # (region, color, [(headline, one-line body), ...])
    regions = [
        ("MIDDLE EAST", RED, [
            ("Riyadh intercepts 3 Houthi missiles",
             "Third night running."),
            ("Two tankers hit near Strait of Hormuz",
             "UKMTO: two strikes off Khasab."),
            ("Basra power station fire kills 4",
             "Hartha plant blaze hurts 35."),
            ("Trump seeks 'real deal' with Iran",
             "Decision on next steps by new year."),
        ]),
        ("EUROPE", NAVY, [
            ("Triple-tap strike kills boy, 7, in Kryvyi Rih",
             "58 hurt, six of them children."),
            ("Russian cargo ship Sparta II ablaze",
             "Crew evacuates; ship adrift."),
            ("Finland probes Russian helicopter incursion",
             "Incursion reaches 4.1 km in."),
            ("Denmark expels Russian defence attaché",
             "Alleged plot to kill a rapper."),
        ]),
        ("ASIA", TEAL, [
            ("Myanmar rejects ICJ genocide ruling",
             "France seeks UN meeting."),
            ("Toxic alcohol kills 11 in Manipur",
             "180+ in hospital."),
            ("Ladakh votes in first local polls since 2019",
             "Local polls return to Ladakh."),
            ("EU and Indonesia sign trade deals",
             "CEPA and investment pacts signed."),
        ]),
        ("AMERICAS", ORANGE, [
            ("Mexico captures 'El Chapo Isidro'",
             "At least 11 dead in Guasave."),
            ("FBI crime database hacked",
             "Crime records breached."),
            ("Palisades arson verdict delivered",
             "12 dead; 6,800+ buildings lost."),
            ("Trump posts 'Great Powers 1945, 2026'",
             "Zelensky calls Putin a killer."),
        ]),
        ("MARKETS", AMBER, [
            ("AI sell-off becomes a correction",
             "Worst week since March 2020."),
            ("Anthropic debut nears $2 trillion",
             "Shares fall 8.5% on Friday."),
            ("Canada retail posts best since 2022",
             "Strongest in four years."),
            ("US stocks post worst week in years",
             "S&P, Dow −5.7%; Nasdaq −6.5%."),
        ]),
        ("SCIENCE", GREEN, [
            ("Wolbachia mosquitoes cut child dengue 69%",
             "Brazil study proves it at scale."),
            ("Voyager reaches one light-day out",
             "A first for a human-made object."),
            ("UN makes progress on killer-robot rules",
             "No binding treaty yet."),
            ("Voyager 1 suffers data outage",
             "Telemetry lost at one light-day."),
        ]),
        ("AFRICA", BROWN, [
            ("Ethiopia clashes displace 700,000",
             "50,000 flee into Kenya."),
            ("Bayelsa boat accident kills 4",
             "24 rescued in Bayelsa."),
            ("Tanzania–Zambia $1.4bn rail overhaul under way",
             "China's CCECC rebuilding TAZARA."),
            ("EU sends €550k aid for Moyale",
             "For refugees fleeing to Kenya."),
        ]),
        ("SPORT", PURPLE, [
            ("Cavalry FC win Canadian Premier League",
             "Beat Atlético Ottawa 3–2."),
            ("Harden scores 51, passes Kobe",
             "Cavs beat Pacers 128–119."),
            ("Herro scores 50 in Bucks loss",
             "76ers edge Milwaukee 132–129."),
        ]),
    ]
    gx, gy = M, 336
    pw, ph, pgap = 231, 291, 12
    rkf = font(SANS_B, 15)
    rcf = font(SANS, 11)
    rhf = font(SANS_B, 13)
    rbf = font(SANS, 11)
    for i, (name, color, stories) in enumerate(regions):
        x = gx + (i % 4) * (pw + pgap)
        yy = gy + (i // 4) * (ph + pgap)
        d.rectangle([x, yy, x + pw, yy + ph], fill=CARD, outline=INK, width=2)
        d.rectangle([x, yy, x + pw, yy + 6], fill=color)
        d.text((x + 12, yy + 14), name, font=rkf, fill=color)
        cnt = "%d STORIES" % len(stories)
        cw_ = d.textlength(cnt, font=rcf)
        d.text((x + pw - 12 - cw_, yy + 16), cnt, font=rcf, fill=MUTED)
        # lay stories out, spreading leftover space evenly as gaps
        blocks = []
        total = 0
        for head, body in stories:
            hl = wrap(d, head, rhf, pw - 28 - 16)
            bl = wrap(d, body, rbf, pw - 28 - 16)
            h = len(hl) * 16 + len(bl) * 14
            blocks.append((hl, bl, h))
            total += h
        avail = ph - 48 - total
        gap = max(6, avail // max(1, len(blocks)))
        y = yy + 42
        for hl, bl, h in blocks:
            d.ellipse([x + 12, y + 5, x + 20, y + 13], fill=color)
            y = text_block(d, x + 28, y, hl, rhf, INK, 16)
            y = text_block(d, x + 28, y + 1, bl, rbf, MUTED, 14)
            y += gap

    # ---------- ticker ----------
    tx0, ty0, tw_, th = M, 942, W - 2 * M, 50
    d.rectangle([tx0, ty0, tx0 + tw_, ty0 + th], fill=NAVY)
    tf2 = font(SANS_B, 15)
    d.text((tx0 + 14, ty0 + 16), "ALSO TODAY", font=tf2, fill=GOLD)
    tick = ("Estonia warns of drone attacks as NATO jets scramble   •   "
            "Russian missiles land in Poland   •   "
            "Haiti blast kills 3 Salvadoran soldiers")
    tkf = font(SANS, 14)
    tlines = wrap(d, tick, tkf, tw_ - 150)
    text_block(d, tx0 + 132, ty0 + 6, tlines, tkf, WHITE, 18)

    # ---------- footer ----------
    ff = font(SANS, 14)
    foot = ("Compiled from reports published Saturday 21 November 2026  ·  "
            "Sources: CNN, Reuters, AP, WSJ  ·  One day. 34 stories.")
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1000), foot, font=ff, fill=MUTED)

    out = os.environ.get("OUT", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
