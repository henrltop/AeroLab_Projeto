# Suporte de ventoinha + TCRT5000 — protótipo V1

## Antes de imprimir
Esta é uma primeira versão mecânica gerada a partir das medidas informadas, não um encaixe nem uma leitura óptica já validados fisicamente.

O fundo branco é uma placa pequena do lado oposto ao sensor. A leitura deve alternar entre pá e espaço, não depender de uma marca única. A distância óptica nominal desta V1 é **19,1 mm**. Isso ultrapassa a faixa de 0,2–15 mm com mais de 20% da resposta relativa publicada para o TCRT5000; sua resposta máxima fica perto de 2,5 mm. Portanto, teste primeiro o sensor e um papel branco separados por aproximadamente 19 mm, com a ventoinha entre eles e girada manualmente, DESLIGADA. Confirme contraste e um evento por pá/espaço. Se não houver contraste, imprimir o suporte não corrige a limitação óptica. Não avance o sensor/alvo na trajetória das pás.

Ficha técnica: https://www.vishay.com/docs/83760/tcrt5000.pdf

## O que há nos arquivos
- `stl/00_conjunto_integral_FIXO.stl`: suporte inteiro em uma peça. Encaixe do sensor e alvo ficam na posição radial fixa de 19 mm. Imprimir esta opção OU as cinco peças seguintes, não ambas para a mesma montagem. A versão integral exige suportes de impressão e não tem regulagem após impressa.
- `stl/01_moldura.stl`: encaixe externo da ventoinha e aba de fixação dos braços.
- `stl/02_braco_sensor.stl`: braço frontal, alojamento do sensor e passagem dos terminais.
- `stl/03_braco_alvo_branco.stl`: braço traseiro com área de 16 × 12 mm para o fundo branco.
- `stl/04_espacador_frontal_7mm.stl`: separa o braço frontal da moldura.
- `stl/05_espacador_traseiro_0_6mm.stl`: separa o braço traseiro da moldura.
- `suporte_parametrico.scad`: fonte editável; parâmetros no início. `part="integral"` é o suporte único; `assembly` mostra a montagem modular; `layout` organiza as peças; `exploded` separa as peças visualmente.
- `Previa_Suporte_V1.png`: prévia dos mesmos STLs. A ventoinha e o sensor desenhados são apenas referências; o rotor real e as travessas não foram medidos.
- `verificacao_malhas.json`: verificação geométrica dos STLs.
- `Prompt_para_Claude.md`: requisitos para pedir uma proposta independente ao Claude.

## Medidas e suposições
Unidades: milímetros; escala de impressão 100%.

| Item | Dimensão nesta V1 |
|---|---|
| Ventoinha informada | 58 × 58 × 15 |
| Encaixe interno | 58,8 × 58,8; 0,4 de folga por lado |
| Moldura externa com aba | 65,8 × 84,9 × 18 |
| Abertura do lábio frontal | 56,5 × 56,5 |
| Corpo do sensor informado | 10 × 5 × 5 |
| Cavidade do sensor | 10,4 × 5,4, com face óptica exposta |
| Folga entre face óptica e face frontal da ventoinha | 2 |
| Folga entre alvo e face traseira da ventoinha | 2,1, sem descontar adesivo/papel |
| Distância face óptica → fundo branco | 19,1 |
| Ajuste radial na montagem modular | 14 a 24 do eixo |
| Alvo branco localizado | 16 × 12 |
| Conjunto integral | 65,8 × 84,9 × 31,6 |

A medida informada para o sensor é aproximada e difere do encapsulamento publicado pela Vishay (10,2 × 5,8 × 7). Confirme o corpo real, incluindo as saliências, antes de uma impressão definitiva; os três parâmetros são editáveis. A cavidade desta V1 segue a medida fornecida pelo usuário.

Não foram assumidos espaçamento dos furos originais, número de pás, diâmetro do cubo, travessas, perfil ou posição axial real das pás. Abertura frontal, janela lateral de carga, trajeto dos fios e posição de leitura precisam ser conferidas no componente real.

## Fixação e materiais
Na versão modular:
- Um parafuso M3 × 40, uma porca M3 e duas arruelas para o eixo de montagem dos braços na aba externa. Atravessa braço frontal, espaçador de 7, moldura, espaçador de 0,6 e braço traseiro.
- Os rasgos permitem deslocar os braços radialmente em até 5 mm para cada lado. Alinhe o sensor e o alvo na mesma faixa antes de apertar.
- A moldura possui dois pilotos de 2,8 mm para parafusos M3 curtos na parede superior (+Y), próximos às regiões de canto da carcaça. Servem para prender levemente a carcaça fixa, não para entrar no motor. Use M3 de 6–8 mm, apertando apenas até encostar. Não perfure a ventoinha. Confirmar se essa região da carcaça suporta o contato.
- Para reter o sensor na cavidade com folga, use uma quantidade mínima de silicone neutro removível na lateral do corpo, sem cobrir as janelinhas ou prender as pernas na raiz. Não forçar o encaixe.
- No alvo traseiro, a face voltada para a ventoinha/sensor deve ser branca e fosca. A versão integral pode ser impressa em outra cor e receber adesivo branco só nessa face. A resposta no infravermelho ainda precisa ser testada.

Na versão integral, braços e espaçadores já estão fundidos à moldura; não é necessário o parafuso de montagem dos braços. Os parafusos laterais continuam opcionais para a retenção da ventoinha. A moldura tem uma janela lateral aberta (+X). Deslize a ventoinha por essa janela, acima do lábio de apoio, sem forçar os braços. Abertura livre nominal de entrada: 58,8 de largura e 16,5 de altura. Após inserir, prenda levemente com os parafusos superiores para impedir deslocamento. Não há trava de impacto certificada; avaliar retenção na peça real.

## Impressão sugerida para primeiro teste
- PLA para protótipo de bancada ou PETG, conforme temperatura e aplicação.
- Camada de 0,2; 3–4 perímetros; aproximadamente 25–35% de preenchimento.
- Peças separadas: importar cada STL na orientação fornecida, com a base plana na mesa. Espaçador traseiro de 0,6 equivale a três camadas de 0,2. Os pequenos pilotos horizontais podem exigir limpeza ou ajuste no fatiador.
- Integral: base do braço frontal na mesa, como exportado. São necessários suportes para a moldura suspensa e o braço traseiro; inspecione o fatiamento para não bloquear a cavidade do sensor ou os caminhos dos fios.
- Faça o primeiro ensaio da moldura e do encaixe do sensor antes de imprimir a opção integral. Tolerância de impressora/material pode exigir ajuste dos parâmetros.

## Montagem e contagem
1. Com tudo desligado, deslize a ventoinha pela janela lateral da moldura; o lábio apoia a carcaça frontal.
2. Na versão modular, coloque os dois espaçadores, braços e o parafuso M3. Posicione o sensor no braço frontal com as janelinhas voltadas para o fundo branco. Passe e prenda os fios fora das pás, com alívio de tração.
3. A pequena placa traseira deve coincidir com uma faixa dos espaços entre pás, evitando cubo e travessas fixas. A face branca fica virada para o sensor. O restante da traseira permanece aberto, embora os braços e a placa ainda causem alguma obstrução local.
4. Gire a ventoinha manualmente por uma volta completa, verificando que nada encosta. Valide o contraste com o ESP32 antes de energizar o motor.
5. O código anterior considerava 1 pulso por volta. Na leitura por espaços, altere `PULSOS_POR_VOLTA` para o número de espaços detectados em uma volta completa. Não presuma 1 nem um número de pás desconhecido.
6. Recalibre os limiares do ADC na geometria final. As leituras de papel próximo (3550/77) não garantem os mesmos valores no fundo distante. Conte uma borda por ciclo, não ambas.

## O que foi verificado
Os seis STLs foram renderizados no OpenSCAD e verificados quanto a malha fechada, duas faces por aresta, volume positivo e um único componente conectado por arquivo. Isso verifica o arquivo 3D; não substitui ensaio de encaixe, resistência, fluxo de ar, acesso para montagem ou leitura óptica.
