import calendar
import xlrd
import pandas as pd
from openpyxl import load_workbook
class Worker:
    def __init__(self, name, workdays, endTime=9, cCount=0):
        self.name = name #TA's name
        self.workdays = self.beautifyWorkDays(workdays) #TA's days of work
        self.cleanCount = cCount #TA's number of times cleaned
        self.workEnd = endTime #time the TA gets off work

    def stats(self):
        """ prints the instance variables of a TA"""
        print(self.name, self.workdays, self.cleanCount, self.workEnd)

    def beautifyWorkDays(self,ugly):
        """ Removes white space and commas for a TA's workdays from the excel file 
            Workdays must be comma deliminated to work
            
            Takes in the string ugly and returns pretty"""

        pretty = []
        tempString = ""
        for duck in ugly:
            if duck == ",":
                pretty.append(tempString)
                tempString = ""
            elif duck == " ":
                pass
            else:
                tempString += duck
        pretty.append(tempString)
        
        return pretty

    def getName(self):
        return self.name
    
    def getWorkDays(self):
        return self.workdays

    def getCleanCount(self):
        return self.cleanCount

    def getWorkEnd(self):
        return self.workEnd

    def cleaned(self):
        self.cleanCount += 1

    def mopped(self):
        self.cleanCount += 2


def calendarDays(excluded=[]):
    """ Returns a list of repeated Mon-Sun days of the week
        Corresponds to the lab days for the month

        excluded: the dates without lab days
                  a list of numbers
        """
    #Use Calendar to get the right days and dates for the month/year
    labDays = []
    weekdays = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Sun"}

    #IMPORTANT# 
    #IMPORTANT# 
    year = 2019 #Change this for the correct year
    #IMPORTANT# 
    #IMPORTANT# 
    days = []
    month = int(input("What month number is it?:"))
    cal = calendar.Calendar()
    for i in cal.itermonthdays(year, month): # loops through the month and adds only lab days 
        if i in excluded: # if the date is in the list of dates to exclude, don't do anything
            pass
        elif i > 0:
            days.append(i)
            day = calendar.weekday(year, month, i)
            if 0 <= day <= 4: # if the date is Sun-Thur
                labDays.append(weekdays[day])
    print(days)
    return labDays

def getAvailableWorkers(day, labDays,workers):
    """returns a list of only the TAs available for this day
        day: the current day (0-31)
        labDays: list of labDays consiting of Mon-Thu repetitions
        workers: list of worker objects
        """
    availableWorkers = []
    for worker in workers:
        if labDays[day] in worker.getWorkDays():
            availableWorkers.append(worker)
    return availableWorkers
    
def decideWorkers(availableWorkers,today,num=4,mopping=False):
    """ takes the available workers and appends num workers with lowest clean count to the current work day.
        
        availableworkers: workers that are available to work on the current day
        daySched:         a list representing who works the current day
        num:              how many people to pick for working"""
    secondary = 0 # count for how many secondaries are working today

    availableWorkers.sort(key=lambda worker: worker.getCleanCount())
    for minion in availableWorkers[:num]: # take the first four lowest
        if minion.getWorkEnd() != 9.0: # find the number of secondaries
            secondary += 1

    for minion in availableWorkers[:num+secondary]: # take the first four lowest and additionals to replace secondaries
        if mopping and (minion.getWorkEnd() == 9.0): #only people who will be at the end of lab to mop gets mopping counted
            minion.mopped()
        else: #if they aren't mopping or cannot mop, they only clean
            minion.cleaned()
        # Add this assignment to the schedule
        working = (minion.getName(),minion.getCleanCount()) #make the name and clean count a tuple
    
        
        
        today.append(working)
    return today

def makeSchedule(labDays, workers,mopFreq=3):
    """ Returns a list of lists representing who works each day lab is open
        
        labDays: list of lab days
        workers: list of workers 
        mopFreq: how often to mop AKA every # days to mop"""
    cleaningSched = [] #nested list of who cleans each day
    #For every day in labDays
    mopTime = False
    mopCount = 2
    for i in range(len(labDays)):
        daySched = [] # list of today's workers
        daySched.append(labDays[i])  # Add Current Day to the list

        if mopCount%mopFreq==0:
            mopTime = True
        
        availableWorkers = getAvailableWorkers(i,labDays,workers) #find who can work today
        cleaningSched.append(decideWorkers(availableWorkers,daySched,4,mopTime)) # add workers to the day and append it to the cleaning schedule
        
        #append "Mopped" to the end of the day's schedule instead of the beginning
        if mopTime:
            daySched.append("Mopped")
        #set mopTime to false, so we don't make everyone mop
        mopTime = False
        mopCount += 1
    return cleaningSched


def main():
    
    workers = []
    #find the excel sheet
    loc = ("TASched.xlsx")
    rb = xlrd.open_workbook(loc)
    sheet = rb.sheet_by_index(0)
    #############################
    # each row is a person
    # make a TA object out of them
    for i in range(1,sheet.nrows):
        person = Worker(sheet.cell_value(i,0), list(sheet.cell_value(i,1)), sheet.cell_value(i,2), sheet.cell_value(i,3))
        workers.append(person)
        #print(sheet.cell_value(i,0))
    ##############################

    #Use Calendar to get the right days and dates for the month/year
    exclusions = [11,29,30]
    print(exclusions)
    labDays = calendarDays(exclusions)
    ###########################################################################################
    #Create the cleaning schedule then print it
    cleaningSched = makeSchedule(labDays,workers)
    for day in cleaningSched:
        print(day)
    ########################################################################## 

main()
