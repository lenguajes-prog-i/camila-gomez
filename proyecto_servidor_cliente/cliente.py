import socket
import threading

class ChatClient:
    """Cliente de chat que se conecta a un servidor por TCP"""

    def __init__(self, host, port, nickname, server_name):
        """
        Constructor del cliente.
        - host: dirección IP del servidor al que se conectará
        - port: puerto del servidor
        - nickname: nombre del cliente (usuario)
        - server_name: nombre del servidor al que se conecta (ej. 'Servidor Estudio')
        """
        self.host = host
        self.port = port
        self.nickname = nickname
        self.server_name = server_name
        # Crear socket TCP para la conexión
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False  # Estado de conexión

    def receive_messages(self):
        """
        Hilo en segundo plano que recibe mensajes del servidor.
        Se ejecuta mientras el cliente esté conectado.
        - Si el mensaje es privado (prefijo [Privado]), se muestra resaltado con ***.
        - Si es un error (prefijo [ERROR]), se muestra tal cual.
        - Si es público, se muestra con el nombre del servidor.
        """
        while self.connected:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if msg:
                    # Mensajes privados
                    if msg.startswith("[Privado"):
                        print(f"\n*** {msg} ***")
                    # Mensajes de error
                    elif msg.startswith("[ERROR]"):
                        print(f"\n{msg}")
                    # Mensajes normales
                    else:
                        print(f"\n[{self.server_name}] {msg}")
            except:
                print("\n[ERROR] Comunicación con el servidor perdida.")
                self.connected = False
                break

    def start(self):
        """
        Inicia la conexión con el servidor y el bucle principal del chat.
        - Envía el nickname al servidor
        - Lanza un hilo para recibir mensajes
        - Permite enviar mensajes desde la consola
        """
        try:
            # Conectar al servidor
            self.client.connect((self.host, self.port))
            self.connected = True
            print(f"[INFO] Conectado a {self.server_name} ({self.host}:{self.port}) como {self.nickname}")

            # Enviar nickname al servidor
            self.client.send(self.nickname.encode("utf-8"))

            # Iniciar hilo para recibir mensajes
            thread = threading.Thread(target=self.receive_messages)
            thread.daemon = True
            thread.start()

            # Bucle principal para enviar mensajes
            while self.connected:
                try:
                    msg = input(f"{self.nickname}@{self.server_name} > ")
                    if msg.lower() == "salir":  # Comando para desconectar
                        self.connected = False
                        self.client.close()
                        print(f"[INFO] {self.nickname} salió de {self.server_name}.")
                        break
                    else:
                        # Enviar mensaje al servidor (público o privado según formato)
                        self.client.send(msg.encode("utf-8"))
                except:
                    self.connected = False
                    self.client.close()
                    print("\n[ERROR] Error al enviar mensaje.")
                    break

        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor: {e}")


# ------------------- MENÚ PRINCIPAL -------------------

def main():
    """
    Menú principal para gestionar servidores y clientes.
    Permite:
    - Crear servidores (solo se registran, no se ejecutan aquí)
    - Listar servidores
    - Crear clientes
    - Listar clientes
    - Seleccionar cliente y servidor para chatear
    """
    servidores = []  # Lista de servidores disponibles (diccionarios con puerto y nombre)
    clientes = []    # Lista de clientes creados (diccionarios con nickname)
    host = input("Ingrese la IP de los servidores: ")

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Crear servidor")
        print("2. Listar servidores")
        print("3. Crear cliente")
        print("4. Listar clientes")
        print("5. Seleccionar cliente y servidor para chatear")
        print("6. Salir del programa")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            port = int(input("Ingrese el puerto del nuevo servidor: "))
            name = input("Ingrese el nombre del servidor: ")
            servidores.append({"port": port, "name": name})
            print(f"[INFO] Servidor '{name}' creado en puerto {port}.")

        elif opcion == "2":
            if servidores:
                print("\n--- Lista de servidores ---")
                for idx, s in enumerate(servidores, start=1):
                    print(f"{idx}. {s['name']} ({host}:{s['port']})")
            else:
                print("[INFO] No hay servidores creados.")

        elif opcion == "3":
            nickname = input("Ingrese el nombre del nuevo cliente: ")
            nuevo_cliente = {"nickname": nickname}
            clientes.append(nuevo_cliente)
            print(f"[INFO] Cliente '{nickname}' creado.")

        elif opcion == "4":
            if clientes:
                print("\n--- Lista de clientes ---")
                for idx, c in enumerate(clientes, start=1):
                    print(f"{idx}. {c['nickname']}")
            else:
                print("[INFO] No hay clientes creados.")

        elif opcion == "5":
            if not clientes:
                print("[INFO] No hay clientes disponibles.")
                continue
            if not servidores:
                print("[INFO] No hay servidores disponibles.")
                continue

            print("\nSeleccione un cliente:")
            for idx, c in enumerate(clientes, start=1):
                print(f"{idx}. {c['nickname']}")
            idx_cliente = int(input("Ingrese el número del cliente: "))
            if not (1 <= idx_cliente <= len(clientes)):
                print("[ERROR] Cliente inválido.")
                continue
            cliente_info = clientes[idx_cliente-1]

            print("\nSeleccione un servidor:")
            for idx, s in enumerate(servidores, start=1):
                print(f"{idx}. {s['name']} ({host}:{s['port']})")
            idx_servidor = int(input("Ingrese el número del servidor: "))
            if not (1 <= idx_servidor <= len(servidores)):
                print("[ERROR] Servidor inválido.")
                continue
            servidor_info = servidores[idx_servidor-1]

            cliente_obj = ChatClient(
                host=host,
                port=servidor_info["port"],
                nickname=cliente_info["nickname"],
                server_name=servidor_info["name"]
            )
            cliente_obj.start()

        elif opcion == "6":
            print("[INFO] Programa finalizado.")
            break

        else:
            print("[ERROR] Opción inválida.")


# ------------------- PUNTO DE ENTRADA -------------------

if __name__ == "__main__":
    main()
