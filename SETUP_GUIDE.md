# Simple Windows Setup Guide

## 1. Install Python
Download Python 3 from https://www.python.org/downloads/. During setup, tick **Add Python to PATH**. Open PowerShell and run `python --version`.

## 2. Set your K
Open `Part-B-Assembler/config.json` in Notepad or VS Code. If your roll number ends in 41, set the value to `41`. Save the file.

## 3. Run Part B
In PowerShell, `cd` into the project folder, then run:

```powershell
cd Part-B-Assembler
python -m unittest discover -s tests -v
python assembler.py programs/Add.asm
```

Expected: four assembler tests pass, then a success message says six instructions were written for Add.asm.

## 4. Generate Part C
```powershell
cd ..\Part-C-Box-Program
python generate_box.py
cd ..\Part-B-Assembler
python assembler.py ..\Part-C-Box-Program\Box.asm -o ..\Part-C-Box-Program\Box.hack
cd ..\Part-C-Box-Program
python emulator.py Box.hack
```

A window opens with a 512×256 screen. Click the window and hold a key. The black rectangle should appear at row K. Release the key and it should disappear.

## 5. Screenshots
- Part A: official HardwareSimulator after each of the five supplied tests passes.
- Part B: PowerShell showing test results and successful assembly; optionally show `symbols.txt`.
- Part C: emulator window with the box visible, plus the generated `Box.asm` and `Box.hack` in Explorer/editor.

Use **Win + Shift + S** to capture. Save the original screenshots; do not fake test results.
