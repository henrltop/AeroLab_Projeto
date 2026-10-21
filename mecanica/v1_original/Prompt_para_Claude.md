# Projeto: suporte 3D para ventoinha com medição óptica de RPM

Quero que você projete e gere de verdade um modelo 3D imprimível, com STL e arquivo CAD editável/paramétrico. Não quero somente uma imagem conceitual. Use seu próprio julgamento para propor a melhor solução mecânica.

## Objetivo
Unir uma ventoinha e um sensor óptico em um conjunto compacto e rígido, preservando a passagem de ar. Prefiro uma opção de suporte integral em uma única impressão, mas aceito peças de ajuste que se montem como uma unidade se isso melhorar alinhamento, impressão e manutenção. Explique a escolha e, se viável, entregue as duas opções.

## Componentes e medidas fornecidas
- Ventoinha DC de 12 V e dois fios, corpo externo de **58 × 58 × 15 mm** (não assumir que é 60 mm).
- Sensor **TCRT5000 avulso**, corpo medido aproximadamente **10 × 5 × 5 mm**. Tem duas janelinhas lado a lado e quatro pernas. Uma janelinha é o LED emissor infravermelho; a outra é o fototransistor receptor. Ambos ficam no mesmo componente, apontando para a mesma direção.
- As pernas precisam de espaço para passagem e ligação dos fios, sem apertar, cortar ou dobrar na raiz.
- Ainda não medi diâmetro do rotor, diâmetro do cubo central, número de pás, posição axial das pás, travessas fixas ou distância entre furos da ventoinha.
- Não invente essas medidas como fatos. Use parâmetros explícitos e indique o que falta confirmar. Prefira encaixe pela carcaça externa em vez de depender de furos desconhecidos.

## Funcionamento óptico desejado
O método mudou: **não quero depender de uma única marca branca colada no rotor**.
Quero um **pequeno fundo branco sólido, fixo, atrás da região varrida pelas pás**. Na frente, o TCRT5000 deve olhar para esse fundo através dos espaços entre as pás. Quando uma pá passa, ela altera/oculta a reflexão; quando passa um espaço, o fundo branco aparece novamente. O ESP32 deve contar esses eventos para medir RPM.
- O fundo branco deve ocupar só uma pequena região; não tampar toda a traseira nem fechar o fluxo de ar.
- Alinhar os dois elementos ópticos do sensor com o fundo, fora do cubo central e evitando travessas fixas.
- O sensor, alvo, braços, parafusos e fios não podem tocar ou invadir o volume varrido pelo rotor.
- A cor visível não garante contraste no infravermelho: considerar a necessidade de validar a reflexão das pás e do alvo.
- Considerar cada ciclo completo pá/espaço como um evento; não contar as duas bordas como duas rotações. O número de eventos por volta depende do número de pás/espaços reais e deve ser confirmado experimentalmente.

## Restrição óptica que precisa ser avaliada
O TCRT5000 é REFLEXIVO, não um sensor de barreira com emissor de um lado e receptor separado do outro. Não proponha separar as duas janelinhas nem cortar o componente.
A ficha da Vishay informa resposta máxima perto de 2,5 mm e faixa de 0,2 a 15 mm com mais de 20% da resposta relativa, nas condições especificadas. Fonte: https://www.vishay.com/docs/83760/tcrt5000.pdf
A ventoinha já tem 15 mm de profundidade. Sensor na frente + folgas + alvo atrás podem levar a uma distância óptica próxima ou superior a 19 mm. Avalie essa geometria explicitamente e não prometa que funcionará sem teste. Não avance peças para dentro da trajetória das pás para resolver a distância sem medidas reais. Diferencie protótipo mecânico de funcionamento óptico validado e proponha um teste físico simples antes da impressão definitiva.

## Requisitos do modelo
1. Encaixe estável para o corpo de 58 × 58 × 15 mm, com folga de impressão parametrizável.
2. Alojamento do TCRT5000 que preserve as janelinhas e permita saída dos quatro terminais.
3. Ajuste de posição radial e, se possível, distância do sensor, sem peças que possam cair nas pás.
4. Pequena área traseira adequada a PLA branco, adesivo branco ou papel branco fosco, com face voltada para o sensor.
5. Grande região aberta para o ar circular; braços estreitos, mas suficientemente rígidos para não vibrar.
6. Montagem acessível para inserir/remover a ventoinha e o sensor. Uma peça integral também precisa permitir a montagem dos componentes depois de impressa.
7. Preferir impressão FDM simples. Informar orientação, suportes, tolerâncias, parafusos ou outros materiais necessários.
8. Furos, espessuras e encaixes devem existir no CAD; evitar sólidos desconectados ou geometria somente decorativa.
9. Não incluir caixa para ESP32, fonte ou MOSFET nesta versão: não forneci suas dimensões.

## Contexto eletrônico
O sensor já funcionou na bancada com alimentação em 3,3 V, resistor de 220 Ω no emissor, resistor de 10 kΩ no receptor e sinal no GPIO4. Com papel, obtive ADC aproximado 3550 sem reflexão e 77 com reflexão próxima. Esses números não validam a leitura através da ventoinha.
A ventoinha funciona em 12 V. Há controle por MOSFET IRLZ44N, comandado pelo GPIO21. O projeto deste pedido é mecânico; não é necessário refazer a eletrônica.

## Entregas
- Arquivo STL da opção integral e/ou de cada componente necessário à montagem.
- Arquivo CAD paramétrico editável, de preferência OpenSCAD, FreeCAD ou equivalente.
- Prévia fiel à geometria real gerada e vista de montagem/explodida.
- Instruções curtas de impressão e montagem, lista de fixadores e parâmetros principais.
- Verificação das malhas fechadas e de componentes conectados; declarar o que foi checado e o que ainda depende da peça física.
- Explicitar a distância entre face óptica e alvo branco, as folgas em relação à carcaça e as limitações por falta das medidas do rotor.

Faça uma primeira versão com as informações disponíveis, marcando claramente as suposições e sem exigir medidas não essenciais antes de apresentar uma solução revisável.
