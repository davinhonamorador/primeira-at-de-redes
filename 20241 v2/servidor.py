from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from datetime import datetime

# Função para gerenciar a comunicação com um cliente específico
def conexao_cliente(cliente_socket, endereco_cliente):
    # Solicita um nome para o cliente
    cliente_socket.send("Digite seu nome: ".encode())
    nome_cliente = cliente_socket.recv(1500).decode('utf-8')

    print(f'Conexão estabelecida com o cliente {nome_cliente} ({endereco_cliente})')
    cliente_socket.send(f'Olá, {nome_cliente}!'.encode())

    def handle_receive():
        while True:
            try:
                mensagem = cliente_socket.recv(1500).decode('utf-8')
                if mensagem:
                    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Mensagem recebida do cliente {nome_cliente} ({endereco_cliente}): {mensagem}')
            except:
                print(f'Conexão com o cliente {nome_cliente} ({endereco_cliente}) perdida')
                cliente_socket.close()
                break

    def handle_send():
        while True:
            try:
                mensagem = input(f'Digite uma mensagem para o cliente {nome_cliente}: ')
                cliente_socket.send(mensagem.encode('utf-8'))
            except BrokenPipeError:
                print(f'Conexão com o cliente {nome_cliente} foi interrompida.')
                break
            except KeyboardInterrupt:
                print('Encerrando o servidor.')
                cliente_socket.close()
                break

    Thread(target=handle_receive).start()
    Thread(target=handle_send).start()

# Cria o socket servidor
server_socket = socket(AF_INET, SOCK_STREAM)

# Liga o servidor ao endereço IP e porta
server_socket.bind(('localhost', 8000))

# Coloca o servidor em modo de escuta
server_socket.listen()
print('Aguardando por novas conexões na porta 8000')

# Ficar esperando por novas conexões de diferentes clientes
while True:
    # Aceita a conexão
    cliente_socket, endereco_cliente = server_socket.accept()
    Thread(target=conexao_cliente, args=(cliente_socket, endereco_cliente)).start()
