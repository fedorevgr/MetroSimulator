import asyncio
import random
import time
import os
import signal
import Plots
import Graphics


def signal_handler(signal, frame):
    os.system('clear')
    time.sleep(2)
    graphics.draw_plot()
    exit(0)


def station_info():
    out = ''
    average = []
    for station in Stations:
        amount_of_passengers = len(station.Passengers)
        average.append(amount_of_passengers)
        out += station.Name + ': ' + str(amount_of_passengers) + '\n'

    graphics.Averages.append(average)

    out += '\n'
    return out


def train_info():
    out = ''
    i = 1
    average = 0
    for smth in Trains:
        average += len(smth.Passengers)
        out += str(i) + ' ' + smth.show_station() + '\n'
        i += 1
    if i == 1:
        return out
    graphics.TrainAverages.append(average / (i - 1))
    return out


async def print_stats():
    while True:
        os.system('clear')  # 'clear' for Mac
        graphics.add_second()
        graphics.finalize()
        station_info()
        train_info()
        # print(to_print)
        await asyncio.sleep(UpdateTime)

os.system('clear')  # 'clear' for Mac

Multiply = float(input('Enter how much faster you want to observe the model: '))
AmountOfTrains = int(input('Enter the amount of trains: '))
os.system('clear')

Minute = 1 / Multiply  # second real time

TimeToStations = {
    0: 6,
    1: 3,
    2: 2,
    3: 7,
    4: 0
}

TimeToStationsReverse = {
    4: 0,
    3: 6,
    2: 3,
    1: 2,
    0: 7
}

TimeToDrop = 0.25 * Minute  # 15 seconds
Delay = Minute * 2


class Train:
    def __init__(self):
        self.spaces = 0
        self.current_station = 0  # Рокоссовская
        self.is_commuting = False
        self._headed_to_right = True
        self.capacity = 400
        self.Passengers = []

    def show_station(self):  # printing train info
        if self.is_commuting:
            if self._headed_to_right:
                message = Stations[self.current_station].Name + ' -> ' + Stations[self.current_station + 1].Name
            else:
                message = Stations[self.current_station].Name + ' -> ' + Stations[self.current_station - 1].Name
        else:
            message = Stations[self.current_station].Name

        return message

    def _drop_off(self):
        self.is_commuting = False

        new_passenger_list = []

        for passenger in self.Passengers:
            if passenger != self.current_station:
                new_passenger_list.append(passenger)

        self.Passengers = new_passenger_list

    def _load(self):
        #  Stations[self.current_station].Passengers <-- passengers list
        new_passenger_list_on_station = []
        for passenger in Stations[self.current_station].Passengers:
            if len(self.Passengers) <= 400:
                if self._headed_to_right:
                    if self.current_station == 4:
                        self.Passengers.append(passenger)
                        continue
                    if passenger > self.current_station:
                        self.Passengers.append(passenger)
                    else:
                        new_passenger_list_on_station.append(passenger)
                else:
                    if self.current_station == 0:
                        self.Passengers.append(passenger)
                        continue
                    if passenger < self.current_station:
                        self.Passengers.append(passenger)
                    else:
                        new_passenger_list_on_station.append(passenger)
            else:
                new_passenger_list_on_station.append(passenger)

        Stations[self.current_station].Passengers = new_passenger_list_on_station

    async def _get_to_next_station(self):  # works
        self.is_commuting = True

        if self._headed_to_right:
            if self.current_station < 4:
                for _ in range(TimeToStations[self.current_station]):
                    self.spaces += 1
                    await asyncio.sleep(Minute)
                self.current_station += 1
                self.spaces += 1

            elif self.current_station == 4:
                self._headed_to_right = False

        if not self._headed_to_right:
            if self.current_station > 0:
                for _ in range(TimeToStationsReverse[4 - self.current_station]):
                    self.spaces -= 1
                    await asyncio.sleep(Minute)
                self.current_station -= 1
                self.spaces -= 1
            elif self.current_station == 0:
                self._headed_to_right = True

    async def do_everything_what_train_does(self):
        while True:
            self._drop_off()
            await asyncio.sleep(TimeToDrop)
            self._load()
            await self._get_to_next_station()


class Station:
    def __init__(self, n, name):
        self.Name = name
        self.Passengers = []
        self.Station = n
        self._other_stations = [0, 1, 2, 3, 4]
        del self._other_stations[n]

    def generate_passenger(self):
        destination = random.choice(self._other_stations)

        graphics.add_time_by_destination(self.Station, destination)

        self.Passengers.append(destination)


Stations = [
    Station(0, 'Рокоссовская'),
    Station(1, 'Соборная'),
    Station(2, 'Кристалл'),
    Station(3, 'Заречная'),
    Station(4, 'Библиотека им. Пушкина')
]


async def station_updater():
    while (time.time() - StartTime) * Multiply < 18:
        await asyncio.sleep(0.1)

    while True:
        for station in Stations:
            station.generate_passenger()
            await asyncio.sleep(0)

        await asyncio.sleep(Minute / 60)


async def run_trains():
    for _ in range(AmountOfTrains):
        to_add = Train()
        Trains.append(to_add)

        loop.create_task(to_add.do_everything_what_train_does())

        # print(f'Train {_ + 1} is launched.')
        await asyncio.sleep(Interval)


StartTime = time.time()

Graphics.define_start(StartTime, Minute)

UpdateTime = 1

graphics = Plots.Graphics(StartTime, Minute)

os.system('clear')

Trains = []
Interval = 38 * Minute / AmountOfTrains

signal.signal(signal.SIGINT, signal_handler)

loop = asyncio.get_event_loop()
loop.create_task(print_stats())
loop.create_task(Graphics.graphics(Trains, Stations))
loop.create_task(run_trains())
loop.create_task(station_updater())
loop.run_forever()




