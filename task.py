import random
from time import sleep
import multiprocessing


class Event:
    def __init__(self, name, timer) -> None:
        self.name = name
        self.timer = timer

    def process_event(self):
        if self.timer != 0:
            self.timer -= 1
            return self
        else:
            return None


class Environment:
    def __init__(self) -> None:
        self.event = next(self.generate_event())

    def generate_event(self):
        event_types = ['obstacle', 'straight road', 'pedestrian',
                       'turn left', 'turn right', 'speed bump', 'traffic light']
        while True:
            event_type = random.choice(event_types)
            duration = int(random.gauss(5, 2))
            yield Event(event_type, duration)

    def process_event(self):
        if self.event is not None:
            self.event = self.event.process_event()
        if self.event is None:
            self.event = next(self.generate_event())
        return self.event


class Car:
    def __init__(self, car_number):
        self.car_number = car_number
        self.wheel_angle = 0
        self.speed = 0
        self.target_speed = 0
        self.target_wheel_angle = 0
        self.environment = Environment()

    def change_speed_gradually(self):
        if self.speed < self.target_speed:
            self.speed += 5
        elif self.speed > self.target_speed:
            self.speed -= 5

    def change_wheel_angle_gradually(self):
        if self.wheel_angle < self.target_wheel_angle:
            self.wheel_angle += 2
        elif self.wheel_angle > self.target_wheel_angle:
            self.wheel_angle -= 2

    def emergency_brake(self):
        self.target_speed = 0
        if self.speed < self.target_speed:
            self.speed = 0
        elif self.speed > self.target_speed:
            self.speed -= 20

    def set_target_values(self, event: Event):
        if event.name == 'turn left':
            self.target_wheel_angle = -60
        elif event.name == 'turn right':
            self.target_wheel_angle = 60
        elif event.name == 'obstacle' or event.name == 'pedestrian':
            self.emergency_brake()
        elif event.name == 'straight road':
            self.target_speed = 80
        elif event.name == 'speed bump':
            self.target_speed = 30
        elif event.name == 'traffic light':
            self.target_speed = 0

    def process_event(self, event: Event):
        self.set_target_values(event)

    def start(self):
        while True:
            event = self.environment.process_event()
            self.process_event(event)
            self.change_speed_gradually()
            self.change_wheel_angle_gradually()
            sleep(1)
            return f"Car {self.car_number}: Speed = {self.speed}, Wheel angle = {self.wheel_angle}"


def simulate_car(car_number):
    car = Car(car_number)
    while True:
        car_status = car.start()
        print(car_status)


if __name__ == "__main__":
    num_cars = 3
    with multiprocessing.Pool(num_cars) as p:
        p.map(simulate_car, range(num_cars))
