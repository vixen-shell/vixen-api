import asyncio
import os

async def read_unix_socket(socket_path):
    # Ouvrir le socket Unix
    reader, _ = await asyncio.open_unix_connection(socket_path)

    # Lire de manière asynchrone
    while True:
        data = await reader.readline()
        if not data:
            break
        print("Nouvelle ligne reçue :", data.decode().strip())  # Affichage de la ligne reçue

    # Fermer le socket à la fin de la lecture
    reader.feed_eof()

# Remplacer 'chemin_du_socket' par votre chemin de socket Unix
socket_path = "/tmp/hypr/{}/.socket2.sock".format(os.getenv('HYPRLAND_INSTANCE_SIGNATURE'))

# Lancer l'événement de lecture du socket
asyncio.run(read_unix_socket(socket_path))