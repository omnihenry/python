#!/usr/bin/python
 
import sys
import os
import re
import shutil
import datetime
import glob
import subprocess
 
 
###################################################
#
# usage: <script> YYYY-MM-DD
#
#
###################################################
 
 
####################################################
# validate argument                                #
####################################################
if len(sys.argv) < 2: 
   print('Error: date(e.g. 2017-06-18) is needed.')
   sys.exit()
 
try:
   datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
except:
   print('Error: wrong format of date(must be YYYY-MM-DD.')
   sys.exit()
 
theDate = sys.argv[1].replace('-', '_')
 
 
####################################################
# get Message IDs from emails.txt                  #
####################################################
idStr = ''
failedIdList = []
with open('app.log', 'r') as f:
   for line in f:
      if 'Message Id:' in line:
         failedIdList += re.findall('\d+', line)
 
if len(failedIdList) == 0:
   print('No, message ids found, exiting ...')
   sys.exit()
 
#idStr = ','.join(failedIdList)
print (failedIdList)
 
 
####################################################
# put order files to msgs/failed/ dir              #
####################################################
 
 
msgDir = '/home/msgs/'
failedDir = '/home/msgs/failed/'
tmpMsgDir = '/home/msgs/tmp/'
msgProcFile = '/home/bin/messenger.sh'
 
# copy msgs of the day (theDate) to tmp dir
if os.path.isdir(tmpMsgDir):
   shutil.rmtree(tmpMsgDir)
os.mkdir(tmpMsgDir)
for node in os.listdir(msgDir):
   orgDir = os.path.join(msgDir, node)
   if node != 'failed' and os.path.isdir(orgDir):
      for f in glob.glob(orgDir+'/'+theDate+'*'):
         subDir = os.path.basename(os.path.normpath(f))
         shutil.copytree(f, tmpMsgDir+node+'/'+subDir)
 
 
# find the failed msgs in tmp dir, and copy them to failed dir
if os.path.isdir(failedDir):
   shutil.rmtree(failedDir)
os.mkdir(failedDir)
 
for root, dirs, files in os.walk(tmpMsgDir):
    for f in files:
      r = re.search('_(\d{3,})_', f)
      if r.group(1) in failedIdList:        # found msg
         rootPath = os.path.normpath(root)
         destPath = failedDir+rootPath[rootPath.rfind('/')+1:]
         os.mkdir(destPath)
         shutil.copy(os.path.join(root, f), destPath)
         
 
