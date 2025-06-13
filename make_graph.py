ontofile = 'ontology.json'
kwfile = 'keywords.json'
jsonfile = 'SPP.json'
vault = 'SPP-KG'



import os
import shutil
import json
from glob import glob
from geopandas.io import file

project_string = 'SPP-2451-Project'
# project_string = 'SPP-2451-'


# projects = json.load(open(jsonfile))['projects']
projects = [json.load(open(file,'r')) for file in glob(f'projects{os.sep}*.json')]
people = [json.load(open(file,'r')) for file in glob(f'people{os.sep}*.json')]
ontology = json.load(open(ontofile))
keywords = json.load(open(kwfile))

name = dict()
for parent in ontology.keys():
  for instance in ontology[parent]: 
    name[instance] = parent.upper()+'_'+instance.upper()

# sanity check
try:
  for topic in name.keys():
    _ = keywords[topic]
  for topic in keywords.keys():
    _ = name[topic]
except:
  raise KeyError('name and keywords must include the same items')

# assign topics to projects
for project in projects:
  abstract = project['abstract_de'].lower()
  project['topics'] = []
  project['researchers'] = []
  for topic in keywords.keys():
    for keyword in keywords[topic]:
      idx = abstract.find(keyword)
      if idx >= 0:
        project['topics'].append(topic)
        abstract = f'{abstract[:idx]}[[{name[topic]}]]{abstract[idx:]}'
        orig = project['abstract_de']
        project['abstract_de'] = f'{orig[:idx]}[[{name[topic]}]]{orig[idx:]}'
  # project['abstract_de'] = abstract


# create Obsidian vault
os.makedirs(vault, exist_ok=True)
os.makedirs(f'{vault}{os.sep}projects', exist_ok=True)
os.makedirs(f'{vault}{os.sep}topics', exist_ok=True)
os.makedirs(f'{vault}{os.sep}people', exist_ok=True)


# add people to vault
for person in people:
  filename = f"{vault}{os.sep}people{os.sep}{person['name']}.md"
  with open(filename, 'w') as file:
    file.write('## Full Name\n')
    file.write(f"{person['title']} {person['name']}\n")
    file.write('\n## Affiliations\n')
    for affil in person['affiliations']:
      file.write(f'- {affil}\n')
    num = int(person['project'][-2:])
    # print(num)#DEBUG
    file.write(f'- [[{project_string}{str(num).zfill(2)}]]')
    for project in projects:
      if project['alphabetical_number'] == num:
        project['researchers'].append(f"{person['name']}")
    file.write('\n## Contact\n')
    if person['phone']: file.write(f"- {person['phone']}\n")
    if person['email']: file.write(f"- {person['email']}\n")
    if person['website']: file.write(f"- {person['website']}\n")


# add projects to vault
for project in projects:
  # pid = project['lfd-nr']
  pid = str(project['alphabetical_number']).zfill(2)
  filename = f'{vault}{os.sep}projects{os.sep}{project_string}{pid}.md'
  with open(filename,'w') as file:
    file.write('## Title\n')
    file.write(project['title_de'])
    file.write('\n\n## Researchers\n')
    for person in project['researchers']:
      file.write(f'- [[{person}]]\n')
    file.write('\n## Principal investigators\n')
    for idx,PI in enumerate(project['principal_investigators']):
      loc = project['locations'][idx]
      file.write(f'{PI} ({loc})\n')
    file.write('\n## Zusammenfassung\n')
    file.write(project['abstract_de'])

for topic in name.keys():
  tid = name[topic]
  filename = f'{vault}{os.sep}topics{os.sep}{tid}.md'
  with open(filename,'w') as file:
    # file.write('.')
    for project in projects:
      if topic in project['topics']:
        # pid = project['lfd-nr']
        pid = str(project['alphabetical_number']).zfill(2)
        title = project['title_de']
        file.write(f'- [[{project_string}{pid}]]: {title}\n')