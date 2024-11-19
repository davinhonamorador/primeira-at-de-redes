import socket
import threading

# Função para receber mensagens do servidor
def receber_mensagens(sock):
    while True:
        try:
            mensagem = sock.recv(1500)
            if not mensagem:
                print("Conexão com o servidor encerrada.")
                break
            print(f"Mensagem recebida do servidor: {mensagem.decode()}")
        except ConnectionResetError:
            print("Servidor desconectado.")
            break

# Função para enviar mensagens ao servidor
def enviar_mensagens(sock):
    while True:
        try:
            mensagem = input("Digite sua mensagem (digite @nome_usuario para enviar a um cliente específico): ")
            sock.send(mensagem.encode())
        except BrokenPipeError:
            print("Conexão com o servidor foi interrompida.")
            break
        except KeyboardInterrupt:
            print("Encerrando o cliente...")
            sock.close()
            break

# Configuração do cliente e conexão ao servidor
cliente_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_sock.connect(('127.0.0.1', 8000))

# Solicita ao usuário um nome
nome_usuario = input("Digite seu nome: ")
cliente_sock.send(nome_usuario.encode())

print(f"Conectado ao servidor na porta 8000 como {nome_usuario}")

# Inicia threads para enviar e receber mensagens
threading.Thread(target=receber_mensagens, args=(cliente_sock,)).start()
threading.Thread(target=enviar_mensagens, args=(cliente_sock,)).start()
