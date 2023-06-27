import queue
import random
import simpy
from my_queue import myQueue
from stack import Stack

RANDOM_SEED = 42
NUM_MACHINES = 3  # Number of machines in the carwash
WASHTIME = random.randint(4, 10)     # Minutes it takes to clean a car
T_INTER = 20       # Create a car every ~7 minutes
SIM_TIME = 120     # Simulation time in minutes


class Car(object):
    """A car has no specific type in this simulation."""
    pass


class Carwash(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime
        self.queue = myQueue() # queue to store cars waiting for wash
        self.stack = Stack() # stack to store cars waiting for pick-up
        self.car_available = env.event() # event to signal when a car becomes available
        self.car_counter = 0 # counter for the car number
        self.total_wash_time = 0

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        washtime = random.randint(4, 10)
        yield self.env.timeout(washtime)

        # after washing, add car to the stack
        self.stack.push(car)
        self.total_wash_time += washtime

    def start_wash(self):
        """Start a new wash if a bay is available or a new car is in the queue."""
        while True:
            # request the machine
            with self.machine.request() as request:
                # wait for a machine to become available
                yield request

                # check if there is a car waiting in the queue
                if not self.queue.is_empty():
                    # get the next car in the queue
                    car = self.queue.pop()
                    print('%s enters the carwash at %.2f.' % (car.name, self.env.now))

                    # wash the car
                    yield self.env.process(self.wash(car))

                    # print the car leaving the carwash
                    print('%s leaves the carwash at %.2f.' % (car.name, self.env.now))
                    self.pick_up_car()

            # check the queue periodically even if no machine is available
            if not self.queue.is_empty():
                yield self.env.timeout(1)

            # add a new car to the queue every T_INTER minutes
            if self.env.now % T_INTER == 0:
                self.add_car()

            # break out of the loop if the simulation time has elapsed
            if self.env.now >= SIM_TIME and self.queue.is_empty():
                break

    def add_car(self):
        """Add a new car to the queue."""
        # increment the car counter
        self.car_counter += 1

        # create a new car object with the current car number
        car_name = f'Car {self.car_counter}'
        car = Car()
        car.name = car_name

        # add the car to the queue
        self.queue.add(car)

        #?????


        print('%s enters the queue at %.2f.' % (car_name, self.env.now))

        # signal that a car is available
        self.car_available.succeed()
        self.car_available = self.env.event()

    def pick_up_car(self):
        """Pick up the first car in the stack."""
        if not self.stack.is_empty():
            print('A car is picked up at %.2f.' % (self.env.now))


def customer(env, name, cw):
    """A car arrives at the carwash for washing.

    It requests a washing machine from the carwash and starts the washing process.
    After the washing process is complete, the car leaves the carwash.

    """
    cw.add_car()

    # wait for the car to be washed and picked up
    yield env.process(cw.start_wash())
    yield env.timeout(1)
    cw.pick_up_car()


def generate_customer(name):
    for i in range(1, SIM_TIME):
        yield name + str(i)



print('Carwash simulation')
env = simpy.Environment()
carwash = Carwash(env, NUM_MACHINES, WASHTIME)

for name in generate_customer('Car '):
    env.process(customer(env, name, carwash))


env.run(until=SIM_TIME)


# TODO
# average percentage of machines usage (PMU = accumulated time in which a machine is
# occupied / (TTS * number of machines) * 100%);
# 2. average waiting time (TME = accumulated waiting time in the queue / number of vehicles
# that come out of the system) in the queue ESPERA;
# 3. average length of stay in the system per entity (TPS = accumulated of the difference
# between the time of exit of the system and the time of entry for all entities / number of
# vehicles that leave the system);