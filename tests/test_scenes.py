"""Behavior checks for live scene changes; no terminal or dependencies needed."""
import os
from pathlib import Path
import re
import runpy
import unittest
from unittest.mock import patch


APP = runpy.run_path(str(Path(__file__).resolve().parents[1] / "driftlight"))
Scene = APP["Scene"]
STYLES = APP["STYLES"]


def scene(style="plankton", size=(100, 30), extra=()):
    args = APP["build_parser"]().parse_args([
        "--style", style, "--seed", "42", "--no-circadian", "--truecolor",
        *extra,
    ])
    with patch("shutil.get_terminal_size", return_value=os.terminal_size(size)):
        return Scene(args)


def render(s, t=2, dt=1 / 22):
    out = []
    s.render_frame(t, dt, out)
    return "".join(out)


class SceneTests(unittest.TestCase):
    def test_every_style_is_seeded_and_animates(self):
        for style in STYLES:
            with self.subTest(style=style):
                a, b = scene(style), scene(style)
                early = None
                for i in range(90):
                    self.assertEqual(render(a, i / 22), render(b, i / 22))
                    if i == 30:
                        early = dict(a.disp if style == "plankton" else a.style_disp)
                late = a.disp if style == "plankton" else a.style_disp
                self.assertTrue(late, "scene must draw visible art")
                self.assertNotEqual(early, late, "scene must keep moving")

    def test_settings_survives_a_full_style_cycle_both_directions(self):
        s = scene()
        s.handle_key("s")
        for direction in ("right", "left", "enter"):
            for _ in STYLES:
                s.handle_key(direction)
                output = render(s)
                self.assertIn(APP["CLEAR"], output)
                self.assertIn("driftlight — settings", output)
                self.assertIn(s.args.style, output)
                self.assertIn("enter select", output)
                self.assertEqual(s.overlay, "settings")
                self.assertIn("driftlight — settings", render(s))
        s.handle_key("down")
        palette = s.args.palette
        s.handle_key("right")
        self.assertNotEqual(s.args.palette, palette)
        s.handle_key("esc")
        self.assertIsNone(s.overlay)
        self.assertIn("s settings", render(s))

    def test_close_panel_repaints_covered_art(self):
        s = scene("ribbons")
        render(s, dt=0)
        expected = dict(s.style_disp)
        s.handle_key("s")
        render(s, dt=0)
        self.assertNotEqual(expected, s.style_disp)
        s.handle_key("esc")
        render(s, dt=0)
        self.assertEqual(expected, s.style_disp)

    def test_pebble_only_applies_in_ripple_scene(self):
        s = scene("ripple")
        render(s)
        self.assertEqual(len(s.ripples), 1)
        s.handle_key("space")
        render(s)
        self.assertEqual(len(s.ripples), 2)
        s.handle_key("s")
        s.handle_key("space")
        self.assertEqual(s.args.style, "plankton")
        self.assertFalse(s.pebble_pending)
        self.assertFalse(s.ripples)

    def test_panels_and_art_stay_inside_small_terminals(self):
        for size in ((18, 8), (1, 1), (60, 16), (100, 30)):
            for style in STYLES:
                with self.subTest(size=size, style=style):
                    s = scene(style, size, extra=("--breath", "4-7-8"))
                    for key in (None, "s", "up", "esc", "h", "esc"):
                        if key:
                            s.handle_key(key)
                        for row, col in re.findall(r"\x1b\[(\d+);(\d+)H", render(s)):
                            self.assertLessEqual(int(row), size[1])
                            self.assertLessEqual(int(col), size[0])
                    s.handle_key("s")
                    for _ in s.fields:
                        s.handle_key("down")
                        if size[0] >= 60:
                            self.assertIn(s.fields[s.sel]["label"], render(s))

    def test_sleep_slows_new_scenes_without_reversing_time(self):
        awake = scene("orrery")
        sleepy = scene("orrery", extra=("--sleep", "1"))
        render(awake, t=59, dt=0.1)
        render(sleepy, t=59, dt=0.1)
        self.assertGreater(sleepy.art_time, 0)
        self.assertLess(sleepy.art_time, awake.art_time)


if __name__ == "__main__":
    unittest.main()
