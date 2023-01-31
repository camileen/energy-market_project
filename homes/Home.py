import sysv_ipc
import random
import sys

GIVE_ONLY = 1
SELL_ONLY = 2
GIVE_AND_SELL = 3
ENERGY_TRADES = [GIVE_ONLY, SELL_ONLY, GIVE_AND_SELL]

INITIAL_MONEY = 100



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

  def __init__(self, initial_params, home_id, energy_trade, keys):
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
    self.money = INITIAL_MONEY
    try:
      self.mq_demand = sysv_ipc.MessageQueue(keys[0])
      self.mq_response = sysv_ipc.MessageQueue(keys[1])
    except sysv_ipc.ExistentialError:
      print("Cannot connect to message queue", keys, ", terminating.")
      sys.exit(1) 
    
  def print_state(self):
    """
    Prints home's id and current energy, producing and consuming rates
    """

    #print("**** HOME " + str(self.home_id) + " ****")
    print("Home "+ str(self.home_id) + " energy: " + str(self.energy))
    print("Home "+ str(self.home_id) + " producing rate: " + str(self.producing_rate) + " times/s")
    print("Home "+ str(self.home_id) + " consuming rate: " + str(self.consuming_rate) + " times/s")

  def consume(self):
    """
    Generates a random amount energy that is substrat from the inital energy
    only if the result is positive
    """

    consumed_energy = random.randint(1, 5)
    if (self.energy - consumed_energy) > 0:
      self.energy = self.energy - consumed_energy
      print("Home "+ str(self.home_id) + " consumed energy: " + str(consumed_energy))
    else: 
      print("Home "+ str(self.home_id) +" CONSUME ERROR : lack of energy!")

  def produce(self):
    """
    Generates a random amount energy that is added to the inital energy
    only if the latter is above the energy threshold of the home
    """

    if (self.energy > self.energy_threshold):
      produced_energy = random.randint(1, 5)
      self.energy = self.energy + produced_energy
      print("Home "+ str(self.home_id) + " produced energy: " + str(produced_energy))
    else:
      print("Home "+ str(self.home_id) +" PRODUCE ERROR : lack of energy!")

  def exchange(self):
    if self.energy > self.energy_threshold:
      if self.energy_trade == GIVE_ONLY:
        try:
          self.give()
        except sysv_ipc.BusyError:
          pass
      elif self.energy_trade == SELL_ONLY:
        self.send_market_sell_request()
      elif self.energy_trade == GIVE_AND_SELL:
        try:
            self.give()
        except sysv_ipc.BusyError:
          self.send_market_sell_request()
    else: # lack of energy
      print("Home "+ str(self.home_id) + ": lack of energy in exchange()\n")
      try:
        demand = self.energy_threshold - self.energy + 1
        msg = str(demand).encode()
        print("Home "+ str(self.home_id) +" tries to send a demand: " + str(demand))
        self.mq_demand.send(msg, type=self.home_id)
        print("Home "+ str(self.home_id) + " tries to receive a response...")
        _, _ = self.mq_response.receive(type=self.home_id)
        self.energy += demand
        self.print_state()
      except NoGivers:
        self.send_market_request()
        self.wait_response()
      except EnoughEnergy:
        pass



  def give(self):
    surplus = self.energy - self.energy_threshold
    for i in range(3):
      print("Home "+ str(self.home_id) +" tries to get a demand...")
      msg, home_id = self.mq_demand.receive(block=False)
      demand = int(msg.decode())
      print("Home " + str(home_id) + " demands: " + msg.decode())
      if surplus >= demand:
        print("Home "+ str(self.home_id) +" tries to send a response...")
        self.mq_response.send("OK".encode(), type=home_id)
        self.energy -= demand
        break
      else:
        print("Home "+ str(self.home_id) +" tries to resend a demand...")
        self.mq_demand.send(msg, type=home_id)
    self.print_state()
    
  
  def run(self):
    """
    Launches the home in an infinite loop to consume, produce and exchange energy
    in this order
    """

    #while True:
    self.consume()
    self.produce()
    self.exchange()


  




