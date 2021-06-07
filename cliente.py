#!/usr/bin/env python3
#!/usr/bin/env python3
import socket
import sys
import threading
semapharo = threading.Semaphore(1)

TAM_MSG = 1024         
HOST = ''     
PORT = 40000        

def decode_cmd(cmd_usr):
        cmd_map = {
                'exit': 'quit',
                'ls' : 'list',
                'cd' : 'cwd',
                'down': 'get',
                'cat' : 'read',
                'touch': 'write',
                'mv': 'move',
                'mkdir': 'crd',
                'rmdir': 'rmd',
                'rm': 'rmf'
        }
        tokens = cmd_usr.split()
        if tokens[0].lower() == 'help':
                return 'LIST OF COMMAND'

        elif tokens[0].lower() in cmd_map:
                tokens[0] = cmd_map[tokens[0].lower()]
                return " ".join(tokens)
        else:
                return False


if len(sys.argv) > 1:
    HOST = sys.argv[1]
print('Server:', HOST+':'+str(PORT))
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)
print('To finish use EXIT, CTRL+D or CTRL+C\n')
while True:
        try:
                cmd_usr = input("\033[0;32m"+'Prompt:'+'\033[0;0m ')
                
        except:
                cmd_usr = 'EXIT'
        cmd = decode_cmd(cmd_usr)
        if not cmd:
                
                print('\033[31m'+'Undefined command:'+'\033[0;0m', cmd_usr)
        if cmd == 'LIST OF COMMAND':
                print('\nLIST OF COMMAND: \n\n  ls(list) cd(cwd) down(get) \n\n  cat(read) touch(write) mv(to move) \n\n  mkdir(create dir) rmdir(remove dir) rm(remove file) \n\n  exit(quit)\n')
        else:
                sock.send(str.encode(cmd))
                dados = sock.recv(TAM_MSG)
                if not dados: break
                msg_status = dados.decode().split('\n')[0]
                dados = dados[len(msg_status)+1:]
                print(msg_status)
                cmd = cmd.split()
                cmd[0] = cmd[0].upper()
                if cmd[0] == 'QUIT':
                        break
                elif cmd[0] == 'LIST':
                        num_arquivos = int(msg_status.split()[1])
                        dados = dados.decode()
                        while True:
                                arquivos = dados.split('\n')
                                residual = arquivos[-1] # último sem \n fica parapróxima
                                for arq in arquivos[:-1]:
                                        print(arq)
                                        num_arquivos -= 1
                                if num_arquivos == 0: break
                                dados = sock.recv(TAM_MSG)
                                if not dados: break
                                dados = residual + dados.decode()
                elif cmd[0] == 'GET':
                        nome_arq = " ".join(cmd[1:])
                        print('Download :', nome_arq)
                        arq = open(nome_arq, "wb")
                        tam_arquivo = int(msg_status.split()[1])
                        while True:
                                semapharo.acquire()
                                arq.write(dados)
                                semapharo.release()
                                tam_arquivo -= len(dados)
                                if tam_arquivo == 0: break
                                dados = sock.recv(TAM_MSG)
                                if not dados: break
                        arq.close()

                elif cmd[0] == 'READ':
                        nome_arq = " ".join(cmd[1:])
                        print('Reading:', nome_arq)
                        tam_arquivo = int(msg_status.split()[1])
                        while True:
                                print(dados.decode('utf-8'))
                                tam_arquivo -= len(dados)
                                if tam_arquivo == 0: break
                                dados = sock.recv(TAM_MSG)
                                if not dados: break
                        print()
                        
sock.close()



