import urllib2
import json

OS_API = '32cabcec9c4b9305dc3b94acd5109c9e'

#url =''
#above is provided by website. a JSON url code. This is for reference now. Repeatable URL is below.



def OS_Search(query):
	api_key = OS_API
	url = 'thePiecesOfTheURLThatAlwaysAreTheSame' + api_key
	senator = query
	final_url = url + "senatorName" + senatorName + "contributorNames"

	json_obj = urllib2.urlopen(final_url)
#tool to open the data in the terminal but is not converted from json 'text'
	data = json.load(json_obj)
#converts it to 'readable' format. more like what it would look like in python. a dictionary!
	for item in data['list of senators']:
		print (item['name of senator']), (item['name of contributor'])
	#printing the above where each item is a line item
OS_Search('Toomey')
