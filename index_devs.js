const { Client, Buttons, LocalAuth, List  } = require('whatsapp-web.js');
const qrcode = require("qrcode-terminal");
const client = new Client({authStrategy: new LocalAuth()});

const productsList = new List(
  "Here's our list of products at 50% off",
  "View all products",
  [
    {
      title: "Products list",
      rows: [
        { id: "apple", title: "Apple" },
        { id: "mango", title: "Mango" },
        { id: "banana", title: "Banana" },
      ],
    },
  ],
  "Please select a product"
);


client.initialize();

client.on('qr', (qr) => {
  // Generate and display QR code to authenticate WhatsApp session
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('WhatsApp Bot is ready!');
});


client.on('message', message => {
  console.log('message from', message.from)
  if (message.body === "/button") {
    const url = 'https://jovemnerd.com.br/';
    
    const preview = {
      link: url,
      title: 'Example Website',
      description: 'This is an example website.',
      thumbnail: 'https://example.com/thumbnail.png',
    };

    message.reply(preview);

  }
});
