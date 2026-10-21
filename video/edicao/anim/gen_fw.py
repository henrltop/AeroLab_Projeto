#!/usr/bin/env python3
"""Gera pages/fw.js com as linhas EXATAS do firmware (numeração real, 1-based)."""
import json, pathlib
SRC = pathlib.Path('/home/claude/edit/proj/firmware/Ventoinha_Percentual_RPM/Ventoinha_Percentual_RPM.ino')
lines = SRC.read_text(encoding='utf-8').split('\n')
out = pathlib.Path(__file__).parent / 'pages' / 'fw.js'
out.write_text('// gerado por gen_fw.py a partir de ' + SRC.name + '\nwindow.FW = ' +
               json.dumps({str(i + 1): l.rstrip('\r') for i, l in enumerate(lines)}, ensure_ascii=False) + ';\n',
               encoding='utf-8')
print('ok', len(lines), 'linhas ->', out)
