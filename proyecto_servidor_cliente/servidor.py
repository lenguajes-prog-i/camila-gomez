import socket
import threading

class ChatServer:
    """Servidor de chat que maneja múltiples clientes"""

    def __init__(self, host="192.168.1.128", port=5002, name="Servidor"):
        self.host = host
        self.port = port
        self.name = name
        self.clients = []       # Lista de conexiones de clientes
        self.nicknames = []     # Lista de nombres de usuarios
        self.client_map = {}    # Diccionario {nickname: socket}
        self.messages = []      # Historial de mensajes del servidor

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def broadcast(self, message, sender_conn=None):
        """Envía un mensaje a todos los clientes excepto al remitente"""
        try:
            self.messages.append(message.decode("utf-8"))
        except:
            pass

        for client in self.clients:
            if client != sender_conn:
                try:
                    client.send(message)
                except:
                    client.close()
                    self.remove_client(client)

    def send_private(self, target_name, message, sender_name):
        """Envía un mensaje privado a un cliente específico"""
        if target_name in self.client_map:
            try:
                self.client_map[target_name].send(
                    f"[Privado de {sender_name}] {message}".encode("utf-8")
                )
            except:
                self.remove_client(self.client_map[target_name])
        else:
            # Avisar al remitente si el usuario no existe
            if sender_name in self.client_map:
                self.client_map[sender_name].send(
                    f"[ERROR] Usuario '{target_name}' no encontrado.".encode("utf-8")
                )

    def handle_client(self, client_conn):
        nickname = None

        while True:
            try:
                message = client_conn.recv(1024)
                if not message:
                    break

                decoded = message.decode("utf-8")

                if nickname is None:
                    # Primer mensaje: el nickname
                    nickname = decoded
                    self.nicknames.append(nickname)
                    self.clients.append(client_conn)
                    self.client_map[nickname] = client_conn
                    print(f"[+] {nickname} conectado")
                    self.broadcast(f"{nickname} se ha unido al chat".encode("utf-8"), client_conn)

                else:
                    if decoded.strip().lower() == "/salir":
                        print(f"[INFO] {nickname} salió de la sala.")
                        self.broadcast(f"{nickname} ha salido del chat".encode("utf-8"), client_conn)
                        self.remove_client(client_conn)
                        if nickname in self.nicknames:
                            self.nicknames.remove(nickname)
                        if nickname in self.client_map:
                            del self.client_map[nickname]
                        break

                    # --- NUEVA LÓGICA PARA PRIVADOS ---
                    if "/" in decoded:
                        # Si el mensaje contiene /usuario en cualquier parte
                        parts = decoded.split("/")
                        texto = parts[0].strip()
                        target_name = parts[1].strip()
                        self.send_private(target_name, texto, nickname)
                    else:
                        # Mensaje público
                        full_msg = f"{nickname}: {decoded}".encode("utf-8")
                        self.broadcast(full_msg, client_conn)

            except:
                if nickname:
                    print(f"[-] {nickname} desconectado")
                    self.broadcast(f"{nickname} ha salido del chat".encode("utf-8"), client_conn)
                    if nickname in self.nicknames:
                        self.nicknames.remove(nickname)
                    if nickname in self.client_map:
                        del self.client_map[nickname]
                self.remove_client(client_conn)
                break

    def remove_client(self, client_conn):
        if client_conn in self.clients:
            self.clients.remove(client_conn)
        client_conn.close()

    def start(self):
        self.server.listen()
        print(f"[INFO] {self.name} escuchando en {self.host}:{self.port}")

        try:
            while True:
                client_conn, addr = self.server.accept()
                print(f"[INFO] Conexión entrante desde {addr}")
                thread = threading.Thread(target=self.handle_client, args=(client_conn,))
                thread.start()
        except KeyboardInterrupt:
            print(f"\n[INFO] {self.name} detenido por el usuario.")
        finally:
            self.server.close()


# ------------------- FUNCIONES DE MENÚ -------------------

def crear_servidores_iniciales():
    """
    Permite crear el primer servidor solicitando IP, puerto y nombre.
    Luego pregunta cuántos servidores adicionales crear (solo puerto y nombre).
    Inicia todos los servidores en hilos independientes.
    """
    servidores = []

    host = input("Ingrese la IP para el primer servidor: ")
    port = int(input("Ingrese el puerto para el primer servidor: "))
    name = input("Ingrese el nombre para el primer servidor: ")

    servidor_principal = ChatServer(host=host, port=port, name=name)
    servidores.append(servidor_principal)

    cantidad = int(input("¿Cuántos servidores adicionales desea crear?: "))

    for i in range(cantidad):
        port_extra = int(input(f"Ingrese el puerto para el servidor {i+2}: "))
        name_extra = input(f"Ingrese el nombre para el servidor {i+2}: ")
        servidor_extra = ChatServer(host=host, port=port_extra, name=name_extra)
        servidores.append(servidor_extra)

    # Iniciar todos los servidores en hilos
    for servidor in servidores:
        hilo = threading.Thread(target=servidor.start, daemon=True)
        hilo.start()

    return servidores


def crear_servidor_extra(servidores):
    """
    Permite crear un nuevo servidor adicional en cualquier momento desde el menú.
    """
    host = servidores[0].host  # Usamos la misma IP del primer servidor
    port = int(input("Ingrese el puerto para el nuevo servidor: "))
    name = input("Ingrese el nombre para el nuevo servidor: ")
    servidor_extra = ChatServer(host=host, port=port, name=name)
    servidores.append(servidor_extra)

    hilo = threading.Thread(target=servidor_extra.start, daemon=True)
    hilo.start()

    print(f"[INFO] Servidor '{name}' creado en {host}:{port}")


def menu(servidores):
    """
    Menú interactivo para:
    - Listar servidores creados
    - Ver conversaciones de un servidor
    - Crear más servidores en cualquier momento
    - Salir del programa
    """
    while True:
        print("\n--- MENÚ ---")
        print("1. Listar servidores")
        print("2. Ver conversaciones de un servidor")
        print("3. Crear otro servidor")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            for idx, servidor in enumerate(servidores, start=1):
                print(f"{idx}. {servidor.name} ({servidor.host}:{servidor.port})")

        elif opcion == "2":
            idx = int(input("Ingrese el número del servidor: "))
            if 1 <= idx <= len(servidores):
                servidor = servidores[idx-1]
                print(f"\n--- Conversaciones en {servidor.name} ---")
                for msg in servidor.messages:
                    print(msg)
                input("\nPresione ENTER para volver al menú...")
            else:
                print("Servidor inválido.")

        elif opcion == "3":
            crear_servidor_extra(servidores)

        elif opcion == "10":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida.")


# ------------------- PUNTO DE ENTRADA -------------------

if __name__ == "__main__":
    servidores = crear_servidores_iniciales()
    menu(servidores)
