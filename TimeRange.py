import datetime

class TimeRange:
    def __init__(self, start, end, interval):
        self.start = start
        self.end = end
        self.interval = interval
        self._generateList()
    def _generateList(self):
        self.times = []
        currentTime = self.start
        while currentTime < self.end:
            self.times.append(currentTime)
            currentTime += datetime.timedelta(minutes = self.interval)
    def validTimeSlot(self, timeSlot):
        return timeSlot.start >= self.start and timeSlot.end <= self.end
