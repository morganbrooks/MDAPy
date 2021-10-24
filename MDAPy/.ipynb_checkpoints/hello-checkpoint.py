

import anvil.server

anvil.server.connect("AFCHM4M2HNKYTXCACMPTPIEK-TBI26WNF3B2VMUTD")

@anvil.server.callable
def say_hello(name):
  print(f"Hello from your own machine!")

anvil.server.wait_forever()