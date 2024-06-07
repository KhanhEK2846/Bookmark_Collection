import os, time
import requests as rq
import pandas as pd

path = ".\.."

mdfiles = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith(".md") and root.find(".tool") == -1]


urls = {}
for item in mdfiles:
  datafile = open(item, "r",encoding="utf8")
  data = datafile.read()
  arrs = data.split('\n')
  for arr in arrs:
    url = arr[arr.find("(")+1:arr.find(")")]
    if url.startswith('http') or url.startswith('www'):
      urls[arr[arr.find('[')+1:arr.find(']')]]=url
      
pingResults = None
name = []
url = []
result = []
count = 1
for key, value in urls.items():
  #print(f'Key = {key} and Value = {value}')
  flag = None
  print("-------------------------------------------")
  print(f'Ping {key} - {value}')
  try:
    r = rq.get(value,timeout=5,headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Cache-Control": "no-cache",
    "Pragma": "no-cache"})
    if r.status_code == 200: flag = 'Successful'
    else: flag = f'Failure - {r.status_code}'
    r.close()
  except: flag = "Error"
  name.append(key)
  url.append(value)
  result.append(flag)
  print(f'{key} - Done {count}/{len(urls)}')
  count +=1
  time.sleep(2.5)
print("------------------Save in Excel----------------------------")
pingResults = {'Name': name, 'Url': url, 'Result': result}

df = pd.DataFrame(pingResults)
df.to_excel("ResultsPing.xlsx")
print("----------------------All Done-----------------------")