import random

class Home:
  def __init__(self, inital_params, home_id):
    (initial_energy, initial_producing_rate, initial_consuming_rate) = inital_params
    self.home_id = home_id
    self.energy = initial_energy
    self.producing_rate = initial_producing_rate
    self.consuming_rate = initial_consuming_rate
  
  def print_state(self):
    print("**** HOME " + str(self.home_id) + " ****")
    print("Current energy: " + str(self.energy))
    print("Current producing rate: " + str(self.producing_rate) + " times/s")
    print("Current consuming rate: " + str(self.consuming_rate) + " times/s")

  def consume(self):
    pass

  def produce(self):
    pass

  def exchange(self):
    pass

  def run(self):
    while True:
      self.consume()
      self.produce()
      self.exchange()


def init_param(HOMES_NB):
    params = []
    for i in range(HOMES_NB):
      params.append((random.randint(1, 10), random.randint(1, 5), random.randint(1, 5)))
    return params

if __name__ == "__main__":
  HOMES_NB = 3
  homes = []
  inital_params = init_param(HOMES_NB)

  for i in range(3):
    homes.append(Home(inital_params[i], i + 1))
    #homes[i].print_state()
    #homes[i].run()
