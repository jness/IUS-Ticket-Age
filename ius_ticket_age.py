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
    messagecount = bug.bug.message_count

    # Add our data to the List
    bugs.append([id, status, assignee, subject, lastupdate])

now = datetime.now().date()

print """To: user@domain.com 
From: IUS Coredev <ius-coredev@lists.launchpad.net>
Subject: IUS Bugs older than 60 days
Content-Type: text/html; charset="us-ascii"

<pre>
"""

print "-"*78
print '%-7s %-10s %-4s %-8s %s' % ('#', 'Status', 'Age', 'Assignee', 'Subject')
print "-"*78

for bug in sorted(bugs, key=lambda age: age[4]):
    delta = (now -  bug[4])
    if delta > timedelta(days = 60):
        print '%-7s %-10s %-4s %-8s %s' % (
        bug[0], 
        bug[1][0:9], 
        delta.days, 
        bug[2][0:7], 
        '<a href="https://bugs.launchpad.net/ius/+bug/' + bug[0] + '">' + bug[3][0:49] + '</a>'
        )

print '</pre>'
