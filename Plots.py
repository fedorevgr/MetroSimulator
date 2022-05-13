import time
import matplotlib.pyplot as plt


class Graphics:
    _TimeToStations = {
        1: {
            0: 6,
            1: 3,
            2: 2,
            3: 7
        },
        -1: {
            1: 6,
            2: 3,
            3: 2,
            4: 7
        }
    }

    _TimeToDrop = 0.25

    def __init__(self, start_time, minute):
        self.Minute = minute

        self.StartTime = start_time

        self.Seconds = []  # seconds passed real time

        self.Averages = []

        self.TrainAverages = []

        self.AverageTransportTime = []
        self.SecondsForTransportTime = []

        self.AveragesPerSecond = []

    def add_second(self):
        self.Seconds.append(int(time.time() - self.StartTime) / self.Minute)

    def add_time_by_destination(self, start, destination):
        self.AveragesPerSecond.append([start, destination])

    def finalize(self):
        if self.AveragesPerSecond:
            self.AverageTransportTime.append(self.AveragesPerSecond)
            self.AveragesPerSecond = []

    def _count_time_by_destinations(self):
        AverageTime = []

        for second in self.AverageTransportTime:
            Numbers = []
            for elem in second:
                step = (elem[1] - elem[0]) // (abs(elem[1] - elem[0]))
                TimeCount = 0
                for i in range(elem[0], elem[1], step):  # step = 1 start = 2 end = 4: [2, 3]
                    TimeCount += self._TimeToStations[step][i]
                    TimeCount += self._TimeToDrop
                TimeCount -= self._TimeToDrop
                Numbers.append(TimeCount)
            AverageTime.append(sum(Numbers) / len(Numbers))
        self.AverageTransportTime = AverageTime.copy()

    def _assign_the_averages_on_stations(self):
        out = [[], [], [], [], []]

        for second in self.Averages:
            for i in range(5):
                out[i].append(second[i])

        return out

    def _assign_the_average_transport_times(self):
        out = [[], []]
        for elem_id in range(len(self.AverageTransportTime)):
            if self.AverageTransportTime[elem_id]:
                out[0].append(self.AverageTransportTime[elem_id])
                out[1].append(self.Seconds[elem_id])

        return out

    def draw_plot(self):
        if self.Seconds[-1] > 18:
            try:
                self._count_time_by_destinations()
            except TypeError:
                exit(0)

            AveragesToSecond = self._assign_the_average_transport_times()
            temp = self._assign_the_averages_on_stations()

            fig, (StationsGraph,
                  TrainsGraph,
                  TransportGraph) = plt.subplots(nrows=1, ncols=3, sharex=True, figsize=(13, 6))

            line1, = StationsGraph.plot(self.Seconds, temp[0], label='Рокосовская', linewidth=0.6)
            line2, = StationsGraph.plot(self.Seconds, temp[1], label='Соборная', linewidth=0.6)
            line3, = StationsGraph.plot(self.Seconds, temp[2], label='Кристал', linewidth=0.6)
            line4, = StationsGraph.plot(self.Seconds, temp[3], label='Заречная', linewidth=0.6)
            line5, = StationsGraph.plot(self.Seconds, temp[4], label='Библиотека им. Пушкина', linewidth=0.6)
            StationsGraph.legend()
            StationsGraph.set_title('Amount of passengers on stations')

            TrainsGraph.plot(self.Seconds[1:], self.TrainAverages)
            TrainsGraph.set_title('Average train fullness')

            TransportGraph.plot(AveragesToSecond[1], AveragesToSecond[0])
            TransportGraph.set_title('Average transport time')

            plt.tight_layout()
            plt.show()
        else:
            print('Not enough time have passed!')
