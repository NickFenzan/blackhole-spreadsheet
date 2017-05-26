class ResourceUsage:
    def __init__(self, name, resourceType, duration):
        self.name = name
        self.resourceType = resourceType
        self.duration = duration
    def __str__(self):
        return self.name + " | " + self.resourceType + " | " + str(self.duration)
    def __repr__(self):
        return self.__str__()
