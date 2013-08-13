"""
Parse EdSurge Newsletter and fetch screenshots of web pages 
"""
from bs4 import BeautifulSoup
import os
import Image
import stat
import sys

# Setup output directory
if not os.path.exists(os.path.join(os.getcwd(), 'output')):
    os.system('mkdir output')
    
# Find latest EdSurge file
dirfiles = os.listdir('.')
edsurgefile = ''
for file in dirfiles:
   if file.startswith('EdSurge'):
      edsurgefile = file
      
if len(edsurgefile) == 0:
   print "Save EdSurgeNN.html here"
   sys.exit()
else:  
   print "Parsing "  + edsurgefile

if raw_input("Delete all .png files for fresh run? ") != 'y':
   sys.exit()
   
soup = BeautifulSoup(open(edsurgefile))
links = soup.find_all('a')
urls = []
urlnumbers = {}
urlnumber = 100
for link in links:
  if link.has_attr('href'):
     if link['href'].startswith('http'):
        urls.append(link['href'])
        urlnumbers[link['href']] = urlnumber
        urlnumber = urlnumber + 1
urlset = set(urls)
print(`len(urlset)` + " unique http URLs found")

# create shell script to run webkit2png
print "Fetching website links"
os.system('rm *.png')
os.system('rm output/*.png')

savedPath = os.getcwd()

for url in urlset:
   os.system('mkdir '+`urlnumbers[url]`)
   os.chdir(os.path.join(savedPath,str(urlnumbers[url])))
   os.system('webkit2png -F '+url)
   os.system('mv *.png ../output/'+ `urlnumbers[url]` +'.png')
   os.chdir(savedPath)
   
# clean up
for url in urlset:
   os.system('rm '+str(urlnumbers[url])+"/*.png")
   os.system('rmdir '+str(urlnumbers[url]))

dirfiles = os.listdir('output')
pngs = []
for filename in dirfiles:
  if filename.endswith(".png"):
     pngs.append(filename)
      
print(`len(pngs)` + " URLs imaged")
    
def imgCrop(im):
    if (im.size[1]*1.0)/im.size[0] > 1.1:
       box = (0, 0, im.size[0], int(im.size[0]*0.75))
    else:
       box = (0, 0, im.size[0], im.size[1])
    region = im.crop(box)
    path,filename=os.path.split(im.filename)
    region.save("CROPPED" + filename)
    
for png in pngs:
    imgCrop(Image.open(os.path.join(os.getcwd(), 'output/' + png)))
    
print(`len(pngs)` + " URLs cropped")
