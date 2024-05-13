import ClientManager
from threading import Thread

client = ClientManager.ClientManager()
menu_thread = Thread(target=client.menu_thread)
menu_thread.start()

client.received_thread()
menu_thread.join()
