from selenium import webdriver
from Quora_utils import *

def main(argv):
## Initializing selenium and chromedriver
    ##webdriver.Chrome().close()
    chromedriver="chromedriver1.exe"
    try:
        webdriver.Chrome().delete_all_cookies()
        print("Driver closed")
    except:
        None
    chromedriver = 'chromedriver.exe'
    os.environ["webdriver.chrome.driver"]= chromedriver
    option=argv

    browser=webdriver.Chrome(chromedriver)

## Step 1: Fetching the topic of interests
## Step 2: Extracting the html links
## Step 3: Writing the questions in the file

    if option=="Question_Search":
        browser = webdriver.Chrome(chromedriver)
        topic_links=GetTopic()
        print("Topic_Links:",topic_links)
        for topic in topic_links:
            html_link=pagedownload(browser,topic)
            links=ExtractLinks(html_link,False)
            with open('..../Data/Questions.txt',mode='a')as file:
                w='\n'.join(links).encode('utf-8')
                file.write(w)
            print("Questions Ready!!")

    elif option == "Answer_Write":
        links=[]
        fin=[]
        with open('..../Data/Questions.txt',mode='r')as file:
            links= file.read().split('\n')
        links_start=set(links)

        for link in links_start:
            result=answer(browser,link)
        if result !=0:
            with open('.../Data/Questions_Complete .txt',mode='r')as file:
                try:
                    file.write((link + '\n').encode('utf-8'))
                except (UnicodeEncodeError,UnicodeDecodeError ):
                    print("Errrorrrr....")
        print("Answers Ready....")




if __name__ == "__main__":
    main(argv="Topic_Links")
