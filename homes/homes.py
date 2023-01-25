from multiprocessing import Process

def home(interaction, rates):
  PRODUCING_RATE =  rates[0]
  CONSUMPTION_RATE = rates[1]
  energy = 0

  while True:
    energy = produce(PRODUCING_RATE, energy)
    sleep()
    energy = consume(CONSUMPTION_RATE, energy)
    sleep()
    interaction()

def produce(rate, energy):
  pass

def consume(rate, energy):
  pass

def sleep():
  pass

def init_rates(nb_homes):
  pass


if __name__ == "__main__":
  NB_HOMES = 3
  homes = [] # list of child processes
  trade_policies = [] # all possible energy trade policies
  rates = init_rates(NB_HOMES) # initial rates for each home : [(producing rate, consuming rate), ...]

  for i in range(NB_HOMES):
    homes.append(Process(target=home, args=(trade_policies[i], rates[i])))
    homes[i].start()