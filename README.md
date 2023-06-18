# Trabalho 2 - 2023/1

## Adne Moretti Moreira - 200013181

Trabalho 2 da disciplina de Fundamentos de Sistemas Embarcados (2023/1)

## 1. Objetivos
O trabalho envolve o desenovlimento do software que efetua o controle completo de um forno AirFyer incluindo ligar/desligar o equipamento, controlar a temperatura, temporização e diferentes modos de alimentos. Especificamente a temperatura do forno é controlada à partir de dois elementos *atuadores*: um resistor de potência de 15 Watts utilizado para aquecer o forno e uma ventoinha que puxa o ar externo (temperatura ambiente) para reduzir a temperatura do sistema. 

Os comandos do usuário do sistema para definir a temperatura desejada serão controlados de três maneiras:
1. Através de botões físicos (encoder rotatório);
2. Botões digitais via Dashboard (UART);
3. Seguindo os tempo e temperaturas pré-definidas para cada tipo de alimento.

**Botões de Entrada**
- Liga/Desliga  
- Inicia/Cancela
- Temperatura +/- (A cada 5 ˚C)  
- Tempo +/- (Minutos)  
- Dial (Para Temperatura/Tempo)

## 2. Instruções de execução

Para execução do projeto, é necessário primeiramente carregar o diretório para a placa, em seguida executar: 

```
cd fse-trabalho-2-2023-1-controle-da-airfryer-AdneMoretti
cd src
```

E para de fato inicar o programa pelo dashboard: 

```
python main.py 1

```
Já pelo encoder: 

```
python main.py 2

```
## 3 . Vídeo de apresentação do trabalho

Segue link para vídeo não listado no youtube que apresenta o programa em execução a partir da dashboard: 

>> https://youtu.be/NsYiqDuFAg8