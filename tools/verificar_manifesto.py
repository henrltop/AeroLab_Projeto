"""Integridade dos arquivos distribuídos; Python 3, sem dependências."""
from pathlib import Path
import hashlib, json, sys
root = Path(__file__).resolve().parents[1]
target = root / 'MANIFESTO_SHA256.json'
def included(p):
    rel=p.relative_to(root)
    if not p.is_file() or p == target: return False
    if any(x in rel.parts for x in ['.git','__pycache__','node_modules']): return False
    if rel.parts[:2] in [('video','entrada'),('video','saida')]:
        return p.name in ['README.md','.gitkeep']
    return True
actual={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if included(p)}
if '--gerar' in sys.argv:
    target.write_text(json.dumps(actual,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Manifesto gerado: {len(actual)} arquivos.')
else:
    expected=json.loads(target.read_text(encoding='utf-8'))
    missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected))
    changed=sorted(k for k in expected.keys() & actual.keys() if expected[k]!=actual[k])
    for title,items in [('Ausentes',missing),('Novos',extra),('Alterados',changed)]:
        if items: print(title+': '+', '.join(items))
    if missing or extra or changed: sys.exit(1)
    print(f'Integridade conferida: {len(actual)} arquivos.')
