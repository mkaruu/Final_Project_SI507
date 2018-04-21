import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
from bs4 import BeautifulSoup
import requests
import json
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import sqlite3 as sqlite
import csv
import sqlite3

CACHE_FNAME = 'mass_shootings_data_cache.json'
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()

# if there was no file, no worries. There will be soon!
except:
	CACHE_DICTION = {}

full_url = 'https://en.wikipedia.org/wiki/List_of_school_massacres_by_death_toll#References' 
def make_request_using_cache(full_url):

	unique_ident = full_url
	# print('THIS IS UNIQUE IDENT')
	# print(unique_ident)
	if unique_ident in CACHE_DICTION: ## first, look in the cache to see if we already have this data
		# print("Getting cached data...")
		return CACHE_DICTION[unique_ident]

	## if not, fetch the data afresh, add it to the cache,
	## then write the cache to file
	else:
		print("Making a request for new data...")
		# Make the request and cache the new data
		resp = requests.get(full_url)  #fetch the html data at this URL
		CACHE_DICTION[unique_ident] = resp.text  ##DON'T FORGET THE .TEXT
		dumped_json_cache = json.dumps(CACHE_DICTION)
		fw = open(CACHE_FNAME,"w")
		fw.write(dumped_json_cache)
		fw.close() # Close the open file
		return CACHE_DICTION[unique_ident]

###########################################################################
class shootings():
	def __init__(self, year=None, state= None, location=None, deaths=None, injuries=None, description=None):
		self.year = year
		self.location = location
		self.state = state
		self.deaths = deaths
		self.injuries = injuries
		self.description = description

	def __str__(self):
		return "Location: {} Year: {} Deaths: {} Injuries: {} description: {} {}".format(self.location, self.year, self.deaths, self.injuries, self.description, "\n")

	def __repr__(self):
		return self.__str__()
#############################################################################


def get_wiki_data():
	data = []
	base_url = 'https://en.wikipedia.org/wiki/'
	site_url = base_url+'List_of_school_massacres_by_death_toll#References'
	resp = make_request_using_cache(site_url) #request for each state
	site_page_soup = BeautifulSoup(resp,'html.parser')
	page_dig = site_page_soup.find_all('table', class_ ="wikitable")
	# print('!!!!!!!!!!!')
	# print(page_dig)
	table_rows = page_dig[0].find_all('tr')
	# print(len(table_dig)) #124
	# print(table_dig[2])

	wiki_shootings = []
	for row in table_rows:
	# # 	print(each)
		table_cells = row.find_all('td')
		if len(table_cells) > 10:
			num = table_cells[0].text.strip()
			name = table_cells[1].text.strip()
			date = table_cells[2].text.strip()
			year = table_cells[3].text.strip()
			# location = table_cells[4].text.strip()
			# print(location)
			location =  table_cells[5].text.strip() #country
			# print(country)
			deaths = table_cells[6].text.strip()
			injuries = table_cells[7].text.strip()
			# injuries = injuries[:-2]
			weapon = table_cells[8].text.strip()
			perpetrator = table_cells[9].text.strip()
			fate_perp = table_cells[10].text.strip()
			instance = shootings(year,location, deaths, injuries)
			# wiki_shootings.append(instance)
	# print(all_shootings)
	us_school_shootings =base_url+'List_of_school_shootings_in_the_United_States'
	site_resp = make_request_using_cache(us_school_shootings)
	page_soup = BeautifulSoup(site_resp,'html.parser')
	page_data = page_soup.find_all('table', class_= 'wikitable')
	# print(page_data[1])
	# print(len(page_data))

	
	for table in page_data:
		table_rows = table.find_all('tr')
		# print(len(table_rows[1]))
		# print(table_rows)

		us_shootings_list = []
		for row in table_rows:
			table_cells = row.find_all('td')
			# print(len(table_cells))
			if len(table_cells) >4:
				date = table_cells[0].text.strip()
				year = date[-4:]
				location = table_cells[1].text.strip()
				state_chunk = location.split()
				state = state_chunk[-1]
				deaths = table_cells[2].text.strip()
				injuries = table_cells[3].text.strip()
				description = table_cells[4].text.strip()
				instance = shootings(year, state, location, deaths, injuries, description)
				# print(instance)
				wiki_shootings.append(instance) ###UNCOMMENT!!!!!
 

	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
		
	statement = '''
	DROP TABLE IF EXISTS 'Wiki_data';
'''
	cur.execute(statement)
	conn.commit()

	wiki_table_statement = '''
	CREATE TABLE 'Wiki_data' (
		'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
		'year' TEXT NOT NULL, 
		'location' TEXT NOT NULL,
		'state' TEXT NOT NULL,  
		'deaths' INTEGER NOT NULL, 
		'injuries' INTEGER NOT NULL, 
		'Description' TEXT NOT NULL
		
	);
'''
	cur.execute(wiki_table_statement)
	conn.commit()
	# print(wiki_shootings[400:])
	for each in wiki_shootings:
		year = each.year
		location = each.location
		deaths = each.deaths
		injuries = each.injuries
		description = each.description
		state = each.state
		# print(year)
		values = (None, year, location, state, deaths, injuries, description)
		# print(values)
		statement = 'INSERT INTO "Wiki_data" '
		statement += ' VALUES (?, ?, ?, ?, ?, ?, ?)' #not sure if null or ? for the primary
		cur.execute(statement, values)
		conn.commit()
	conn.close()
	print('CODE IS RUNNING')
	# print(wiki_shootings)
	return wiki_shootings



# get_wiki_data()
#######################################################################################
GOOGLE_CACHE_FNAME = 'google_data.json'

try:
	google_cache_file = open(GOOGLE_CACHE_FNAME, 'r')
	google_cache_contents = google_cache_file.read()
	GOOGLE_CACHE_DICTION = json.loads(google_cache_contents)
	google_cache_file.close()

# if there was no file, no worries. There will be soon!
except:
	GOOGLE_CACHE_DICTION = {}


# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params, private_keys=['api_key']):
	alphabetized_keys =sorted(params.keys())
	res = []
	for k in alphabetized_keys:
		if k not in private_keys:
			res.append("{}-{}".format(k, params[k]))
	return baseurl + "_".join(res) #join it all into a big string

####################################################################
def google_text_search(search_text):
	Google_API = '' 
	baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
	params_diction= {}
	params_diction['query'] = search_text
	params_diction['key'] = Google_API
	# url = baseurl + national park + site_type 
	# text_result = make_google_request_using_cache(baseurl,params)
	# return text_result
	unique_id = params_unique_combination(baseurl,params_diction)
	print(unique_id) #THIS IS WHAT IS USEDD TO SAVE THE QUERY
	## first, look in the cache to see if we already have this data
	if unique_id in GOOGLE_CACHE_DICTION:
		print("THIS IS UNIQUE ID IN THE CACHE")
		# print(unique_id)
		print("GETTING CACHED DATA!!!!")
		return GOOGLE_CACHE_DICTION[unique_id]

	## if not, fetch the data afresh, add it to the cache,
	## then write the cache to file
	else:
		print("!!!!!!!!MAKING A REQUEST FOR NEW DATA!!!!!!!! ")
		#Make the request and cache the new data
		google_resp = requests.get(baseurl, params=params_diction) #!!!
		print(google_resp.url) #THIS IS DIFFERENT FROM WHAT IS BEING USED TO SAVE THE QUERY
		GOOGLE_CACHE_DICTION[unique_id] =json.loads(google_resp.text) 
		google_dumped_json_cache =json.dumps(GOOGLE_CACHE_DICTION)
		google_fw = open(GOOGLE_CACHE_FNAME,"w")
		google_fw.write(google_dumped_json_cache)
		google_fw.close() # Close the open file
		print("THIS IS URL FROM NEW REQUEST!!!")
		# print (unique_id)
		return GOOGLE_CACHE_DICTION[unique_id]
		print("This is the end!!!")
#################################################################
def get_coordinates():
	list_of_coordinates =  []
	wiki_data = get_wiki_data()
	for each in wiki_data:
		search_text = (each.location)
		site_search = google_text_search(search_text)
		print('THIS IS SITE SEARCH!!!!!!')
		print(site_search)
	#   if site_search['results'] 
		coordinates = site_search['results'][0]['geometry']['location']
		latitude = coordinates['lat']
		longitude = coordinates['lng']
		lon_lat = str(latitude), str(longitude)
		print(lon_lat)
		list_of_coordinates.append(lon_lat)
	# print(list_of_coordinates[0])
 # print(list_of_coordinates[0])
	return list_of_coordinates

# get_coordinates()
########################################################################
#read data in DB from motherjones
def mass_1982_count_stats():
	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
	statement = "SELECT Year, COUNT(Year) FROM MJonesUSMassShootings GROUP BY Year"
	result = cur.execute(statement)
	result = cur.fetchall()

	year = []
	count = []
	for row in result:
		shooting_year = str(row[0])
		num_shooting = str(row[1])
		res = "In " + shooting_year + " there were " + num_shooting + " shootings in the US"
		year.append(shooting_year)
		count.append(num_shooting)
		# print(shooting_year)
	# conn.close()

	trace0 = go.Scatter(dict(x=year,y=count),)
	data =Data([trace0])

	layout = dict(title = 'Mass Shootings in the US since 1982',
				  xaxis = dict(title = 'Year Since 1982'),
				  yaxis = dict(title = 'Number of Mass Shootings'),
				  )

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'basic-line')

###############################################################################
def school_count_stats():
	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
	statement = "SELECT year, COUNT(year) FROM Wiki_data GROUP BY year"
	result = cur.execute(statement)
	result = cur.fetchall()

	year = []
	count = []
	for row in result:
		shooting_year = str(row[0])
		num_shooting = str(row[1])
		res = "In " + shooting_year + " there were " + num_shooting + " shootings in the US"
		year.append(shooting_year)
		count.append(num_shooting)
		# print(shooting_year)
	# conn.close()

	trace0 = go.Scatter(dict(x=year,y=count),)
	data =Data([trace0])

	layout = dict(title = 'School Shootings in the US History',
				  xaxis = dict(title = 'Year'),
				  yaxis = dict(title = 'Number of Shootings'),
				  )

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'basic-line')


###########################Graph 2 deaths and inj since 1982 ###################
def injuries_deaths_1982stats():
	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
	statement = "SELECT Year, SUM(Fatalities) FROM MJonesUSMassShootings GROUP BY Year"
	result2 = cur.execute(statement)
	result2 = cur.fetchall()
	# print(result2)

	deaths_year = []
	count_deaths = []
	for row in result2:
		fatalities_year = str(row[0])
		num_deaths = str(row[1])
		res = "In " + fatalities_year + " there were " + num_deaths + " deaths in the US"
		deaths_year.append(fatalities_year)
		count_deaths.append(num_deaths)
		# print(res)
	# conn.close()

	statement = "SELECT Year, SUM(Injured) FROM MJonesUSMassShootings GROUP BY Year"
	result3 = cur.execute(statement)
	result3 = cur.fetchall()
	# print(result3)

	injured_year = []
	count_injured = []
	for row in result3:
		inj_year = str(row[0])
		num_inj = str(row[1])
		res = "In " + inj_year + " there were " + num_inj + " deaths in the US"
		injured_year.append(inj_year)
		count_injured.append(num_inj)
		# print(res)
	conn.close()

	trace1 = go.Scatter(dict(x=deaths_year,y=count_deaths),
		name= 'deaths',)
	trace2 = go.Scatter(dict(x=injured_year,y=count_injured), name= 'injured',)

	data =[trace1, trace2]

	layout = dict(title = 'Deaths from Mass Shootings in US since 1982',
				  xaxis = dict(title = 'Year Since 1982'),
				  yaxis = dict(title = 'Number of Deaths/Injuries'),
				  )

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'basic-line')

# shootings_stats()
###############################################################################
def school_deaths_stats():
	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
	statement = "SELECT year, SUM(deaths) FROM Wiki_data GROUP BY year"
	result4 = cur.execute(statement)
	result4 = cur.fetchall()
	# print(result3)

	schools_death_x = []
	schools_count_y = []
	for row in result4:
		school_d_year = str(row[0])
		school_d_count = str(row[1])
		res = "In " + school_d_year + " there were " + school_d_count + " deaths in the US"
		schools_death_x.append(school_d_year)
		schools_count_y.append(school_d_count)
		# print(res)

	statement = "SELECT year, SUM(injuries) FROM Wiki_data GROUP BY year"
	result4 = cur.execute(statement)
	result4 = cur.fetchall()
	# print(result3)

	schools_inj_x = []
	schools_inj_y = []
	for row in result4:
		schools_inj_year = str(row[0])
		schools_inj_count = str(row[1])
		res = "In " + schools_inj_year + " there were " + schools_inj_count + " injuries in the US"
		schools_inj_x.append(schools_inj_year)
		schools_count_y.append(schools_inj_count)
		# print(res)
	# 

	trace3 = go.Scatter(dict(x=schools_death_x,y=schools_count_y),
		name= 'deaths',)
	trace4 = go.Scatter(dict(x=schools_inj_x, y=schools_inj_y), name= 'injured',)

	data =[trace3, trace4]

	layout = dict(title = 'Deaths from School Shootings in US since 1764',
				  xaxis = dict(title = 'Year Since 1764'),
				  yaxis = dict(title = 'Number of Deaths/Injuries'),
				  )

	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename = 'US Schools Injuries deaths line plot')
	conn.close()
#######################################################################

def top_10_states():
	conn = sqlite3.connect('mass_shootings.db')
	cur = conn.cursor()
	statement = "SELECT state, COUNT(state) FROM Wiki_data GROUP BY state ORDER BY count(*) DESC LIMIT 10"
	result5 = cur.execute(statement)
	result5 = cur.fetchall()
	# print(result5)
	x_list= []
	y_list=[]
	for state in result5:
		x_axis = state[0]
		y_axis = state[1]
		x_list.append(x_axis)
		y_list.append(y_axis)

	trace = go.Bar(dict(x=x_list,y=y_list),)
	data = [trace]
	layout = dict(title = 'States with the Highest Number of Shootings in US History',
			  xaxis = dict(title = 'State'),
			  yaxis = dict(title = 'Number of Shootings'),
			  )
	fig = go.Figure(data=data, layout=layout)
	py.plot(fig, filename='basic-bar')

# top_10_states()
#######################################################################
#map of school shootings in the US
def school_shootings_maps():

	# coordinates = get_coordinates()
	# print(coordinates)
	json_data = open('google_data.json')
	shootings_data = json.loads(json_data.read()) #list of dictionaries
	
	site_lat = []
	site_lon= []
	dates = []
	for diction in shootings_data.values():
		try:
			coordinates = diction['results'][0]['geometry']['location']
			site_latitude = coordinates['lat']
			site_longitude = coordinates['lng']
			site_lat.append(site_latitude)
			site_lon.append(site_longitude)
			# year =shootings(diction)
			# dates.append(year)
		except:
			continue


	mapbox_access_token ='pk.eyJ1IjoibWthcnV1IiwiYSI6ImNqZzc5Zml0ZDBrZ2EzNG10ZmVhZGFvcHgifQ.8IXFhJSY_T49MO209b2kEA'

	data = Data([
		Scattermapbox(
			lat=site_lat,
			lon=site_lon,
			mode='markers',
			marker=Marker(
				size=17,
				color='rgb(255, 0, 0)',
				opacity=0.7
			),
			# text=locations_name,
			hoverinfo='text'
		),
		Scattermapbox(
			lat=site_lat,
			lon=site_lon,
			mode='markers',
			marker=Marker(
				size=8,
				color='rgb(242, 177, 172)',
				opacity=0.7
			),
			hoverinfo='none'
		)]
	)
			
	layout = Layout(
		title='Shootings in the US',
		autosize=True,
		hovermode='closest',
		showlegend=False,
		mapbox=dict(
			accesstoken=mapbox_access_token,
			bearing=0,
			center=dict(
				lat=38,
				lon=-94
			),
			pitch=0,
			zoom=3,
			style='light'
		),
	)

	fig = dict(data=data, layout=layout)
	py.plot(fig, filename='Shootings in US History')
######################################################################

while True:

    search = input("Enter command (or 'help' for options): ")   
    args = search.split()
    cmd = args[0]
    if cmd == 'exit':
        break
    print(args)
    if cmd == "stats":
        user_input = args[1] #mass vs. school
        if user_input == 'mass':
        	mass_1982_count_stats() #count of mass shootings since 1982
        if user_input == 'injuries/deaths':
        	injuries_deaths_1982stats() #count of inj/deaths since 1982
        if user_input == 'schools':
        	school_count_stats() #count of school shootings in US history
        if user_input == 'top10':
        	top_10_states() #top 10 states with the most shootings
        if user_input == 'schooldeaths':
        	school_deaths_stats() #deaths from school shootings since 1764
    if cmd =="map":
    	school_shootings_maps() #map of school shootings
			
    if cmd == 'help':
        print(''' 
       all searches available anytime
       		count of mass shootings in US since 1982
   	search  <stats mass>
       		count of injuries/deaths in US since 1982
   	search  <stats injuries/deaths>
       		count of school shootings in US history
    search  <stats schools>
       		top 10 states with the most shootings
    search  <stats top10>
    	   deaths from school shootings since 1764
    search  <stats schooldeaths>
   map
   see map of all shootings in U.S History and massacres across the world
   		search  <map>
   exit
       exits the program
   help
       lists available commands (these instructions)''')
#interactive part
#type in state and find out how many mass (mjones) or school shootings (wiki) have occured in that state and deaths and injuries associated with each shooting