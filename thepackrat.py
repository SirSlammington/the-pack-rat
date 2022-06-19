#!/usr/bin/python3
import requests, re
from bs4 import BeautifulSoup
from argparse import ArgumentParser; import sys
from export import Export

# Aggregate data found
agg_data = []

regex = {
  'email': re.compile(r'[\w\.-]+@[\w\.-]+'),
  'phone': re.compile(r'(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'),
  'ipv4': re.compile(r'((1?\d\d?|2[0-4]\d|25[0-5])\.){3}(1?\d\d?|2[0-4]\d|25[0-5])')
}

# Default header params
def_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

# Obtain info from soup object
def getData(target, data):
  for a_match in target.find_all(string=regex.get(data)):
    if a_match in agg_data:
      pass
    else:
      agg_data.append(re.search(regex.get(data), a_match).group())

# Format phone numbers to be homogenous
def formatPhone(phone_number):
  numeric_filter = filter(str.isdigit, phone_number)
  numeric_phone_number = ''.join(numeric_filter)
  return f'({numeric_phone_number[:3]}) {numeric_phone_number[2:5]}-{numeric_phone_number[-4:]}'

# Format data to be exported
def formatData(collected_data, spec_data):
  # Ensure that each individual item is only ever a string
  for item in collected_data:
    item = str(item)

  spec_data = spec_data.lower()

  try:
    if spec_data == 'phone':
        collected_data = [formatPhone(phone_num) for phone_num in collected_data]
        return collected_data
    else:
      return collected_data
  except ValueError or TypeError:
    print('Preferred data to scrape is invalid or otherwise unavailable.')
    return None

# I know this is a poor way of accomplishing this, but it is how I will do it
def exportData(collected_data, exp, spec_data):
  exp = exp.lower()
  match exp:
    case 'txt':
      Export(collected_data, spec_data).toTXT()
    case 'xml':
      Export(collected_data, spec_data).toXML()
    case 'csv':
      Export(collected_data, spec_data).toCSV()
    case 'json':
      Export(collected_data, spec_data).toJSON()

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
    
    -u, --url\t\t Provide the URL of the web page you would like to scrape from
    -d, --data\t\t Specify the type of data you'd like to collect (email [for email addresses], phone [for phone numbers])
    -x, --export\t File format to export your data to (`txt`, `xml`, `csv`, `json`)
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
  
  ''' Finds every instance of the desired data on the page. '''
  ''' This is the sequence that gets the data, formats it, and exports it. '''
  getData(soup, pref_data)
  for item in agg_data:
    print(item)

  exportData(formatData(agg_data, pref_data), export_option, pref_data)
  
