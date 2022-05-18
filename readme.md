# NanoRPN

A lightweight scientific RPN calculator modeled after the HP 35s, a fast and ergonomic pocket calculator.

## Features

✔️ Near-infinite RPN stack, with the most recent eight values visible

✔️ Minimalist interface, to stay out of your way so you can focus on calculations

✔️ Keyboard support!

✔️ User-configurable save file path

## Screenshot

![Screenshot](https://github.com/nevadaperry/NanoRPN/raw/main/screenshot.png)

## Installation

NanoRPN requires [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap), which can be installed with pip according to the author's instructions:

`python -m pip install ttkbootstrap`

On MacOS and Linux, this should work in the default Terminal app. On Windows, Python can be installed from the Windows Store or [python.org](https://www.python.org/downloads/windows/), and run using PowerShell (found in the Start Menu).

After ttkbootstrap is installed, download [NanoRPN.py](https://github.com/nevadaperry/NanoRPN/raw/main/main.py) from this repository and navigate to its location in Terminal/PowerShell.

## Usage

`python3 NanoRPN.py [save-file-path]`

If supplied, `save-file-path` will be used for both loading and saving state.

## Creating an app shortcut

On MacOS, a shortcut can be created with Script Editor with a line similar to the following:

`do shell script "source ~/.bash_profile; python3 ~/Documents/NanoRPN.py ~/.nanorpn_state"`

On Windows, a shortcut can be created by right-click dragging `python.exe` and selecting "Create shortcut here", then editing the shortcut: Properties -> Shortcut tab -> Target:, and adding the arguments ` "path\to\NanoRPN.py" "%APPDATA%\.nanorpn_state"`.

## Keyboard shortcuts

| NanoRPN button | Default key | Alternate name |
| :-: | :-: | :-: |
| ⬅︎Bksp | Backspace |
| Enter⬆ | Enter |
| Drop⬇ | D |
| ln | L |
| (-) | N | Negate |
| 1/ | R | Reciprocal |
| √ | S | Square root |
| E | E | 10^ |

All numeric (`0-9.`) and arithmetic (`+-*/^`) buttons are themselves.

## Configuration

Keyboard configuration can be changed by simply editing `NanoRPN.py` line 126, `btn_keys =` which corresponds with button labels.

The theme can be changed by editing `NanoRPN.py` line 32, `themename=`, line 100, `bootstyle=`, line 102, `bootstyle=`, and line 136, `bootstyle=`.
