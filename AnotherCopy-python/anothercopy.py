#!/usr/bin/env python

# python anothercopy.py
# python anothercopy.py example_exec.xml
# python anothercopy.py -c ./ -d ../another-dir
# python anothercopy.py -l filelist.txt -d ../another-dir
# python anothercopy.py -l filelist.txt --ftp ftp.test.com


import os, zlib, zipfile, ftplib, shutil
import xml.dom.minidom
from optparse import OptionParser
from time import strftime

class anothercopy:
	"will copy, zip,and FTP file backups. It can be commanded directly or through a batch file."
	archivePath =""
	archiveName = ""
	curArchiveName = ""
	curZip = None
	curZipInc = 0
	ignoreSVN = True
	exclusionList = ("jpg","ppt","gif","mov","avi","mp3","swf")
	archiveList = []
	cmdOptions = None
	cmdArgs = None
	curSpaces = "  "
	testMode = False
	reportLevel = 2
	reportSampleInc = 0
	reportSampleFreq = 8
	props={'ignoresvndir':1,'noarchive':0,'srcPath':'','destPath':'','archiveFile':'',
			 'reportLevel':2,'reportSampleInc':0,'reportSampleFreq':8}
	tags={}
	basePath = ""
	reportInc = 0

	def __init__(self):
		self.data = []
		self.processors = []
		self.returnStr = ""
		self.ignoreSVN = True
		self.tags['DATE'] = strftime("%m%d%y")
		self.tags['TIME'] = strftime("%H%M")

	# Get the current revision for output header
	def getRev(self):
		revStr= "$Rev: 316 $"
		tempArray = revStr.split()
		return "1.1."+str(tempArray[1])

	# Replace {tag} items in specified string
	def replaceTags(self,outStr):
		for key, value in self.tags.iteritems():
			outStr = outStr.replace("{" + key + "}", value);
		return outStr

	# Test the passed file to see if the three letter file extension is in the exclusion list
	def testExtension(self,inFile):
		return inFile[-3:].lower() in self.exclusionList

	# For status output, all messages are passed here and then based on user preferences,
	# different levels of output are used.
	def report(self,inStr,inInc=0):
		self.reportInc += inInc
		# 0 = Report all
		if self.reportLevel<1:
			print inStr
		# 1 = Report most
		elif self.reportLevel<2:
			print inStr
		# 2 = Report sample
		elif self.reportLevel<3:
			if self.reportSampleInc % int(self.props['reportSampleFreq']) == 0:
				print "\n#"+str(self.reportInc)+":sample: " + inStr
			else:
				print ".",
			self.reportSampleInc += 1
		# 3 = Report status marker
		elif self.reportLevel<4:
			print ".",
		# 4 = Report most
		elif self.reportLevel<5:
			print inStr

	def copyFile(self, inPath,destPath):
		(srcPath,fileName) = os.path.split(inPath)
		outPath = os.path.join(destPath,srcPath)
		bpLen = len(self.basePath)
		if bpLen>0:
			# If paths are the same, remove base path
			if os.path.abspath(srcPath[0:bpLen])==os.path.abspath(self.basePath):
				outPath = os.path.join(destPath,srcPath[bpLen:])

		src = os.path.join(srcPath,fileName)
		dest = os.path.join(destPath,srcPath,fileName)
		self.report("Copying file:" + src+ " to: "+dest)
		try:
			if not os.path.isdir(outPath):
				os.makedirs(outPath)
			shutil.copyfile(src,os.path.join(outPath,fileName))
		except (IOError, os.error), why:
			print "Can't copy %s to %s: %s" % (src, dest, str(why))

	def copyFiles(self,srcDir,destDir,recurse=True,inLog=False):
		self.returnStr = ""
		self.ignoreSVN = True
		self.basePath = srcDir
		i = 0
		#walkLog=open(walkDir+'codescan_log.txt', 'w')
		if recurse:
			for curPath,dirs,files in os.walk(srcDir):
				for inName in files:
					#if inName[-3:] == "php":
					#	processFile(inName,curPath,walkLog)
					#print "Copy file:"+curPath+"/"+inName+" to "+destDir+curPath+"/"+inName
					self.copyFile(curPath+"/"+inName,destDir)
					i += 1
				if self.ignoreSVN:
					if '.svn' in dirs:
						dirs.remove('.svn')  # ignore the SVN metadata directories
			#walkLog.close()
		if i>1:
			print "\nCopied "+str(i)+" files"
		return True

	def copyList(self,inListPath,destPath):
		f=open(inListPath, 'r')
		fileList = f.read()
		fileArray = fileList.split("\n")

		for curFile in fileArray:
			if(len(curFile)>0):
				self.copyFile(curFile, destPath)

	# Create XML-based manifest of files to backup with CRC32 checksums
	def createManifest(self,compareManifestName=None):
		# If a manifest name was passed, use it for comparison
		if compareManifestName:
			pass
	def ftpSendFile(self,inFtpRef,inFileName):
		myFile = open(inFileName,'rb')
		(fName,fExt) = os.path.splitext(inFileName)
		try:
			inFtpRef.storbinary("STOR " + inFileName,myFile)
		except Exception:
			print "Upload failed!"
		myFile.close()
		return

	def ftpConnect(self,inURL,inUsername,inPassword):
		#   "anonymous" "Anonymous" "anonymous" "Anonymous":
		ftph = ftplib.FTP(inURL)
		ftph.login(inUsername,inPassword)
		print ftph.getwelcome()
		ftph.cwd("bu")
		curFtpPath = ftph.pwd()
		print "Current path:"+curFtpPath
		return ftph

	# Get the manifest on the remote directory
	def ftpGetManifest(self):
		pass
	def ftpArchiveList(self,inList,ftpURL,username,password):
				connectPtr = self.ftpConnect(ftpURL,username,password)
				#for arc in inList:
				(head, tail) = os.path.split(inList)
				print "Sending "+tail+"...\n"
				self.ftpSendFile(connectPtr,tail)
				print "Completed ftp."
	def doExec(self,cmdStr):
		rows = []
		for row in os.popen(cmdStr).readlines():     # run find command
			rows.append(row)
		return rows
	def attr(self,attrList,attrName,default=''):
		if attrList.has_key(attrName):
			return attrList[attrName]
		else:
			return default

# -------------  TASKS  -------------
# These tasks can be included in a batch file and perform specific operations

	def taskExec(self,inAttr):
		# TODO: If reporterror, tack on the &2>1 stuff
		if inAttr:
			cmdStr = ''
			if inAttr.has_key('value'):
				cmdStr = inAttr['value'].value
			if inAttr.has_key('executable'):
				cmdStr = inAttr['executable'].value
			returnArray = self.doExec(cmdStr)
			print ''.join(returnArray)

	def taskSVN(self,inAttr):
		# TODO: Process return info as XML and report specific items.
		cmdStr = "svn status -u"
		returnArray = self.doExec(cmdStr)
		print ''.join(returnArray)

	# Output a crontab string from human-readable batch input
	def taskCrontab(self,inAttr):
		crCmd = self.attr(inAttr, 'cmd','/etc/myprog')
		crOutfile = self.attr(inAttr, 'log','')
		if len(crOutfile)>0:
			crOutfile = " > "+crOutfile
		crMonth = self.attr(inAttr, 'month','*')
		crDay = self.attr(inAttr, 'day','*')
		crHour = self.attr(inAttr, 'hour','*')
		crMin = self.attr(inAttr, 'min','*')
		dow = self.attr(inAttr, 'dayofweek').lower()
		dowNum = '*'
		if(dow=='sunday' or dow=='sun'):
			dowNum='0'
		elif(dow=='monday' or dow=='mon'):
			dowNum='1'
		elif(dow=='tuesday' or dow=='tue'):
			dowNum='2'
		elif(dow=='wednesday' or dow=='wed'):
			dowNum='3'
		elif(dow=='thursday' or dow=='thu'):
			dowNum='4'
		elif(dow=='friday' or dow=='fri'):
			dowNum='5'
		elif(dow=='saturday' or dow=='sat'):
			dowNum='6'
		print "crontab string: "+crMin+" "+crHour+" "+crDay+" "+crMonth+" "+dowNum+" "+crCmd+" "+crOutfile
	def taskEmail(self,inAttr):
		print "Sending email."
		# TODO: Check OS type property
		emailMethod = self.attr(inAttr,'method','sendmail')
		emailFrom = self.attr(inAttr,'from','source@email.com')
		emailTo = self.attr(inAttr,'to','destination@email.com')
		emailSubject = self.attr(inAttr,'subject','Copy process')
		emailBody = self.attr(inAttr,'body',"The SC Body\nSome more text.\n")

		if emailMethod=='sendmail':
			cmdSendMail = "/usr/sbin/sendmail"
			p = os.popen("%s -t -v " % cmdSendMail, "w")
			p.write("To: "+emailTo+"\n")
			p.write("From: "+emailFrom+"\n")
			p.write("Subject: "+emailSubject+"\n")
			p.write("\n")
			p.write(emailBody)
			sts = p.close()
			if sts != 0:
				print "Sendmail exit status", sts
		else:
			import sys, smtplib
			server = smtplib.SMTP('localhost')
			server.sendmail(emailFrom, emailTo, emailBody)
			server.quit()

	# Output to screen or files information supplied in <log> tags
	def taskLog(self,inAttr):
		msg = self.attr(inAttr, 'msg')
		logFile = self.attr(inAttr, 'file')
		toFile = self.attr(inAttr, 'tofile')
		if(toFile=='0'):
			toFile = False
		toScreen = self.attr(inAttr, 'toscreen')
		if(toScreen=='0'):
			toScreen = False
		if(len(logFile)==0):
			logFile = "sclog.log"
		logStr = strftime("%y%m%d-%H:%M") + "\t" + msg+"\n"
		if(toFile):
			try:
				f=open(logFile, 'a')
				f.write(logStr)
				f.close()
			except (IOError, os.error), why:
				print "Can't write %s to %s: %s" % (logStr,logFile,str(why))
		if(toScreen):
			print logStr

	def taskFTP(self,fileList,ftpURL,username,password):
		print "\nStarting ftp to "+ftpURL+"..."
		passList = (fileList)
		self.ftpArchiveList(passList,ftpURL,username,password)
	def taskZip(self,inSrc,inDest,inFile,recurse=True,inLog=False):
		if self.props['noarchive']:
			print "No archiving, just transfer file."
			self.archiveList.append(self.props['noarchive'])
		else:
			if inFile:
				self.curArchiveName = os.path.join(inDest,inFile+"_"+str(self.curZipInc)+".zip")
				self.curZip = zipfile.ZipFile(self.curArchiveName,'w') # ,zipfile.ZIP_DEFLATED
				self.archiveList.append(self.curArchiveName)
			if self.testMode:
				print "zipping:"+inSrc+" recurse:"+str(recurse)+" to:"+self.curArchiveName
			self.processDir(inSrc,recurse,inLog)
			if self.props['archiveFile']:
				self.curZip.close()
	# Perform MySQL tasks
	def taskMySQL(self):
		action = self.props['action']
		# Dump the MySQL database
		if action=='dump':
			print "Dumping:"+self.props['db_name']
			dumpFile = os.path.join(self.props['destPath'],self.props['dest_file'])
			pathMySQL = os.path.join(self.props['path_mysql'],'mysqldump')
			dumpCmd = os.path.normpath(pathMySQL)+" -u "+self.props['db_username']+" -p"+self.props['db_password']+" --databases "+self.props['db_name']+" > "+dumpFile
			os.system(dumpCmd)
		# Execute MySQL code
		elif action=='query':
			print 'Querying: '+self.props['msg']
			rows = []
			queryCmd = "mysql -u "+self.props['db_username']+" -p"+self.props['db_password']+' --execute="'+self.props['query']+'" '+self.props['db_name']
			for row in os.popen(queryCmd).readlines():     # run find command
				rows.append(row)
			# print rows
		# Import a directory full of .sql files and add permissions to specified user
		elif action=='import':
			srcPath = self.props['srcPath'];
			print 'MySQL import from '+srcPath+'...'
			for filename in os.listdir(os.path.abspath(srcPath)):
				path = os.path.join(srcPath, filename)
				if not os.path.isfile(path):
					continue
				if filename[-3:] == "sql":
						os.chdir(os.path.abspath(srcPath))
						importCmd = "mysql -u "+self.props['db_username']+" -p"+self.props['db_password']+" < "+filename
						os.system(importCmd)
						if filename[0:2] == "sp" or filename[0:2] == "fn":
							spName = filename[:-4]
							grantSQL = "GRANT EXECUTE ON PROCEDURE "+self.props['db_name']+"."+spName+" TO '"+self.props['sp_user']+"'@'localhost';"
							grantCmd = "mysql -u "+self.props['db_username']+" -p"+self.props['db_password']+' --execute="'+grantSQL+'" '
							os.system(grantCmd)
							grantSQL = "GRANT EXECUTE ON PROCEDURE "+self.props['db_name']+"."+spName+" TO '"+self.props['sp_user']+"'@'%';"
							grantCmd = "mysql -u "+self.props['db_username']+" -p"+self.props['db_password']+' --execute="'+grantSQL+'" '
							os.system(grantCmd)
						self.report("Import: "+importCmd)

# -----------------------------  End Tasks -----------------------------

	def processFile(self,inDir,inFile):
		if self.testMode:
			pass
			#print "Processing file:"+inDir+inFile
		if self.props['archiveFile']:
			if self.testExtension(inFile):
				zipType = zipfile.ZIP_STORED
			else:
				zipType = zipfile.ZIP_DEFLATED
			#self.curZip = zipfile.ZipFile(archivePath+archiveFile+"_"+str(self.curZipInc)+".zip",'w')
			archiveSize = os.stat(self.curArchiveName).st_size
			oneMeg = 1000000
			oneGig = 1000 * oneMeg
			fileLimit = 600 * oneMeg
			if archiveSize - fileLimit > 1:
				self.curZip.close()
				self.curZipInc += 1
				self.curArchiveName = os.path.join(self.props['destPath'],self.props['archiveFile']+"_"+str(self.curZipInc)+".zip")
				self.curZip = zipfile.ZipFile(self.curArchiveName,'w',zipfile.ZIP_DEFLATED)
				self.archiveList.append(self.curArchiveName)
				print archiveSize,
		if self.testMode:
			print "Zipping file:"+os.path.join(inDir,inFile)
		else:
			try:
				inDir = inDir.encode('ascii','ignore')
				inFile = inFile.encode('ascii','ignore')
				self.curZip.write(os.path.join(inDir,inFile),None,zipType)
			except (IOError, os.error), why:
				print "Can't copy %s to %s: %s" % (os.path.join(inDir,inFile), '', str(why))
		return zlib.crc32(inFile)

	def processDir(self,inDir,recurse=False,inLog=False):
		self.returnStr = ""
		inDir = os.path.abspath(inDir)
		i = 0
		if recurse:
			if self.testMode:
				print "Beginning recurse of:"+inDir
			for curPath,dirs,files in os.walk(inDir):
				for inName in files:
					result = self.processFile(curPath,inName)
					i += 1
					if result:
						if(inLog):
							inLog.write(result)
							inLog.flush()
						else:
							self.returnStr += "" #result
					self.report(os.path.join(curPath,inName),1)
				if self.ignoreSVN:
					if '.svn' in dirs:
						dirs.remove('.svn')  # don't visit CVS directories
			#walkLog.close()
		return True

	def startCopy(self,inDir,recurse,inLog=False):
		print "Starting copy..."
		if self.cmdOptions.sourcelist:
			self.copyList(self.cmdOptions.sourcelist, self.cmdOptions.destination)
		elif(self.cmdOptions.copydir):
			self.copyFiles(self.cmdOptions.copydir, self.cmdOptions.destination)
		else:
			if self.cmdOptions.noarchive:
				print "No archiving, just transfer file:"+self.cmdOptions.noarchive
				self.archiveList.append(self.cmdOptions.noarchive)
			else:
				if archiveFile:
					self.curArchiveName = archivePath+archiveFile+"_"+str(self.curZipInc)+".zip"
					self.curZip = zipfile.ZipFile(self.curArchiveName,'w') # ,zipfile.ZIP_DEFLATED
					self.archiveList.append(self.curArchiveName)
				self.processDir(inDir,recurse,inLog)
				if archiveFile:
					self.curZip.close()
			if self.cmdOptions.ftpdest:
				print "\nStarting ftp to "+self.cmdOptions.ftpdest+"..."
				self.ftpArchiveList(self.cmdOptions.ftpdest,"root","password")
		print "Copy complete."

	# Execute each command in the XML batch script
	def executeScript(self,xmlDOM):
		execStartTime = strftime("%H:%M")
		targetDefault = xmlDOM.getElementsByTagName("project").item(0).getAttribute('default')
		targets = xmlDOM.getElementsByTagName("project").item(0).childNodes
		for target in targets:
			curType=target.localName
			if curType:
				# If item has enabled attribute set to zero, move to the next one
				if target.getAttribute('enabled') != '0':
					# Create a dictionary of the current XML attributes
					attrList = {}
					if target.attributes:
						attrList = {}
						for attr in target.attributes.keys():
							attrList[attr]=target.attributes[attr].value
					# Set common attributes
					if target.getAttribute('src'):
						self.props['srcPath'] = self.replaceTags(str(target.getAttribute('src')))
					if target.getAttribute('dest'):
						self.props['destPath'] = self.replaceTags(str(target.getAttribute('dest')))

					if curType == 'copy':
						if self.testMode:
							print self.curSpaces+"Copy src:"+target.getAttribute('src')+" dest:"+target.getAttribute('dest')
						else:
							self.copyFiles(target.getAttribute('src'), target.getAttribute('dest'))
					elif curType == 'ftp':
						if self.testMode:
							print self.curSpaces+"ftp src:"+target.getAttribute('src')+" dest:"+target.getAttribute('dest')
						self.taskFTP(self.props['srcPath'],target.getAttribute('dest'),target.getAttribute('username'),target.getAttribute('password'))
					elif curType == 'zip':
						self.props['archiveFile'] = self.replaceTags(str(target.getAttribute('archiveFile')))
						if self.testMode:
							print self.curSpaces+"zip src:"+target.getAttribute('src')+" dest:"+target.getAttribute('dest')+" archiveFile:"+target.getAttribute('archiveFile')
						self.taskZip(self.props['srcPath'],self.props['destPath'],self.props['archiveFile'])
					elif curType == 'pause':
						if self.testMode:
							print self.curSpaces+"pause"
						raw_input("Press the ENTER key to continue...")
					elif curType == 'exec':
						if self.testMode:
							print self.curSpaces+"exec"
						self.taskExec(target.attributes)
					elif curType == 'crontab':
						if self.testMode:
							print self.curSpaces+"crontab"
						self.taskCrontab(attrList)
					elif curType == 'mysql':
						self.props['action'] = str(target.getAttribute('action'))
						if target.getAttribute('db_name'):
							self.props['db_name'] = str(target.getAttribute('db_name'))
						if target.getAttribute('db_host'):
							self.props['db_host'] = str(target.getAttribute('db_host'))
						self.props['db_username'] = str(target.getAttribute('username'))
						self.props['db_password'] = str(target.getAttribute('password'))
						self.props['sp_user'] = str(target.getAttribute('sp_user'))
						self.props['dest_file'] = self.replaceTags(str(target.getAttribute('dest_file')))
						self.props['query'] = str(target.getAttribute('query'))
						self.props['msg'] = str(target.getAttribute('msg'))
						if self.testMode:
							print self.curSpaces+"mysql"
						else:
							self.taskMySQL()
					elif curType == 'log':
						if self.testMode:
							print self.curSpaces+"log"
						else:
							self.taskLog(attrList)
					elif curType == 'email':
						if self.testMode:
							print self.curSpaces+"email"
						else:
							self.taskEmail(attrList)
					elif curType == 'property':
						if target.getAttribute('name'):
							#print self.curSpaces+"set property '" + target.getAttribute('name') + "' to " + target.getAttribute('value')
							self.props[target.getAttribute('name')] = target.getAttribute('value')
					elif curType == 'tag':
						if target.getAttribute('name'):
							print self.curSpaces+"set tag '" + target.getAttribute('name') + "' to " + target.getAttribute('value')
							self.tags[target.getAttribute('name')] = target.getAttribute('value')

		print "Script execute complete. ST:"+execStartTime+" ET:"+strftime("%H:%M")

	# Parse the XML batch file
	def loadScript(self,fName):
		f = open(fName,'r')
		xmlStr = f.read()
		f.close()
		return xml.dom.minidom.parseString(xmlStr)

	# Process the command line arguments
	def processArgs(self,options,args):
		if self.props['ignoresvndir']:
			print "Ignoring SVN folders."
		if options.testmode:
			self.testMode = True
			print "*** Test Mode is on ***"

	def controller(self,options,args):
		print "--- #"+AnotherCopy.getRev()+" --- "
		AnotherCopy.ignoreSVN = True
		AnotherCopy.cmdOptions = options
		AnotherCopy.cmdArgs = args
		autorunFName = "sc_autorun.xml"
		self.processArgs(options,args)
		if len(args)==0:
			if os.path.isfile(autorunFName):
				print "Executing autorun..."
				tempDOM = self.loadScript(autorunFName)
				self.executeScript(tempDOM)
				return
			else:
				usage = "  usage: python smartcopy.py [options] arg1 arg2"
				print usage
				return

		srcDir = "c:/TestCompress/"
		archivePath = "c:/"
		archiveFile = "Test_BU022108"
		if len(args)==1:
			if args[0][-3:].lower()=="xml":
				tempDOM = self.loadScript(args[0])
				self.executeScript(tempDOM)
				return
		if args[0]:
			srcDir = args[0]
			self.props['srcPath'] = args[0]
		if args[1]:
			archivePath = args[1]
			self.props['destPath'] = args[1]
		if args[2]:
			archiveFile = args[2]
			self.props['archiveFile'] = args[2]
		insSmartCopy.startCopy(srcDir,True,False)

if __name__ == '__main__':
	AnotherCopy = anothercopy()
	usage = "usage: %prog [options] arg1 arg2"
	parser = OptionParser(usage=usage)
	parser.add_option("-o", "--outfile", dest="outfile",help="output data to OUTFILE", metavar="OUTFILE")
	parser.add_option("-f", "--ftp", dest="ftpdest",help="ftp archive files to FTPDEST", metavar="FTPDEST")
	parser.add_option("-n", "--noarchive", dest="noarchive",help="no file archiving", metavar="ARCHIVENONE")
	parser.add_option("-l", "--list", dest="copylist",help="INI format file of files/dirs to copy", metavar="FILE")
	parser.add_option("-d", "--destination", dest="destination", help="Destination path for copy", metavar="DEST")
	parser.add_option("-s", "--sourcelist", dest="sourcelist", help="Text file list of files to copy", metavar="SOURCELIST")
	parser.add_option("-c", "--copydir", dest="copydir", help="Source directory of files to copy", metavar="COPYDIR")
	parser.add_option("-t", "--test",action="store_true", dest="testmode", default=False,help="Don't actually copy or create files")
	(options, args) = parser.parse_args()
	AnotherCopy.controller(options,args)

