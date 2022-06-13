import socket, banco, threading
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
 
s.bind(('10.13.11.101', 8084))
s.listen(10)

class Client(threading.Thread):
    
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):

        try:

            content = self.client.recv(1024)
            banco.salvaArray(content)
            print(content)

        except Exception as inst:
        
            print(type(inst))
            print(inst.args)

        finally:

            print("Closing connection")
            client.close()



while True:
 
    client, addr = s.accept()

    ct = Client(client)
    ct.start()
