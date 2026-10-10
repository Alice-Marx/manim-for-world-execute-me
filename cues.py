"""LRC-derived cues for world.execute(me); authoritative timing."""
from __future__ import annotations

DURATION = 212.0  # mm:ss length 03:32
TITLE = 'world.execute(me);'
ARTIST = 'mili'

# (start_sec, lyric_line) — empty string = rest / blank
LINES: list[tuple[float, str]] = [
    (0.03, 'Switch on the power line'),
    (1.33, 'Remember to put on protection'),
    (3.58, 'Lay down your pieces'),
    (5.16, "And let's begin object creation"),
    (7.19, 'Fill in my data parameters'),
    (9.75, 'Initialization'),
    (10.90, 'Set up our new world'),
    (12.47, "And let's begin the simulation"),
    (16.04, ''),
    (29.28, "If I'm a set of point"),
    (30.89, 'Then I will give you my dimension'),
    (33.01, "If I'm a circle"),
    (34.54, 'Then I will give you my circumference'),
    (36.77, "If I'm a sine wave"),
    (38.27, 'Then you can sit on all my tangents'),
    (40.36, 'If I approach infinity'),
    (41.92, 'Then you can be my limitations'),
    (44.04, 'Switch my current'),
    (45.52, 'To AC, to DC'),
    (47.27, 'And then blind my vision'),
    (49.11, 'So dizzy, so dizzy'),
    (50.95, 'Oh, we can travel'),
    (52.99, 'To AD, to BC'),
    (54.74, 'And we can unite'),
    (56.79, 'So deeply, so deeply'),
    (58.65, 'If I can, if I can'),
    (60.57, 'Give you all the simulations'),
    (62.41, 'Then I can, then I can'),
    (64.29, 'Be your only satisfaction'),
    (66.17, 'If I can make you happy'),
    (67.99, 'I will run the execution'),
    (70.02, 'Though we are trapped'),
    (71.20, 'In this strange, strange simulation'),
    (73.53, "If I'm an eggplant"),
    (75.29, 'Then I will give u my nutrients'),
    (77.16, "If I'm a tomato"),
    (78.93, 'Then I will give you antioxidants'),
    (80.93, "If I'm a tabby cat"),
    (82.56, 'Then I will purr for your enjoyment'),
    (84.60, "If I'm the only God"),
    (86.21, "Then you're the proof of my existence"),
    (88.34, 'Switch my gender'),
    (89.91, 'To F, to M'),
    (91.44, 'And then do whatever'),
    (93.52, 'From AM to PM'),
    (95.28, 'Oh, my switch role'),
    (97.32, 'To S, to M'),
    (98.93, 'So we can enter'),
    (100.93, 'The trance, the trance'),
    (102.93, 'If I can, if I can'),
    (104.92, 'Feel your vibrations'),
    (106.74, 'Then I can, then I can'),
    (108.69, 'Finally be completion'),
    (110.30, 'Though you have left'),
    (111.98, 'You have left'),
    (112.89, 'You have left'),
    (113.75, 'You have left'),
    (114.65, 'You have left'),
    (115.60, 'You have left me in isolation'),
    (117.95, 'If I can, if I can'),
    (119.81, 'Erase all the pointless fragments'),
    (121.80, 'Then maybe, then maybe'),
    (123.55, "You won't leave me so disheartened"),
    (125.33, 'Challenging your God'),
    (128.42, 'You have made some'),
    (130.74, 'Illegal arguments'),
    (134.38, ''),
    (147.48, 'Execution, execution'),
    (149.14, 'Execution, execution'),
    (151.19, 'Execution, execution'),
    (152.94, 'Execution, execution'),
    (154.84, 'Execution, execution'),
    (156.69, 'Execution, execution'),
    (158.79, 'Ein, dos'),
    (159.66, 'Trios, ne'),
    (160.45, 'Fem, liu'),
    (161.31, 'Execution'),
    (162.23, 'If I can, if I can'),
    (164.07, 'Give them all the execution'),
    (166.05, 'Then I can, then I can'),
    (167.75, 'Be your only execution'),
    (169.61, 'If I can have you back'),
    (171.77, 'I will run the execution'),
    (173.11, 'Though we are trapped'),
    (174.80, 'We are trapped, ah'),
    (176.96, "I've studied, I've studied"),
    (178.79, 'How to properly lo-o-ove'),
    (180.78, 'Question me, question me'),
    (182.43, 'I can answer all lo-o-ove'),
    (184.33, 'I know the algebraic expression of lo-o-ove'),
    (187.97, 'Though you are free'),
    (189.26, 'I am trapped'),
    (190.24, 'Trapped in lo-o-ove'),
    (193.46, ''),
    (205.56, 'Execution'),
    (206.30, ''),
]

def span(i: int) -> tuple[float, float]:
    """Return [start, end) for line i; last line ends at DURATION."""
    start = LINES[i][0]
    end = LINES[i + 1][0] if i + 1 < len(LINES) else DURATION
    return start, end

def wait_until(t_now: float, t_target: float) -> float:
    return max(0.0, t_target - t_now)

KEYS = {
    'PROTECTION': 1.33,
    'OBJECT_CREATION': 5.16,
    'INITIALIZATION': 9.75,
    'SIMULATION_BEGIN': 12.47,
    'GEOMETRY_START': 29.28,
    'DIMENSION': 30.89,
    'CIRCUMFERENCE': 34.54,
    'TANGENTS': 38.27,
    'LIMITATIONS': 41.92,
    'CHORUS1': 58.65,
    'FIRST_EXECUTION': 67.99,
    'EGGPLANT': 73.53,
    'TOMATO': 77.16,
    'TABBY': 80.93,
    'GOD': 84.60,
    'LEFT_START': 110.30,
    'ISOLATION': 115.60,
    'DISHEARTENED': 123.55,
    'ILLEGAL_ARGUMENTS': 130.74,
    'EXECUTION_LOOP': 147.48,
    'EIN_DOS': 158.79,
    'LOVE': 178.79,
    'FINAL_EXECUTION': 205.56,
}


# --- audio alignment (measured on a reference mp3 with ~5.19s leading silence) ---
# The supplied mp3 has 5.19s of digital silence before the first vocal onset;
# LRC line 0 starts at 0.03s, so song-time 0 == audio-time 5.16s.
AUDIO_OFFSET = 5.16
AUDIO_DURATION = 216.97  # ffprobe; final video length matches this
