import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import ElementNotInteractableException
import pandas as pd
from dateutil.parser import parse


driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")
df = pd.DataFrame(columns=['Theatre','Date','Movie Name','Runtime','Rating','Timings','URL'])
movie_details = {}
dataValues = {}
exception_list=(TimeoutException,SessionNotCreatedException,ElementClickInterceptedException,WebDriverException,NoSuchWindowException,StaleElementReferenceException,NoSuchWindowException)
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
details = []
try:
    driver.get('https://epictheatres.com')
except exception_list:
    time.sleep(10)
    driver.get("https://epictheatres.com")
try:
    driver.maximize_window()
    print('maxize window worked')
except exception_list:
    print('exception occured retrying wait')
    driver.maximize_window()

def getTheatresList():
    try:  
        theatre_list=[]
        theatres=WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='find-theater']/option")))
        for theatre in theatres:
            theatre_name=theatre.text
            theatre_list.append(theatre_name) 
        return theatre_list
    except exception_list:
    	print("exception occured in getTheatres")

def getmovienames(y,dateee,locations):
    date = dateee
    global df
    movie_list=[]
    movie_urls=[]
    try:
        movie_names=WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='showtimes']/div/section/h3/a")))  
        for movie in movie_names:
            movie_title = movie.text
            movie_list.append(movie_title)
            movie_url = movie.get_attribute('href')
            movie_urls.append(movie_url)
    except exception_list:
        time.sleep(4)	
    n = len(movie_list)
    times = []
    show_links = []
    durations = []
    for i in range(1,n+1):
        #for the Runtime and ratings of the movie
        try:
            runtime = len(WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='showtimes']//div[@class='movie']//section"))))
            rate = []
            rn = []
            for t in range(1,runtime+1):
                rating = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='showtimes']//div[@class='movie']["+str(t)+"]//section")))
                rat = rating.text
                ratings = rat.split('\n')
                if len(ratings) == 2:
                    rate.append(ratings[1])
                    rn.append('NA')
                elif len(ratings) == 3:
                    rate.append('NA')
                    rn.append(ratings[2])
                elif len(ratings) == 4:
                    rate.append(ratings[2])
                    rn.append(ratings[3])
                else:
                    rate.append('NA')
                    rn.append('NA')
        except exception_list:
            continue
        try:
            movie_timings = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='showtimes']/div["+str(i)+"]/div/div/a/button")))
            temp =[]
            for j in movie_timings:
                j = j.text
                s = j
                if "pm" or "PM" in s:
                    s = s.replace("PM", "")
                    t = s.split(":")
                    if t[0] != '12':
                        t[0] = str(int(t[0])+12)
                        s = (":").join(t)
                    show_tim = s.strip()
                else:
                    s = s.replace("AM", "")
                    t = s.split(":")
                    if t[0] == '12':
                        t[0] = '00'
                        s = (":").join(t)
                    show_tim = s.strip()

                temp.append(show_tim)
            times.append(temp)
            temp = []
        except exception_list:

            continue

        try:
            timing_links = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='showtimes']/div["+str(i)+"]/div/div/a")))
            shows = []
            for j in timing_links:
                j = j.get_attribute('href')
                shows.append(j)
            show_links.append(shows)
        except exception_list:
            continue
    try:
        count = 0
        url_count = 0
        for i,j,k,l,m in zip(movie_list,rn,rate,times,show_links):
            count += 1
            for g in range(len(l)):
                movie_details['Theatre'] = y
                movie_details['Date'] = date
                movie_details['Movie Name'] = i
                movie_details['Runtime'] = j
                movie_details['Rating'] = k
                movie_details['Timings'] = l[g]
                movie_details['URL'] = m[g]
                df = df.append(movie_details,ignore_index=True)

                split1 = m[g].split('&')
                theater_id = split1[0].split('=')[-1]
                movie_id = split1[1].split('=')[-1]
                #show_time_id = split1[-2].split('=')[-1]


                dataValues = {
                "id": '',
                "theater_id": theater_id,
                "theater_name": y,
                "address": locations[2],
                "city": locations[1],
                "state": y.split(',')[-1],
                "zipcode": locations[0],
                "movie_id": movie_id,
                "movie_name": i,
                "rating": k,
                "runtime": j,
                "amenities": '', 
                "date": date ,
                "time": l[g],
                "status": 'PENDING',
                "localtz": '',
                "local_datetime": '',
                "ticketing_url":m[g],
                "ticketing_available": 'available',
                "auditorium": '',
                "movie_format": 'standard'
                }

                for v in dataValues:
                    print(v," -->",dataValues[v])
                url_count += 1
                df.index += 1
    except exception_list:
        time.sleep(10)

    return df


def iteratingTheatres():
    lis = getTheatresList()
    m=len(lis)
    print(m," theatres found")
    #for i in range(2,3):
    for i in range(2,m+1):
        try:
            driver.get('https://epictheatres.com/')
        except exception_list:
            time.sleep(10)
            driver.get("https://epictheatres.com")
        locations = []
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='find-theater']"))).click()
        y = lis[i-1]
        if (y.find("NOW OPEN!") == -1):#For the theatres that are not open
            continue
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='find-theater']/option["+str(i)+"]"))).click()
         #theatre that is going in iteration
        location = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='info']/p[3]"))).text
        location_code = location.split(' ')[-1]
        city = location.split(' ')[0]
        address = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='info']/p[2]"))).text
        locations.append(location_code)
        locations.append(city)
        locations.append(address)
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='location']/div[2]/div[2]/div/div/div/div/div[1]"))).click()
        #popup
        except exception_list:
            time.sleep(5)
        finally:
            pass
        try:
            d_list = getdates()
            x = len(d_list)
            weekend = ['2020-12-03']
            for j in range(1,x+1):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='loc-date']/option["+str(j)+"]"))).click()
                date = d_list[j-1] #date that is going in iteration
                datee = str(parse(date).date())
                print(datee)
                if(datee in weekend):
                    output = getmovienames(y,datee,locations)
                else:
                    print(datee,"  date skipped")
        except exception_list:
            print("exception occured in iterating through dates")
    #output.to_csv('epictheatres.csv')
    output.to_excel('epictheatres111.xlsx')
    return 

def getdates():
    try:
        date_list=[]
        dates=WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='loc-date']/option")))
        for date in dates:
            datee=date.text
            date_list.append(datee) 
        return date_list
    except exception_list:
        return []

iteratingTheatres()
print("script end")
time.sleep(4)
driver.quit()
