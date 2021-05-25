'''
This is just a proof-of-concept. All it is capable of doing is opening up a console and giving you 
an interface to input a URL, retrieve all instances of any string that matches an email regex, and
output that result to a file (assuming stdout redirection isn't an option). It also does not check 
for repeats of emails.
'''

print(
'''
 _____ _           ______          _     ______      _   
|_   _| |          | ___ \        | |    | ___ \    | |  
  | | | |__   ___  | |_/ /_ _  ___| | __ | |_/ /__ _| |_ 
  | | | '_ \ / _ \ |  __/ _` |/ __| |/ / |    // _` | __|
  | | | | | |  __/ | | | (_| | (__|   <  | |\ \ (_| | |_ 
  \_/ |_| |_|\___| \_|  \__,_|\___|_|\_\ \_| \_\__,_|\__|
                                                         
''')

# Necessary modules
import requests, re, os
from bs4 import BeautifulSoup
from datetime import datetime

# URL
url = input('URL to scrape emails from: ')

# Checks to see if the input was correct
# Pretty awful input validation, but it works
if 'http://' in url or 'https://' in url:
  pass
else:
  url = 'http://' + url

# Emails
emails = []

# Email regex
'''
This took a long time | Raw strings would've been a very useful tool to know a long time ago
Got help from http://www.regexone.com/ and https://emailregex.com/
'''
pattern = r'(^[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.])'
regex = re.compile(pattern)

# Sends an HTTP GET request, stores the HTTP response and soupifies the content of the response
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

''' Finds every email addr on the page '''
for email in soup.find_all(string=regex):
  emails.append(email)

# Print List to the console & write each email to a file
resultFile = open(f'PackRat_{datetime.now().strftime("%H-%M-%S")}_EmailList.txt', 'w')

# Loop to print and write
for email in emails:
  print(email)
  resultFile.write(email + '\n')

# Print location of the file
print(os.get)

# Close the file
resultFile.close()
