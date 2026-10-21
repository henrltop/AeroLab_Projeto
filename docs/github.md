# Publicar no GitHub

Esta pasta já contém README, fontes, firmware, CAD, documentação, `.gitignore` e uma rotina de testes para GitHub Actions. Nenhum repositório remoto foi criado ou acessado.

## Passos

1. Extraia o ZIP e abra a pasta `AeroLab_Projeto` no terminal.
2. Confira os arquivos, inclusive as três fotos originais do sensor e os materiais históricos que deseja tornar públicos.
3. Crie um repositório vazio na sua conta GitHub. Não preencha aqui nome de conta ou endereço por suposição.
4. Execute:

```sh
git init
git add .
git status
git commit -m "Adiciona projeto AeroLab: ESP32, painel, CAD e roteiro"
git branch -M main
```

5. Use a URL real fornecida pelo GitHub para adicionar o remoto:

```sh
git remote add origin URL_REAL_DO_REPOSITORIO
git push -u origin main
```

Substitua o argumento `URL_REAL_DO_REPOSITORIO`; ele é uma indicação, não um endereço válido. Autentique usando seu método normal; não coloque tokens em arquivos.

## Vídeo

O conteúdo de `video/entrada/` e `video/saida/` fica fora do Git por padrão. O roteiro, storyboard, configurações e visuais leves são versionados. Compartilhe gravações grandes com o agente local por outra pasta ou use Git LFS se decidir versioná-las.

Depois de publicar, preencha `github_url` em `video/config.json`. Só então gere o QR code com essa URL e confirme o destino. Não há QR code fictício neste pacote.

## Licença

Não foi adicionado arquivo LICENSE porque Henrique ainda não escolheu uma licença. A presença de arquivos no GitHub, por si só, não define uma licença de reutilização. Os esquemas históricos e o material gerado com assistência de IA estão identificados no inventário.

## Atualização de arquivos derivados

Depois de editar o firmware, rode `python3 tools/atualizar_trechos.py`. Depois de editar o painel, rode `node web/build.cjs`. Ao terminar mudanças intencionais, rode `python3 tools/verificar_manifesto.py --gerar` e depois `python3 tools/verificar_manifesto.py`.
