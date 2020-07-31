# Linkedin Scraper Draft



Gathering data manually for performing analysis is a very difficult task. It would take more time and a lot of manpower. Linked-in might also be selling their research analysis data, but that would again be expensive for a small capital organization.

*I’d like to propose a solution to this issue using selenium library in python. As we already have the sample data with LinkedIn URLs, we can run them in a loop and use selenium to web scrape it and generate our needed data.*

*Let us start by creating a webdriver*

```driver = webdriver.Chrome()
driver = webdriver.Chrome()
```



Many times the profiles are not public, so we would need to login to LinkedIn inside the chromedriver. The code below can be used to  login.

```driver.get('https://www.linkedin.com')
username = driver.find_element_by_id('session_key')
username.send_keys(linkedin_username)
sleep(0.5)
password = driver.find_element_by_id('session_password')
password.send_keys(linkedin_password)
sleep(0.5)
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(20)
```

 

Next we would need to parse the profile_urls one by one and then web-scrape the needed data.

```for linkedin_url in linkedin_urls:
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
```



To fetch the webpage ```driver.get(linkedin_url)``` can be used and a selector sel can be created for it. 

The sel can be pointed to X-paths of details like name, university, employer, previous_job etc.

The following function was used to extract details using sel. It takes sel, and a writer object to write to a csv file as input.



```python
def writetoFile(sel, writer):
    name= sel.xpath('//ul//*[@class="inline t-24 t-black t-normal break-words"]/text()').extract_first().strip()
    
    university = sel.xpath('//section[@id="education-section"]//h3[@class="pv-entity__school-name t-16 t-black t-bold"]//text()').extract()[0]
        
    
    degree =  sel.xpath('//section[@id="education-section"]//span[@class="pv-entity__comma-item"]//text()').extract()[0]
    
    degreein=sel.xpath('//section[@id="education-section"]//span[@class="pv-entity__comma-item"]//text()').extract()[1]
    frmdate= sel.xpath('//*[@id="education-section"]//time/text()').extract()[0]
    todate= sel.xpath('//*[@id="education-section"]//time/text()').extract()[1]
    fulldate= frmdate+'-'+todate
    
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
    
```



I have used .strip() function wherever necessary to clear out bad characters in the end like spaces or dots.



The last line  ```writer.writerow([name, degree, degreein, university, fulldate, totalconnections, current_employer, current_position, previous_stuff])```

would write the details like name, degree, degreein, university etc. to a file. And the next LinkedIn URL would be fetched.

The file looks like :-

| Name           | Degree                   | DegreeIn               | University              | DegreeDuration | TotalConnections | CurrentEmployer | CurrentPosition            | PreviousWork                                                 |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| -------------- | ------------------------ | ---------------------- | ----------------------- | -------------- | ---------------- | --------------- | -------------------------- | ------------------------------------------------------------ | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
|                |                          |                        |                         |                |                  |                 |                            |                                                              |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
| Aaron Campbell | Bachelor of Science - BS | Electrical Engineering | Northeastern University | 2015-2020      | 114 connections  | WSP             | Electrical Engineer at WSP | {'prev_positions': ['Electrical  Engineer', 'Technology Manager', 'Director of Information Technology',  'Signal Engineer Co-op', 'Electrical Engineering Co-op', 'Math/Science  Tutor'], 'prev_employer': ['WSP', '', 'The Saints Academy', '', 'Campbell  Enterprises, Inc', '', 'VHB', '', 'WSP \| Parsons Brinckerhoff', ''],  'prev_start_dt': ['', '', 'Jan 2019 – Present', '', '', '', 'Aug 2016 –  Present', '', '', '', 'Apr 2013 – Oct 2019', '', '', '', 'Jan 2018 – Jun  2018', '', '', '', 'Jan 2017 – Jun 2017', ''], 'prev_duration': ''} |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
|                |                          |                        |                         |                |                  |                 |                            |                                                              |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |
|                |                          |                        |                         |                |                  |                 |                            |                                                              |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |      |

The last column **PreviousWork** is a dictionary, like a json object. which represents the previous companies where the person was working, its duration and also the employer details. We can read it like  Aron Campbell worked as an Electrical  Engineer at WSP 

from Jan 2019 – Present.



## Drawbacks

I'm not sure if linkedin woud allow doing such things, they might have obfuscated code like Facebook. i.e. Facebook's source code changes every time we open it. But I tried for 4-5 times, it didn't change for me yet. Unfortunately I don't have linkedin premium yet so currently I'm not able to parse it further. 

I have attached a rough draft of the code, I'm looking forward to work on this further.



Thank you for your time,

Rushi Chaudhari



