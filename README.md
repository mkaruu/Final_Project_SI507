# SI507-Final-Project
Final Project Submission

Data sources
Wikipedia: List of school massacres by death toll (diff countries), Wikipedia (List of School Shootings in the US) (scraped muliple pages)
MotherJones (List of Mass Shootings and their characteristics since 1982) (CSV)
Google Places: Need API Key: https://developers.google.com/places/web-service/search  


I scraped data from Wikipedia on all the school shootings that have ever happened in U.S history and also the school shootings with the highest death toll globally and wrote them into my database.
I then used google places to get the coordinates for all the places where the school shootings happened so that I could make a map
I also used data on Mass shootings in the U.S since 1982 to look at the increase of shootings in the U.S in the last few decades. I looked at the increase in deaths and injuries from mass shootings in the U.S with this data
To run the code you need a Google places API key. The beginning of the code (get_wiki_data function) scrapes data from wikipedia and writes it into the database. The class shootings separates all the data into the important components (location of shooting, year, deaths, injuries, and description) and this is how the data is returned from the get_wiki_data function. Next the code gets coordinates for the locations of the shootings from the google_api (several API keys were needed for this because it is a big dataset). The get_coordinates function then returns a list of tuples with the coordinates for all the locaitons which is used later to create maps of shootings in the US. A separate python file csv.write was used to write in CSV data from Motherjones into the database and both of these datasets were used to produce graphs and maps using plotly. The command lines below produce the different graphs.

I present graphs and maps with the data
1. count of mass shootings in US since 1982 (Mjones) search  <stats mass>

2. count of injuries/deaths in US since 1982 (Mjones) search  <stats injuries/deaths>
       	
3. count of school shootings in US history search  <stats schools>
        
4. top 10 states with the most shootings  search  <stats top10>
        
5. deaths from school shootings since 1764 search  <stats schooldeaths>
       
6. see map of all shootings in U.S History and massacres across the world search  <map>
        		
7. exits the program <exit>
     
8. list available commands (these instructions)''') <help>
     
