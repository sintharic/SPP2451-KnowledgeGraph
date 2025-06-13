import os
import json
from glob import glob

SRC = f'.{os.sep}people'
DST = f'..{os.sep}people'

projects = os.listdir(SRC)
os.makedirs(DST, exist_ok=True)

lines = ['']
for project in projects:
  people = glob(f'{SRC}{os.sep}{project}{os.sep}*.txt')
  for file in people:
    person = {'name': '', 'title': '', 'role': '', 'project': project, 'affiliations': [], 'email': '', 'phone': '', 'website': ''}
    with open(file,'r') as fid:
      lines = fid.readlines()

    # get name and title
    name = lines[0].rstrip()
    title = '' 
    if name.startswith('Prof. '): 
      title += 'Prof. '
      name = name[6:]
    if name.startswith('Dr.-Ing. '): 
      title += 'Dr.-Ing. '
      name = name[9:]
    if name.startswith('Dr. '): 
      title += 'Dr. '
      name = name[3:]
    name = name.lstrip()
    title = title.rstrip()
    if not title: title = 'M.Sc.'
    # print(f'({title}) {name}')
    person['name'] = name
    person['title'] = title
    print(f'[{name} ({title})]')

    # get role
    role = lines[1].rstrip()
    # print(role)
    person['role'] = role

    # get affiliations
    affil = []
    for line in lines[2:]:
      if ('Phone' in line) or ('E-mail' in line) or ('https' in line): break
      line = line.rstrip()
      if len(line)<2: continue
      affil.append(line)
    # print('Affil.:', affil)
    person['affiliations'] = affil

    # get Phone
    for line in lines[2:]:
      if line.startswith('Phone: '):
        person['phone'] = line[7:].rstrip()
        # print('Phone:', person['phone'])
      if line.startswith('E-mail: '):
        person['email'] = line[8:].rstrip()
        # print('E-mail:', person['email'])

    if lines[-1].startswith('https'):
      person['website'] = lines[-1].rstrip()
      # print('Website:', person['website'])

    json.dump(person, open(f'{DST}{os.sep}{name}.json', 'w'), indent='  ')
    print(person)
    print()