import requests
import json
from datetime import date, timedelta
from calendar import monthrange
import calendar
import time
#here we want to ask the user to type in what campground they want to select
campGroundTarget = input("Please enter the name of the campgound you wish to select(NO TYPOS BRUH): ")
campgroundHeaders = {
    'authority': 'www.recreation.gov',
    'accept': 'application/json, text/plain, */*',
    'pragma': 'no-cache',
    'cache-control': 'no-cache, no-store, must-revalidate',
    'authorization': '',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.recreation.gov/',
    'accept-language': 'en-US,en;q=0.9',
}
campgroundParams = (
    ('q', campGroundTarget),
    ('geocoder', 'true'),
)
campgroundResponse = requests.get('https://www.recreation.gov/api/search/suggest', headers=campgroundHeaders, params=campgroundParams)
campgroundData = json.loads(campgroundResponse.text)
# print(campgroundData)
campgroundCode = campgroundData['inventory_suggestions'][0]['entity_id']
# print(campgroundCode)



#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.recreation.gov/api/search/suggest?q=E&geocoder=true', headers=headers)



#here we will declare a fucntion that will alow the program to derive the total days in any given starting month
def number_of_days_in_month(year, month):
    t  = (calendar.monthrange(year, month))
    return t[1]

# here we grab the user input for the reservation info
reservationStartDate = input("Enter the first day of the reservation(yyyy-mm-dd):")
reservationStartDate += 'T00:00:00Z'

#prompt the user for input on the month their start date lies in
dateVal = reservationStartDate[0:8] + '01T00:00:00.000Z'
print(dateVal)
startDateVal = dateVal 
#here we extract the starting day of the month to be used in a calculation 
# figuing out how many days are in between the start day and the end day
startDayDigit = int(reservationStartDate[8:10])
startMonthDigit = int(reservationStartDate[5:7])
starYear = int(startDateVal[0:4])
#extract the day that the reservation starts on and convert it to an int 
# so we can add +1 after each previously scanned day returns "available"
startDayIncrement = int(reservationStartDate[8:10])
#we need to convert the reservation start date into a modular format that allows us to increment the day value
#if the increment day variable is below ten we need to add a 0 into the string before hand 
# if not, then we can just add the increment counter in as is
if(startDayIncrement-10<0):
    modularReservationStartDate = reservationStartDate[0:8] + "0" + str(startDayIncrement) + reservationStartDate[10:]
else:
    modularReservationStartDate = reservationStartDate[0:8] + str(startDayIncrement) + reservationStartDate[10:]
#generate variables that contains the day and month of start/end so we can compare
#if the month is the same then we will only need to make one request to get one month worth of reservation data
#if the months differ, then we will need to make 2 calls to api and double our efforts to create a dict of the second data stream
reservationEndDate = input("Enter the last day of the reservation(yyyy-mm-dd):")
reservationEndDate += 'T00:00:00Z'
#here we extract the ending day of the month to be used in a calculation 
# figuing out how many days are in between the start day and the end day
endDayDigit = int(reservationEndDate[8:10])
endMonthDigit = int(reservationEndDate[5:7])
yearInQuestion = int(reservationStartDate[0:4])
# parsing the end month date so we can get the first of that month, 
# which is required to make a get request to get that months availabilities
endDateVal = reservationEndDate[0:8] + "01T00:00:00.000Z"
daysInFirstMonth =number_of_days_in_month(starYear, startMonthDigit)

siteWeWant = ''
siteWeWant = input("Enter your site in all capitals, no spaces, single digit sites need to be preceeded by a 0 (B03, A02, etc...): ")

def userExperience2():
    print(time.ctime())
    
    siteWeWant = input("Enter your site in all capitals, no spaces, single digit sites need to be preceeded by a 0 (B03, A02, etc...): ")

    #right here is the logic we will put in that takes the length of stay 
    # and attatches it to a for loop in terms of range
    begin = date(yearInQuestion, startMonthDigit, startDayDigit)
    end = date(yearInQuestion, endMonthDigit, endDayDigit)
    lengthOfStay = (end -begin)
    # print("Length of stay is: " + str(lengthOfStay.days))
    #the method via which we check individual days of each month
    def singleDayCheck2(dayInQuestion, siteInQuestion, dateValue, campgroundID):

        url1 = 'https://www.recreation.gov/camping/campgrounds/' + campgroundID + '/availability'
        url2 = 'https://www.recreation.gov/api/camps/availability/campground/' + campgroundID + '/month'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Connection': 'keep-alive',
            'Referer': url1,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }

        params = (
        ('start_date', dateValue),
        )

        response = requests.get(url2, headers=headers, params=params)
        data = json.loads(response.text)
        
        # 3383 is the starting id in the response JSON
        # 4629 is the ending id in the response JSON
        #a total of 217 sites exist each with their own respective reserved/avaiable status
        #  essentially a vitural 2 dimensional array
        rows, cols = (217, 2)
        # create 2 arrays, one for sites and one for associated availabilities
        siteNames = []
        siteReserved = []
        #we will now calculate the total length of stay by subtracting 
        # the ending day of the reservation from the first day of the reservation



        # start the site counter a the lowest campsite i-d it doesnt necessarily mean that its the first campsite alphabetically 
        siteCounter = 3383
        for j in data['campsites']:
            if(siteCounter==3463):
                siteCounter = 3465
            if(siteCounter==3469):
                siteCounter = 3471
            if(siteCounter==3473):
                siteCounter = 3475
            if(siteCounter==3476):
                siteCounter = 3478
            if(siteCounter==3480):
                siteCounter = 3482
            if(siteCounter==3483):
                siteCounter = 3488
            if(siteCounter==3489):
                siteCounter = 3490
            if(siteCounter==3491):
                siteCounter = 3493
            if(siteCounter==3494):
                siteCounter = 3495
            if(siteCounter==3496):
                siteCounter = 4507
            stringCounter = str(siteCounter)
            siteNames.append(data['campsites'][j]['site'])
            siteReserved.append(data['campsites'][j]['availabilities'][dayInQuestion])
            siteCounter += 1
        campSitesDict = dict(zip(siteNames, siteReserved))
        all_sites = list(campSitesDict.items())
        # print(all_sites)

        #this will simulate iterating over the days specified in the reservation
        #if all == "Avaiable" then we can break out of the loop and return true
        # print(campSitesDict[siteInQuestion])
        if(campSitesDict[siteInQuestion]=="Reserved"):
            # print("printing false")
            return False
        else:
            # print("printing true")
            return True



    #now we make our big fork in the road choice - 
    # is the reservation consolidated into one month or spread between two?
    #if the start month and end month are the same then we only make one call/python request
    if(startMonthDigit==endMonthDigit):
        # print("only one month search needed")
        #pull the day digit from the user input above so it can be incremented upon
        dayTarget = int(reservationStartDate[8:10])
        # print(siteWeWant)
        #this loops helps us scan the multiple days included in the reservation
        for x in range(endDayDigit-startDayDigit + 1):

            if(dayTarget-10<0):
                dayTargetFormatted = reservationStartDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
            else:
                dayTargetFormatted = reservationStartDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
            # print(dayTarget)
            # print(dayTargetFormatted)
            if(singleDayCheck2(dayTargetFormatted, siteWeWant, startDateVal, campgroundCode)==False):

                print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                # continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                # if(continueLooking=='y'):
                #     userExperience()
                # else:
                # exit()

                break
            else:
                print("")
            dayTarget += 1
            loopCounter = str(x)
            # print("Finished one pass " + loopCounter + " of the loop")
            # print(dayTarget)
            if(x==endDayDigit-startDayDigit):
                print("The entire reservation is avaiable yayyyyy")
                print("-------------------------------------------")
                continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                if(continueLooking=='y'):
                    userExperience()
                else:
                    exit()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
    #if the start month and end month are not the same then we make two calls/python requests 
    # because we will need to see availabilities for both months
    else:
        # print("two months of data will be needed")
        #this is the request that calls for the first months data
        def secondRequest2():
            # print("we are in the second request")
            #pull the day digit from the user input above so it can be incremented upon
            dayTarget = 1
            secondMonthDeliniator = int(lengthOfStay.days) - (daysInFirstMonth - startDayDigit)
            # print("second month deliniator is: " + str(secondMonthDeliniator))
            #this loops helps us scan the multiple days included in the reservation
            for x in range(secondMonthDeliniator):
                # print("we are in the second loop")
                if(dayTarget-10<0):
                    dayTargetFormatted = reservationEndDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
                else:
                    dayTargetFormatted = reservationEndDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
                # print(dayTarget)
                # print(dayTargetFormatted)
                if(singleDayCheck2(dayTargetFormatted, siteWeWant, endDateVal, campgroundCode)==False):
                    print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                    # continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    # if(continueLooking=='y'):
                    #     userExperience()
                    # else:
                    #     exit()
                    break
                else:
                    print("")
                dayTarget += 1
                loopCounter = str(x)
                # print("Finished one pass " + loopCounter + " of the loop")
                # print(dayTarget)
                if(x==secondMonthDeliniator-1):
                    print("The entire reservation is avaiable BIIIIIIITCH")
                    print("-------------------------------------------")
                    continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    if(continueLooking=='y'):
                        userExperience2()
                    else:
                        exit()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
        #if the start month and end month are not the same then we make two calls/python requests 
        # because we will need to see availabilities for both months
        
        
        def firstRequest2():
            # print("we are in the first request")
            #pull the day digit from the user input above so it can be incremented upon
            dayTarget = int(reservationStartDate[8:10])
            # print("days in month " + str(daysInFirstMonth))
            firstMonthDeliniator = daysInFirstMonth - startDayDigit
            # print(firstMonthDeliniator)
            #this loops helps us scan the multiple days included in the reservation
            for x in range(firstMonthDeliniator + 1):
                # print(x)
                if(dayTarget-10<0):
                    dayTargetFormatted = reservationStartDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
                else:
                    dayTargetFormatted = reservationStartDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
                # print(dayTarget)
                # print(dayTargetFormatted)
                if(singleDayCheck2(dayTargetFormatted, siteWeWant, startDateVal, campgroundCode)==False):
                    print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                    continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    if(continueLooking=='y'):
                        userExperience2()
                    else:
                        exit()
                    break
                else:
                    print("")
                dayTarget += 1
                loopCounter = str(x)
                # print("Finished one pass " + loopCounter + " of the loop")
                # print(dayTarget)
                if(x==firstMonthDeliniator):
                    # print("we are calling the second request")
                    secondRequest2()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
        #if the start month and end month are not the same then we make two calls/python requests 
        # because we will need to see availabilities for both months
        
        firstRequest2()



def userExperience():
    print(time.ctime())
    

    #right here is the logic we will put in that takes the length of stay 
    # and attatches it to a for loop in terms of range
    begin = date(yearInQuestion, startMonthDigit, startDayDigit)
    end = date(yearInQuestion, endMonthDigit, endDayDigit)
    lengthOfStay = (end -begin)
    # print("Length of stay is: " + str(lengthOfStay.days))
    #the method via which we check individual days of each month
    def singleDayCheck(dayInQuestion, siteInQuestion, dateValue, campgroundID):

        url1 = 'https://www.recreation.gov/camping/campgrounds/' + campgroundID + '/availability'
        url2 = 'https://www.recreation.gov/api/camps/availability/campground/' + campgroundID + '/month'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Connection': 'keep-alive',
            'Referer': url1,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }

        params = (
        ('start_date', dateValue),
        )

        response = requests.get(url2, headers=headers, params=params)
        data = json.loads(response.text)
        
        # 3383 is the starting id in the response JSON
        # 4629 is the ending id in the response JSON
        #a total of 217 sites exist each with their own respective reserved/avaiable status
        #  essentially a vitural 2 dimensional array
        rows, cols = (217, 2)
        # create 2 arrays, one for sites and one for associated availabilities
        siteNames = []
        siteReserved = []
        #we will now calculate the total length of stay by subtracting 
        # the ending day of the reservation from the first day of the reservation



        # start the site counter a the lowest campsite i-d it doesnt necessarily mean that its the first campsite alphabetically 
        siteCounter = 3383
        for j in data['campsites']:
            if(siteCounter==3463):
                siteCounter = 3465
            if(siteCounter==3469):
                siteCounter = 3471
            if(siteCounter==3473):
                siteCounter = 3475
            if(siteCounter==3476):
                siteCounter = 3478
            if(siteCounter==3480):
                siteCounter = 3482
            if(siteCounter==3483):
                siteCounter = 3488
            if(siteCounter==3489):
                siteCounter = 3490
            if(siteCounter==3491):
                siteCounter = 3493
            if(siteCounter==3494):
                siteCounter = 3495
            if(siteCounter==3496):
                siteCounter = 4507
            stringCounter = str(siteCounter)
            siteNames.append(data['campsites'][j]['site'])
            siteReserved.append(data['campsites'][j]['availabilities'][dayInQuestion])
            siteCounter += 1
        campSitesDict = dict(zip(siteNames, siteReserved))
        all_sites = list(campSitesDict.items())
        # print(all_sites)

        #this will simulate iterating over the days specified in the reservation
        #if all == "Avaiable" then we can break out of the loop and return true
        # print(campSitesDict[siteInQuestion])
        if(campSitesDict[siteInQuestion]=="Reserved"):
            # print("printing false")
            return False
        else:
            # print("printing true")
            return True



    #now we make our big fork in the road choice - 
    # is the reservation consolidated into one month or spread between two?
    #if the start month and end month are the same then we only make one call/python request
    if(startMonthDigit==endMonthDigit):
        # print("only one month search needed")
        #pull the day digit from the user input above so it can be incremented upon
        dayTarget = int(reservationStartDate[8:10])
        # print(siteWeWant)
        #this loops helps us scan the multiple days included in the reservation
        for x in range(endDayDigit-startDayDigit + 1):

            if(dayTarget-10<0):
                dayTargetFormatted = reservationStartDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
            else:
                dayTargetFormatted = reservationStartDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
            # print(dayTarget)
            # print(dayTargetFormatted)
            if(singleDayCheck(dayTargetFormatted, siteWeWant, startDateVal, campgroundCode)==False):

                print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                # continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                # if(continueLooking=='y'):
                #     userExperience()
                # else:
                # exit()

                break
            else:
                print("")
            dayTarget += 1
            loopCounter = str(x)
            # print("Finished one pass " + loopCounter + " of the loop")
            # print(dayTarget)
            if(x==endDayDigit-startDayDigit):
                print("The entire reservation is avaiable yayyyyy")
                print("-------------------------------------------")
                continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                if(continueLooking=='y'):
                    userExperience2()
                else:
                    exit()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
    #if the start month and end month are not the same then we make two calls/python requests 
    # because we will need to see availabilities for both months
    else:
        # print("two months of data will be needed")
        #this is the request that calls for the first months data
        def secondRequest():
            # print("we are in the second request")
            #pull the day digit from the user input above so it can be incremented upon
            dayTarget = 1
            secondMonthDeliniator = int(lengthOfStay.days) - (daysInFirstMonth - startDayDigit)
            # print("second month deliniator is: " + str(secondMonthDeliniator))
            #this loops helps us scan the multiple days included in the reservation
            for x in range(secondMonthDeliniator):
                # print("we are in the second loop")
                if(dayTarget-10<0):
                    dayTargetFormatted = reservationEndDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
                else:
                    dayTargetFormatted = reservationEndDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
                # print(dayTarget)
                # print(dayTargetFormatted)
                if(singleDayCheck(dayTargetFormatted, siteWeWant, endDateVal, campgroundCode)==False):
                    print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                    # continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    # if(continueLooking=='y'):
                    #     userExperience()
                    # else:
                    #     exit()
                    break
                else:
                    print("")
                dayTarget += 1
                loopCounter = str(x)
                # print("Finished one pass " + loopCounter + " of the loop")
                # print(dayTarget)
                if(x==secondMonthDeliniator-1):
                    print("The entire reservation is avaiable BIIIIIIITCH")
                    print("-------------------------------------------")
                    continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    if(continueLooking=='y'):
                        userExperience2()
                    else:
                        exit()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
        #if the start month and end month are not the same then we make two calls/python requests 
        # because we will need to see availabilities for both months
        
        
        def firstRequest():
            # print("we are in the first request")
            #pull the day digit from the user input above so it can be incremented upon
            dayTarget = int(reservationStartDate[8:10])
            # print("days in month " + str(daysInFirstMonth))
            firstMonthDeliniator = daysInFirstMonth - startDayDigit
            # print(firstMonthDeliniator)
            #this loops helps us scan the multiple days included in the reservation
            for x in range(firstMonthDeliniator + 1):
                # print(x)
                if(dayTarget-10<0):
                    dayTargetFormatted = reservationStartDate[0:8] + "0" + str(dayTarget)  + 'T00:00:00Z'
                else:
                    dayTargetFormatted = reservationStartDate[0:8] + str(dayTarget)  + 'T00:00:00Z'
                # print(dayTarget)
                # print(dayTargetFormatted)
                if(singleDayCheck(dayTargetFormatted, siteWeWant, startDateVal, campgroundCode)==False):
                    print("At least one of the days is taken on the desired so the reservation cannot be made yet")
                    continueLooking = input("Would you like to look for another site? (Enter 'y' or 'n'): ")
                    if(continueLooking=='y'):
                        userExperience2()
                    else:
                        exit()
                    break
                else:
                    print("")
                dayTarget += 1
                loopCounter = str(x)
                # print("Finished one pass " + loopCounter + " of the loop")
                # print(dayTarget)
                if(x==firstMonthDeliniator):
                    # print("we are calling the second request")
                    secondRequest()
        #once the entire loop finishes and no false have been returned,
        #  we can be sure that the reservation is avaiable
        #if the start month and end month are not the same then we make two calls/python requests 
        # because we will need to see availabilities for both months
        
        firstRequest()
        
while True:
    userExperience()
    time.sleep(5)





  