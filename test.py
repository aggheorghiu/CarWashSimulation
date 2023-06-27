import numpy as np
import random
import simpy

NUM_MACHINES = 3  # Number of machines in the carwash
WASHTIME = np.random.randint(4, 10)  # Minutes it takes to clean a car
T_INTER = 20  # Create a car every ~7 minutes
SIM_TIME = 120  # Simulation time in minutes


class Car(object):
    """A car has no specific type in this simulation."""
    pass


class Carwash(object):
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime
        self.queue = []  # list to store cars waiting for wash
        self.stack = []  # list to store cars waiting for pick-up
        self.car_available = env.event()  # event to signal when a car becomes available
        self.car_counter = 0  # counter for the car number
        self.total_wash_time = 0
        self.machine_usage = 0  # total time machines are in use
        self.start_time = {}  # dictionary to store start times of each wash

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        washtime = np.random.randint(4, 10)
        self.start_time[car.name] = self.env.now  # record start time
        yield self.env.timeout(washtime)

        # after washing, add car to the stack
        self.stack.append(car)
        self.total_wash_time += washtime
        self.machine_usage += washtime

    def start_wash(self):
        while True:
            # request the machine
            with self.machine.request() as request:
                # wait for a machine to become available
                yield request

                # check if there is a car waiting
                if self.queue:
                    # get the next car in the queue
                    car = self.queue.pop(0)
                    print('%s enters the carwash at %.2f.' % (car.name, self.env.now))

                    # wash the car
                    yield self.env.process(self.wash(car))

                    # print the car leaving the carwash
                    print('%s leaves the carwash at %.2f.' % (car.name, self.env.now))
                    self.pick_up_car()

            # check the queue periodically
            if self.queue:
                yield self.env.timeout(1)

            # add a new car to the queu
            if self.env.now % T_INTER == 0:
                self.add_car()

            # break out of the loop
            if self.env.now >= SIM_TIME and not self.queue:
                break

    def add_car(self):
        """Add a new car to the queue."""
        # increment the car counter
        self.car_counter += 1
        car_name = f'Car {self.car_counter}'
        car = Car()
        car.name = car_name
        self.queue.append(car)
        print('%s enters the queue at %.2f.' % (car_name, self.env.now))

    def pick_up_car(self):
        """Pick up the first car in the stack."""
        if self.stack:
            car = self.stack.pop(0)
            end_time = self.env.now
            wash_time = end_time - self.start_time[car.name]
            self.machine_usage -= wash_time  # decrement total machine usage time
            print('A car is picked up at %.2f.' % end_time)

    def machine_usage_percentage(self):
        """Calculate average percentage of machines usage."""
        total_sim_time = self.env.now
        total_machine_time = NUM_MACHINES * total_sim_time

        if total_machine_time == 0:
            return 0

        try:
            pmu = (self.machine_usage / total_machine_time) * 100
        except ZeroDivisionError:
            pmu = 0

        return pmu


def customer(env, name, cw):
    cw.add_car()
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

pmu = carwash.machine_usage_percentage()
print('Average percentage of machines usage: %.2f%%' % pmu)


env.run(until=SIM_TIME)


# TODO
# average percentage of machines usage (PMU = accumulated time in which a machine is
# occupied / (TTS * number of machines) * 100%);
# 2. average waiting time (TME = accumulated waiting time in the queue / number of vehicles
# that come out of the system) in the queue ESPERA;
# 3. average length of stay in the system per entity (TPS = accumulated of the difference
# between the time of exit of the system and the time of entry for all entities / number of
# vehicles that leave the system);