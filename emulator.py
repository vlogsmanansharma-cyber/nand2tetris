#!/usr/bin/env python3
"""Small Hack CPU emulator + simple screen window. Requires only Python standard library."""
from pathlib import Path
import argparse, tkinter as tk

COMP={0b0101010:lambda d,a,m:0,0b0111111:lambda d,a,m:1,0b0111010:lambda d,a,m:-1,0b0001100:lambda d,a,m:d,0b0110000:lambda d,a,m:a,0b1110000:lambda d,a,m:m,0b0001101:lambda d,a,m:~d,0b0110001:lambda d,a,m:~a,0b1110001:lambda d,a,m:~m,0b0001111:lambda d,a,m:-d,0b0110011:lambda d,a,m:-a,0b1110011:lambda d,a,m:-m,0b0011111:lambda d,a,m:d+1,0b0110111:lambda d,a,m:a+1,0b1110111:lambda d,a,m:m+1,0b0001110:lambda d,a,m:d-1,0b0110010:lambda d,a,m:a-1,0b1110010:lambda d,a,m:m-1,0b0000010:lambda d,a,m:d+a,0b1000010:lambda d,a,m:d+m,0b0010011:lambda d,a,m:d-a,0b1010011:lambda d,a,m:d-m,0b0000111:lambda d,a,m:a-d,0b1000111:lambda d,a,m:m-d,0b0000000:lambda d,a,m:d&a,0b1000000:lambda d,a,m:d&m,0b0010101:lambda d,a,m:d|a,0b1010101:lambda d,a,m:d|m}
def s16(x): return x&0xffff
class HackMachine:
 def __init__(self,words): self.rom=words; self.ram=[0]*32768; self.a=self.d=self.pc=0; self.key=0
 def step(self):
  if not 0<=self.pc<len(self.rom): self.pc=0; return
  ins=self.rom[self.pc]; old_a=self.a; self.pc+=1
  if ins>>15==0: self.a=ins&0x7fff; return
  comp=(ins>>6)&0x7f; dest=(ins>>3)&7; jump=ins&7
  m=self.ram[old_a] if old_a< len(self.ram) else 0
  if old_a==24576: m=self.key
  if comp not in COMP: raise ValueError(f'Unsupported comp bits {comp:07b} at ROM {self.pc-1}')
  out=s16(COMP[comp](self.d,self.a,m)); signed=out if out<32768 else out-65536
  if dest&1 and old_a<24576: self.ram[old_a]=out
  if dest&2: self.d=out
  if dest&4: self.a=out
  take={0:False,1:signed>0,2:signed==0,3:signed>=0,4:signed<0,5:signed!=0,6:signed<=0,7:True}[jump]
  if take: self.pc=old_a

def main():
 p=argparse.ArgumentParser(); p.add_argument('hack',nargs='?',default=str(Path(__file__).with_name('Box.hack'))); p.add_argument('--steps',type=int,default=200000); a=p.parse_args()
 words=[int(x.strip(),2) for x in Path(a.hack).read_text().splitlines() if x.strip()]; machine=HackMachine(words)
 root=tk.Tk(); root.title('Hack Computer — Box Program'); root.geometry('720x560')
 info=tk.Label(root,text='Hold any key inside this window to draw the box. Release to erase it.',font=('Segoe UI',11)); info.pack(pady=8)
 canvas=tk.Canvas(root,width=512,height=256,bg='white',highlightthickness=1,highlightbackground='#777'); canvas.pack(padx=10,pady=8)
 status=tk.Label(root,text='Keyboard: released | Screen: blank',font=('Consolas',10)); status.pack(pady=5)
 running=True
 def draw():
  # Screen memory has 512 x 256 pixels; each word stores 16 horizontal pixels.
  canvas.delete('pixel')
  for row in range(256):
   for word in range(32):
    value=machine.ram[16384+row*32+word]
    if value == 0xFFFF:
     x=word*16; canvas.create_rectangle(x,row,x+16,row+1,fill='black',outline='black',tags='pixel')
    elif value:
     for bit in range(16):
      if value & (1<<(15-bit)):
       x=word*16+bit; canvas.create_rectangle(x,row,x+1,row+1,fill='black',outline='black',tags='pixel')
  status.config(text=f"Keyboard: {'pressed' if machine.key else 'released'} | PC: {machine.pc} | Hold a key to draw")
 def tick():
  if not running:return
  for _ in range(1500): machine.step()
  draw(); root.after(30,tick)
 def down(_): machine.key=65
 def up(_): machine.key=0
 root.bind('<KeyPress>',down); root.bind('<KeyRelease>',up); root.focus_force()
 def close():
  nonlocal running; running=False; root.destroy()
 root.protocol('WM_DELETE_WINDOW',close); tick(); root.mainloop()
if __name__=='__main__': main()
