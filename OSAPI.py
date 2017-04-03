#getLegislators pulls basic info for legislators by state
	#url ='http://www.opensecrets.org/api/?method=getLegislators&id=NJ&apikey=__32cabcec9c4b9305dc3b94acd5109c9e__'
	#above is provided by website. a JSON url code. This is for reference now. Repeatable URL is below.

	#this specific call didn't have an example of what a space (" ") looks like
import urllib.request
import json
import pprint

printer = pprint.PrettyPrinter(indent=4)
OS_API = '32cabcec9c4b9305dc3b94acd5109c9e'
state_List = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
          'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

def OS_Search(item):
	api_key = OS_API
	url_Base = 'https://www.opensecrets.org/api/?method=getLegislators'
# state = 'NJ'
	state = item
	output = 'json'
	final_url = url_Base + "&id=" + state + "&apikey=" + api_key + '&output=' + output
	# I am trying this in the loop, but I don't think it is necessary or advised.
	# Andrew wrote the below code. It is a module that can be looked into @ https://docs.python.org/3/library/urllib.request.html
	req = urllib.request.Request(final_url, headers={'User-Agent': 'Mozilla/5.0'})
		# Thank god we have to pretend to be a browser????? This line is needed because OS doesn't like Python 3 calls when they are not from a browser.
	return_value = urllib.request.urlopen(req)
	print(return_value.status) 
		# This line specifically gives us a status code for how the pull went
	body = return_value.read()
	decoded_body = body.decode('utf-8')
	json_data = json.loads(decoded_body)

	printer.pprint(json_data)
# printer.pprint(json_data.keys())
# printer.pprint(json_data['response'].keys())
# printer.pprint(json_data['response']['legislator'].keys()) 
	# this will let you check what the keys are in the data field names. 
	# might have to repeat several times, they are nested
all_Data = []
for item in state_List:
	all_Data.append([item, OS_Search(item)])


# 	json_obj = urlopen(final_url)
# #tool to open the data in the terminal but is not converted from json 'text'
# 	data = json.load(json_obj)
# #converts it to 'readable' format. more like what it would look like in python. a dictionary!