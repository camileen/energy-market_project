from multiprocessing import Process
from time import sleep
import random
import os


def home(interaction, rates):
  print("********** START OF HOME", os.getpid(), "**********")
  PRODUCING_RATE =  rates[0] # example : X times per second
  CONSUMPTION_RATE = rates[1]
  energy = 0

  #while True:
  
  try:
    energy = action("produce", PRODUCING_RATE, energy)
    print("production of home", str(os.getpid()) +":", "energy =", energy)
    energy = action("consume", CONSUMPTION_RATE, energy)
    print("consumption of home", str(os.getpid()) +":", "energy =", energy)
  except (ValueError):
    print("Home", str(os.getpid()) + " -->", "Lack of energy!")
  #interaction()
  #print("after interaction of home", str(os.getpid()) +":", "energy =", energy)
  print("********** END OF HOME", os.getpid(), "**********")

def action(task, rate, energy):
  
  if energy < 0: raise ValueError
  
  coeff = random.randint(0, 10) # random integer between 0 and 10 included
  rand_energy = coeff*random.random() # random amount of energy between 0 and 10 excluded
  sleep(1/rate)

  if task == "produce":
    return energy + rand_energy
  elif task == "consume":
    if (energy - rand_energy) < 0 :
      raise ValueError
    return (energy - rand_energy)


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
  print("**** initial rates:", rates)

  for i in range(NB_HOMES):
    homes.append( Process(target=home, args=(trade_policies[i], rates[i])) )
    homes[i].start()
  
  for i in range(NB_HOMES):
    homes[i].join()