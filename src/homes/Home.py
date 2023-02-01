import sysv_ipc
import random
import socket
import struct
import time
import sys

from colors.bcolors import bcolors

GIVE_ONLY = 1
SELL_ONLY = 2
GIVE_AND_SELL = 3
ENERGY_TRADES = [GIVE_ONLY, SELL_ONLY, GIVE_AND_SELL]

INITIAL_MONEY = 100

HOST = "localhost"
PORT = 23333

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
  exchange()
    Exchange energy with other home or with the market
  give()
    Fulfills one request of another home if possible
  ask_home()
    Sends a demand of a certain amount of energy
  sell_to_market()
    Sends energy to the market within a socket
  buy_to_market()
    Sends a demand of energy to the market within a socket
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
      print(bcolors.FAIL + "Cannot connect to message queue", keys, ", terminating." + bcolors.ENDC)
      sys.exit(1) 
    
  def print_state(self):
    """
    Prints home's id and current energy, producing and consuming rates
    """

    print("Home "+ str(self.home_id) + ": energy=" + str(self.energy) + ", money=" + str(round(self.money, 2)))
    #print("Home "+ str(self.home_id) + " producing rate: " + str(self.producing_rate) + " times/s")
    #print("Home "+ str(self.home_id) + " consuming rate: " + str(self.consuming_rate) + " times/s")


  def consume(self):
    """
    Generates a random amount energy that is substrat from the inital energy
    only if the result is positive
    """

    consumed_energy = random.randint(1, 5)
    if (self.energy - consumed_energy) > 0:
      self.energy = self.energy - consumed_energy
    else: 
      print(bcolors.FAIL + "Home "+ str(self.home_id) +" CONSUME ERROR : lack of energy!" + bcolors.ENDC)


  def produce(self):
    """
    Generates a random amount energy that is added to the inital energy
    only if the latter is above the energy threshold of the home
    """

    if (self.energy > self.energy_threshold):
      produced_energy = random.randint(1, 5)
      self.energy = self.energy + produced_energy
    else:
      print(bcolors.FAIL + "Home "+ str(self.home_id) +" PRODUCE ERROR : lack of energy!" + bcolors.ENDC)


  def exchange(self):
    """
    Exchanges energy with other homes or the market depending on
    the amount of energy, money and energy trade
    """

    if self.energy > self.energy_threshold:
      if self.energy_trade == GIVE_ONLY:
        try:
          self.give()
        except sysv_ipc.BusyError:
          pass
      elif self.energy_trade == SELL_ONLY:
        self.send_to_market()
      elif self.energy_trade == GIVE_AND_SELL:
        try:
            self.give()
        except sysv_ipc.BusyError:
          self.send_to_market()
    else: # lack of energy
      demand = self.energy_threshold - self.energy + 1
      try:
        self.ask_home(demand)
      except sysv_ipc.BusyError:
        _, _ = self.mq_demand.receive(type=self.home_id) # Cancel my demand
        self.buy_to_market(demand)
    self.print_state()
        

  def send_to_market(self):
    """
    Sends surplus of energy to the market within a socket. The latter sends back the price of
    per unit of energy: the home updates its amount of money and of energy
    """

    offer = self.energy - self.energy_threshold
    print(bcolors.OKGREEN + "Home "+ str(self.home_id) + " want to sell: " + str(offer) + bcolors.ENDC)
    # Sells energy to the market
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
      client_socket.connect((HOST, PORT))
      msg = [offer, 1]
      client_socket.sendall(struct.pack('2d', *msg))
      response = client_socket.recv(1024)
      price = struct.unpack('2d', response)[0]
      print(bcolors.OKGREEN + "Market's response: current price of energy is " + str(round(price, 2)) + bcolors.ENDC)
      # Update energy and money
      self.money += price * offer
      self.energy -= offer


  def buy_to_market(self, demand):
    """
    Buys energy to the market only if there is enough money by sending a request
    within a socket.

    Parameters
    ---------
    demand : int
      The amount of energy requested by the home
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
      client_socket.connect((HOST, PORT))
      msg = [demand, 0]
      client_socket.sendall(struct.pack('2d', *msg))
      response = client_socket.recv(1024)
      price = struct.unpack('2d', response)[0]
      print(bcolors.OKCYAN + "Market's responds current price of energy is: " + str(round(price, 2)) + bcolors.ENDC)
      # Update energy and money
      if self.money >= (price * demand):
        self.money -= price * demand
        self.energy += demand


  def ask_home(self, demand):
    """
    Asks home for a certain amount of energy. Waits three seconds before looking
    the offers in the corresponding message queue. 
    Raises a BusyError if there is no giver.

    Parameters
    ----------
    demand : int
      The amount of energy requested by the home
    """

    msg = str(demand).encode()
    print(bcolors.WARNING + "Home "+ str(self.home_id) +" tries to send a demand: " + str(demand) + bcolors.ENDC)
    self.mq_demand.send(msg, type=self.home_id)
    print(bcolors.WARNING + "Home "+ str(self.home_id) + " tries to receive a response..." + bcolors.ENDC)
    time.sleep(3)
    _, _ = self.mq_response.receive(block=False,type=self.home_id)
    self.energy += demand


  def give(self):
    """
    Takes a demand in the corresponding message queue and fulfills it if possible.
    If not, it sends back the demand in the message queue.
    Waits five seconds before taking a demand.
    If there is no demand a BusyError is raised. 
    """

    surplus = self.energy - self.energy_threshold
    print(bcolors.FAIL + "Home "+ str(self.home_id) +" tries to get a demand..." + bcolors.ENDC)
    time.sleep(5)
    msg, home_id = self.mq_demand.receive(block=False)
    demand = int(msg.decode())
    if surplus >= demand:
      print(bcolors.WARNING + "Home "+ str(self.home_id) +" tries to send a response..."  + bcolors.ENDC)
      self.mq_response.send("OK".encode(), type=home_id)
      self.energy -= demand
    else:
      print(bcolors.WARNING + "Home "+ str(self.home_id) +" tries to resend a demand..."  + bcolors.ENDC)
      self.mq_demand.send(msg, type=home_id)
    
  
  def run(self):
    """
    Launches the home in an infinite loop to consume, produce and exchange energy
    in this order
    """

    while True:
      self.consume()
      self.produce()
      self.exchange()


  




