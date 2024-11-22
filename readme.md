# Baixe Imagens do google com esse projeto

## Objetivos:

O objetivo desse projeto é que a partir de determinado termo, você possa baixar o tanto de imagens que você quiser,
relacionado a ele

## Como executar

Para executá-lo é preciso ter o python instalado, caso não tenha, baixe aqui: https://www.python.org/downloads/

Após instalar o python, de preferência execute o projeto em uma maquina virtual, para criar uma com o python digite:

```console
python -m venv .venv
```

Após a criação da mesma, no terminal do Windows digite:

```console
.\.venv\Scripts\activate
```

Certifique-se de que após executar o comando acima, apareça antes do endereço do cmd, o nome da maquina virtual criada.

Para instalar os pacotes na maquina virtual execute:

```console
pip install -r requirements.txt
```

Após ter instalado tudo, execute o arquivo principal [main.py](main.py)

```console
python main.py
```

Digite o que está pedindo no CMD, e então espere o script ser executado, após a execução será criada uma pasta chamada
imagens, onde sera separado em subdiretórios, com o nome do termo pesquisado, dentro delas estarão as imagens baixadas
