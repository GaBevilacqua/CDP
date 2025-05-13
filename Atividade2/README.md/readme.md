=> INICIAR SERVIDOR

    "python server/server_main.py"

    Esse código inicia o servidor 


=>INICIAR USUÁRIO

    python -m client.client_main --username admin --password admin123 --mode RR

    Esse código inicia o cliente, onde depos do "--username" coloca o usuário de um dos usuários JSON, o mesmo para "--password" para a senha
    A parte do "--mode" o usuário definie entre os três tipos de usuários par R, RR ou RRA

=> Prompt

    Depois de em um terminal ligar o sevidor e no outro o usuário, masta seguir os passos para atualizar a master que está nas opções do prompt

=> Master

    Após isso a master é atualizada, em tese deveria atualizar a slave, mas está tendo algum problema ainda.

=> sync e server

    No arquivo gerado pelo código surgem fora da pasta o "sync" que mostra os timestamps e o "server" que mostra as atualizações do servidor