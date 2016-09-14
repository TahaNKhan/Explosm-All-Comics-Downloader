#! python3
# downloadExplosmComics.py - Downloads every single Cyanide and Happiness comic.
import requests, os, bs4

link = 'http://explosm.net/comics/'
res = requests.get(link)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
try:
# uses the permalink to get the current comic number
	comicNumber = int(soup.find(id = "permalink" ).get('value').partition('comics/')[2].partition('/')[0])
except:
# backup if the other route fails. Comic 4408 = Sept 10 2016 Comic
	comicNumber = 4408
# store comics in ./explosm
os.makedirs('explosm', exist_ok=True) 
while comicNumber is not 0:
# Get the page.
	try:
		url = link + str(comicNumber) + '/' 
		print('Downloading page %s...' % url)
		comicNumber -= 1
		res = requests.get(url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, "html.parser")
# Find the URL of the comic image.
		
		comicElem = soup.find(id = 'main-comic').get('src')

		if comicElem == []:
			print('Could not find comic image.')
		else:
			comicUrl = comicElem
#remove the crap text after ? in image src
			comicUrl = comicUrl.partition('?')[0]
# Download the image
			print('Downloading image' + (comicUrl))
			res = requests.get('http:'+comicUrl)
			res.raise_for_status()
# Save the image
			imageFile = open(os.path.join('explosm', os.path.basename(comicUrl)), 'wb')
			for chunk in res.iter_content(100000):
				imageFile.write(chunk)
			imageFile.close()

		

	except:
		continue
		
print('Done.')