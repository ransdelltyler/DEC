import sacn
import uuid
import time

cid_bytes = uuid.UUID('1ACAA578-60C3-22D4-AA6F-577E7724B769').bytes
sender = sacn.sACNsender(source_name='Test', cid=tuple(cid_bytes))

sender.start()

time.sleep(1)  # <-- give thread time to start

u = sender.activate_output(1420)
print("Universe:", u)
sender.stop()
