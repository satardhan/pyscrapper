import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

def all_href_ext(url):
    lis =[]
    driver.get(url)
    lnks_1 = driver.find_elements(By.TAG_NAME,'div')
    found_link = False
    for a in lnks_1:
         lnks_2 = a.find_elements(By.CLASS_NAME,'vn-sheduleList')
         for b in lnks_2:
            lnks=b.find_elements(By.TAG_NAME,"li")
            for lnk in lnks:
                ln = lnk.find_element(By.CLASS_NAME,'vn-schedule-head')
                _num = lnk.find_element(By.CLASS_NAME,'w20')
                ln = lnk.find_element(By.CLASS_NAME,'vn-ticnbtn')
                l = ln.find_elements(By.TAG_NAME,"a")
                try:
                    found_link = True
                    for h_ref in l:
                        dta ={}
                        if 'match/' in h_ref.get_attribute('href'):
                            dta['num']=str(_num.text)
                            dta['url']=h_ref.get_attribute('href')
                            lis.append(dta)
                except:continue
            if found_link:break
         if found_link:break
    return lis


# Function to get match result from ipl season page
def get_match_res(url):
    driver.get(url)
    div_ele= driver.find_elements(By.TAG_NAME,"div")
    for links_ in div_ele:
        lnks = links_.find_elements(By.CLASS_NAME,"ap-match-innerwrp")
        match_result=set()
        for lnk in lnks:
            try:
                stad_name = lnk.find_element(By.CLASS_NAME,"matGround")
                stad_name = stad_name.text
                match_date = lnk.find_element(By.CLASS_NAME,"ms-matchdate")
                match_date = match_date.text
                match_time = lnk.find_element(By.CLASS_NAME,"ms-matchtime")
                match_time = match_time.text
                liinks=lnk.find_elements(By.CLASS_NAME,"ms-matchComments")
                for i in liinks:
                    if len(i.text)>1:
                        match_result.add(i.text)
                    else:continue
            except StaleElementReferenceException:continue
            except NoSuchElementException:continue
        if len(match_result)>1:
            for match_res in match_result:
                if "D/L Method" in match_res: return stad_name,match_date,match_time,match_res
        else:
            for match_res in match_result: return stad_name,match_date,match_time,match_res


# Function to get home team and away team from schedule page
def hm_tm_aw_tm(url):
   all_lst=[]
   driver = webdriver.Chrome(options=options)
   driver.get(url)
   time.sleep(10)
   lnks=driver.find_elements(By.TAG_NAME,"li")
   for lnk in lnks:
      teams=[]
      try:
         nams = lnk.find_element(By.CLASS_NAME,'live-score')
         nam = nams.find_elements(By.CLASS_NAME,'vn-shedTeam')
         ln = lnk.find_element(By.CLASS_NAME,'vn-schedule-head')
         _num = lnk.find_element(By.CLASS_NAME,'w20')
      except:continue
      for na in nam:
         n = na.find_element(By.CLASS_NAME,'vn-teamTitle')
         i = n.text.split('\n')
         teams.append(i[0])
      if len(teams)==2:
          rtn_dct={}
          rtn_dct['Match Number'] = _num.text
          rtn_dct['Home Team'] = teams[0]
          rtn_dct['Away Team'] = teams[1]
          all_lst.append(rtn_dct)
   return all_lst

# Function to append ball by ball data on identifying innings
def ball_by_ball(_num,stad_name,match_date,match_time,match_res,url,hm_tm,aw_tm):
   innings_num = 0
   ball_values = []
   driver.get(url)
   try:
       cookie_button = driver.find_element(By.CLASS_NAME,"cookie__accept_btn")
       cookie_button.click()
   except ElementNotInteractableException:innings_num = 0
   atags_list = driver.find_elements(By.CLASS_NAME,"ap-outer-tb-wrp")
   for atags in atags_list:
      button_list = atags.find_elements(By.CLASS_NAME,"ap-inner-tb-click")
      time.sleep(10)
      for button in range(len(button_list)):
         driver.execute_script("arguments[0].click();", button_list[button])
         time.sleep(10)
         bat_innings = button_list[button].text
         innings_num += 1
         if innings_num>2:break
         wait = WebDriverWait(driver, 10)
         ball_elements = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "p.cmdOver.mcBall")))
         commentary_start = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryStartText.ng-binding.ng-scope")))
         commentary_text = wait.until(presence_of_all_elements_located((By.CSS_SELECTOR, "div.commentaryText.ng-binding")))
         for i in range(len(ball_elements)):
            data = {}
            ball_number = ball_elements[i].text.split('\n')[0]
            ball_value = ball_elements[i].text.split('\n')[1]
            start = commentary_start[i].text
            text = commentary_text[i].text
            try:
                bowler,batsmen = start.split("bowling to")
            except:bowler = start
            # print(_num,stad_name,match_date,match_time,match_res)
            data['Match Number']=_num
            data['Stadium']=stad_name
            data['Date']=match_date
            data['Time']=match_time
            data['Home Team']=hm_tm
            data['Away Team']=aw_tm
            data['Innings']=str(innings_num)
            data['Batting Team']=bat_innings
            data['Over']=ball_number
            data['Runs']=ball_value
            data['Bowler']=bowler
            data['Batsmen']=batsmen
            data['Commentary']=text
            data['Result']=match_res
            ball_values.append(data)
      with open(r"/home/scrapper/pyscrapper/"+str(date.today().year)+_num+".txt","w") as appf:
        for ball in ball_values:
                     s = str(ball)
                     appf.write(s)
                     appf.write("\n")
        return
      


if __name__ == '__main__':

    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")  # Prevent issues with sandboxing in Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Use /tmp instead of /dev/shm to avoid memory issues
    options.add_argument("--remote-debugging-port=9222")  # Required for headless Chrome to avoid DevToolsActivePort error
# Old statement working in windows
    driver = webdriver.Chrome(options=options)
    
    lnk = 'https://www.iplt20.com/matches/results/'+str(date.today().year)
    while(True):
        try:
            hm_tm_aw_tm_lst =hm_tm_aw_tm(lnk)
            if len(hm_tm_aw_tm_lst)> 0:
                break
        except TypeError:
            print("Error")
            driver.quit()
    lis = all_href_ext(lnk)
    # print(hm_tm_aw_tm_lst)
    # # print(lis)
    # Code to run the program manually
    # with open(r'F:\Projects\Data-scraping\IPL-Data-Scraping\data.txt','r+') as rwf:
    #     rwf.write(str(hm_tm_aw_tm_lst))
    #     rwf.write("\n")
    #     rwf.write(str(lis))

    hm_tm_aw_tm_lst.reverse()
    lis.reverse()
    # File to save all the extracted links
    hm_tm_aw_tm_lst = [ {'Match Number': 'MATCH 57', 'Home Team': 'Sunrisers Hyderabad', 'Away Team': 'Lucknow Super Giants'}]
    lis = [{'num': 'MATCH 57', 'url': 'https://www.iplt20.com/match/2024/1439'}]
    with open(r'/home/scrapper/pyscrapper/data.txt','r+') as rwf:
        urls = rwf.readlines()
        url_lst = [line.rstrip() for line in urls]
        for i in lis:
            _num = i['num']
            _url = i['url']
            # print(_url)
            if _url in url_lst:
                print(_url)
                continue
            for ele in hm_tm_aw_tm_lst:
                if ele['Match Number'] ==_num:
                    try:
                        print(ele)
                        # input()
                        hm_tm = ele['Home Team']
                        aw_tm = ele['Away Team']
                        stad_name,match_date,match_time,match_res = get_match_res(_url)
                        ball_by_ball(_num,stad_name,match_date,match_time,match_res,_url,hm_tm,aw_tm)
                    except ElementNotInteractableException:
                        driver.quit()
                        driver = webdriver.Chrome(options=options)
                        hm_tm = ele['Home Team']
                        aw_tm = ele['Away Team']
                        stad_name,match_date,match_time,match_res = get_match_res(_url)
                        ball_by_ball(_num,stad_name,match_date,match_time,match_res,_url,hm_tm,aw_tm)
                    # rwf.write(_url)
                    # rwf.write("\n")
                    print(_num+" Data written")
                    # input()
