class ResourceColumn:
    def __init__(self, name, timeSlots=None):
        self.name = name
        if timeSlots == None:
            self.timeSlots = []
        else:
            self.timeSlots = timeSlots

    def splitOverlap(self):
        cols = []
        i = 1
        for timeSlot in self.timeSlots:
            for col in cols:
                if(not any([existing.overlaps(timeSlot) for existing in col.timeSlots])):
                    col.timeSlots.append(timeSlot)
                    break
            else:
                cols.append(ResourceColumn(self.name + " " + str(i), [timeSlot]))
                i += 1
        return cols

    def __str__(self):
        return self.name + " - " + str(self.timeSlots)
    def __repr__(self):
        return self.__str__()
