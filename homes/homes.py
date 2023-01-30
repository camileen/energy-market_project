import random

GIVE_ONLY = 1
SELL_ONLY = 2
GIVE_AND_SELL = 3
energy_trades = [GIVE_ONLY, SELL_ONLY, GIVE_AND_SELL]


class Home:
  """
  A class that represent an Home

  Attributes
  ----------
  initial_params : str tuple
    The initial energy, producing and consuming rates of the home
  home_id : int
    A number that identify the home
  energy_trade : int
    The type of homes' energy trade

  Methods
  -------
  print_state()
    Prints home's id and current energy, producing and consuming rates
  consume()
    Decreases the energy of the home
  produce()
    Increses the energy of the home
  run()
    Launches the home in an infinite loop to consume, produce and exchange energy
  """

  def __init__(self, initial_params, home_id, energy_trade):
    """
    Parameters
    ----------
    initial_params : str tuple
      The initial energy, producing and consuming rates of the home
    home_id : int
      A number that identify the home
    energy_trade : int
      The type of homes' energy trade
    """

    (initial_energy, initial_producing_rate, initial_consuming_rate) = initial_params
    self.home_id = home_id
    self.energy = initial_energy
    self.producing_rate = initial_producing_rate
    self.consuming_rate = initial_consuming_rate
    self.energy_threshold = 2
    self.energy_trade = energy_trade
  
  def print_state(self):
    """
    Prints home's id and current energy, producing and consuming rates
    """
    
    print("**** HOME " + str(self.home_id) + " ****")
    print("Current energy: " + str(self.energy))
    print("Current producing rate: " + str(self.producing_rate) + " times/s")
    print("Current consuming rate: " + str(self.consuming_rate) + " times/s")

  def consume(self):
    """
    Generates a random amount energy that is substrat from the inital energy
    only if the result is positive
    """

    consumed_energy = random.randint(1, 5)
    if (self.energy - consumed_energy) > 0:
      self.energy = self.energy - consumed_energy
      print("Consumed energy: " + str(consumed_energy))
    else: 
      print("CONSUME ERROR : lack of energy!")

  def produce(self):
    """
    Generates a random amount energy that is added to the inital energy
    only if the latter is above the energy threshold of the home
    """

    if (self.energy > self.energy_threshold):
      produced_energy = random.randint(1, 5)
      self.energy = self.energy + produced_energy
      print("Produced energy: " + str(produced_energy))
    else:
      print("PRODUCE ERROR : lack of energy!")
  
  def run(self):
    """
    Launches the home in an infinite loop to consume, produce and exchange energy
    in this order
    """

    #while True:
    self.consume()
    self.produce()
    self.exchange()


  




