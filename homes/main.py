import random

import Home


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
  inital_params = init_params(HOMES_NB)
  
  for i in range(HOMES_NB):
    homes.append(Home.Home(inital_params[i], i + 1, Home.ENERGY_TRADES[i%(len(Home.ENERGY_TRADES))]))
    homes[i].print_state()
    homes[i].run()
  
  print("\n")
  for i in range(HOMES_NB):
    homes[i].print_state()
  print("\n\n")