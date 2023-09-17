const { exec } = require('child_process');
const venom = require('venom-bot');
require('dotenv').config();

venom.create({
  session: 'STONE', //name of session
  multidevice: true // for version not multidevice use false.(default: true)
})
.then((client) => start(client))
.catch((error) => console.error('Error initializing WhatsApp bot:', error));

function start(client) {
  // Event listener for incoming messages
  client.onMessage((message) => {
    console.log('Received message:', message);

    // Process the received message and send a response
    const response = processMessage(message.body, message.from);

    if (message.body == "1" || message.body == "2" || message.body == "3"){
      console.log(response);
      client.sendImage(message.from, '', '', `Acesse o link abaixo para iniciar o atendimento com nosso vendedor especialista: \n ${response}`).then(() => {
        console.log('Acesse o link para iniciar o atendimento');  
      });
      client.sendLinkPreview(message.from, response, 'Iniciar Atendimento Stone').then((result) => {
        console.log('Message sent successfully');
      }).catch((error) => {
        console.log('Error sending message:', error);
      });       

    } else{
      client.sendText(message.from, response).then(() => {
        console.log(`Sent link message to ${message.from}:`);  
      });      
      
    }   
  });
  console.log('WhatsApp bot is running. Ready to receive messages!');
}

function processMessage(message,NUMBER_from) {
  // Process the received message and return a response
  // Customize this function according to your chatbot's logic
  console.log(message)
  if (message === "1") {
    if (NUMBER_from.includes("5527")){
      if (process.env.MY_VARIABLE == "1"){
        process.env.MY_VARIABLE = "2";
        return 'https://x.gd/8dFYR';      
      }else if (process.env.MY_VARIABLE == "2"){
        process.env.MY_VARIABLE = "1";
        return 'https://x.gd/UzFNc';
      }
    }else{
      return 'https://x.gd/p3DBp';
    }
  } else if (message === "2") {
    return 'https://x.gd/Hsbdz';
  } else if (message === "3") {
    return 'https://x.gd/m9uJD';
  } else {
    return 'Olá, para que eu possa fazer um atendimento mais personalizado poderia me informar a qual grupo de clientes você mais se identifica ?\n*1 - MARMORARIA/DEPOSITO*\n*2 - ARQUITETURA/DESIGNER*\n*3 - CONSUMIDOR FINAL*';
  }
}
