import random
import simpy
import numpy as np

Num_Employees = 2
Avg_Support_Time = 5
Customer_Interval = 2
Sim_Time = 120

customers_handled = 0


class CallCenter:

    def __init__(self, env, num_employees, support_time):
        self.env = env
        self.staff = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Support finished for {customer} at {self.env.now:.2f}")

def customer(env, name, call_center):
    global customers_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}!")
    with call_center.staff.request() as request:
        yield request
        print(f"Customer {name} enters call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        print(f"Customer {name} left call at {env.now:.2f}")
        customers_handled += 1

def setup(env, num_employees, support_time, customer_interval):
    call_center = CallCenter(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i +=1
        env.process(customer(env, i, call_center))

print("Starting call center simulation")
env = simpy.Environment()
env.process(setup(env, Num_Employees, Avg_Support_Time, Customer_Interval))
env.run(until=Sim_Time)

print("Customers handled: " + str(customers_handled))
