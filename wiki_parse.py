
import sys
import os
import re

##########################################

subdirectory = 'webdata'

DEBUG = 0

##########################################

# Set console output to utf (for print command):
sys.stdout.reconfigure(encoding='utf-8')

files = []

# Make list of files with .htm extemsion:
for myfile in os.listdir(subdirectory):
    if myfile.endswith(".htm"):
        files.append(myfile)

print(f'Find {len(files)} files\n')

for filename in files:
    filepath = os.path.join(subdirectory, filename)

    if DEBUG and filename != 'Q91.htm':
            continue

    print(f'Parse file {filename} .... ', end="")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r"</tbody></table>\s*<p><b>(.*?)</p>"
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        result = match.group(1)
        # Clean of html-tags
        clean_text = re.sub(r"<[^>]*>", "", result)
        
        if(DEBUG):
            print(clean_text)
        
    else:
        print('\n\nError: paragraph not found. The HTML might be more complex than it seems.')
        print(f'Error in file {filename}\n')
        continue

    print('done')
        
#####################################

print('\nScript finished')

        
        