# Human Typer

Simulates realistic human-like typing with configurable WPM, accuracy, typos, and natural pauses. Cross-platform — works on **Mac**, **Windows**, and **Linux**.

Built for platforms that monitor typing activity — like **Google Docs**, where teachers can review edit history, typing speed, and input patterns to check if the work was written by hand. Human Typer makes any text look like it was naturally typed in real time: with realistic speed variation, occasional typos, corrections, and thinking pauses.

## Features

- ⌨️ Realistic typing speed based on your [MonkeyType](https://monkeytype.com) stats
- 🔤 Adjacent-key typos with natural correction behavior
- ⏸ Random thinking pauses and burst typing
- 🖥 Cross-platform support (Mac / Windows / Linux)
- ⚙️ Fully configurable via `config.ini`

## Quick Start

### 1. Install Python 3

Make sure you have [Python 3](https://www.python.org/downloads/) installed.

### 2. Install dependencies

**Mac:**
```bash
pip install pyautogui
```

**Windows / Linux:**
```bash
pip install pynput
```

### 3. Set your OS

Open `config.ini` and set your operating system:

```ini
[os]
mode = 1   # 1 = Mac, 2 = Windows, 3 = Linux
```

### 4. Paste your text

Open `text.txt` and paste the text you want to type. No formatting needed — just plain text.

### 5. Run

```bash
python3 app.py
```

Switch to your target window during the countdown. The script will start typing automatically.


## Configuration

All settings live in `config.ini`:

### `[os]`

| Key | Values | Description |
|-----|--------|-------------|
| `mode` | `1` / `2` / `3` | `1` = Mac, `2` = Windows, `3` = Linux |

### `[typing]`

| Key | Default | Description |
|-----|---------|-------------|
| `wpm` | `62` | Words per minute |
| `accuracy` | `0.93` | Accuracy (0.0 – 1.0). Lower = more typos |
| `consistency` | `0.69` | Consistency (0.0 – 1.0). Lower = more speed variation |

### `[delays]`

Fine-tune all timing parameters:

| Key | Default | Description |
|-----|---------|-------------|
| `countdown` | `3` | Seconds before typing starts |
| `think_pause_chance` | `0.02` | Chance of a mid-word "thinking" pause |
| `think_pause_min/max` | `0.3 / 0.8` | Duration range of thinking pauses (sec) |
| `burst_chance` | `0.15` | Chance of a fast typing burst |
| `burst_min_len/max_len` | `2 / 5` | Number of chars in a burst |
| `burst_delay_min/max` | `0.05 / 0.10` | Delay between chars in a burst (sec) |
| `backspace_delay_min/max` | `0.06 / 0.15` | Speed of backspace when fixing typos (sec) |
| `notice_pause_min/max` | `0.15 / 0.45` | Pause when "noticing" a typo (sec) |
| `retype_pause_min/max` | `0.05 / 0.2` | Pause before retyping correct char (sec) |
| `char_delay_min/max` | `0.05 / 0.6` | Min/max per-character delay (sec) |

### `[text]`

| Key | Default | Description |
|-----|---------|-------------|
| `file` | `text.txt` | Path to the text file to type |

## File Structure

```
typer/
├── app.py        # Main script
├── config.ini    # All settings
├── text.txt      # Your text goes here
└── README.md
```

## Platform Notes

| Platform | Backend | Notes |
|----------|---------|-------|
| **Mac** | `pyautogui` | Failsafe: move mouse to top-left corner to abort |
| **Windows** | `pynput` | Run as administrator if typing doesn't work |
| **Linux** | `pynput` | Requires X11. Wayland is not supported |

## License

MIT
