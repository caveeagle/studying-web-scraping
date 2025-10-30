
import requests
import sys
import json
import time
import os

####################################

INPUT_JSON_FILE = 'leaders.json'

DELAY = 1  # Delay for web scraping (in seconds)

####################################

# Set console output to utf (for print command):
sys.stdout.reconfigure(encoding='utf-8')

####################################

# Read list of leaders:

with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as j_file:
    
    leaders = json.load(j_file)  

####################################    

for leader in leaders:

    wiki_url = leader['wikipedia_url']
    
    # Check url:
    
    if not 'wikipedia.org' in wiki_url:
        print('Error with the URL: ',wiki_url)
        continue  # skip this url
    
    print(f"Download for: {leader['first_name']} {leader['last_name']} ...", end="")
    
    time.sleep(DELAY)
    
    ###############
    
    # Download page
    
    filename = os.path.join(".","webdata", f"{leader['id']}.htm")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        # GET-request
        response = requests.get(wiki_url, headers=headers, timeout=10)  # timeout - in seconds!
        response.raise_for_status()  # raise HTTPError if code ne 200
    
        html_text = response.text  
    
        # check if this is html page:
        if '<head>' not in html_text.lower(): 
            raise ValueError("It's not true html page")
    
        # Write to file
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_text)
    
        print(' done!')
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection fail: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout exceded: {e}")
    except requests.exceptions.RequestException as e:
        print(f"general error: {e}")
    except ValueError as e:
        print(f"Error: {e}")    
    
    
    ###############
    
    #break # DEBUG !!!!
    

####################################
####################################

#####################################

print('\n\nScript finished')

