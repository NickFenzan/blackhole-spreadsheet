class AppointmentType:
    def __init__(self, name, resourceUsageList):
        self.name = name
        self.resourceUsageList = resourceUsageList
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
