# causp-lock-server

Este repositório contém a API de geração de QR Codes do projeto CAUSP-LOCK.

## Tipos de QR Codes
Há quatro grandes tipos de QR Code:
- **ACCESS**: destinados à entrada e saída, que podem ser CHECK_IN, CHECK_OUT (registrados na memória do ESP32-CAM) ou BI_ACCESS (sem registro, apenas liberação).

- **SYNC**: utilizado para sincronizar o relógio interno do ESP32-CAM com um tempo específico. O nome do QR Code é SET_TIME.

- **CONFIG**: conjunto de QR Codes utilizados para configurar parâmetros e chaves secretas do ESP32-CAM. Para setar as chaves MASTER, ACCESS, SYNC e CONFIG, use os QR Codes SET_MASTER_KEY, SET_ACCESS_KEY, SET_SYNC_KEY e SET_CONFIG_KEY.

- **DEBUG**: utilizados para depuração do ESP32-CAM, o que permite verificar se a leitura dos QR Codes funciona se o dispositivo está sincronizado.

<p align="center">
  <img src="imgs/causp-lock-protocol-HEADER_ENCODING.png" alt="Logotipo do Coletivo Autista da USP (CAUSP)" style="width: 450px;" />
</p>

## Codificação
Os payloads dos QR Codes são divididos em três partes:
- **HEADER**: cabeçalho da mensagem; informa o tipo de QR Code
- **BODY**: corpo da mensagem, contém os dados relevantes à operação
- **HASH**: assinatura digital da mensagem.

O HEADER e o BODY são obrigatórios para todos os tipos de QR Code. Mas, o campo de HASH é opcional nos QR Codes de tipo DEBUG.

<p align="center">
  <img src="imgs/causp-lock-protocol-GENERAL_MESSAGE.png" alt="Logotipo do Coletivo Autista da USP (CAUSP)" style="width: 450px;" />
</p>

A imagem abaixo ilustra a codificação de QR Code do tipo ACCESS, com a operação CHECK_IN (entrada de cliente na sala, com registro no ESP32-CAM), para um usuário fictício.

<p align="center">
  <img src="imgs/causp-lock-protocol-DATA_ENCODING.png" alt="Logotipo do Coletivo Autista da USP (CAUSP)" style="width: 450px;" />
</p>

## Chaves secretas
A criação das assinaturas digitais para os QR Codes demanda uma chave secreta, de tamanho arbitrário. Para facilitar sua criação, o módulo `auth.secret_key` implementa funções de alto nível para facilitar a criação e manipulação dessas chaves em código. Para criar uma chave secreta, importe a classe `SecretKey` do módulo `auth.secret_key` e passe uma string hexadecimal.

```python
>>> from src.auth.secret_key import >>> SecretKey
my_secret_key = SecretKey('aa bb cc dd 12 34 56 78')
```

Para visualizar o conteúdo da chave, pode-se dar um print direto.

```python
>>> print(my_secret_key)
00 00 00 00 00 00 00 00 00 00 00 00 aa bb cc dd 12 34 56 78
```

Note que a chave possui endianness little endian e tamanho fixo de 20 bytes, que é uma decisão de projeto. Se for informada uma quantidade de bytes menor que o tamanho fixo da chave, a classe automaticamente a preenche com zeros à esquerda.

Além disso, a classe pode criar chaves pseudo-aleatórias facilmente. Basta chamar o construtor da classe sem passar argumentos.

```python
>>> random_key = SecretKey()
e7 8c fe 91 5a 88 de 83 50 3b 5e 57 2a ae b9 7a 57 88 10 3d
```

Outra alternativa, sem criar uma classe nova, é chamar diretamente o método estático `generate_key()` da classe `SecretKey`, que retorna uma sequência de `length` bytes pseudo-aleatórios (por padrão, 20 bytes) com endianness `byte_order` (por padrão, `'little'`, de little endian), ambos os parâmetros passados como argumentos argumentos opcionais.


```python
>>> random_key = SecretKey.generate_key()
b'pE\x0f\xcf\xafw!7\x17;\xe3\xbc+\x9d\xfcAY\x16\x0e['
```

Os métodos implementados pelos módulos de codificação e autenticação aceitam tanto os bytes puros quanto uma instância da classe `SecretKey` como argumentos, portanto, não é necessário fazer uma conversão explícita de um tipo para o outro.

## Gerador de QR Codes
A biblioteca `qr_code` permite a geração de QR Codes a partir de dados de alto nível, graças ao módulo `encoder.py` e ao `generator.py`, responsáveis, respectivamente, pela codificação dos dados em bytes puros, para composição do payload do QR Code, e pela geração das imagens `.png` ou `.jpg` dos QR Codes, para uso pelo usuário.

Por exemplo, para criar, um QR Code CHECK_IN, importe os módulos `qr_code.generator`, `qr_code.encoder`, crie uma chave secreta com `SecretKey` ou bytes puros, e crie uma instância da classe `QR_CODE_CHECK_IN`, com os dados, conforme o exemplo abaixo.

```python
from auth.secret_key import SecretKey
from qr_code.generator import *
from qr_code.encoder import *

access_key = SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')

qrcode_check_in = QRCODE_CHECK_IN(
    user_id=2305947582,
    generated_at=datetime(year=2025, month=7, day=17, hour=15, minute=14),
    access_key=SecretKey('85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc')
)
```

Para ver o conteúdo do QR Code gerado, pode-se dar um print nele diretamente.

```python
>>> print(qrcode_check_in)
QR Code Info
action: CHECK_IN
user_id: 2305947582
generated_at: 2025-07-17 15:14:00
access_key: 85 f1 e2 04 ba 63 fe 41 a0 f0 da 37 74 3e 8d 1c 6a f5 33 fc 
payload: 00 89 71 f7 be 68 79 3d 68 56 13 24 e0 34 23 a7 e2 f0 1b 58 b0 17 d3 6b 60 16 f7 36 d3 
```

Para gerar a imagem do QR Code, basta usar o método `save_qrcode` do próprio objeto, passando no argumento `path` o diretório em que a imagem será salva e o nome do arquivo, conforme o exemplo abaixo.

```python
qrcode_check_in.save_qrcode('./test_qrcodes/CHECK_IN.png')
```