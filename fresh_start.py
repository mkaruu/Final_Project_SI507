import json
import requests
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

CACHE_FNAME = "Wiki_data.json"

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents) #convert this json file into something that python can work with
    cache_file.close()
except: # But if anything doesn't work,
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params_d): #constructing the key for us that will always be unique to whatever search that we make.
    alphabetized_keys = sorted(params_d.keys()) #keeps the paramaters in the same order by sorting by the keys
    res = []
    for k in alphabetized_keys:
        # if k not in private_keys:
	    res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res) #join it all into a big string

def get_wiki_data ():
    baseurl = "https://en.wikipedia.org/w/api.php"
    params_d = {}
    params_d["format"] = 'json'
    params_d["action"] = 'query'
    params_d["titles"] = "List of school massacres by death toll|List of school shootings in the United States"
    params_d["prop"] = 'revisions'
    params_d["rvprop"] = 'content'
    # params_d['action'] = 'parse'
    unique_identifier = params_unique_combination(baseurl, params_d)
    
    if unique_identifier in CACHE_DICTION:
        print("WIKIW!!: It's in the cache so we'll go and get the value there")
        return CACHE_DICTION[unique_identifier]
    else:
        print("WIKI!!: We have to make a request to the API then save it to the cache")
        response_obj = requests.get(baseurl, params_d) #request made to API to get response object. #This line will 1. make the url 2. call the url - make request to FLICKR and 3 return a response object

        resp = response_obj.text
        CACHE_DICTION[unique_identifier] = json.loads(resp) # Now lets's store the object in our cache by saving the text (converted to a python object) to the value for unique identifier
        dump_json_cache = json.dumps(CACHE_DICTION) #Convert our cache diction back into a JSON formatted thing
        updated_cache = open (CACHE_FNAME, 'w')
        updated_cache.write(dump_json_cache) #write the dumps (JSON formatted string retried from the API into our cache dictionary)
        updated_cache.close()
        print("WIKI confirmation that this code is running")
        return CACHE_DICTION[unique_identifier]

get_wiki_data()