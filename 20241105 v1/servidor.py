from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

# Worker para gerenciar a comunicação com o cliente
def conexao_cliente(cliente_socket, endereco_cliente):
    print(f'Conexão estabelecida com o {endereco_cliente}')

    # Envia uma mensagem para o cliente
    cliente_socket.send('Olá, cliente!'.encode())

    def handle_receive():
        while True:
            try:
                mensagem = cliente_socket.recv(1500).decode('utf-8')
                if mensagem:
                    print(f'Mensagem recebida do cliente ({endereco_cliente}): {mensagem}')
            except:
                print(f'Conexão com o {endereco_cliente} perdida')
                cliente_socket.close()
                break
            
    def handle_send():
        while True:
            mensagem = input('Digite uma mensagem para o cliente: ')
            cliente_socket.send(mensagem.encode('utf-8'))

    Thread(target=handle_receive).start()
    Thread(target=handle_send).start()

# Cria o socket servidor
server_socket = socket(AF_INET, SOCK_STREAM)

# Liga o servidor ao endereço IP e porta
server_socket.bind(('127.0.0.1', 8000))

# Coloca o servidor em modo de escuta
server_socket.listen()
print('Aguardando por novas requisiçõse na porta 8000')



# Ficar esperando por novas conexões de diferentes clientes
while True:
    # Aceita a conexão
    cliente_socket, endereco_cliente = server_socket.accept()
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()

    