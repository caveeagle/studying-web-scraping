
import requests
import sys
import json

####################################

VERBOSE = 0  # 1 - if we want to print extendet information

OUTPUT_JSON_FILE = 'leaders.json'

base_url = 'https://country-leaders.onrender.com'

status_suffix = '/status/'

countries_suffix = '/countries'

cookie_suffix = '/cookie/'

leaders_list_suffix = '/leaders'

####################################

# Set console output to utf (for print command):
sys.stdout.reconfigure(encoding='utf-8')

# Init session object:
session = requests.Session()

####################################

# Check if API available:
    
req_url = base_url + status_suffix

response = session.get(req_url)
if response.status_code == 200:
    data = response.json()
    if(data=='Alive'):
        print('- API available')
else:
    print("Error - API not available: ", response.status_code, response.text)
    raise SystemExit(0)
  

#####################################

# Set cookies for this sessions:

### ! Within a single session, cookies are stored automatically! 

req_url = base_url + cookie_suffix

response = session.get(req_url)

if not response.status_code == 200:
    print("Error with getting cookies: ", response.status_code, response.text)
    raise SystemExit(0)

print('- Cookies recieved')

#####################################

# Get list of countries:

countries = []

req_url = base_url + countries_suffix

response = session.get(req_url)
if response.status_code == 200:
    countries = response.json()
else:
    print("Error with list of countries: ", response.status_code, response.text)
    raise SystemExit(0)
    
print('- List of countries: ',countries,'\n\n')

#####################################

# Get leader's information: list of dictionary

leaders = []

for country_code in countries:
    
    params = {"country": country_code}
    
    if(VERBOSE):
        print('\n')
        print('- Country: ',country_code)
        print('\n')
    else:
        print('- Country: ',country_code)    
    
    req_url = base_url + leaders_list_suffix
    
    response = session.get(req_url, params=params)
    
    if response.status_code == 200:
        
        leaders_in_countries = response.json()
        
        for lead in leaders_in_countries:
            
            # Add country code to each leader dictionary:
            lead['country_code'] = country_code
            
            # Add leader to list:
            leaders.append(lead)
            
            if(VERBOSE):
                print(f"Leader: {lead['first_name']} {lead['last_name']}")
        
    else:
        print("Error with list of leaders: ", response.status_code, response.text)
        raise SystemExit(0) 
    
#####################################

# Write json file

with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as j_file:
    # ensure_ascii=False allows you to preserve Unicode characters instead of escaping them.
    
    json.dump(leaders, j_file, ensure_ascii=False, indent=4)

#####################################

print('\n\nScript finished')

session.close()
