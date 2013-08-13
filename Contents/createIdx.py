#!/opt/local/bin/python2.7

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'Resources/Documents'

page = open(os.path.join(docpath,'toc.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0 and not re.compile("\[\d+\]").match(name):
        path = tag.attrs['href'].strip()
        elems = path.split('#')
        resName = elems[0]
        if (path in ('')):
            continue
        _type = 'Guide'
        if resName not in ('index.html', 'intro.html', 'toc.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, _type, path))
            print 'name: %s, path: %s, type: %s' % (name, resName, _type)

page = open(os.path.join(docpath,'tasksoverview.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0 and not re.compile("\[\d+\]").match(name):
        path = tag.attrs['href'].strip()
        elems = path.split('#')
        resName = elems[0]
        if (len(elems) > 1 and elems[1] in ('top')) or (re.compile("http:|https:").match(path)) or (len(resName) == 0):
            continue
        _type = 'Tag'
        if resName not in ('tasksoverview.html', 'intro.html', 'toc.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, _type, path))
            print 'name: %s, path: %s' % (name, resName)


page = open(os.path.join(docpath,'conceptstypeslist.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0 and not re.compile("\[\d+\]").match(name):
        path = tag.attrs['href'].strip()
        elems = path.split('#')
        resName = elems[0]
        if (len(elems) > 1 and elems[1] in ('top')) or (re.compile("http:|https:").match(path)) or (len(resName) == 0):
            continue
        _type = 'Type'
        if resName not in ('tasksoverview.html', 'intro.html', 'toc.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, _type, path))
            print 'name: %s, path: %s' % (name, resName)

db.commit()
db.close()
