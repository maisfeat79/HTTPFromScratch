import socket
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s | %(message)s')
logger = logging.getLogger(' http-server ')

HOST = "127.0.0.1"
PORT = 60000

db = {
    "/":{},
    "/tr":{},
    "/eu":{}
}

def get_defaultHTTPResponse(db, path) -> str:
    return "HTTP/1.1 200 OK" \
        "\nContent-Type: application/json\nContent-Length: " + str(len(str(db[path]).encode())) + "\n\n" + str(db[path])

def handle_get(path) -> str:
    return get_defaultHTTPResponse(db, path)

def handle_post(path, name, age) -> str:
    logger.info(f"Name: {name}, Age: {age} added to database")
    db[path][name] = age
    return get_defaultHTTPResponse(db, path)

def handle_put(path, name, age) -> str:
    logger.info(f"Name: {name}, Age: {age} updated in database")
    db[path][name] = age
    return get_defaultHTTPResponse(db, path)

def handle_delete(path, name, age) -> str:
    if name in db[path]:
        del db[path][name]
        logger.info(f"Name: {name} deleted from database")
    return get_defaultHTTPResponse(db, path)

Routes = { 
    "GET": handle_get,
    "POST": handle_post,
    "PUT": handle_put,
    "DELETE": handle_delete
}

def method_handler(method, data, path):
    if method == handle_get:
        return handle_get(path)
    else:
        split_data = data.split("\n\n")[1]
        name = split_data.split('"')[3]
        age = split_data.split('"')[7]
        return method(path, name, age)



def get_method(data: str):
    method = data.split(" ")[0].strip().upper()
    return Routes[method]

def get_path(data: str):
    return data.split(" ")[1].strip()



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    logger.info(f"Server started at {HOST}:{PORT}")

    s.listen()
    logger.info(f"Server listens at {HOST}:{PORT}")

    while True:
        logger.info("Waiting for connection")
        conn, addr = s.accept()
        logger.info("Connection accepted from " + str(addr))
        with conn:
            response = ""
            data = conn.recv(1024)
            try:
                method = get_method(data.decode())
                path = get_path(data.decode())
                response = method_handler(method, data.decode(), path)
            except Exception as e:
                logger.error(f"Invalid request: {e}")

            logger.info("Request received:")
            print("-----------------------------------\\")
            print(data.decode())
            print("------------------------------------/")
            conn.sendall(response.encode())
        logger.info("Connection closed")


