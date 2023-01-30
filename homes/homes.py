import random

GIVE_ONLY = 1
SELL_ONLY = 2
GIVE_AND_SELL = 3
energy_trades = [GIVE_ONLY, SELL_ONLY, GIVE_AND_SELL]


class Home:
  def __init__(self, inital_params, home_id, energy_trade):
    (initial_energy, initial_producing_rate, initial_consuming_rate) = inital_params
    self.home_id = home_id
    self.energy = initial_energy
    self.producing_rate = initial_producing_rate
    self.consuming_rate = initial_consuming_rate
    self.energy_threshold = 2
    self.energy_trade = energy_trade
  
  def print_state(self):
    print("**** HOME " + str(self.home_id) + " ****")
    print("Current energy: " + str(self.energy))
    print("Current producing rate: " + str(self.producing_rate) + " times/s")
    print("Current consuming rate: " + str(self.consuming_rate) + " times/s")

  def consume(self):
    consumed_energy = random.randint(1, 5)
    if (self.energy - consumed_energy) > 0:
      self.energy = self.energy - consumed_energy
      print("Consumed energy: " + str(consumed_energy))
    else: 
      print("CONSUME ERROR : lack of energy!")

  def produce(self):
    if (self.energy > self.energy_threshold):
      produced_energy = random.randint(1, 5)
      self.energy = self.energy + produced_energy
      print("Produced energy: " + str(produced_energy))
    else:
      print("PRODUCE ERROR : lack of energy!")
  
  def run(self):
    #while True:
      self.consume()
      self.produce()
      self.exchange()

"""
  def exchange(self):
    exchanged_energy, price = 0, 0
    if self.energy > self.energy_threshold:
      if (self.energy_trade == GIVE_ONLY):
        exchanged_energy = give()
      elif (self.energy_trade == SELL_ONLY):
        exchanged_energy, price = send_market_sell_request()
      elif (self.energy_trade == GIVE_AND_SELL):
        try:
            exchanged_energy = give()
        except NoNeed:
          exchanged_energy, price = send_market_sell_request()
    else: # lack of energy
      try:
        send_home_request()
        exchanged_energy  = wait_response()
      except NoGivers:
        send_market_request()
        exchanged_energy = wait_response()
      except EnoughEnergy:
        continue

    update_state()
"""
  




