import datetime
class TimeSlot:
    def __init__(self, start, duration):
        self.start = start
        self.duration = duration
        self.end = start + datetime.timedelta(minutes = duration)

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __eq__(self, other):
        return (self.start == other.start and self.duration == other.duration)

    def overlaps(self, other):
        return not ((other.end <= self.start) or (other.start >= self.end))

    def __str__(self):
        return self.start.strftime("%H:%M") + " - " + self.end.strftime("%H:%M")
    def __repr__(self):
        return self.__str__()


def splitOverlap(appts):
    cols = [[]]
    for appt in appts:
        for col in cols:
            if(not any([existing.overlaps(appt) for existing in col])):
                col.append(appt)
                break
        else:
            cols.append([appt])
    return cols
