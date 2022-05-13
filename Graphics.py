import asyncio
import os
import time

TimeToStations = [0, 6, 3, 2, 7]

StartTime = 0
Minute = 0


def define_start(start, minute):
    global StartTime
    global Minute
    StartTime = start
    Minute = minute


async def graphics(trains, passengers):
    while True:
        os.system('clear')
        current_time = int((time.time() - StartTime) / Minute)
        start_str = f'Time elapsed: ' + str(current_time) + '\n'
        start_str += str(len(passengers[0].Passengers)) + ' ' * (14 - len(str(len(passengers[0].Passengers))))
        start_str += str(len(passengers[1].Passengers)) + ' ' * (8 - len(str(len(passengers[1].Passengers))))
        start_str += str(len(passengers[2].Passengers)) + ' ' * (6 - len(str(len(passengers[2].Passengers))))
        start_str += str(len(passengers[3].Passengers)) + ' ' * (16 - len(str(len(passengers[3].Passengers))))
        start_str += str(len(passengers[4].Passengers))
        start_str += '\n'
        start_str += 'R - - - - - - S - - - K - - Z - - - - - - - B\n'
        for train in trains:
            spaces = train.spaces
            start_str += '  ' * spaces + '🚂' + str(len(train.Passengers)) + '\n'
        print(start_str)
        await asyncio.sleep(1/25)

