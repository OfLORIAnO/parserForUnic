import requests
from bs4 import BeautifulSoup
from time import sleep
from random import uniform

myKod = '164-417-424 61'
ball = 234



def dataFromSite (soup):
    paragraph = (soup.find("p").get_text(separator=" ").replace('\n', '')).split('. ')[2::]
    paragraph = [*(paragraph[0].split('- ')[1::]), paragraph[1], paragraph[2]]
    p2 = paragraph[0].split()
    placeNum = int(p2[len(p2)-1])
    name = ''
    for word in p2:
        if word == 'Бюджетная' or word == 'Специалитет' or word == 'очная':
            break
        else:
            name = name + word + ' '
    return [placeNum, name]

def calculatePriority(priority):
    priorityString=''
    for i in range(len(priority)):
        if i != 0 and i!= len(priority)-1:
            priorityString = priorityString + str(i)+' - '+ str(priority[i])+'; '
        if i == len(priority)-1:
            priorityString = priorityString +str(i)+' - '+ str(priority[i])
    return priorityString
urls = ['https://technolog.edu.ru/content/alists/04.03.01_Химия_Бюджетная_Основа_Очная',
        'https://technolog.edu.ru/content/alists/08.03.01_Строительство_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/09.03.00_Информатика%20и%20вычислительная%20техника%20очная_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/15.03.00_Машиностроение_Бюджетная%20основа%20Очная',
        'https://technolog.edu.ru/content/alists/15.05.01_Проектирование%20технологических%20машин%20и%20комплексов_Специалитет_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/18.03.00_Химические%20технологии_очная_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/18.05.00_Химические%20технологии_Специалитет_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/19.03.01_Биотехнология_Бюджетная%20основа%20Очная',
        'https://technolog.edu.ru/content/alists/20.03.01_техносферная%20безопасность_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/22.03.01_материаловедение%20и%20технологии%20материалов_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/27.03.03_системный%20анализ_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/27.03.04_управление%20в%20технических%20системах_Бюджетная%20основа',
        'https://technolog.edu.ru/content/alists/28.03.03_наноматериалы_Бюджетная%20основа%20Очная',
        ]
myUrls = [
            'https://technolog.edu.ru/content/alists/09.03.00_Информатика%20и%20вычислительная%20техника%20очная_Бюджетная%20основа',
            'https://technolog.edu.ru/content/alists/08.03.01_Строительство_Бюджетная%20основа',
            'https://technolog.edu.ru/content/alists/15.03.00_Машиностроение_Бюджетная%20основа%20Очная',
            'https://technolog.edu.ru/content/alists/15.05.01_Проектирование%20технологических%20машин%20и%20комплексов_Специалитет_Бюджетная%20основа',
        ]
bigMass = []




def checkEnemy(kodOfEnemy, enemyPriority, nameFrom, urlFrom):
    urlsCopy = urls.copy()
    urlsCopy.remove(urlFrom)
    for urlEnemy in urlsCopy:
        response = requests.get(urlEnemy)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="sticky-headers")
        res = dataFromSite(soup)
        placeNum = res[0]
        name = res[1]
        flag = False
        try:
            for row in table.find_all("tr"):
                row_data = []
                for cell in row.find_all(["td", "th"]):
                    row_data.append(cell.text)
                try:
                    # sleep(.5)
                    if int(row_data[0]) < placeNum:
                        if str(row_data[1])==str(kodOfEnemy) and name != nameFrom and str(row_data[-5]) < str(enemyPriority):
                            try:
                                with open("logs.txt", "a", encoding="utf-8") as file:
                                    strochkakka =  str(nameFrom) + str(name) + '. Код этого енеми: '+str(kodOfEnemy) + '. Его был приоритет: ' + str(enemyPriority)+ '. Его Место: ' + str(row_data[0]) + '. Его тут приоритет: ' + str(row_data[-5])
                                    file.write(strochkakka + "\n")
                                print(strochkakka)
                            except:
                                # print('errer')
                                break
                    else:
                        break
                except:  
                    # print('error')
                    continue
        except:
            print('Ошибка с сединением') 
        delay = uniform(.1, .5)  # Генерация случайной задержки между 1, 2.0
        sleep(delay)
    return

def entedRowData(urlLLL, soup):
    data = []
    priority = [0]*6
    res = dataFromSite(soup)
    placeNum = res[0] 
    name = res[1]
    dataAboutMe=[]
    for row in table.find_all("tr"):
        row_data = []
        for cell in row.find_all(["td", "th"]):
            row_data.append(cell.text)
        try:
            data.append(row_data)
            # if int(row_data[-5]) > 1 and len(dataAboutMe) == 0:
                # checkEnemy(row_data[1], row_data[-5], name, urlLLL)
            priority[int(row_data[-5])] += 1
            if row_data[1] == myKod:
                dataAboutMe = row_data
                break
        except:
            continue
    priorityString = calculatePriority(priority)
    return [data, name, placeNum, priorityString, dataAboutMe]



bigData = []

for url in myUrls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="sticky-headers")
    data, name, placeNum, priorityString, dataAboutMe = entedRowData(url, soup)
    for n in range(len(data)):
        row = data[n]
        if int(row[0]) == placeNum and len(dataAboutMe) > 0:
            string = name +  '. моё место: '+ str(dataAboutMe[0]) + ' из ' + str(row[0]) + '. Минимальный балл: ' + str(row[2]) + '. Приоритет других: ' + priorityString 
            bigData.append(string)
        elif int(row[0]) == placeNum :
            bigData.append('Не прошёл. '+ name + ' Минимальный балл: ' + str(row[2]) )

for m in bigData:
    print(str(m))
    print('-'*90)