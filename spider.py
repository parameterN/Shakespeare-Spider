import requests
import re
import os

session = requests.session()
headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
   like Gecko) Chrome/109.0.0.0 Safari/537.36', 
   }
base = "http://shakespeare.mit.edu/"
response = session.get(url=base,headers=headers)
URLs = re.findall('<a href="(.*?)">',response.text)

if not os.path.exists("./save"):
   os.makedirs("./save")

for url in URLs:
   new_url = base + url
   response = session.get(url=new_url,headers=headers)
   tittle = re.search('<title>([\\s\\S]*?):',response.text)
   if tittle is None:
      tittle = re.search('<TITLE>([\\s\\S]*?)<',response.text)
   tittle = tittle.group(1).strip()
   
   save_path = f"./save/{tittle}"
   if not os.path.exists(save_path):
      os.makedirs(save_path)
   if tittle in ["A Lover's Complaint","THE RAPE OF LUCRECE",\
                 "Venus and Adonis","A Funeral Elegy for Master William Peter"]:
      filtered = re.sub('<HEAD>[\\s\\S]*?</HEAD>','',response.text)
      filtered = re.sub('<[\\s\\S]*?>','',filtered)
      with open(save_path + "/" + f"{tittle}.txt","w") as f:
         f.write(filtered.strip())
      continue
   elif tittle == "The Sonnets":
      scenes = re.findall('<DT><A HREF="(.*?)">.*?</A>',response.text)
   else:
      scenes = re.findall(': <a href="(.*?)">.*?</a><br>',response.text)
   for scene in scenes:
      if tittle == "The Sonnets":
         new_new_url = new_url[:-12] + scene
      else:   
         new_new_url = new_url[:-10] + scene
      new_response = session.get(url=new_new_url,headers=headers)
      filtered = re.sub('<html>[\\s\\S]*?<h3>','',new_response.text)
      filtered = re.sub('<html>[\\s\\S]*?<H3>','',filtered)
      filtered = re.sub('<HEAD>[\\s\\S]*?</HEAD>','',filtered)
      filtered = re.sub('<tr><td class="nav" align="center">[\\s\\S]*?</html>','',filtered)
      filtered = re.sub('<[\\s\\S]*?>','',filtered)
      # print(filtered)
      with open(save_path + "/" + f"{scene[:-5]}.txt","w") as f:
         f.write(filtered.strip())