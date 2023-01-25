from multiprocessing import Process
from time import sleep
import random
import os


def home(interaction, rates):
  print("***** Starting of home", os.getpid())
  PRODUCING_RATE =  rates[0] # example : X times per second
  CONSUMPTION_RATE = rates[1]
  energy = 0

  #while True:
  energy = action("produce", PRODUCING_RATE, energy)
  print("***** production of home", str(os.getpid()) +":", "energy =", energy)
  energy = action("consume", CONSUMPTION_RATE, energy)
  print("***** consumption of home", str(os.getpid()) +":", "energy =", energy)
  #interaction()
  #print("***** after interaction of home", str(os.getpid()) +":", "energy =", energy)
  print("***** End of home", os.getpid())

def action(task, rate, energy):
  coeff = random.randint(0, 10) # random integer between 0 and 10 included
  rand_energy = coeff*random.random() # random amount of energy between 0 and 10 excluded
  sleep(1/rate)
  return energy + rand_energy if task == "produce" else energy - rand_energy


def init_rates(nb_homes):
  rates = []
  for _ in range(nb_homes):
    rates.append((random.randint(1, 5), random.randint(1, 5)))
  return rates


if __name__ == "__main__":
  NB_HOMES = 3
  homes = [] # list of child processes
  trade_policies = [1, 2, 3] # all possible energy trade policies
  rates = init_rates(NB_HOMES) # initial rates for each home : [(producing rate, consuming rate), ...]
  print("***** initial rates:\n", rates)

  for i in range(NB_HOMES):
    homes.append( Process(target=home, args=(trade_policies[i], rates[i])) )
    homes[i].start()
  
  for i in range(NB_HOMES):
    homes[i].join()