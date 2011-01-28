#!/usr/bin/python
import os
import sys
from re import compile
from launchpadlib.launchpad import Launchpad
from datetime import datetime, timedelta

# Login with your Launchpad OpenID
launchpad = Launchpad.login_with(os.path.basename(sys.argv[0]), 'production')

# API Calls to get bug data for IUS 
ius = launchpad.projects.search(text='ius')[0]
iusbugs = ius.searchTasks()

bugs = []

for bug in iusbugs:

    # Strip out the ID and Subject
    slim = compile('Bug #(\d*) in IUS Community Project: "(.*)"').findall(str(bug.title))

    #Determine is this bug is assigned
    if bug.assignee:
        assignee = bug.assignee.name
    else:
        assignee = ''

    id = slim[0][0]
    subject = slim[0][1]
    lastupdate = bug.bug.date_last_updated.date()
    status = bug.status

    # Add our data to the List
    bugs.append([id, status, assignee, subject, lastupdate])

now = datetime.now().date()
print "="*110
print '%-10s %-15s %-15s %-60s %s' % ('#', 'Status', 'Assignee', 'Subject', 'Age')
print "="*110

for bug in sorted(bugs, key=lambda age: age[4]):
    delta = (now -  bug[4])
    if delta > timedelta(days = 60):
        print '%-10s %-15s %-15s %-60s %s' % (bug[0], bug[1], bug[2], bug[3], delta.days)
