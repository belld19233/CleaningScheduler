#Scott says Add comments
import calendar


class TA:
    def __init__(self, name, workdays, cCount=0):
        self.name = name
        self.workdays = [i[0:2] for i in workdays]
        self.cleanupCount = cCount


def parseSched(textFile):
    schedFile = open(textFile, 'r')
    sched = []
    for line in schedFile:
        sched.append(
            TA(
                line.split(",")[0],
                line.split(",")[1:], int(line.split(",")[-2])))

    return sched


def main():
    #Change this to match the days of the month
    labDays = []
    weekdays = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Su"}
    year = 2018
    month = int(input("What month number is it?:"))
    cal = calendar.Calendar()
    for i in cal.itermonthdays(year, month):
        if 0 < i:
            day = calendar.weekday(year, month, i)
            if 0 <= day <= 4:
                labDays.append(weekdays[day])

    TASched = parseSched("TASched.txt")

    cleaningSched = []
    #For every day in labDays
    for i in range(len(labDays)):
        daySched = []
        daySched.append(labDays[i])  # Add Current Day
        # Create a list of only the TAs available for this day
        availableTAs = []
        for TA in TASched:
            if labDays[i] in TA.workdays:
                availableTAs.append(TA)
        # Get 3 Lowest Count TAs and assign them
        availableTAs.sort(key=lambda x: x.cleanupCount)
        for TA in availableTAs[:3]:
            TA.cleanupCount += 1
            # Add this assignment to the schedule
            daySched.append(TA.name)
            daySched.append(str(TA.cleanupCount))
        cleaningSched.append(daySched)

    [print(' '.join(day)) for day in cleaningSched]

    print("")
    for TA in TASched:
        print(TA.name, "cleans", TA.cleanupCount, "times")


main()
