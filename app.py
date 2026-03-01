import configparser
import random
import time
import string
import os

_cfg = configparser.ConfigParser()
_cfg.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini'), encoding='utf-8')

OS_MODE      = _cfg.getint('os', 'mode')
WPM          = _cfg.getint('typing', 'wpm')
ACCURACY     = _cfg.getfloat('typing', 'accuracy')
CONSISTENCY  = _cfg.getfloat('typing', 'consistency')

COUNTDOWN          = _cfg.getint('delays', 'countdown')
THINK_PAUSE_CHANCE = _cfg.getfloat('delays', 'think_pause_chance')
THINK_PAUSE_MIN    = _cfg.getfloat('delays', 'think_pause_min')
THINK_PAUSE_MAX    = _cfg.getfloat('delays', 'think_pause_max')
BURST_CHANCE       = _cfg.getfloat('delays', 'burst_chance')
BURST_MIN_LEN      = _cfg.getint('delays', 'burst_min_len')
BURST_MAX_LEN      = _cfg.getint('delays', 'burst_max_len')
BURST_DELAY_MIN    = _cfg.getfloat('delays', 'burst_delay_min')
BURST_DELAY_MAX    = _cfg.getfloat('delays', 'burst_delay_max')
BACKSPACE_DELAY_MIN = _cfg.getfloat('delays', 'backspace_delay_min')
BACKSPACE_DELAY_MAX = _cfg.getfloat('delays', 'backspace_delay_max')
RETYPE_PAUSE_MIN   = _cfg.getfloat('delays', 'retype_pause_min')
RETYPE_PAUSE_MAX   = _cfg.getfloat('delays', 'retype_pause_max')
NOTICE_PAUSE_MIN   = _cfg.getfloat('delays', 'notice_pause_min')
NOTICE_PAUSE_MAX   = _cfg.getfloat('delays', 'notice_pause_max')
CHAR_DELAY_MIN     = _cfg.getfloat('delays', 'char_delay_min')
CHAR_DELAY_MAX     = _cfg.getfloat('delays', 'char_delay_max')

_script_dir = os.path.dirname(os.path.abspath(__file__))
_text_file = _cfg.get('text', 'file')
with open(os.path.join(_script_dir, _text_file), 'r', encoding='utf-8') as f:
    TEXT = f.read().strip()

BASE_CPS = (WPM * 5) / 60

if OS_MODE == 1:
    import pyautogui
    pyautogui.FAILSAFE = True
else:
    from pynput.keyboard import Controller as PynputController, Key as PynputKey
    _kb = PynputController()

ADJACENT_KEYS = {
    'a': 'sqwz', 'b': 'vghn', 'c': 'xdfv', 'd': 'srfce', 'e': 'wrsdf',
    'f': 'drtgv', 'g': 'ftyhb', 'h': 'gyujn', 'i': 'ujko', 'j': 'huikm',
    'k': 'jiol', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhij', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx', ' ': ' ',
}


def _type_char(char):
    if OS_MODE == 1:
        if char.isascii() and char in string.printable:
            pyautogui.typewrite(char, interval=0)
        else:
            import subprocess
            subprocess.run(['pbcopy'], input=char.encode('utf-8'), check=True)
            pyautogui.hotkey('command', 'v')
    else:
        _kb.type(char)


def _press_backspace():
    if OS_MODE == 1:
        pyautogui.hotkey('backspace')
    else:
        _kb.press(PynputKey.backspace)
        _kb.release(PynputKey.backspace)


def get_typo_char(char):
    c = char.lower()
    if c in ADJACENT_KEYS and ADJACENT_KEYS[c] != ' ':
        return random.choice(ADJACENT_KEYS[c])
    return random.choice(string.ascii_lowercase)


def char_delay():
    base = 1.0 / BASE_CPS
    variance = base * (1.0 - CONSISTENCY) * 1.2
    delay = random.gauss(base, variance)
    return max(CHAR_DELAY_MIN, min(delay, CHAR_DELAY_MAX))


def should_make_typo():
    return random.random() > ACCURACY


def type_text(text):
    os_names = {1: "Mac", 2: "Windows", 3: "Linux"}
    print(f"OS Mode: {os_names.get(OS_MODE, 'Unknown')}")
    print(f"Starting in {COUNTDOWN} seconds... Switch to your target window!")
    for i in range(COUNTDOWN, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("Typing...")

    i = 0
    while i < len(text):
        char = text[i]

        if random.random() < THINK_PAUSE_CHANCE:
            time.sleep(random.uniform(THINK_PAUSE_MIN, THINK_PAUSE_MAX))

        if random.random() < BURST_CHANCE:
            burst_len = random.randint(BURST_MIN_LEN, BURST_MAX_LEN)
            burst_end = min(i + burst_len, len(text))
            for j in range(i, burst_end):
                _type_char(text[j])
                time.sleep(random.uniform(BURST_DELAY_MIN, BURST_DELAY_MAX))
            i = burst_end
            continue

        if should_make_typo() and char.isalpha():
            typo = get_typo_char(char)

            _type_char(typo)
            time.sleep(char_delay() * random.uniform(0.5, 1.5))

            notice_delay = random.randint(0, 2)
            extra_typed = 0
            for k in range(notice_delay):
                if i + 1 + k < len(text):
                    _type_char(text[i + 1 + k])
                    time.sleep(char_delay())
                    extra_typed += 1

            time.sleep(random.uniform(NOTICE_PAUSE_MIN, NOTICE_PAUSE_MAX))

            for _ in range(extra_typed + 1):
                _press_backspace()
                time.sleep(random.uniform(BACKSPACE_DELAY_MIN, BACKSPACE_DELAY_MAX))

            time.sleep(random.uniform(RETYPE_PAUSE_MIN, RETYPE_PAUSE_MAX))

            _type_char(char)
            time.sleep(char_delay())

        else:
            _type_char(char)
            time.sleep(char_delay())

        i += 1

    print("Done!")


if __name__ == "__main__":
    type_text(TEXT)