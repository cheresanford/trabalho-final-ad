# Simulaçãozinha de AD (em pythonzinho.)

## Alunos
- Carlos Henrique Luiz Correa Filho 118029467
- Pedro Gabriel Morsch de Freitas 118050248

## Documentação do código
- Deixamos o código em si bem comentadinho, então deixaremos essa documentação lá no próprio código :)
- É necessário instalar os pacotes simpy e numpy para rodar esse programa!
- O simpy é uma biblioteca que permite a fácil simulação de eventos discretos
- O numpy nos dá algumas facilidades como calcular a esperança, variância, etc.

## Descrição do Problema

Este experimento consiste em simular uma rede aberta de filas com três servidores (S1, S2 e S3), cada um com uma fila de espera ilimitada. Ele funciona assim:

1. **Chegadas:**  
   O processo de chegada de jobs ao sistema segue um processo de Poisson com taxa λ = 2 jobs/seg, resultando em tempos entre chegadas exponenciais com média 0,5 s.

2. **Servidores e Encaminhamento:**
   - Cada job, ao chegar, é primeiro atendido por S1.  
   - Após completar o serviço em S1, o job segue para S2 ou S3 com igual probabilidade (0,5 cada).
   
3. **Comportamento no S2:**
   - Ao sair de S2, o job tem 20% de chance de retornar ao final da fila de S2 e receber outro atendimento. Isso pode acontecer repetidas vezes (potencialmente infinito).  
   - Quando finalmente não retorna (80% de chance), o job deixa o sistema.
   
4. **Comportamento no S3:**
   - Ao sair de S3, o job sai determinística e definitivamente do sistema (sem retornos).

## Cenários de Tempos de Serviço

Foram simuladas três situações distintas em relação aos tempos de serviço:

1. **Determinístico:**  
   - S1 = 0,4 s  
   - S2 = 0,6 s  
   - S3 = 0,95 s

2. **Uniforme:**  
   - S1 ~ Uniforme(0,1; 0,7) s  
   - S2 ~ Uniforme(0,1; 1,1) s  
   - S3 ~ Uniforme(0,1; 1,8) s

3. **Exponencial:**  
   - S1 ~ Exp(média=0,4 s)  
   - S2 ~ Exp(média=0,6 s)  
   - S3 ~ Exp(média=0,95 s)

## Metodologia da Simulação

- Foram gerados um total de 250.000 jobs, dos quais os primeiros 10.000 foram descartados (warm-up) para garantir que o sistema atingisse uma condição mais próxima do regime estacionário.
- Decidimos aumentar de 20.000 pra o valor acima pois notamos que as execuções estavam com uma oscilação bem grande, então fizemos isso para atenuar.
- Após o período de aquecimento, as métricas (tempo médio no sistema e desvio padrão desse tempo) foram coletadas dos outros jobs.
- O tempo no sistema de um job é o intervalo desde sua chegada até sua saída definitiva do sistema (após S2 ou S3).

## Resultados Obtidos

As tabelas abaixo mostram 3 exemplos de execução de simulação:

| Cenário       | Tempo Médio (s) | Desvio Padrão (s) |
|---------------|-----------------|-------------------|
| Determinístico| 6,7365          | 7,3531            |
| Uniforme      | 8,1728          | 9,4133            |
| Exponencial   | 11,5228         | 12,6127           |


| Cenário       | Tempo Médio (s) | Desvio Padrão (s) |
|---------------|-----------------|-------------------|
| Determinístico| 7.1666          | 8.0993            |
| Uniforme      | 8.2563          | 9,4133            |
| Exponencial   | 12.1801         | 13.9512           |


| Cenário       | Tempo Médio (s) | Desvio Padrão (s) |
|---------------|-----------------|-------------------|
| Determinístico| 6.9625          | 7.8043            |
| Uniforme      | 8.6554          | 10.3326           |
| Exponencial   | 13.2444         | 16.6529           |

**Análise dos Resultados:**

- Observa-se que o cenário **determinístico** resulta no menor tempo médio no sistema. Isso ocorre porque a ausência de variabilidade reduz a incerteza nos tempos de atendimento, facilitando o fluxo dos jobs.
  
- O cenário **uniforme** apresenta um aumento tanto do tempo médio quanto do desvio padrão em relação ao determinístico. A presença de variabilidade moderada (uniforme) faz com que ocasionalmente ocorram atendimentos mais longos, aumentando a chance de formação de filas e, consequentemente, o tempo no sistema.

- O cenário **exponencial** resulta nos maiores tempos médios e desvios padrão. A distribuição exponencial possui caudas longas, o que significa que ocasionalmente ocorrerão tempos de serviço muito maiores que a média. Esses eventos extremos provocam filas mais longas e aumentam significativamente tanto a média quanto a variabilidade do tempo no sistema.

## Conclusões

# Impacto da variância no tempo médio
A simulação mostra claramente aquilo que foi comentado em aula sobre a variância afetar os tempos médios de atendimento. Os resultados obtidos (exponencial > uniforme > determinístico) confirmam essa predição. Achamos também [este artigo](https://medium.com/luizalabs/a-influencia-da-variabilidade-na-eficiencia-de-fluxo-b8af69e31079) que fala um pouco a respeito desse tema.

# Qualidade de serviço
Esses resultados deixaram bem mais claro também a importância de ter sob controle a variabilidade nos tempos de serviço para poder, cof cof, **AVALIAR** e **MODELAR** bem um sistema, que é algo bem relevante na vida real.

# Dúvida
Tivemos uma curiosidade não confirmada entretanto, será que é por isso que no trânsito nós vemos aqueles engarrafamentos sem motivo aparente? Por conta da "variância" de cada motorista? Uns aceleram mais rápidos, outros freiam mais rápido, etc... Assim se formando essas "caudas" mais longas no trânsito :)


