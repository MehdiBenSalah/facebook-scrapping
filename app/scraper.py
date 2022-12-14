from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta




'''

Facebook pages has 2 different structures (Example: (new structure) https://www.facebook.com/facebook/ and (old structure) https://www.facebook.com/insat.rnu.tn/)
The scrapping method is the same, the difference comes to the HTML selectors

'''

def scrape_old_structure_page(driver, max_post_to_extract, data):

    '''
    
    This function used to scrape old structure page. Example: https://www.facebook.com/insat.rnu.tn/

    '''

    ##### Scrape page title, page intro and header (followers and likes) ###############

    data['page title']= driver.find_element(By.TAG_NAME,'h1').text
    try :
        data['About']=driver.find_element(By.XPATH,'//div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]').text
    except:
        print('Intro not found')
    try :
        followers = driver.find_element(By.PARTIAL_LINK_TEXT,'followers').text
        data['followers'] = followers
    except :
        print('No data for followers')
    try :
        likes = driver.find_element(By.PARTIAL_LINK_TEXT,'likes').text
        data['likes'] = likes
    except :
        print('No data for likes')


    ##### Go to About section then scrape infos ###########

    driver.find_element(By.LINK_TEXT,"About").click()
    try :
        blocks = driver.find_element(By.XPATH,'//div[@class="xyamay9 xqmdsaz x1gan7if x1swvt13"]').find_elements(By.XPATH,'*')
        for block in blocks :
            title = block.find_element(By.CSS_SELECTOR,'span.x1s688f.xzsf02u').text
            elements = block.find_elements(By.CSS_SELECTOR,'span.xo1l8bm.xzsf02u')
            
            if len(elements)==1:
                data[title]= elements[0].text
            else:
                data[title] = []
                for element in elements:
                    data[title].append(element.text)
    except :
        print("No data from About section")

    ######### back to home #########
    driver.find_element(By.LINK_TEXT,"Posts").click()

    ########### Select post, scroll to post then scrape post infos ##################

    data['posts']=[]
    driver.execute_script("return document.body.scrollHeight")
    extracted_posts = 0

    while(extracted_posts < max_post_to_extract or max_post_to_extract==-1):
        try :
            post = driver.find_element(By.XPATH,f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli x1iyjqo2 xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj x65f84u']/div/div[{extracted_posts+1}]/div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']")
            driver.execute_script('arguments[0].scrollIntoView();', post)
            data['posts'].append(extract_post_infos(post))
            extracted_posts+=1
            print(f'POST N°{extracted_posts} SCRAPED')
        except:
            print('No more posts')
            break

    return data

def scrape_new_structure_page(driver, max_post_to_extract, data):

    '''
    
    This function used to scrape old structure page. Example: https://www.facebook.com/facebook/

    '''
    
    ##### Scrape page title ###############
    data['page title']= driver.find_element(By.TAG_NAME,'h1').text


    ##### Go to About section then scrape infos ###########
    driver.find_element(By.LINK_TEXT,"About").click()

    general = driver.find_elements(By.XPATH,"//*[text() = 'General']/../../div/div/div")
    contact_info = driver.find_elements(By.XPATH,"//*[text() = 'Additional contact info']/../../div/div/div")
    more_info = driver.find_elements(By.XPATH,"//*[text() = 'More info']/../../div/div/div")
    for general_data in general:
        general_data = general_data.text
        if "like" in general_data: 
            data["likes"] = ''.join([s for s in general_data if s.isdigit()])
        elif "follower" in general_data: 
            data["followers"] = ''.join([s for s in general_data if s.isdigit()])
        elif "checked" in general_data:
            data["checks"] = ''.join([s for s in general_data if s.isdigit()])
        else:
            data['Category'] = general_data
    data['Contact info'] = [contact_data.text for contact_data in contact_info]
    for infos in more_info:
        title = infos.find_element(By.CSS_SELECTOR,"span.x1lliihq.x6ikm8r.x10wlt62.x1n2onr6").text
        data[title]=infos.find_element(By.CSS_SELECTOR,'span > div.x78zum5.xdt5ytf.xz62fqu.x16ldp7u > div.xu06os2.x1ok221b > span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h').text
        if "See more" in data[title]:
            try:
                button = infos.find_element(By.CSS_SELECTOR,"div.xzsf02u.x1s688f")
                driver.execute_script('arguments[0].scrollIntoView();', button)
                button.click()
                data[title]=infos.find_element(By.CSS_SELECTOR,'span > div.x78zum5.xdt5ytf.xz62fqu.x16ldp7u > div.xu06os2.x1ok221b > span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x6prxxf.xvq8zen.xo1l8bm.xzsf02u.x1yc453h').text
            except :
                pass
            
    
    ######### back to home #########
    driver.find_element(By.LINK_TEXT,"Home").click()

    ########### Select post, scroll to post then scrape post infos ##################

    data['posts']=[]
    driver.execute_script("return document.body.scrollHeight")
    extracted_posts = 0

    while(extracted_posts < max_post_to_extract or max_post_to_extract==-1):
        try :
            post = driver.find_element(By.XPATH,f'//div[@class="x6s0dn4 x78zum5 xdt5ytf x193iq5w x1t2pt76 xh8yej3"]/div/div[{extracted_posts+1}]/div[@class="x1n2onr6 x1ja2u2z"]')
            driver.execute_script('arguments[0].scrollIntoView();', post)
            data['posts'].append(extract_post_infos(post))
            extracted_posts+=1
            print(f'POST N°{extracted_posts} SCRAPED')
        except:
            print('No more posts')
            break 
    return data



def extract_post_infos(post):
    '''

    Extract post infos (description, publication date, number of likes, comments and shares)

    '''
    num_comments = '0'
    num_likes = '0'
    num_shares = '0'
    date = None 
    text = None

    ####### Description ###########
    try:
        text = post.find_element(By.CSS_SELECTOR,'div.x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13')
        if "See more" in text.text:
            try:
                button = text.find_element(By.CSS_SELECTOR,"div.xzsf02u.x1s688f")
                button.click()
                text = post.find_element(By.CSS_SELECTOR,'div.x1iorvi4.x1pi30zi.x1l90r2v.x1swvt13')
            except :
                pass
        text = text.text
    except:
        pass

    ######### Likes comments and shares (same div) #############
    try :
        likes_comments_shares = post.find_element(By.CSS_SELECTOR,'div.x6s0dn4.xi81zsa.x78zum5.x6prxxf.x13a6bvl.xvq8zen.xdj266r.xktsk01.xat24cr.x1d52u69.x889kno.x4uap5.x1a8lsjc.xkhd6sd.xdppsyt').text.split('\n')
        for elem in likes_comments_shares:
            if 'comment' in elem or 'comments' in elem: num_comments = elem
            elif 'share' in elem or 'shares' in elem: num_shares = elem
            else : num_likes = elem
    except:
        pass

    ################# publication time #################
    try :
        date = reformulate_date(post.find_element(By.CSS_SELECTOR,"a.xo1l8bm").text)
    except:
        pass

    return {
                'description':text,
                'date':date,
                'number of likes':num_likes,
                'number of comments':num_comments,
                'number of shares':num_shares 
            }



def reformulate_date(date):
    '''
    
    Transform recent publication facebook date to actual date
    
    Example:               "10d"  ----->  "3 December 2022"

    '''

    if(len(date)<7):
        char_date = []
        int_date = []
        for c in date :
            if c.isdigit():
                int_date.append(c)
            else:
                char_date.append(c)
        int_date = int(''.join(int_date))
        char_date = ''.join(char_date)
        if char_date=='d': return (datetime.today()+timedelta(days=int_date)).strftime("%B %d, %Y")
        if char_date=='h': return (datetime.today()+timedelta(hours=int_date)).strftime("%B %d, %Y")
        if char_date=='m': return (datetime.today()+timedelta(minutes=int_date)).strftime("%B %d, %Y")
        if char_date=="instant": return datetime.today().strftime("%B %d, %Y")
        else: return date
    else:
        return date




####################################################################
#                                                                  #
#                            main                                  #
#                                                                  #
####################################################################
def scrape_facebook_page(URL, max_post_to_extract:int =-1, max_sec:int = 5):

    '''
    
    Scrape data from public facebook page

    max_post_to_extract : is the maximum number of posts data to scrape. If not specified, it will scrape it all.

    max_sec : the maximum number of seconds for the code to search for data. If the time is elapsed, it moves on to the next entry.

    '''

    data = {} #### dict to store scrapped data
    if('https://' not in URL and 'http://' not in URL):
        URL = 'https://'+URL
        
    data['url']=URL

    ########### start session ##################

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_experimental_option("detach", True)
    options.add_argument('--window-size=1920,1080')  
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(max_sec)
    driver.get(URL)


    ############# Extract ID from DOM HTML. (If not found, random id will be generated by the database)
    
    try :
        id_ = driver.find_element(By.CSS_SELECTOR,'body > script:nth-child(14)').get_attribute('innerHTML')
        first_index = id_.find("page_id")
        last_index = id_[first_index:].find('",')
        data['_id'] = id_[first_index+10:first_index+last_index]
    except:
        print('Random id will be generated by the database')

    ###### 2 structures differs from their Home/Posts button

    find_structure = driver.find_element(By.XPATH,'//a[@class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou xe8uvvx xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct xjbqb8w x18o3ruo x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1heor9g x1ypdohk xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg x1vjfegm x3nfvp2 xrbpyxo xng8ra x16dsc37"]').text
    if (find_structure=='Home'):
        data = scrape_new_structure_page(driver, max_post_to_extract, data)
    elif(find_structure=='Posts'):
        data = scrape_old_structure_page(driver, max_post_to_extract, data)
    else:  
        raise Exception('Unkown structure')

    return data






    
if __name__=="__main__":

    URL = "https://www.facebook.com/insat.rnu.tn"
    data = scrape_facebook_page(URL, max_post_to_extract = 20)
    print(data)