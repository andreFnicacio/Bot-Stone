let {PythonShell} = require('python-shell');
const venom = require('venom-bot');

venom
  .create()
  .then((c) => {
    qttTarefas(c)
    allExecutions(c)
});

function qttTarefas(client) {
  console.log('invocando funcao da tarefa');
}

function allExecutions(client) {
  console.log('iniciando all exec')
  PythonShell.run('scripts/all_execution.py', null, function (err, results) {
      if (err) throw err;  
      client
      .sendFile(
      contact,
      'reports/auditorias_thaylla.xlsx',
      'Execuções',
      'See my file in xlsx'
      )
      .then((result) => {
       console.log('Result: ', result);
      })
      .catch((erro) => {
      console.error('Erro ao enviar mensagem: ', erro);
     });
  });
}

module.exports = {qttTarefas,allExecutions}
