# Projeto P2P

Este projeto é uma implementação de um sistema de comunicação **Peer-to-Peer (P2P)**, que permite o compartilhamento e troca de dados diretamente entre dispositivos conectados sem a necessidade de um servidor centralizado. O sistema visa oferecer um ambiente seguro e eficiente para transferência de arquivos e troca de mensagens entre pares.

## Índice
- [Projeto P2P](#projeto-p2p)
  - [Índice](#índice)
  - [Descrição](#descrição)
  - [Funcionalidades](#funcionalidades)
  - [Tecnologias Utilizadas](#tecnologias-utilizadas)
  - [Instalação](#instalação)
  - [Como Execuatar](#como-executar)
---

## Descrição
O **novo_p2p** foi desenvolvido com o objetivo de explorar o conceito de redes descentralizadas, permitindo que usuários se conectem diretamente uns aos outros. Esse tipo de arquitetura é amplamente utilizado em sistemas de compartilhamento de arquivos e pode ser aplicado em soluções de mensagens instantâneas, redes sociais e mais.

## Funcionalidades
- **Conexão entre pares**: Permite que usuários conectem seus dispositivos diretamente, sem a necessidade de um servidor central.
- **Transferência de Arquivos**: Compartilhe arquivos de forma segura e rápida entre os pares.
- **Mensagens Instantâneas**: Troque mensagens com outros usuários conectados à rede.
- **Conexão Segura**: Utilização de criptografia para proteger os dados trocados.

## Tecnologias Utilizadas
- **Linguagem de Programação**: Python
- **Bibliotecas**:
  - socket
  - threading
  - os
  - sys
  - cryptography
  - argparse
  - time
  - json
  - hashlib
  - base64
  - select
  - logging

## Instalação

1. **Clone o Repositório:**
    ```bash
    git clone https://github.com/astromar2187/novo_p2p.git>
    ```
2. **Navegue para o diretório do projeto:**
    ```bash
    cd novo_p2p
    ```
3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## Como Executar

1. **Inicie o programa:**
    ```bash
    python main.py
    ```
2. **Configuração da Conexão:**
   - Após iniciar, o sistema solicitará a configuração do IP e da porta para estabelecer uma conexão P2P com outro dispositivo.
3. **Transferência de Arquivos/Mensagens:** 
   - Utilize a interface para escolher entre envio de mensagens ou arquivos.
4. **Encerramento da Conexão:** 
   - Para encerrar, finalize o processo no terminal ou na interface de usuário, caso exista.
