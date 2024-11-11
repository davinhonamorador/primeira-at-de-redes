from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

def handle_receive(client):
    while True:
        try:
            message = client.recv(1500).decode('utf-8')
            if message:
                print(f'Servidor: {message}')
        except:
            print('Erro na recepção da mensagem')
            client.close()
            break
def handle_send(client):
    while True:
        message = input('Digite uma mensagem para o servidor: ')
        client.send(message.encode('utf-8'))
        


# Cria o socket
s = socket(AF_INET, SOCK_STREAM)


print(f'Tentando conectar ao servidor na porta 8000')
# Conecta ao servidor
s.connect(('127.0.0.1', 8000))

# Recebe uma mensagem do servidor
mensagem = s.recv(1500)

Thread(target=handle_receive, args=(s , )).start()
Thread(target=handle_send, args=(s, )).start()

print(f'Mensagem recebida do servidor: {mensagem.decode()}')

#pegar hora atual



# Fecha a conexão
# s.close()