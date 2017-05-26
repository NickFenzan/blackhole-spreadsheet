from datetime import datetime
import stafftimes
from TimeRange import TimeRange
from AppointmentType import AppointmentType
from ResourceUsage import ResourceUsage
from TimeSlot import TimeSlot
import ExcelWriter
from TimeSlot import TimeSlot
from ResourceColumn import ResourceColumn

START_TIME = datetime.strptime("08:00 AM", "%I:%M %p")
END_TIME = datetime.strptime("05:00 PM", "%I:%M %p")
LUNCH = TimeSlot(datetime.strptime("11:30 AM", "%H:%M %p"), 30)
INTERVAL_MINUTES = 15
timeRange = TimeRange(START_TIME, END_TIME, INTERVAL_MINUTES)

consult = AppointmentType("Consult", [
    ResourceUsage("Intake", "MedTech", 15),
    ResourceUsage("Ultrasound", "Ultrasound", 45),
    ResourceUsage("Pictures", "Physician", 15),
    ResourceUsage("Nurse", "Nurse", 30),
    ResourceUsage("Physician", "Physician", 30)
])
staffList = consult.resourceUsageList
timeSlots = [TimeSlot(time,step.duration) for time in timeRange.times for step in staffList if step.resourceType=="Physician"]
resCol = ResourceColumn("Physician",timeSlots)
print(resCol)

# staffColumns = stafftimes.generateColumnsRelativeToRole(timeRange, consult, "Physician", LUNCH)
#
# ExcelWriter.createStaffWorksheet(timeRange, staffColumns)
