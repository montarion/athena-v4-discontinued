from components.networking import Networking
from components.modules import Modules
from components.website import website
from components.filewatch import filewatch
import threading, queue
from time import sleep



t1 = threading.Thread(target=Networking().startserving)
t2 = threading.Thread(target=Modules().standard)
t3 = threading.Thread(target=website().runserver)
t4 = threading.Thread(target=filewatch().msgcheck)

t1.start()
t2.start()
t3.start()
t4.start()
