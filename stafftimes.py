import datetime
from TimeSlot import TimeSlot
import TimeSlot as ts
from ResourceColumn import ResourceColumn
import random
import names

def generateColumnsRelativeToRole(timeRange, appointmentType, role, lunch):
    def randomColor():
        r = lambda: random.randint(0,255)
        return ('%02X%02X%02X' % (r(),r(),r()))

    def findPrimaryRoleTimes(timeRange, staffList, role, lunch):
        timeSlots = []
        for time in timeRange.times:
            roleIndex = next(i for i,v in enumerate(staffList) if v.resourceType == role)
            for staffTime in [v.duration for i,v in enumerate(staffList) if i < roleIndex]:
                time += datetime.timedelta(minutes = staffTime)
            timeSlot = TimeSlot(time, staffList[roleIndex].duration)
            timeSlot.color = randomColor()
            timeSlot.patient = names.get_first_name()
            timeSlot.info = staffList[roleIndex].name
            for staffTime in [v.duration for i,v in enumerate(staffList) if i > roleIndex]:
                time += datetime.timedelta(minutes = staffTime)
            latestStaffTimeSlot = TimeSlot(time, staffList[-1].duration)
            if (timeRange.validTimeSlot(timeSlot) and
                    timeRange.validTimeSlot(latestStaffTimeSlot) and
                    not lunch.overlaps(timeSlot) and
                    not any([existing.overlaps(timeSlot) for existing in timeSlots])):
                timeSlots.append(timeSlot)
        return timeSlots

    def findRelativeTimes(primaryTimes, staffList, relativeRole, role):
        timeSlots = []
        for primaryTimeSlot in primaryTimes:
            start = primaryTimeSlot.start
            primaryIndex = next(i for i,v in enumerate(staffList) if v.resourceType == relativeRole)
            roleIndex = next(i for i,v in enumerate(staffList) if v.resourceType == role)
            for staffTime in [v.duration for i,v in enumerate(staffList) if i < primaryIndex and i >= roleIndex]:
                start -= datetime.timedelta(minutes = staffTime)
            for staffTime in [v.duration for i,v in enumerate(staffList) if i > primaryIndex and i <= roleIndex]:
                start += datetime.timedelta(minutes = staffTime)
            timeSlot = TimeSlot(start, staffList[roleIndex].duration)
            timeSlot.color = primaryTimeSlot.color
            timeSlot.patient = primaryTimeSlot.patient
            timeSlot.info = staffList[roleIndex].name
            timeSlots.append(timeSlot)
        return timeSlots

    def visitDurationFromStaffList(staffList):
        return sum([staff.duration for staff in staffList])

    def createResourceColumnIfNotExists(staffColumns, role):
        for col in [x for x in staffColumns if x.name == role]:
            return col
        else:
            newCol = ResourceColumn(role)
            staffColumns.append(newCol)
            return newCol

    def findPrimaryRoleTimes2(timeRange, staffList, role, lunch, staffColumns):
        def addTimes(timeRange, staffList, role, lunch, resourceColumn, visitDuration):
            def addAppointmentIfValid(timeRange, staffList, role, lunch, resourceColumn, apptEnd, color, patient):
                if (timeRange.end >= apptEnd):
                    tenativeSteps = []
                    for staffStep in staffList:
                        if staffStep.resourceType == role:
                            timeSlot = TimeSlot(time, staffStep.duration)
                            timeSlot.color = color
                            timeSlot.patient = patient
                            timeSlot.info = staffStep.name
                            tenativeSteps.append(timeSlot)
                        time += datetime.timedelta(minutes = staffStep.duration)
                    if (not any(step.overlaps(lunch) for step in tenativeSteps)
                    and not any(step.overlaps((x for x in resourceColumn.timeSlots)) for step in tenativeSteps)):
                        resourceColumn.timeSlots.extend(tenativeSteps)
            for time in timeRange.times:
                apptEnd = time + datetime.timedelta(minutes = visitDuration)
                color = randomColor()
                patient = names.get_first_name()
                addAppointmentIfValid(timeRange, staffList, role, lunch, resourceColumn, apptEnd, color, patient)

        # firstPrimaryRoleIndex = next(i for i,v in enumerate(staffList) if v.resourceType == role)
        # lastPrimaryRoleIndex = len(staffList) - next(i for i,v in enumerate(list(reversed(staffList))) if v.resourceType == role)
        resourceColumn = createResourceColumnIfNotExists(staffColumns, role)
        addTimes(timeRange, staffList, role, lunch, resourceColumn)






    staffColumns = []
    staffList = appointmentType.resourceUsageList
    findPrimaryRoleTimes2(timeRange, staffList, role, lunch, staffColumns)

    ResourceColumn(role,[])
    # primaryRoleTimes = findPrimaryRoleTimes(timeRange, staffList, role, lunch)
    # for staff in staffList:
    #     if staff.resourceType == role:
    #         staffColumns.append(ResourceColumn(staff.resourceType, primaryRoleTimes))
    #     else:
    #         roleTimes = findRelativeTimes(primaryRoleTimes, staffList, role, staff.resourceType)
    #         resourceCol = ResourceColumn(staff.resourceType, roleTimes)
    #         for col in resourceCol.splitOverlap():
    #             staffColumns.append(col)
    return staffColumns
