import os
import json
import numpy as np
from glob import glob

SRC_projects = 'Antragsübersicht bewilligte Anträge.csv'
DST_info = f'..{os.sep}SPP.json'
DST_projects = f'..{os.sep}projects'
nheader = 2
colheader = 1

english_title = {
  4: 'Adaptive biomaterials through mechano-modulating bacteria',
  6: 'Adaptive capsule-based materials for programming engineered living systems',
  19: 'Adaptive Engineered Bacterial Coacervates',
  27: 'Adaptive Living Seed Coatings',
  21: 'Combining stimuli-responsive hydrogels and scaffold-supported microbial biofilms for a self-controlled catalytic activity of a microbial leaf',
  22: 'ContainELMs – Material-centric genetic programming of biocontainment in Engineered Living Materials',
  20: 'Engineered Living Actuators from Filamentous Cyanobacteria',
  3: 'Engineering adaptive Vibrio natriegens strains for bacteria-hybrid light-emitting diodes (ENABLED)',
  1: 'Living electro-biocatalyst scaffolds for sensing and cleaning',
  23: 'Living Plasmonics: Distributed environmental sensing with photoluminescent sensor ELM through enzymatic coupling of bacterial sensing with nanoplasmonics',
  7: 'Living Therapeutic Materials with long term, sonoresponsive and mechanoadaptive function',
  17: 'ProbioGel as Adaptive Living Skin and Wound Therapeutics',
  5: 'Self-synthesizing, self-organizing, and stimuli-responsive multi-cell-type Engineered Living Materials based on enzymatic polymerizations on cell surfaces (PolyCell-ELMs)',
  12: 'Smart Stimuli-Responsive Opalescent Bacterial Films (OPAL-Bac)',
  13: 'SporoPrinting – 3D matrices for immobilizing and controlling functionalized SporoBeads of B. subtilis as a structured protein displaying ELM platform with adaptive functions',
  8: 'Coordination of SPP-2451'
}


os.makedirs(DST_projects, exist_ok=True)
current = 0
projects = []
info = ''
with open(SRC_projects) as file:
  line = ''
  for _ in range(nheader): line = file.readline()
  info = line.split(';')[0]

  for line in file.readlines()[colheader:]:
    
    split = line.split(';')
    try: 
      num = int(split[0])
    except: 
      projects[-1]['abstract_de'] += line
      #projects[-1]['abstract_de'] += f'\n{line}'
      continue
 
    # append to current project info
    if num==current: 
      projects[-1]['applications'].append(split[1])
      projects[-1]['principal_investigators'].append(split[2])
      projects[-1]['locations'].append(split[4])
      continue

    # start of new project info
    current = num
    projects.append(dict())
    projects[-1]['lfd-nr'] = num
    projects[-1]['applications'] = [split[1]]
    projects[-1]['principal_investigators'] = [split[2]]
    projects[-1]['title_de'] = split[3]
    projects[-1]['title_en'] = english_title[num]
    projects[-1]['locations'] = [split[4]]
    projects[-1]['collaborators'] = split[5]
    projects[-1]['abstract_de'] = split[6]


# clean up abstracts
for project in projects:
  if len(project['abstract_de']) < 3: continue
  if project['abstract_de'][-1]=='\n': project['abstract_de'] = project['abstract_de'][:-1]
  if project['abstract_de'][-1]=='"': project['abstract_de'] = project['abstract_de'][:-1]
  if project['abstract_de'][0]=='"': project['abstract_de'] = project['abstract_de'][1:]

# create individual json files for projects
projects = sorted(projects, key=lambda p: p['title_en'].lower())
# projects = sorted(projects, key=lambda p: p['lfd-nr'])
for i,project in enumerate(projects):
  if project['lfd-nr']==8: continue # skip the coordination project
  project['alphabetical_number'] = str(i+1).zfill(2)
  json.dump(project, open(f"{DST_projects}{os.sep}project{project['alphabetical_number']}.json", 'w'), indent='  ')

# create global json file
data = dict()
for item in info.split(','):
  key, value = item.split(':')
  while key[0]==' ': key = key[1:]
  while value[0]==' ': value = value[1:]
  while key[-1]==' ': key = key[:-1]
  while value[-1]==' ': value = value[:-1]
  data[key] = value

json.dump(data, open(DST_info,'w'), separators=(',',' : '), indent=2, ensure_ascii=False)