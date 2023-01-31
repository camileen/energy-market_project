from multiprocessing import Process
import sysv_ipc
import random

import homes.Home as Home


def init_params(HOMES_NB):
  """ Generates a tuple of three random integers

  Parameters
  ----------
  HOMES_NB : int
    The number of generated homes
  
  Returns
  -------
  three-integers tuple
    a tuple of three random integers : initial energy, producing and consuming rates
  """

  params = []
  for i in range(HOMES_NB):
    params.append((random.randint(1, 10), random.randint(1, 5), random.randint(1, 5)))
  return params

def home(initial_params, id, energy_trade, keys):
  home = Home.Home(initial_params, id, energy_trade, keys)
  home.print_state()
  home.run()


if __name__ == "__main__":
  HOMES_NB = 3
  homes = []
  #inital_params = init_params(HOMES_NB)
  initial_params = [(1, 5, 6), (100, 7, 8)] 
 
  KEYS = [128, 256]
  mq_demand = sysv_ipc.MessageQueue(KEYS[0], sysv_ipc.IPC_CREAT)
  mq_response = sysv_ipc.MessageQueue(KEYS[1], sysv_ipc.IPC_CREAT)

  for i in range(HOMES_NB):
    homes.append(Process(target=home, args=(initial_params[1], i + 1, Home.ENERGY_TRADES[i%len(Home.ENERGY_TRADES)], KEYS)))
    homes[i].start()
  
  for i in range(HOMES_NB):
    homes[i].join()
  