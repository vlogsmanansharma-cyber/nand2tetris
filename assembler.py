#!/usr/bin/env python3
"""Simple two-pass assembler for the Nand2Tetris Hack computer."""
from pathlib import Path
import argparse, json, re, sys

PREDEFINED = {"SP":0,"LCL":1,"ARG":2,"THIS":3,"THAT":4,"SCREEN":16384,"KBD":24576}
PREDEFINED.update({f"R{i}":i for i in range(16)})
DEST = {"": "000", "M":"001", "D":"010", "MD":"011", "A":"100", "AM":"101", "AD":"110", "AMD":"111"}
JUMP = {"": "000", "JGT":"001", "JEQ":"010", "JGE":"011", "JLT":"100", "JNE":"101", "JLE":"110", "JMP":"111"}
COMP = {
 "0":"0101010","1":"0111111","-1":"0111010","D":"0001100","A":"0110000","M":"1110000",
 "!D":"0001101","!A":"0110001","!M":"1110001","-D":"0001111","-A":"0110011","-M":"1110011",
 "D+1":"0011111","A+1":"0110111","M+1":"1110111","D-1":"0001110","A-1":"0110010","M-1":"1110010",
 "D+A":"0000010","D+M":"1000010","D-A":"0010011","D-M":"1010011","A-D":"0000111","M-D":"1000111",
 "D&A":"0000000","D&M":"1000000","D|A":"0010101","D|M":"1010101"}

class AssemblerError(Exception): pass

def clean_lines(path):
    result=[]
    for n, raw in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        line=raw.split('//',1)[0].strip()
        if line: result.append((n,re.sub(r'\s+','',line)))
    return result

def assemble(source, k=0, symbols_path=None):
    lines=clean_lines(source); symbols=dict(PREDEFINED); rom=0; warnings=[]; errors=[]
    # Pass 1: labels
    for line_no,line in lines:
        if line.startswith('(') and line.endswith(')'):
            label=line[1:-1]
            if not re.fullmatch(r'[A-Za-z_.$:][\w.$:]*',label):
                errors.append((line_no,'invalid label')); continue
            if label in symbols:
                if label in PREDEFINED: errors.append((line_no,f'label {label} conflicts with a predefined symbol'))
                else: warnings.append(f'Line {line_no}: duplicate label ({label}); first definition kept')
            else: symbols[label]=rom
        else: rom+=1
    # Pass 2: instructions and variables
    output=[]; next_var=16
    for line_no,line in lines:
        if line.startswith('(') and line.endswith(')'): continue
        try:
            if line.startswith('@'):
                value=line[1:]
                if value.isdigit(): number=int(value)
                else:
                    if not re.fullmatch(r'[A-Za-z_.$:][\w.$:]*',value): raise AssemblerError('invalid A-instruction symbol')
                    if value not in symbols: symbols[value]=next_var; next_var+=1
                    number=symbols[value]
                if not 0 <= number <= 32767: raise AssemblerError('A-instruction value must be between 0 and 32767')
                output.append(f'{number:016b}')
            else:
                dest=''; jump=''; comp=line
                if '=' in comp: dest,comp=comp.split('=',1)
                if ';' in comp: comp,jump=comp.split(';',1)
                if comp not in COMP: raise AssemblerError(f'unknown computation: {comp}')
                if dest not in DEST: raise AssemblerError(f'invalid destination: {dest}')
                if jump not in JUMP: raise AssemblerError(f'invalid jump: {jump}')
                output.append('111'+COMP[comp]+DEST[dest]+JUMP[jump])
        except (AssemblerError,ValueError) as e:
            if k % 3 == 1: errors.append((line_no,str(e)))
            else: raise AssemblerError(f'Line {line_no}: {e}')
    if errors: raise AssemblerError('\n'.join(f'Line {n}: {msg}' for n,msg in errors))
    if symbols_path:
        Path(symbols_path).write_text('\n'.join(f'{name}\t{addr}' for name,addr in sorted(symbols.items(), key=lambda x:(x[1],x[0])))+'\n',encoding='utf-8')
    return output,warnings,symbols

def main():
    p=argparse.ArgumentParser(description='Assemble Hack .asm files into 16-bit .hack files')
    p.add_argument('source',help='input .asm file'); p.add_argument('-o','--output',help='output .hack file')
    p.add_argument('--k',type=int,help='your personal K (last two roll-number digits)')
    args=p.parse_args(); base=Path(__file__).parent
    cfg=json.loads((base/'config.json').read_text())
    k=args.k if args.k is not None else int(cfg.get('K',0))
    dest=Path(args.output) if args.output else Path(args.source).with_suffix('.hack')
    try:
        machine,warnings,_=assemble(args.source,k,base/'symbols.txt')
        dest.write_text('\n'.join(machine)+'\n',encoding='utf-8')
        print(f'Success! {len(machine)} instructions written to {dest}')
        for w in warnings: print('WARNING:',w)
        print(f'K={k}; selected extra feature: {("save symbol table", "line-numbered errors", "duplicate-label warning")[k%3]}')
    except (AssemblerError,OSError) as e:
        print(f'ASSEMBLY FAILED: {e}',file=sys.stderr); sys.exit(1)
if __name__=='__main__': main()
