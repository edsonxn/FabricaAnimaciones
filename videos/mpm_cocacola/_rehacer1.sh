#!/bin/bash
# mpm_cocacola: clips rehechos tras revisar medios_01..06 (24-nov-2026)
cd /c/FabricaAnimaciones
export PYTHONIOENCODING=utf-8
Y=https://www.youtube.com/watch?v=
r(){ python fab.py mpm_cocacola bajar $1 --url $Y$2 --desde $3 2>&1 | grep -E "ok|FALL|scene" | tail -1; }
q(){ python fab.py mpm_cocacola bajar $1 --q "$2" 2>&1 | grep -E "ok|FALL|scene" | tail -1; }
r 1 Hb48mjM7_7Q 0
r 6 S2OuC_-QMUA 33
r 9 u0rQ_7ymRo8 30
r 28 rnpsIe1f84k 55
r 30 nmO5t_RBKzw 67
r 36 o04s4TK8uLU 60
r 41 u0rQ_7ymRo8 12
q 42 "water well drilling rig"
r 61 IUMK2LY3pIs 120
q 70 "soft drink quality control laboratory"
r 73 KwT0tTo-10Q 21
q 74 "tienda de abarrotes Mexico"
q 75 "Mexican corner store"
q 79 "tiendita Mexico refrescos"
r 81 NuteIxJeDUw 29
r 84 S2OuC_-QMUA 120
r 85 zyrzswdZe2g 256
q 91 "rusty nails close up"
r 96 drNnyghVWQ4 541
r 97 hqnUohxXV0I 734
r 99 k5rYCHnVCBs 25
r 110 eDinB9pnzhg 29
r 113 1vKbdAkzOdo 107
