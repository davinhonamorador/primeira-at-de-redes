import socket
import threading

# Dicionário para armazenar clientes conectados
clientes_ativos = {}

def gerenciar_cliente(cliente, endereco):
    # Solicita um nome de usuário
    cliente.send("Informe seu nome: ".encode())
    nome_usuario = cliente.recv(1024).decode()
    
    # Adiciona o cliente à lista de clientes ativos
    clientes_ativos[nome_usuario] = cliente
    print(f"Novo usuário conectado: {nome_usuario} ({endereco})")
    
    try:
        while True:
            mensagem = cliente.recv(1024)
            if not mensagem:
                print(f"{nome_usuario} se desconectou.")
                break
            
            mensagem_str = mensagem.decode()
            print(f"Mensagem de {nome_usuario} ({endereco}): {mensagem_str}")
            
            if mensagem_str.startswith('@'):
                partes = mensagem_str.split(' ', 1)
                if len(partes) > 1:
                    destinatario = partes[0][1:]
                    mensagem_destinatario = partes[1]
                    
                    if destinatario in clientes_ativos:
                        clientes_ativos[destinatario].send(f"Mensagem de {nome_usuario}: {mensagem_destinatario}".encode())
                    else:
                        cliente.send(f"Usuário {destinatario} não encontrado.".encode())
                else:
                    cliente.send("Mensagem para destinatário não especificada.".encode())
            else:
                for nome, sock in clientes_ativos.items():
                    if nome != nome_usuario:
                        sock.send(f"Mensagem de {nome_usuario}: {mensagem_str}".encode())
    except ConnectionResetError:
        print(f"Conexão com {nome_usuario} foi perdida.")
    
    # Remove o cliente da lista de ativos e encerra a conexão
    del clientes_ativos[nome_usuario]
    cliente.close()

# Configuração do servidor
sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_servidor.bind(('127.0.0.1', 8000))
sock_servidor.listen()
print("Servidor ativo e aguardando conexões na porta 8000...")

while True:
    cliente_conectado, endereco_cliente = sock_servidor.accept()
    threading.Thread(target=gerenciar_cliente, args=(cliente_conectado, endereco_cliente)).start()
