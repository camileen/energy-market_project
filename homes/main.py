import random

import homes


def init_param(HOMES_NB):
    params = []
    for i in range(HOMES_NB):
      params.append((random.randint(1, 10), random.randint(1, 5), random.randint(1, 5)))
    return params

if __name__ == "__main__":
  HOMES_NB = 3
  homes = []
  inital_params = init_param(HOMES_NB)
  
  for i in range(HOMES_NB):
    homes.append(homes.Home(inital_params[i], i + 1, homes.energy_trades[i%(len(homes.energy_trades))]))
    homes[i].print_state()
    homes[i].run()
  
  print("\n")
  for i in range(HOMES_NB):
    homes[i].print_state()
  print("\n\n")