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
import xlrd

driver = webdriver.Chrome(r"C:\webdrivers\chromedriver.exe")
exception_list=(TimeoutException,SessionNotCreatedException,ElementClickInterceptedException,WebDriverException,NoSuchWindowException,StaleElementReferenceException,NoSuchWindowException)
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
df = pd.DataFrame(columns=['URL','Total_Seat','Available_Seat','Available_Accessible_Seat','Available_Companion_Seat','Unavailable_Seat','Price','Senior_seat_price','Child_seat_price','Service_Charge','Tax','Total_Price'])
seatings = {}
try:
    driver.maximize_window()
    print('maxize window worked')
except exception_list:
    print('exception occured retrying wait')
    driver.maximize_window()

def getseatingdetails(k,senior,child):
	global df
	try:
		seats = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/button")))
		total = []
		ava = 0
		aas = 0
		acs = 0
		una = 0
		for seat in seats:
			seat = seat.get_attribute('title')
			total.append(seat)
			total_seats = len(total)
		for i in total:
			if(i == "Available  Seat"):
				ava = ava + 1
			elif(i == "Available Accessible Seat"):
				aas = aas+1
			elif(i == "Available Companion Seat"):
				acs = acs+1
			else:
				una = una+1
		price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div/div[3]"))).text
		service_charge = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[4]/span"))).text
		tax = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[4]/span"))).text
		total_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[2]/h3[2]/span"))).text

	except exception_list:
		try:
			total_seats = 'NA'
			ava = 'NA'
			aas = 'NA'
			acs = 'NA'
			una = 'NA'
			price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div/div[3]"))).text
			try:
				service_charge = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[4]/span"))).text
			except exception_list:
				service_charge = 'NA'
			try:
				tax = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[1]/div[4]/span"))).text
			except exception_list:
				tax ='NA'
			try:
				total_price = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[2]/div/div/div[2]/h3[2]/span"))).text
			except exception_list:
				total_price = 'NA'
		except exception_list:
			time.sleep(5)
 
	seatings['URL'] = k
	seatings['Total_Seat'] = total_seats
	seatings['Available_Seat'] = ava
	seatings['Available_Accessible_Seat'] =aas
	seatings['Available_Companion_Seat'] =acs
	seatings['Unavailable_Seat'] =una
	seatings['Price'] =price
	seatings['Senior_seat_price'] = senior
	seatings['Child_seat_price'] = child
	seatings['Service_Charge'] =service_charge
	seatings['Tax'] =tax
	seatings['Total_Price'] =total_price
	for o in seatings:
		print(o,"-->",seatings[o])

	df = df.append(seatings,ignore_index=True)
	return df

def iteratingShows():
	path = (r"C:\Users\Manoj Ramalingappa B\Desktop\python\epictheatres111.xlsx")
	df = pd.read_excel(path)
	data = (df['URL'])
	for i in data:
		try:
			driver.get(i)
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[4]/div/div[2]/div/div/button"))).click()	
			try:
				senior = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[3]/div/div/div[2]/div[2]/p[2]"))).text
			except exception_list:
				senior = ''
			try:
				child = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[3]/div/div/div[3]/div[2]/p[2]"))).text
			except exception_list:
				child = ''
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[3]/div/div/div[1]/div[3]/button"))).click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='root']/div/div/div[1]/div[1]/div[2]/div[4]/div/div/button"))).click()
			try:
				WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div/div/div[3]/div/div/div/button"))).click()
				print("continue worked")
			except exception_list:
				 pass
			output = getseatingdetails(i,senior,child)
		except exception_list:
			print(i)
			continue
	output.to_excel('epictheatres222.xlsx')
	return

iteratingShows()
time.sleep(4)
driver.quit()
