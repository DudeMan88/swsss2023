import datetime as dt # to log the time of onsets in a more readable and useful way
import matplotlib.pyplot as plt
import numpy as np


### IMPORTANT!! Defined functions can't be the same name as intrinsic functions ###
def readascii_ben(file,startline=0,endline = 10**100,rawreturn=0):
    with open(file) as f:
        if rawreturn == 1:
            rtn = [[] for x in f.readline().split()]
            print('Reading file...')
            print('number of elements: ',len(rtn))
            f.seek(0)
            for line in f:
                spln = line.split()
                for x in range(len(spln)):
                    rtn[x].append(int(spln[x]))
            print('File Reading Complete')
            return rtn
        year = [] ### following lists are used to log their respective information
        month = [] ### indicies are the same throughout all of the lists
        day = []
        hour = []
        minute = []
        second = []
        AE = []
        AL = []
        AU = []
        time = [] # A list of all of the time related variables in datetime form
        onsets=[] ### onsets is a list of indicies where an onset starts
        index = 0
        for line in f:
            index += 1
            if index > startline and index < endline:
                temp = line.split() # Makes the string into a list of values, this way the values are at the same index no matter the length
                year.append(int(temp[0]))
                month.append(int(temp[1]))
                day.append(int(temp[2]))
                hour.append(int(temp[3]))
                minute.append(int(temp[4]))
                second.append(int(temp[5]))
                AE.append(int(temp[6]))
                AL.append(int(temp[7]))
                AU.append(int(temp[8]))
                time.append(dt.datetime(int(temp[0]),int(temp[1]),int(int(temp[2])),hour = int(int(temp[3])),minute=int(temp[4]),second=int(temp[5])))
            elif index > endline: # to see if the next line surpasses the provided maximum line
                break 

        index = 0
        npts=len(AL) ### Number of points/enteries on the graph
        while index < npts-30: # can't go above 30 below max because we loop through the following 30 to test
            x=AL[index]
            if AL[index+1] - x  < -15: ### 4 conditions for storm onset ###
                if AL[index+2] - x  < -30:
                    if AL[index+3] - x  < -45:
                        s = sum(AL[index+4:index+30])/26
                        if (s- x  < -100):
                            onsets.append(index)
                            index += 29

            # if index + 31 > len(AL):
            #     # raise "No onset"
            #     break
            index +=1 
        lists = {"year" : year,
        'month':month,
        'day' : day,
        'hour' : hour,
        'minute' : minute,
        'second' : second,
        'AE' : AE,
        'AL' : AL,
        'AU' : AU,
        'time' : time,
        'onsets' : onsets}
        return lists ### Returns a dictionary of all lists in one place, this makes it easier to deal with returns from the function


Assignment = int(input("Assignment to run?(1,2,or 3) "))
NXT = 0
if Assignment == 999:NXT = 1


if Assignment == 1 or NXT == 1:
    ### ASSIGNMENT 1 ###

    data = readascii_ben("sme_2013.txt",startline=106, endline=10000) ### we only need the first onset, so we don't need a high endline
    # time = [str(dt.time(hour = x.hour,minute=x.minute,second=x.second)) for x in data['time']] 
    index = 0
    yValues = []
    xValues = []
    onset = data['onsets'][0]-2 ##gets the first onset and takes it back by 2 to show just before the start of the onset
    while (data['time'][onset+index].hour*60)+data['time'][onset+index].minute <= (data['time'][onset].hour*60) + data['time'][onset].minute + 30:
        yValues.append(data['AL'][onset+index])
        xValues.append(data['time'][onset+index])
        index+=1
        if index+onset >= len(data['time']):
            break
    print('Minimum: ',min(yValues)) # prints the minimum AL value in the graph
    xValues = np.array(xValues);yValues = np.array(yValues)
    plt.ylabel('AL value')
    plt.xlabel('Time of day in month '+ str(data['month'][onset])+' (dd:hh:mm)')
    plt.plot(xValues,yValues)
    plt.show()
    
    
if Assignment == 2 or NXT == 1:            
    ### ASSIGNMENT 2 ###
            
    data = readascii_ben('sme_2013.txt',startline=106)
    ind = data['month'].index(2) ###When does the month switch?
    for x in data['onsets']:
        if x > ind:
            y = data['onsets'].index(x)
            del data['onsets'][y:] ### When is the first index after said month switch?
            break
    del data['month'][ind:] ## Housekeeping and variable maintinance for debugging
    times = ([str(data['time'][x]) for x in data['onsets']])
    print('ONSET TIMES:\n')
    for X in times:
        print(X,'\n')
    
if Assignment == 3 or NXT == 1:
    ### ASSIGNMENT 3 ###
    
    data = readascii_ben('sme_2013.txt',startline=106)
    minimums = []
    for x in range(len(data['onsets'])):    
        index = 0
        yValues = []
        xValues = []
        onset = data['onsets'][x]-2
        while (data['time'][onset+index].hour*60)+data['time'][onset+index].minute <= (data['time'][onset].hour*60) + data['time'][onset].minute + 30:
            yValues.append(data['AL'][onset+index])
            index+=1
            if index+onset >= len(data['time']):
                break
        minimums.append(min(yValues))
        
    plt.hist(minimums,range=(-2200,-200),bins = 80)
    plt.xlabel('Minimum AL value in each onset')
    plt.show()
    
    
### EXTRA, total amount of time spent in substorms in 2013
if Assignment == 4 or NXT == 1:
    TotalMinutes = 0
    TotalStorms = 0
    data = readascii_ben('sme_2013.txt',startline=106)
    for instance in range(len(data['AL'])):
        if data['AL'][instance-1] > -499 and data['AL'][instance] <= -500:
            minutes=1
            TotalStorms += 1
            index = instance
            while data['AL'][index] <= -500:
                minutes += 1
                index += 1
            else:
                TotalMinutes += minutes
    print('total amount of time spent in substorms in 2013 in minutes: ',TotalMinutes)
    print('Total substorms in 2013: ',TotalStorms)
    print('Average time in minutes per substorm in 2013: ',TotalMinutes/TotalStorms)
    
    
    
    
    
    
    
### EXTRA, total amount of time spent in storms in 2003
if Assignment == 5 or NXT == 1:
    TotalMinutes = 0
    TotalStorms = 0
    StormIndicies = []
    years,days,hours,minlist,SYMH = readascii_ben('SYMH_2003.txt',rawreturn=1)
    print('Looping...')
    for instance in range(len(SYMH)):
        if SYMH[instance-1] > -100 and SYMH[instance] <= -100:
            minutes=1
            TotalStorms += 1
            index = instance
            StormIndicies.append(instance)
            while SYMH[index] <= -100:
                minutes += 1
                index += 1

            else:
                TotalMinutes += minutes
    temp = 0
    index = 0
    while StormIndicies[index+1] != StormIndicies[-1]:
        if StormIndicies[index+1] - StormIndicies[index] <= 750:
            print(StormIndicies[index+1],'  ',StormIndicies[index],'  ', StormIndicies[index+1]-StormIndicies[index])
            StormIndicies.remove(StormIndicies[index+1])
            TotalStorms -= 1
            temp += 1
        else:
            index+=1

    
    
    # for x in range(len(StormIndicies)-1):
    #     if StormIndicies[x] + 720 > StormIndicies[x+1]: TotalStorms -= 1;StormIndicies[x+1] = StormIndicies[x];StormIndicies[x] = 0
    print(TotalStorms+temp)
    for storm in StormIndicies:
        print(days[storm],hours[storm],minlist[storm])
        
                
    print('Total amount of time spent in a storm in 2003 in minutes: ',TotalMinutes)
    print('Total storms in 2003: ',TotalStorms)
    print('Average time in minutes per storm in 2003: ',TotalMinutes/TotalStorms)    
    
    
    
    
    
    
    
    
    
    
    
    

    
if Assignment == 77:
    EL = int(input('How many? Anything over 100,000 is a bad idea... no commas'))
    data = readascii_ben("sme_2013.txt",startline=106, endline=EL+106)
    # time = [str(dt.time(hour = x.hour,minute=x.minute,second=x.second)) for x in data['time']]
    for x in range(len(data['onsets'])):    
        index = 0
        yValues = []
        xValues = []
        onset = data['onsets'][x]-2
        while (data['time'][onset+index].hour*60)+data['time'][onset+index].minute <= (data['time'][onset].hour*60) + data['time'][onset].minute + 30:
            yValues.append(data['AL'][onset+index])
            xValues.append(data['time'][onset+index])
            index+=1
            if index+onset >= len(data['time']):
                break
        xValues = np.array(xValues);yValues = np.array(yValues)
        plt.ylabel('AL value')
        plt.xlabel('Time of day in month '+ str(data['month'][onset])+' (dd:hh:mm)')
        plt.plot(xValues,yValues)
        plt.show()
























        
        
        
        
        
        
        