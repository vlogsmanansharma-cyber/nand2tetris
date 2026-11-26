#!/usr/bin/env python3
"""Generate the personalised key-controlled rectangle Hack assembly program."""
from pathlib import Path
import argparse, json

HERE=Path(__file__).resolve().parent
CONFIG=HERE.parent/'Part-B-Assembler'/'config.json'

def generate(k:int)->str:
    if not 0 <= k <= 99: raise ValueError('K must be between 0 and 99')
    words=(k%4)+1
    # Screen starts at 16384; each row occupies 32 words. The rectangle is 20 rows tall.
    lines=[f'// Personal K = {k}',f'// Top row = {k}; height = 20 rows; width = {words*16} pixels ({words} words).',
      '(CHECK_KEY)','@KBD','D=M','@DRAW','D;JGT','@ERASE','0;JMP',
      '(DRAW)',f'@{16384+32*k}','D=A','@ROW','M=D','@20','D=A','@COUNT','M=D',
      '(DRAW_ROW)','@ROW','A=M']
    # Fill exactly `words` consecutive screen words in this row using a pointer loop.
    lines += ['@ROW','D=M','@PTR','M=D', '@'+str(words),'D=A','@WIDTH','M=D', '(DRAW_WORD)','@PTR','A=M','M=-1','@PTR','M=M+1','@WIDTH','MD=M-1','@DRAW_WORD','D;JGT',
      '@ROW','D=M','@32','D=D+A','@ROW','M=D','@COUNT','MD=M-1','@DRAW_ROW','D;JGT','@CHECK_KEY','0;JMP',
      '(ERASE)',f'@{16384+32*k}','D=A','@ROW','M=D','@20','D=A','@COUNT','M=D',
      '(ERASE_ROW)','@ROW','D=M','@PTR','M=D','@'+str(words),'D=A','@WIDTH','M=D','(ERASE_WORD)','@PTR','A=M','M=0','@PTR','M=M+1','@WIDTH','MD=M-1','@ERASE_WORD','D;JGT',
      '@ROW','D=M','@32','D=D+A','@ROW','M=D','@COUNT','MD=M-1','@ERASE_ROW','D;JGT','@CHECK_KEY','0;JMP']
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(); p.add_argument('--k',type=int); a=p.parse_args()
    cfg=json.loads(CONFIG.read_text()); k=a.k if a.k is not None else int(cfg['K'])
    text=generate(k); (HERE/'Box.asm').write_text(text)
    print(f'Generated Box.asm for K={k}: top row {k}, 20 rows high, {(k%4+1)*16} pixels wide.')
if __name__=='__main__': main()
