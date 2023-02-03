from multiprocessing import Process
import sysv_ipc
import random
import signal

from homes.Home import Home, ENERGY_TRADES
from end.end import signal_handler


# Signal -----------------
signal.signal(signal.SIGINT, signal_handler)

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



if __name__ == "__main__":
  HOMES_NB = 3
  homes = []
  initial_params = init_params(HOMES_NB)
 
  KEYS = [128, 256]
  mq_demand = sysv_ipc.MessageQueue(KEYS[0], sysv_ipc.IPC_CREAT)
  mq_response = sysv_ipc.MessageQueue(KEYS[1], sysv_ipc.IPC_CREAT)

  for i in range(HOMES_NB):
    homes.append(Home(initial_params[i], i + 1, ENERGY_TRADES[i%len(ENERGY_TRADES)], KEYS))
    homes[i].start() # Automatically executes run() method in a separate process
    
  for i in range(HOMES_NB):
    homes[i].join()
  