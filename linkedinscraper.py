# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:07:32 2020

@author: Rushi
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv
from parameters import *

def writetoFile(sel, writer):
    # name = sel.xpath('//h1/text()').extract_first()
    name= sel.xpath('//ul//*[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first().strip()
    
    # university = sel.xpath('//ul//*[@class="result-card__title"]/text()').extract_first()
    university = sel.xpath('//section[@id="education-section"]//h3[@class="pv-entity__school-name t-16 t-black t-bold"]//text()').extract()[0]
        
    
    # degree =  sel.xpath('//section[@class="education pp-section"]//h4[@class="result-card__subtitle"]//text()').extract()
    degree =  sel.xpath('//section[@id="education-section"]//span[@class="pv-entity__comma-item"]//text()').extract()[0]
    
    #degreein=  sel.xpath('//section[@class="education pp-section"]//h4[@class="result-card__subtitle"]//text()').extract()[1]
    degreein=sel.xpath('//section[@id="education-section"]//span[@class="pv-entity__comma-item"]//text()').extract()[1]
    #frmdate = sel.xpath('//*[@class="education pp-section"]//time/text()').extract()[0]
    frmdate= sel.xpath('//*[@id="education-section"]//time/text()').extract()[0]
    # todate = sel.xpath('//*[@class="education pp-section"]//time/text()').extract()[1]
    todate= sel.xpath('//*[@id="education-section"]//time/text()').extract()[1]
    fulldate= frmdate+'-'+todate
    
    # totalconnections= sel.xpath('//*[@class= "top-card__subline-item top-card__subline-item--bullet"]/text()').extract()[0]
    totalconnections= sel.xpath('//*[@class= "ph5 pb5"]//span[@class="t-16 t-black t-normal"]/text()').extract()[0].strip()
    
    
    current_employer= sel.xpath('//*[@class="ph5 pb5"]//span[@class="text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view"]/text()').extract()[0].strip()
    current_position= sel.xpath('//*[@class="ph5 pb5"]//h2[@class="mt1 t-18 t-black t-normal break-words"]/text()').extract()[0].strip()
    
    previous_positions= sel.xpath('//*[@class="pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card artdeco-card ember-view"]//h3[@class="t-16 t-black t-bold"]/text()').extract()
    previous_employers= sel.xpath('//*[@class="pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card artdeco-card ember-view"]//p[@class= "pv-entity__secondary-title t-14 t-black t-normal"]/text()').extract()
    previous_employers=[x.strip() for x in previous_employers if x is not '']
    
    
    previous_positions_start_date= sel.xpath('//*[@class="pv-profile-section pv-profile-section--reorder-enabled background-section artdeco-container-card artdeco-card ember-view"]//h4[@class="pv-entity__date-range t-14 t-black--light t-normal"]//text()').extract()
    previous_positions_start_date= [x.strip() for x in previous_positions_start_date if (x is not '' and  'Dates Employed' not in x)]
    
    #previous_positions_duration=sel.xpath('//*[@class="experience pp-section"]//span[@class="date-range__duration"]/text()').extract()
    previous_positions_duration=""
    
    previous_stuff = {
         'prev_positions':previous_positions,
             'prev_employer':previous_employers,
             'prev_start_dt':previous_positions_start_date,
             'prev_duration':previous_positions_duration
         }
    
    writer.writerow([name, degree, degreein, university, fulldate, totalconnections, current_employer, current_position, previous_stuff])


driver = webdriver.Chrome(executable_path="C:\\Users\\h4x3d\\Documents\\chromedriver_win32\\chromedriver.exe")
linkedin_urls=['https://www.linkedin.com/in/aaron-harlap-4a22ba29/', 'https://www.linkedin.com/in/aaron-campbell-953bb9103/']
sel=[]
writer = csv.writer(open('linkedin_dt.csv', 'w'))# writerow() method to the write to the file object
writer.writerow(['Name','Degree','DegreeIn' ,'University','DegreeDuration', 'TotalConnections','CurrentEmployer', 'CurrentPosition', 'PreviousWork'])


from selenium.webdriver.common.keys import Keys
driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(linkedin_username)
sleep(0.5)
password = driver.find_element_by_id('session_password')
password.send_keys(linkedin_password)
sleep(0.5)
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(20)
driver.get('https:www.google.com')
sleep(3)



for linkedin_url in linkedin_urls:
   # get the profile URL 
   driver.get(linkedin_url)
   # add a 5 second pause loading each URL
   sleep(5)
   # assigning the source code for the webpage to variable sel
   sel = Selector(text=driver.page_source) 
   writetoFile(sel, writer)
   sleep(5)
# terminates the application
driver.quit()



