import requests
import time
import pandas as pd
import datetime
from bs4 import BeautifulSoup

query = '''
query ($name: String) {
  User(name: $name) {
    statistics {
      manga {
        volumesRead
      }
    }
  }
}
'''
urlAL = 'https://graphql.anilist.co'
volumes = list()

file = open("data.txt", "r")
nicknamesAL=file.readline().split()
nicknamesMAL=file.readline().split()
file.close()

print('Anilist users: ' + str(len(nicknamesAL)) + '\n' + str(nicknamesAL))




for name in nicknamesAL:
    variables = {'name': name}

    response = requests.post(urlAL, json={'query': query, 'variables': variables})
    data = response.json()
    count = data['data']['User']['statistics']['manga']['volumesRead']
    volumes.append(count)
    print(name + ': ' + str(count) + ' volumes')
    time.sleep(1)


print('MyAnimeList users: ' + str(len(nicknamesMAL)) + '\n' + str(nicknamesMAL))

for name in nicknamesMAL:


    URL = "https://myanimelist.net/profile/" + name
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')
    classes = soup.find_all(class_="di-ib fl-r")
    count =int(classes[6].string.replace(',', ''))
    volumes.append(count)
    print(name + ': ' + str(count) + ' volumes')

    time.sleep(1)

print('Data to write: ' + str(volumes))





# New data to append
volumes.insert(0,datetime.datetime.now().strftime("%d/%m/%Y"))
df_new = pd.DataFrame(volumes)

# # Read existing data
df_existing = pd.read_excel('maniacs.xlsx',sheet_name="Sheet1")

# # Append new data
df_combined = pd.concat([df_existing,df_new],axis=1)

# # Save the combined data to Excel
df_combined.to_excel('maniacs.xlsx',index=False,sheet_name="Sheet1")


