# Envio de Mensagens em Massa via API WhatsApp

> **README.md gerado pelo ChatGPT (OpenAI – modelo GPT-4o).  
> Este conteúdo foi customizado e revisado pelo autor do projeto para o uso específico nesta automação.**

---

## 📄 Sobre este projeto

Este script Python foi desenvolvido para **trabalhar integrado a uma API específica de envio de mensagens via WhatsApp** — normalmente rodando localmente ou em nuvem, já autenticada e com acesso à sua sessão de WhatsApp.

🔗 **Importante:**  
- **A lógica de envio (requisição HTTP/POST)** está implementada para uma determinada API de referência.
- Se você **possui outra solução de API** (Ex: Z-Api, WppConnect, etc.), **pode facilmente adaptar o bloco de envio** do script para o formato esperado pela sua plataforma (ajustando o endpoint, headers e payload).
- **Se deseja usar a mesma API do autor**, basta **solicitar o acesso** para integração, conforme as instruções do projeto.

---

## ⚙️ Requisitos

- Python 3.8+
- Um servidor/instância autenticada no WhatsApp, com a API exposta (Ex: via webhook, instância local/ngrok, ou servidor do autor)
- Arquivo `.env` com credenciais e caminhos dos arquivos de contatos e mensagens
- Arquivo `numeros.json` contendo a lista de destinatários
- Arquivo `mensagens.json` contendo os textos e ids das mensagens a serem enviadas

---

Claro! Vou organizar e formatar seu texto para README.md, mantendo tudo claro, com blocos de código corretos, títulos e espaçamentos apropriados. Veja como fica:

````md
## 📦 Instalação e dependências

No terminal:

```bash
pip install requests python-dotenv
# ou
pip install -r requirements.txt
````

---

## 📁 Configuração dos arquivos

### `.env`

Preencha o arquivo `.env` (na raiz do projeto):

```
API_KEY=sua_key_da_api_aqui
WTT_API_URL=http://xxx.0.0.1:xxx/xxxx/xxxx/xxxx
MENSAGENS_PATH=mensagens.json
NUMEROS_PATH=numeros.json
```

---

### `numeros.json`

Deve ser uma lista de objetos `{nome: telefone}`:

```json
[
    {"João Silva": "5511999999999"},
    {"Maria Souza": "5511978888888"}
]
```

---

### `mensagens.json`

Formato com `id` e `texto`:

```json
[
    {"id": 1, "texto": "Olá, aproveite nossa oferta."},
    {"id": 2, "texto": "Promoção válida só hoje!"}
]
```

---

## 🚦 Fluxo básico

* O script lê todos os contatos e mensagens.
* Para cada contato, sorteia (ou intercala) uma mensagem, envia via API e loga o resultado.
* Entre cada envio, espera 5 segundos.
* A cada 50 envios, aguarda 2 minutos (antispam).
* Gera `saida_envios.json` listando cada envio, mensagem e status (salve esse arquivo se necessitar).

---

## 🛠️ Adaptando para outra API

Se sua infraestrutura usa uma API própria ou diferente, basta modificar o trecho do código abaixo para adequar ao novo endpoint/payload, mantendo toda a lógica de leitura, sorteio e geração de relatório:

```python
response = requests.request("POST", URL_ENVIO, headers=headers, data=payload)
```

Adapte:

* O endereço da API (`URL_ENVIO`)
* O header (`headers`)
* O formato do corpo (`payload`)

Se precisar de ajuda na adaptação para outra API ou quiser acesso à API do autor, entre em contato conforme instruções deste repositório.

---

## 👉 Execução

No terminal:

```bash
python main.py
```

Acompanhe os logs no terminal para saber o status de cada envio!

---

## 🗂️ Saída

O arquivo `saida_envios.json` terá a seguinte estrutura:

```json
[
  {
    "nome": "João Silva",
    "numero": "5511999999999",
    "mensagem_id": 2,
    "mensagem_texto": "Promoção válida só hoje!",
    "status": "enviado"
  }
]
```

---

## ⚠️ Cuidados e Ética

* Não utilize este script para envio de spam, publicidade abusiva ou qualquer ação ilícita.
* O abuso de automação pode gerar bloqueios do WhatsApp.
* Este projeto é uma ferramenta para automação útil, ética e autorizada.

---

## 🧑‍💻 Autor e créditos

MysteryXmon - Uso liberado

