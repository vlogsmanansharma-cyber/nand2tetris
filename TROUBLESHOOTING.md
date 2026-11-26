# Troubleshooting

- **`python` is not recognised:** reinstall Python and tick Add Python to PATH; reopen PowerShell.
- **Assembler says invalid computation:** check the Hack comp spelling against the official comp table. Do not use unsupported arithmetic expressions.
- **Box is not personalised:** check `Part-B-Assembler/config.json`, regenerate `Box.asm`, then assemble it again.
- **Box appears at the wrong row/width:** verify K and calculate `row=K`, `words=(K % 4)+1`, `width=words*16`.
- **Emulator window does not react to keys:** click inside the window first, then hold a key; release it to clear the box.
- **Hardware Simulator reports missing chip:** set the working directory to `Part-A-Computer`, confirm the built-in chip names match your installed suite, and check the error's chip/pin name.
- **A test script is missing:** copy the official `.tst` and `.cmp` files from the Nand2Tetris course/software distribution into `Part-A-Computer/tests/`. Do not create fake passing screenshots.
