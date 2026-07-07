# driftlight

A calming terminal screensaver. Think `cmatrix`, but the opposite feeling.

Your terminal becomes the sea at night. Invisible currents drift through the
dark and, where they pass, bioluminescent points flare cyan-green and slowly
fade. Occasionally a shimmer sweeps across the water. It's slow, sparse, and
low-luminance — built to be watched, or half-watched, while you breathe.

```
       ·           ∙
   •                     ·
         ∙     ·
                •          ∙
   ·                            ·
         ·          •
```

Pure Python 3 standard library. No dependencies. One file. MIT licensed.

## Install

```sh
git clone https://github.com/YOU/driftlight.git
cd driftlight
./install.sh          # copies to ~/.local/bin/driftlight
```

Or just run it in place:

```sh
./driftlight
```

## Controls

driftlight is interactive while it runs:

| key | action |
|-----|--------|
| `h` | toggle the help panel |
| `s` | open the settings panel — change palette, density, breath, etc. **live** |
| `q` / `Ctrl-C` | quit |
| `esc` | close an open panel (or quit if none is open) |

In the settings panel:

| key | action |
|-----|--------|
| `j` / `k` or `↑` / `↓` | move the selection |
| `←` / `→` or `-` / `+` | change the selected value |
| `space` | toggle / cycle the selected value |

Every setting below can be changed live from the `s` panel without restarting —
handy for finding the density and palette that feel right for your terminal.
Pick a palette as a starting point, then fine-tune with the **Hue**,
**Saturation**, **Brightness**, and **Glow** sliders to land on your exact color.

## Why it's calm (and cmatrix isn't)

`cmatrix` is fast, high-contrast, and reads as *urgent*. driftlight inverts all
three: motion is slow, contrast is low (dim pastels, not neon), and events are
irregular and organic instead of rigid falling columns. The magic is in the
timing, not the shape — nothing ever *arrives* or *ends*, it just breathes.

## The premium touches

Everything below is optional and composable.

### Breath-sync
The entire scene brightens on the inhale, holds, and dims on the exhale — and
plankton bloom faster on the inhale. Within a minute your breathing tends to
sync to it without being told to. A faint indicator in the corner shows the
current phase.

```sh
driftlight --breath 4-7-8      # relaxing 4-7-8 breathing
driftlight --breath box        # 4-4-4-4 box breathing
driftlight --breath 5-5-5      # custom inhale-hold-exhale
driftlight --breath 4-4-6-2    # custom inhale-hold-exhale-hold
```

### Circadian palette drift  (on by default)
driftlight reads your system clock. After sunset the palette warms toward amber
and dims ~15%; deep night gets darker still; morning cools back to cyan. It
respects your melatonin. Turn it off with `--no-circadian`.

### Long-arc weather  (on by default)
A hidden meta-state on an ~8-minute cycle slowly modulates how much plankton
bloom, so it never loops into the pattern-fatigue that makes people quit
`cmatrix` after 90 seconds. Tune the cycle with `--weather 12`, or `--weather 0`
to disable.

### Sleep wind-down
A slow ramp to near-stillness over N minutes — a wind-down for the end of the
day. Start it and go to sleep.

```sh
driftlight --sleep 30
```

## Options

| flag | default | what it does |
|------|---------|--------------|
| `--palette NAME` | `teal` | starting color: `teal`, `ice`, `aurora`, `ember`, `mono`, `violet` |
| `--hue DEG` | `0` | rotate the palette hue, -180..180° |
| `--saturation N` | `1.0` | color saturation multiplier, 0..1.5 (lower = washed out) |
| `--brightness N` | `1.0` | overall brightness gain, 0.3..1.8 |
| `--glow N` | `0.5` | how long faint points linger, 0..1 |
| `--density N` | `1.0` | how much plankton (0.2 sparse .. 2.0 dense) |
| `--linger SEC` | `3.2` | seconds a flash takes to fade out |
| `--fps N` | `22` | frames per second |
| `--breath SPEC` | `off` | `off`, `4-7-8`, `box`, or `a-b-c` / `a-b-c-d` |
| `--sleep MIN` | off | wind down to stillness over MIN minutes |
| `--weather MIN` | `8` | long-arc bloom/calm cycle length (0 = off) |
| `--no-circadian` | | disable warm+dim drift after sunset |
| `--no-shimmer` | | disable the diagonal shimmer sweeps |
| `--no-indicator` | | hide the breath indicator |
| `--seed N` | | reproducible randomness |
| `--256` / `--truecolor` | auto | force color depth (auto-detects `COLORTERM`) |

## A few nice recipes

```sh
driftlight                                   # gentle defaults
driftlight --palette violet --density 0.6    # sparse deep-sea purple
driftlight --breath 4-7-8 --palette ice      # cold, meditative, breathing
driftlight --palette ember --density 1.4     # warm firefly swarm
driftlight --sleep 45 --breath box           # bedtime
```

## Requirements

- Python 3.6+
- A terminal with 256-color or truecolor support (basically all of them). Set
  `COLORTERM=truecolor` if your terminal supports 24-bit color but doesn't
  advertise it.

## License

MIT — see [LICENSE](LICENSE).
