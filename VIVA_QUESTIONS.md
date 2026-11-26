# Viva — Short Answers to Practise

1. **What is the Hack computer?** A simple 16-bit computer architecture with an A register, D register, ALU, program counter, RAM, screen, keyboard and instruction ROM.
2. **What does the assembler do?** It translates readable Hack assembly into 16-bit machine instructions.
3. **Why are there two passes?** Pass 1 records label addresses. Pass 2 emits instructions and allocates RAM addresses for variables that were not predefined.
4. **What is an A-instruction?** `@value`; it loads a 15-bit constant or symbol address into the A register.
5. **What is a C-instruction?** `dest=comp;jump`; it performs an ALU operation, optionally stores its result, and may jump.
6. **Why do variables start at RAM[16]?** Addresses 0–15 are reserved for R0–R15; variables begin at 16.
7. **What is a label?** A symbolic name for a ROM instruction address, declared as `(NAME)`.
8. **How is the screen mapped?** It starts at address 16384. Each row uses 32 words; each word controls 16 horizontal pixels.
9. **How does the box appear?** The program checks KBD. If a key is pressed, it writes -1 to the selected screen words; otherwise it writes 0.
10. **Why does -1 make a black word?** In 16-bit two's-complement representation, -1 is sixteen 1-bits, so all 16 pixels in that word are on/black.
11. **How is the width calculated?** Number of words per row is `(K mod 4) + 1`; each word is 16 pixels wide.
12. **How do you move the box down?** Increase the initial screen address by 32 for each row moved down, or increase K and regenerate.
13. **What does K mod 3 control?** It selects the assembler's required extra feature: symbol table, line-numbered errors, or duplicate-label warnings.
14. **Why is Part A HDL and not Python?** The official Hardware Simulator requires HDL descriptions to build and test hardware chips. Python is used for software tools in Parts B and C.
15. **What mistake did you fix?** Prepare your real example: state the error, the file/line, why it happened, the correction, and the test that proved it was fixed.

## On-the-spot change
To move the rectangle down by 1 row, increase K by 1 (ensuring K+20 stays within the screen), regenerate `Box.asm`, assemble it again, and rerun the emulator. Explain that one screen row equals 32 memory words.
