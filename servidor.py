#!/usr/bin/env python3
import socket
import os
import shutil

PORT = 40000
HOST = ''
FORMAT = 'UTF-8'
TAM_MSG = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = (HOST, PORT)
sock.bind(server)

def MsgClient(msg, conn, addr):
    msg = msg.decode()
    msg = msg.split()
    if msg[0].upper() == 'CWD':
        diretorio_name = " ".join(msg[1:])
        print(f'new client request  {addr}: requested the folder {diretorio_name}')
        try:
            os.chdir(diretorio_name)
            conn.send(str.encode(f'+OK\n'))
        except Exception as Erro:
            conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))

    elif msg[0].upper() == 'CRD':
        newdiretorio_name = " ".join(msg[1:])
        print(f'new client request  {addr}: requested the creation of a directory {newdiretorio_name}')
        try:
            current_directory = os.getcwd()
            path = os.path.join(current_directory,newdiretorio_name)
            os.mkdir(path)
            conn.send(str.encode(f'+OK\n'))
        except Exception as Erro:
            conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))

    elif msg[0].upper() == 'RMD':
        remove_dir = " ".join(msg[1:])
        print(f'new client request  {addr}: requested directory removal {remove_dir}')
        try:
            current_directory = os.getcwd()
            path = os.path.join(current_directory,remove_dir)
            os.rmdir(path)
            conn.send(str.encode(f'+OK\n'))
        except Exception as Erro:
            conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))

    elif msg[0].upper() == 'RMF':
        remove_file = " ".join(msg[1:])
        print(f'new client request  {addr}: requested file removal {remove_file}')
        try:
            current_directory = os.getcwd()
            path = os.path.join(current_directory,remove_file)
            os.remove(path)
            conn.send(str.encode(f'+OK\n'))
        except Exception as Erro:
            conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))
    
    elif msg[0].upper() == 'MOVE':
        src = msg[1]
        dst = " ".join(msg[2:])
        print(f'new client request  {addr}: requested to rename the file {src}')
        try:
            
            shutil.move(src, dst)
            conn.send(str.encode(f'+OK\n'))
        except Exception as Erro:
            conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))

    
    elif msg[0].upper() == 'WRITE':
        if len(msg) > 2 and msg[2] == '>':
            name_arq = msg[1]
            print(f'new client request  {addr}: requested the creation of a new file {name_arq}')
            dados = " ".join(msg[3:])
            arq = open(name_arq, "w")
            try:
                arq.write(dados)
                conn.send(str.encode(f'File: {name_arq}\n'))
            except Exception as Erro:
                conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))
        else:
            names_arq = " ".join(msg[1:])
            names_arqs = names_arq.split(' ')
            print(f'new client request  {addr}: requested the creation of a news files {names_arqs}')
            try:
                for name in names_arqs:
                    arq = open(name,"w")
    
                conn.send(str.encode('-Ok'))
            except Exception as Erro:
                conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))


    elif msg[0].upper() == 'GET':
        name_arq = " ".join(msg[1:])
        print(f'new client request  {addr}: requested file {name_arq}')
        try:
                status_arq = os.stat(name_arq)
                conn.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
                arq = open(name_arq, "rb")
                while True:
                        
                        dados = arq.read(TAM_MSG)
        
                        if not dados: break
                        conn.send(dados)
        except Exception as Erro:
                conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))
    
    elif msg[0].upper() == 'READ':
        read_arq = " ".join(msg[1:])
        print(f'new client request  {addr}: requested file {read_arq}')
        try:
                status_arq = os.stat(read_arq)
                conn.send(str.encode('+OK {}\n'.format(status_arq.st_size)))
                arq = open(read_arq, "rb")
                while True:
                        dados = arq.read(TAM_MSG)
                        if not dados: break
                        conn.send(dados)
        except Exception as Erro:
                conn.send(str.encode('\033[31m'+'-ERR'+'\033[0;0m'+'{}\n'.format(Erro)))
    
    elif msg[0].upper() == 'LIST':
        listar_arquivos = os.listdir('.')
        conn.send(str.encode(f'+Ok {len(listar_arquivos)}\n'))
        for nome_arquivo in listar_arquivos:
            if os.path.isfile(nome_arquivo):
                status_listar_arquivos = os.stat(nome_arquivo)
                conn.send(str.encode(f'File: {nome_arquivo} - {status_listar_arquivos.st_size/1024:.1f}\n'))
            elif os.path.isdir(nome_arquivo):
                conn.send(str.encode(f'Dir: {nome_arquivo}\n'))    
            else:
                 conn.send(str.encode(f'esp: {nome_arquivo}\n'))



def processoCliente(conn, addr):
    print(f'New connection: \n{addr} connected')
    while True:
        msg = conn.recv(TAM_MSG)
        if not msg or MsgClient(msg, conn, addr): break
        
    conn.close()
    print('disconnected client...')

    conn.close()
    print(f'{addr} client disconnected')


def start():
    sock.listen(50)
    while True:
        try:
            con, cliente = sock.accept()
        except: break
        if os.fork() == 0:
            sock.close()
            processoCliente(con, cliente) 		
            break
        else:
            con.close()

print('Server operating ...')
start()