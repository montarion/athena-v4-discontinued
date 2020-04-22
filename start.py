from components.networking import Networking
from components.modules import Modules
from components.website import website

import threading
from time import sleep

t1 = threading.Thread(target=Networking().startserving)
t2 = threading.Thread(target=Modules().standard)
t3 = threading.Thread(target=website().runserver)


t1.start()
t2.start()
t3.start()

