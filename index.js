const nodemailer = require('nodemailer');
const fs = require('fs');
const venom = require('venom-bot');
const pm2 = require('pm2');

require('dotenv').config();

venom.create({
  session: 'PRODUCTION_DEPLOY', //name of session
  multidevice: true // for version not multidevice use false.(default: true)
})
.then((client) => start(client))
.catch((error) => console.error('Error initializing WhatsApp bot:', error));

function start(client) {
  // Event listener for incoming messages

  client.onMessage(async (message) => {
    // Process the received message and send a response
    const response = processMessage(message.body, message.from);
0
    if (message.body == "1" || message.body == "2" || message.body == "3"  && message.isGroupMsg === false){

      const filePath = 'data.json';   
      const jsonData = readJsonFile(filePath);        
      jsonData.total_access += jsonData.total_access + 1;
      writeJsonFile(filePath, jsonData)      

      client.sendText(message.from, `Acesse o link abaixo para iniciar o atendimento com nosso vendedor especialista: \n \n ${response}`).then(() => {
        console.log('Acesse o link para iniciar o atendimento');  
      });    
    } else if (message.body == "/report"  && message.isGroupMsg === false ){

      const response = await sendEmailWithAttachment();

      client.sendText(message.from, response).then(() => {
        console.log('Função de email gerada!');  
      });      
    }   
  });
  console.log('WhatsApp bot is running. Ready to receive messages!');
}

function processMessage(message,NUMBER_from) {

  // Example usage
  const filePathFirstSquadOdd = 'odd_or_even_FIRST_squad.json'; 
  const filePathSecondSquadOdd = 'odd_or_even_SECOND_squad.json';   
  const filePathThirdSquadOdd = 'odd_or_even_THIRD_squad.json';     

  const filePath = 'data.json';   

  const jsonData = readJsonFile(filePath);   

  const jsonOddFirstSquad = readJsonOddFile(filePathFirstSquadOdd);  

  const jsonOddSecondSquad = readJsonOddSecondFile(filePathSecondSquadOdd);    

  const jsonOddThirdSquad = readJsonOddSecondFile(filePathThirdSquadOdd);      



  console.log(message)
  if (message === "1") {
    if (NUMBER_from.includes("5527")){
      if (jsonOddFirstSquad.odd == "1"){

        jsonOddFirstSquad.odd = "2";
        writeSquadJsonFile(filePathFirstSquadOdd, jsonOddFirstSquad);

        jsonData.seller_erlandio += jsonData.seller_erlandio + 1;
        writeJsonFile(filePath, jsonData);        

        return 'https://x.gd/AeXGu';              
      }else if (jsonOddFirstSquad.odd == "2"){

        jsonOddFirstSquad.odd = "1";
        writeSquadJsonFile(filePathFirstSquadOdd, jsonOddFirstSquad);

        jsonData.seller_leo += jsonData.seller_leo + 1;
        writeJsonFile(filePath, jsonData);  

        return 'https://x.gd/UzFNc';
      }
    }else{
      process.env.PHOTO_PATH = './stone.jpeg';
      return 'https://x.gd/p3DBp';
    }
  } else if (message === "2") {
    if (jsonOddSecondSquad.odd == "1"){

      jsonOddSecondSquad.odd = "2";
      writeSquadJsonFile(filePathSecondSquadOdd, jsonOddSecondSquad);

      jsonData.seller_carlos += jsonData.seller_carlos + 1;
      writeJsonFile(filePath, jsonData); 

      return 'https://x.gd/mnAWK';      
    }else if (jsonOddSecondSquad.odd == "2"){
      jsonOddSecondSquad.odd = "1";
      writeSquadJsonFile(filePathSecondSquadOdd, jsonOddSecondSquad);

      jsonData.seller_rebecca += jsonData.seller_rebecca + 1;
      writeJsonFile(filePath, jsonData); 

      return 'https://x.gd/XFRrU';
    }    
  } else if (message === "3") {
    if (jsonOddThirdSquad.odd == "1"){

      jsonOddThirdSquad.odd = "2";
      writeSquadJsonFile(filePathThirdSquadOdd, jsonOddThirdSquad);

      jsonData.seller_carlos += jsonData.seller_carlos + 1;
      writeJsonFile(filePath, jsonData); 

      return 'https://x.gd/mnAWK';      
    }else if (jsonOddThirdSquad.odd == "2"){
      
      jsonOddThirdSquad.odd = "1";
      writeSquadJsonFile(filePathThirdSquadOdd, jsonOddThirdSquad);

      jsonData.seller_rebecca += jsonData.seller_rebecca + 1;
      writeJsonFile(filePath, jsonData); 

      return 'https://x.gd/XFRrU';
    }      
  } else if (message === "/report") {
    const dataObject = {
      total: jsonData.total_access,
      carlos: jsonData.seller_carlos,
      rebecca: jsonData.seller_rebecca,
      erlandio: jsonData.seller_erlandio,
      leo: jsonData.seller_leo
    };

    const random_time_travel = timeTravel()
    
    const filePathReport = 'report_by_bot.csv';
    const verify_report_generate = writeObjectToCSV(filePathReport, dataObject)
    const true_path =  verify_report_generate != false ? filePathReport : 'Message: sem dados';

    return true_path;
  }
}

// Function to read JSON data from the file
function readJsonFile(filePath) {
  try {
    const data = fs.readFileSync(filePath);
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}

function readJsonOddFile(filePath) {
  try {
    const data = fs.readFileSync(filePath);
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}

function readJsonOddSecondFile(filePath) {
  try {
    const data = fs.readFileSync(filePath);
    return JSON.parse(data);
  } catch (error) {
    return {};
  }
}


function writeSquadJsonFile(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}


function writeJsonFile(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}



function convertObjectToCSV(object) {
  const header = Object.keys(object).join(',') + '\n';
  const values = Object.values(object).join(',') + '\n';
  return header + values;
}

function writeObjectToCSV(filePath, object) {
  const csvData = convertObjectToCSV(object);

  fs.writeFile(filePath, csvData, 'utf8', (err) => {
    if (err) {
      console.error('Error writing to the file:', err);
      return false
    } else {
      console.log('Data written to the CSV file successfully.');
      return filePath;
    }
  });
}

function getTimeStamp() {
  return Math.floor(Date.now() / 1000); // Divide by 1000 to get the timestamp in seconds
}

// Function to travel through time and get the current date in timestamp format
function timeTravel() {
  const timestamp = getTimeStamp();
  console.log('Current Timestamp:', timestamp);
  return timestamp;
}

const emailConfig = {
  user: 'nicaciodagga@gmail.com',
  pass: 'agxzxrrqxnpkbkvd'
};

// Function to send email with attachment
async function sendEmailWithAttachment() {
  try {
    // Create a transporter using the Gmail SMTP service
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: emailConfig.user,
        pass: emailConfig.pass
      }
    });

    // Replace the following with recipient email and subject
    const mailOptions = {
      from: emailConfig.user,
      to: 'comercial.stoneselect@gmail.com',
      subject: 'Envio automatico bot: Analise de uso',
      text: 'Olá,tudo bem ? Segue a documentação requisitada pelo bot',
      attachments: [
        {
          filename: 'report_analitics_bot.csv', // Replace with the name of the file you want to attach
          content: fs.createReadStream('/home/andre/Documentos/bot-compose/report_by_bot.csv') // Replace with the path to your file
        }
      ]
    };

    // Send the email
    const info = await transporter.sendMail(mailOptions);
    console.log('Email sent:', info.response);
    return 'Relatorio enviado com sucesso! Por favor, acesse o email [Stone] para verificação de recebimento.';
  } catch (error) {
    console.error('Error sending email:', error);
    return 'Relatorio não foi gerado por questões tecnicas. Entrar em contato com o desenvolvedor.';
  }
}

// Schedule a restart every 60 minutes
function scheduleRestart() {
  const intervalInMilliseconds = 60 * 60 * 1000; // 60 minutes in milliseconds

  setInterval(() => {
    console.log('Scheduled restart...');
    pm2.restart('npm', (err) => {
      if (err) {
        console.error('Error restarting PM2 process:', err);
      } else {
        console.log('PM2 process restarted successfully.');
      }
    });
  }, intervalInMilliseconds);
}

// Call the scheduleRestart function to start the scheduled restarts
scheduleRestart();
