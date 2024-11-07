from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def receive_messages(socket):
    while True:
        try:
            msg = socket.recv(1500).decode()
            if msg:
                print(f'Mensagem recebida do servidor: {msg}')
            else:
                break
        except Exception as e:
            print(f'Erro ao receber a mensagem: {e}')

def send_messages(socket):
    while True:
        msg = input('Digite sua mensagem: ')
        socket.send(msg.encode())



# Cria o socket
s = socket(AF_INET, SOCK_STREAM)


print(f'Tentando conectar ao servidor na porta 8000')
# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

# Receber mensagens

Thread(target=receive_messages, args=(s,)).start()

# Enviar mensagens

Thread(target=send_messages, args=(s,)).start()


# Fecha a conexão
# s.close()