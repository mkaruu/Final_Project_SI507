import unittest
import si507_finalproject as finalproj
import json

fname = "google_data.json"
new_file = open(fname, 'r')
new_file_content = new_file.read()
diction =json.loads(new_file_content) 
new_file.close()

class TestShootings(unittest.TestCase):

    maxDiff= 3 

    def testEmptyParams(self):
    	instance1= finalproj.shootings()

    	self.assertEqual(instance1.year, None)
    	self.assertEqual(instance1.state, None)
    	self.assertEqual(instance1.location, None)
    	self.assertEqual(instance1.deaths, None)
    	self.assertEqual(instance1.injuries, None)
    	self.assertEqual(instance1.description, None)
    	self.assertEqual(instance1.__str__(), "Location: None Year: None Deaths: None Injuries: None description: None \n")

    def testFilledParameters(self):
    	instance = finalproj.shootings(year='2018', state= 'Florida', location='Parkland, Florida', deaths= '17', injuries='14', description='Marjory Stoneman Douglas High School shooting: A 19-year-old former student whose behavior had led to his expulsion, began shooting students and staff members with a semi-automatic rifle at Marjory Stoneman Douglas High School after activating a fire alarm. 17 people were killed, and 14 others were injured.')
   	
    	self.assertEqual(instance.year, "2018" )
    	self.assertEqual(instance.state, "Florida")
    	self.assertEqual(instance.location, "Parkland, Florida")
    	self.assertEqual(instance.deaths, '17')
    	self.assertEqual(instance.injuries, '14')
    	self.assertEqual(instance.description[0], 'M')

    def testGetWiki_data(self):
    	wiki_shootings = finalproj.get_wiki_data()

    	self.assertEqual(type(wiki_shootings), list)
    	self.assertEqual(wiki_shootings[-2].__str__(), "Location: Birmingham, Alabama Year: 2018 Deaths: 2 Injuries: 1 description: University of Alabama at Birmingham: A disgruntled employee entered the UAB Highlands Hospital on the campus of the University of Alabama at Birmingham and shot two hospital employees, fatally wounding one, on the second floor. The perpetrator then shot and fatally wounded himself. [564] \n")

    # def testGetCoordinates(self):
    # 	list_of_coordinates = finalproj.get_coordinates()
    # 	self.assertEqual(type(list_of_coordinates), list)
    # 	self.assertEqual(type(list_of_coordinates[0]), tuple)
    # 	self.assertEqual(list_of_coordinates[0], ('39.790371', '-77.7277714'))


unittest.main(verbosity=2)
    	

