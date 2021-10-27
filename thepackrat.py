# Necessary modules
import requests, re
from bs4 import BeautifulSoup

from argparse import ArgumentParser; import sys

# Aggregate data found
agg_data = []

# Regexes
regex = {
  'email': re.compile(r'[\w\.-]+@[\w\.-]+'),
  'phone': re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'),
  'ipv4': re.compile(r'((1?\d\d?|2[0-4]\d|25[0-5])\.){3}(1?\d\d?|2[0-4]\d|25[0-5])'),
  'mac': re.compile(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
}

# Default header params
def_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

# Obtain info from soup object
def getData(target, data):
  for match in target.find_all(string=regex.get(data)):
    if match in agg_data:
      pass
    else:
      agg_data.append(re.search(regex.get(data), match).group())

# Main block
if __name__ == '__main__':
  if not len(sys.argv) > 1:
    print('''
 ___________ __    __   _______        _______    __      ______  __   ___       _______       __ ___________  
("     _   ")" |  | "\ /"     "|      |   __ "\  /""\    /" _  "\|/"| /  ")     /"      \     /""("     _   ") 
 )__/  \\__(:  (__)  :|: ______)      (. |__) :)/    \  (: ( \___|: |/   /     |:  { }   |   /    )__/  \\__/  
    \\_ /   \/      \/ \/    |        |:  ____//' /\  \  \/ \    |    __/      |_____/   )  /' /\  \ \\_ /     
    |.  |   //  __  \\ // ___)_       (|  /   //  __'  \ //  \ _ (// _  \       //      /  //  __'  \|.  |     
    \:  |  (:  (  )  :|:      "|     /|__/ \ /   /  \\  (:   _) \|: | \  \     |:  __   \ /   /  \\  \:  |     
     \__|   \__|  |__/ \_______)    (_______|___/    \___)_______|__|  \__)    |__|  \___|___/    \___)__|     
                                                                                               version 0.5.1     
    -u, --url\t\t Provide the URL of the web page you would like to scrape from
    -d, --data\t\t Specify the type of data you'd like to collect (email [for email addresses], phone [for phone numbers])
    -x, --export\t File format to export your data to (FEATURE NOT YET IMPLEMENTED)
    ''')

  parser = ArgumentParser(description='Select options.')

  # Input params
  parser.add_argument('-u', '--url', type=str, required=True, help='URL of the page to scrape from.')
  parser.add_argument('-d', '--data', type=str, nargs='?',  required=True, help='Data you would like to scrape (email, phone, media).')
  parser.add_argument('-x', '--export', required=False, default='.txt', help='File extension type to export the data to (XML, JSON, CSV, .txt, SQLite DB).')

  args = parser.parse_args()
  url = args.url
  pref_data = args.data
  export_option = args.export

  # Sends an HTTP GET request, stores the HTTP response and "soupifies" the content of the response
  res = requests.get(url, headers=def_headers, verify=True, stream=True)
  soup = BeautifulSoup(res.content, 'html.parser')
  
  ''' Finds every instance of the desired data on the page '''
  getData(soup, pref_data)
  for item in agg_data:
    print(item)