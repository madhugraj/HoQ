from time import sleep, time
from bs4 import BeautifulSoup
from re import compile, match
import os
import json


def GetTopic():
## Getting Topics from the topic_urls.txt in readmode-file open
## Read all the lines -read().split()
    f=open('topic_urls.txt',mode='r')
    lines=f.read().split('\n')
    topic_links=[]

## In a list called topic_links append()everytopic independently till the end of the file
    for line in lines:
        topic_links.append(line)
    return topic_links


def scrolltillBottom(browser):
    print ("On your Mark! Get Set! Go....")
    pre_source = browser.page_source
    while True:
        sleep(3)
        print ("Scrolling script")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        Cur_Source = browser.page_source
        if Cur_Source == pre_source:
            break
        pre_source = Cur_Source
    print ("I am Done scrolling")



def pagedownload(browser,topic):
    url = topic + '?share=1'
    try:
        browser.get(url)
    except:
        return "<html><\html>"
##ScrollBottom till the end of the browser; browse for page_source
    scrolltillBottom(browser)
    sleep(3)
    html_link=browser.page_source
    return html_link



def ExtractLinks(html_link,useCached=False):
    if useCached:
        f=open('index.html',mode='r')
        html_link=f.read()
    soup=BeautifulSoup(html_link)
    links=[]

    for i in soup.find_all('a',{"class": "question_link"}):
        if len(i)>0:
            link=i['href']
            try:
                links.append(link)
            except UnicodeEncodeError:
                pass
    return links

def getQn(soup):
    try:
        s= soup.find('div', { "class" : "question_text_edit" })
        return s
    except:
        return None

def findtopic(soup):
    top=soup.find_all('div',{"class":"TopicListItem QuestionTopicListItem topic_pill"})
    return ','.join(t.getText() for t in top)

def getAnswerText(answer):
    print("getAnswerText....")
    ans = answer.find_all('div', { "class" : " ExpandedAnswer ExpandedContent" })
    result = answer.getText()
    print("Result:: ", result)
    if result:
        return result


def answer(browser,link):
    if not match('/',link):
        print("Wrong Question!")
        return

    url='http://www.quora.com' + link + '?share=1'
    browser.get(url)
    scrolltillBottom(browser)
    sleep(3)
    source=browser.page_source.encode('utf-8')
    soup=BeautifulSoup(source)

    q_text=getQn(soup)
    if q_text == None:
        print("No Questions Found!!")
        return 0
    print("Question:",q_text.getText())

    topic= findtopic(soup)
    print("Topic: ",topic)

    print("Class_List: ", soup.find_all('div'))

    collapsed = compile('\d Answers? Collapsed')
    answers = soup.find('div', {"class": "Answer Toggle UnifiedAnswer AnswerBase"})
    print("Answers::",answers)

    ans=[]

    for a in answers:
        print(a.getText())
        result=collapsed.match(a.getText())
        ##if result in answer['class']:
        ##   continue # skip collapsed answers and answer text box
        a= getAnswerText(a.getText())
        result1=a.getText()
        ans = ans + result1

    try:
        dict ={'Topics: ':topic, 'Questions: ':q_text, 'Answers: ':answers}
    except UnicodeDecodeError:
        print("Unicode Error")
        return 0



    a = []
    if not os.path.isfile('..../output/answers.csv'):
        a.append(dict)
        print(dict)
        with open ('..../output/answers.csv', 'w')as f:
            f.write(json.dumps(a,indent=2))
    else:
        with open ('..../Output/answers.csv') as file:
            feeds = json.load(file)
        feeds.append(dict)
        with open('..../Output/answers.csv', mode= 'w') as f:
            f.write(json.dumps(feeds,indent=2))