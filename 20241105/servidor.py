from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1500).decode()
            if msg: 
                print(f'Mensagem recebida do cliente: {msg}')
                broadcast(msg , client_socket)
            else:
                break
        except Exception as e:
            print(f'Erro com o cliente: {e}')
            break
    client_socket.close()

def broadcast(msg, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg.encode())
            except Exception as e:
                print(f'Erro ao enviar mensagem: {e}')
                client.close()
                clients.remove(client)
# Worker para gerenciar a comunicação com o cliente
#def conexao_cliente(cliente_socket, endereco_cliente):
    #print(f'Conexão estabelecida com o {endereco_cliente}')

    # Envia uma mensagem para o cliente
    #cliente_socket.send('Olá, cliente!'.encode())

def server_send_messages():
    while True:
        msg = input('Mensagem do servidor: ')
        broadcast(f'Servidor: {msg}')

    #while True:
        # Receber uma mensagem do cliente
        #mensagem = cliente_socket.recv(1500)
        #print(f'Mensagem recebida do cliente ({endereco_cliente}): {mensagem.decode()}')

    # Fecha a conexão com o cliente
    # cliente_socket.close()

# Cria o socket servidor
server_socket = socket(AF_INET, SOCK_STREAM)

# Liga o servidor ao endereço IP e porta
server_socket.bind(('127.0.0.1', 8000))

# Coloca o servidor em modo de escuta
server_socket.listen()

clients = []

print('Aguardando por novas requisiçõse na porta 8000')

# Thread para enviar mensagens 
Thread(target=server_send_messages).start()
# Ficar esperando por novas conexões de diferentes clientes
while True:
    # Aceita a conexão

    cliente_socket, addr = server_socket.accept()
    print(f'Cliente conectado: {addr}')
    clients.append(cliente_socket)
    Thread(target=handle_client, args=(cliente_socket,)).start()