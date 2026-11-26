# Part C — Personalised key-controlled box

## Generate and assemble
From the project root in PowerShell:

```powershell
cd Part-B-Assembler
# First edit config.json and set K to your own last two roll-number digits.
cd ..\Part-C-Box-Program
python generate_box.py
cd ..\Part-B-Assembler
python assembler.py ..\Part-C-Box-Program\Box.asm
```

The assembler writes `Part-C-Box-Program/Box.hack` because the output defaults to the input `.asm` filename. If needed, use `-o ..\Part-C-Box-Program\Box.hack` explicitly.

## Run the included Python emulator
From `Part-C-Box-Program`:

```powershell
python emulator.py Box.hack
```

Click the emulator window and hold any key: the black rectangle appears. Release the key: the rectangle is erased. Close the window when finished. This is a lightweight learning emulator for the generated box program; use the official CPU Emulator / Hardware Simulator for course verification.

## Geometry
- Top row: `K`
- Height: 20 rows
- Width: `16 × ((K mod 4) + 1)` pixels
- First screen word: `SCREEN + 32 × K`
- Screen words per row: `(K mod 4) + 1`

The program polls the keyboard, fills the selected screen words with `-1` (all 16 pixels black), and writes `0` to erase them.
