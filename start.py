from components.networking import Networking
from components.modules import Modules

import threading
from time import sleep

t1 = threading.Thread(target=Networking().startserving)
t2 = threading.Thread(target=Modules().standard)


t1.start()
t2.start()


