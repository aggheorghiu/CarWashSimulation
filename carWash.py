import random
import simpy


NUM_MACHINES = 3
WASHTIME = random.randint(4, 10)
T_INTER = 7
SIM_TIME = 20


class Car(object):
    def __init__(self, name):
        self.name = name


class Carwash(object):
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime
        self.queue = simpy.Store(env)
        self.waiting_times = []
        self.car_available = env.event()
        self.stay_times = []
        self.car_counter = 0
        self.total_wash_time = 0

    def wash(self, car):
        washtime = random.randint(4, 10)
        yield self.env.timeout(washtime)

        self.total_wash_time += washtime
        self.car_counter += 1
        yield self.env.process(self.wash(car))


    def start_wash(self):
        while True:
            with self.machine.request() as request:
                yield request
                if len(self.queue.items) > 0:
                    car = self.queue.get()
                    print('%s enters the carwash at %.2f.' % (car_name, self.env.now))
                    yield self.env.process(self.wash(car))
                    print('%s leaves the carwash at %.2f.' % (car_name, self.env.now))
                    self.pick_up_car()
                if len(self.queue.items) > 0:
                    yield self.env.timeout(1)

            if self.env.now % T_INTER == 0:
                self.add_car()

            if self.env.now >= SIM_TIME and len(self.queue.items) == 0:
                break

            # break out of the loop if the simulation time has elapsed
            if self.env.now >= SIM_TIME and len(self.queue.items) == 0:
                break

    def add_car(self):
        # self.arrival_time = self.env.now
        self.car_counter += 1
        global car_name
        car_name = f'Car {self.car_counter}'
        car = Car(car_name)
        # add the car to the queue
        self.queue.put(car)

        print('%s enters the queue at %.2f.' % (car_name, self.env.now))
        # signal that a car is available
        self.car_available.succeed()
        self.car_available = self.env.event()

    def pick_up_car(self):
        """Pick up the car"""
        if not len(self.queue.items) > 0:
            print('A car is picked up at %.2f.' % (self.env.now))

def customer(env, name, cw):
    cw.add_car()
    yield cw.car_available
    yield env.process(cw.start_wash())
    cw.car_available = env.event()
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

# Exec
env.run(until=SIM_TIME)


# 3 evennimente. car arrival / curatare / finalizare
# arrival & finish nu au conditii
# curatarea are nevoie de conditii: o masina in asteptare && o un utilaj disponibil.
