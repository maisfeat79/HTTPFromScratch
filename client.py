import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(' http-server ')

HOST = "127.0.0.1"
PORT = 60000

class RequestBuilder:
    def __init__(
            self, 
            method: str = "GET", 
            path = "/",
            headers="", 
            body=""
            ):
        self.start_line = method.upper() +" " + path + " " + "HTTP/1.1\n"
        self.body = body
        self.headers = "Host: developer.mozilla.org\nContent-Type: application/json\nContent-Length: "+ str(len(body.encode()))+"\n" + headers
        self.itself = self.start_line + self.headers + "\n" + self.body 

def get_user_input():
    method = input("Select Method (GET, POST, PUT, DELETE): ")
    path = input("Select Path: ")
    if method.upper() in ["POST", "PUT", "DELETE"]:
        name, age = input("Name: "), input("Age: ")
        body = '{"name":"'+ name + '", "age": "'+ age +'"}'
    else:
        body = ""

    return method, path, body

while (True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # AF_INET kullanma sebebi IPv4, SOCK_STREAM kullanma sebebi TCP
        method, path, body = get_user_input()
        request = RequestBuilder(method=method, path=path, body=body)
        s.connect((HOST,PORT))
        logger.info(f"Connected to server at {HOST}:{PORT}")
        s.sendall(request.itself.encode())

        data = s.recv(1024)

        logger.info("Response received:")
        print("------------------------------------\\")
        print(data.decode())
        print("------------------------------------/")




