# Stone Bot - Chatbot para Integração com o WhatsApp

Bem-vindo ao projeto Stone Bot! O Stone Bot é um chatbot integrado ao WhatsApp, projetado para filtrar consultas de atendimento ao cliente e orientar o fluxo de vendas. Abaixo, explicaremos como configurar e executar este projeto.

## Visão Geral do Projeto

O Stone Bot oferece as seguintes funcionalidades principais:

- **Integração com o WhatsApp:** O Stone Bot está integrado ao WhatsApp, permitindo interagir com clientes nesta popular plataforma de mensagens.

- **Filtragem de Atendimento ao Cliente:** Ele filtra consultas de atendimento ao cliente e as direciona para os agentes ou respostas apropriados.

- **Orientação no Fluxo de Vendas:** O Stone Bot ajuda a orientar potenciais clientes por meio do processo de vendas, respondendo a perguntas e fornecendo informações.

## Pré-requisitos

Antes de poder executar o projeto Stone Bot, certifique-se de ter os seguintes pré-requisitos instalados em seu sistema:

1. **Node.js:** Verifique se você possui o Node.js instalado, versão 18 ou superior. Você pode baixá-lo em [Node.js Official Website](https://nodejs.org/).

2. **Venom Bot:** Você precisa ter o Venom Bot instalado com uma versão mínima de 5.0.20. Venom é uma biblioteca para automatizar mensagens no WhatsApp. Você pode instalá-lo usando o npm com o seguinte comando:

   ```sh
   npm install -g venom-bot@5.0.20
   ```

3. **Dispositivo Móvel Habilitado para WhatsApp:** Você precisará de um dispositivo móvel com WhatsApp instalado e disponível para escanear o código QR para autenticação.

## Configurando e Executando o Projeto

Siga estas etapas para configurar e executar o projeto Stone Bot:

### 1. Clone este Repositório

Clone este repositório para o seu ambiente local usando o seguinte comando:

```sh
git clone https://github.com/seu-nome-de-usuario/stone-bot.git
```

Substitua `seu-nome-de-usuario` pelo seu nome de usuário no GitHub e `stone-bot` pelo nome do repositório.

### 2. Instale as Dependências do Projeto

Navegue até o diretório do projeto e instale as dependências do projeto usando o npm:

```sh
cd stone-bot
npm install
```

### 3. Inicie o Stone Bot

Para iniciar o Stone Bot, use o seguinte comando npm:

```sh
npm start
```

Este comando iniciará o processo de login no WhatsApp. Use seu dispositivo móvel para escanear o código QR exibido no terminal para autenticação.

### 4. Execução Permanente (Opcional)

Para garantir que o Stone Bot seja executado continuamente, mesmo depois de fechar o terminal, você pode usar um gerenciador de processos como o PM2. Se você não tiver o PM2 instalado, pode instalá-lo globalmente usando o npm:

```sh
npm install -g pm2
```

Em seguida, inicie o Stone Bot usando o PM2:

```sh
pm2 start npm --name "stone-bot" -- start
```

Isso executará o Stone Bot como um processo em segundo plano, e você pode gerenciá-lo com comandos PM2.

## Suporte e Feedback

Se você encontrar algum problema ou tiver dúvidas sobre como configurar ou executar o projeto Stone Bot, não hesite em nos contatar. Estamos aqui para ajudar!

```

Este README revisado fornece uma visão geral do projeto Stone Bot, suas funcionalidades e instruções detalhadas sobre como configurar e executar o projeto. Substitua `seu-nome-de-usuario` e `stone-bot` pelos valores apropriados do seu nome de usuário no GitHub e nome do repositório. Se você tiver mais perguntas ou precisar de assistência adicional, por favor, fique à vontade para perguntar!
