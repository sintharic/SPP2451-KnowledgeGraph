ontofile = 'ontology.json'
kwfile = 'keywords.json'
jsonfile = 'SPP.json'
vault = 'SPP-KG'



import os
import shutil
import json



projects = json.load(open(jsonfile))['projects']
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
  abstract = project['abstract'].lower()
  project['topics'] = []
  for topic in keywords.keys():
    for keyword in keywords[topic]:
      idx = abstract.find(keyword)
      if idx >= 0:
        project['topics'].append(topic)
        abstract = f'{abstract[:idx]}[[{name[topic]}]]{abstract[idx:]}'
        orig = project['abstract']
        project['abstract'] = f'{orig[:idx]}[[{name[topic]}]]{orig[idx:]}'
  # project['abstract'] = abstract


# create Obsidian vault
os.makedirs(vault, exist_ok=True)
os.makedirs(f'{vault}{os.sep}projects', exist_ok=True)
os.makedirs(f'{vault}{os.sep}topics', exist_ok=True)
os.makedirs(f'{vault}{os.sep}people', exist_ok=True)

for project in projects:
  pid = project['lfd-nr']
  filename = f'{vault}{os.sep}projects{os.sep}SPP-2451-{pid}.md'
  with open(filename,'w') as file:
    file.write('## Title\n')
    file.write(project['title'])
    file.write('\n\n## PIs\n')
    for idx,PI in enumerate(project['names']):
      loc = project['locations'][idx]
      file.write(f'{PI} ({loc})\n')
    file.write('\n## Abstract\n')
    file.write(project['abstract'])

for topic in name.keys():
  tid = name[topic]
  filename = f'{vault}{os.sep}topics{os.sep}{tid}.md'
  with open(filename,'w') as file:
    # file.write('.')
    for project in projects:
      if topic in project['topics']:
        pid = project['lfd-nr']
        title = project['title']
        file.write(f'- [[SPP-2451-{pid}]]: {title}\n')