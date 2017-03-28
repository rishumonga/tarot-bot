import requests
import bs4
import re

res = requests.get('http://www.biddytarot.com/tarot-card-meanings/major-arcana/')
len(res.text)
print(res.text[:250])
res.status_code==200
res.raise_for_status()

f = open('file.txt','wb')
for chunk in res.iter_content(10000):
  f.write(chunk);
f.close()


def saveurl(fname, url):
  f = open(fname, 'wb')
  r = requests.get(url)
  for chunk in r.iter_content(10000):
    f.write(chunk);
  f.close()

def savetext(fname, text):
  f = open(fname, 'wt')
  f.write(text)
  f.close()

res = requests.get('http://www.biddytarot.com/tarot-card-meanings/major-arcana/')
soup = bs4.BeautifulSoup(res.text, 'html')
el = soup.select('tr td')


for i in range(0,22):
  #print(el[2*i])
  print(i)
  url = el[2*i].select('a')[0].attrs['href']
  img = el[2*i].select('a img')[0].attrs['src']
  print(img)
  saveurl('c/'+str(i)+'.jpg', img)
  name = el[2*i].select('a')[0].text
  print(name)
  savetext('c/'+str(i)+'-name.txt', name)
  #print(el[2*i+1])
  text = el[2*i+1].text
  p = re.compile('Upright: (.*)Reversed: (.*)') 
  textu = p.match(text).groups()[0]
  textr = p.match(text).groups()[1]
  print(textu)
  savetext('c/'+str(i)+'-short-u.txt', textu)
  print(textr)
  savetext('c/'+str(i)+'-short-r.txt', textr)
  # get the full descriptions
  r = requests.get(url)
  s = bs4.BeautifulSoup(r.text, 'html')
  desc = ''
  for p in s.select('#card-page-description p'):
    desc = desc + p.text + '\n';
  savetext('c/'+str(i)+'-desc.txt', desc)
  umean = ''
  for p in s.select('#card-page-meaning p'):
    umean = umean + p.text + '\n'
  savetext('c/'+str(i)+'-umean.txt', umean)
  rmean = ''
  for p in s.select('#card-page-reversed p'):
    rmean = rmean + p.text + '\n'
  savetext('c/'+str(i)+'-rmean.txt', rmean)


res = requests.get('http://www.biddytarot.com/tarot-card-meanings/minor-arcana/suit-of-cups/')
soup = bs4.BeautifulSoup(res.text, 'html')
el = soup.select('tr td')


for i in range(0,14):
  #print(el[2*i])
  print(i)
  url = el[2*i].select('a')[0].attrs['href']
  img = el[2*i].select('a img')[0].attrs['src']
  print(img)
  saveurl('c1/'+str(i)+'.jpg', img)
  name = el[2*i].select('a')[0].text
  print(name)
  savetext('c1/'+str(i)+'-name.txt', name)
  #print(el[2*i+1])
  text = el[2*i+1].text
  p = re.compile('Upright:(.*)Reversed: (.*)') 
  textu = p.match(text).groups()[0]
  textr = p.match(text).groups()[1]
  print(textu)
  savetext('c1/'+str(i)+'-short-u.txt', textu)
  print(textr)
  savetext('c1/'+str(i)+'-short-r.txt', textr)
  # get the full descriptions
  r = requests.get(url)
  s = bs4.BeautifulSoup(r.text, 'html')
  desc = ''
  for p in s.select('#card-page-description p'):
    desc = desc + p.text + '\n';
  savetext('c1/'+str(i)+'-desc.txt', desc)
  umean = ''
  for p in s.select('#card-page-meaning p'):
    umean = umean + p.text + '\n'
  savetext('c1/'+str(i)+'-umean.txt', umean)
  rmean = ''
  for p in s.select('#card-page-reversed p'):
    rmean = rmean + p.text + '\n'
  savetext('c1/'+str(i)+'-rmean.txt', rmean)



res = requests.get('http://www.biddytarot.com/tarot-card-meanings/minor-arcana/suit-of-pentacles/')
soup = bs4.BeautifulSoup(res.text, 'html')
el = soup.select('tr td')

for i in range(0,14):
  #print(el[2*i])
  print(i)
  url = el[2*i].select('a')[0].attrs['href']
  img = el[2*i].select('a img')[0].attrs['src']
  print(img)
  saveurl('c2/'+str(i)+'.jpg', img)
  name = el[2*i].select('a')[0].text
  print(name)
  savetext('c2/'+str(i)+'-name.txt', name)
  #print(el[2*i+1])
  text = el[2*i+1].text
  p = re.compile('Upright:(.*)Reversed: (.*)') 
  textu = p.match(text).groups()[0]
  textr = p.match(text).groups()[1]
  print(textu)
  savetext('c2/'+str(i)+'-short-u.txt', textu)
  print(textr)
  savetext('c2/'+str(i)+'-short-r.txt', textr)
  # get the full descriptions
  r = requests.get(url)
  s = bs4.BeautifulSoup(r.text, 'html')
  desc = ''
  for p in s.select('#card-page-description p'):
    desc = desc + p.text + '\n';
  savetext('c2/'+str(i)+'-desc.txt', desc)
  umean = ''
  for p in s.select('#card-page-meaning p'):
    umean = umean + p.text + '\n'
  savetext('c2/'+str(i)+'-umean.txt', umean)
  rmean = ''
  for p in s.select('#card-page-reversed p'):
    rmean = rmean + p.text + '\n'
  savetext('c2/'+str(i)+'-rmean.txt', rmean)


res = requests.get('http://www.biddytarot.com/tarot-card-meanings/minor-arcana/suit-of-swords/')
soup = bs4.BeautifulSoup(res.text, 'html')
el = soup.select('tr td')

for i in range(0,14):
  #print(el[2*i])
  print(i)
  url = el[2*i].select('a')[0].attrs['href']
  img = el[2*i].select('a img')[0].attrs['src']
  print(img)
  saveurl('c3/'+str(i)+'.jpg', img)
  name = el[2*i].select('a')[0].text
  print(name)
  savetext('c3/'+str(i)+'-name.txt', name)
  #print(el[2*i+1])
  text = el[2*i+1].text
  p = re.compile('Upright:(.*)Reversed: (.*)') 
  textu = p.match(text).groups()[0]
  textr = p.match(text).groups()[1]
  print(textu)
  savetext('c3/'+str(i)+'-short-u.txt', textu)
  print(textr)
  savetext('c3/'+str(i)+'-short-r.txt', textr)
  # get the full descriptions
  r = requests.get(url)
  s = bs4.BeautifulSoup(r.text, 'html')
  desc = ''
  for p in s.select('#card-page-description p'):
    desc = desc + p.text + '\n';
  savetext('c3/'+str(i)+'-desc.txt', desc)
  umean = ''
  for p in s.select('#card-page-meaning p'):
    umean = umean + p.text + '\n'
  savetext('c3/'+str(i)+'-umean.txt', umean)
  rmean = ''
  for p in s.select('#card-page-reversed p'):
    rmean = rmean + p.text + '\n'
  savetext('c3/'+str(i)+'-rmean.txt', rmean)




res = requests.get('http://www.biddytarot.com/tarot-card-meanings/minor-arcana/suit-of-wands/')
soup = bs4.BeautifulSoup(res.text, 'html')
el = soup.select('tr td')

for i in range(0,14):
  #print(el[2*i])
  print(i)
  url = el[2*i].select('a')[0].attrs['href']
  img = el[2*i].select('a img')[0].attrs['src']
  print(img)
  saveurl('c4/'+str(i)+'.jpg', img)
  name = el[2*i].select('a')[0].text
  print(name)
  savetext('c4/'+str(i)+'-name.txt', name)
  #print(el[2*i+1])
  text = el[2*i+1].text
  p = re.compile('Upright:(.*)Reversed: (.*)') 
  textu = p.match(text).groups()[0]
  textr = p.match(text).groups()[1]
  print(textu)
  savetext('c4/'+str(i)+'-short-u.txt', textu)
  print(textr)
  savetext('c4/'+str(i)+'-short-r.txt', textr)
  # get the full descriptions
  r = requests.get(url)
  s = bs4.BeautifulSoup(r.text, 'html')
  desc = ''
  for p in s.select('#card-page-description p'):
    desc = desc + p.text + '\n';
  savetext('c4/'+str(i)+'-desc.txt', desc)
  umean = ''
  for p in s.select('#card-page-meaning p'):
    umean = umean + p.text + '\n'
  savetext('c4/'+str(i)+'-umean.txt', umean)
  rmean = ''
  for p in s.select('#card-page-reversed p'):
    rmean = rmean + p.text + '\n'
  savetext('c4/'+str(i)+'-rmean.txt', rmean)
