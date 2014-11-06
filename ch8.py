#!/usr/bin/python
#Challenge 8

import pyrax
import sys
import os
import string



def usage():
	sys.exit("USAGE : ./ch3.py index_file_path container")
	
#ARG parsing
if len(sys.argv[1:]) == 2 :
	index_file_path, container_name = sys.argv[1:]
else:
	usage()

#Validations
if not os.access(index_file_path, os.F_OK):
	sys.exit("Path non existent. Please verify the index file path : " + index_file)

file_name=string.rsplit(index_file_path,'/',1)[-1]

	
##Auth	
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('SYD')
pyrax.set_credentials('denzelfernando', 'blah')

#cloud file handler
cf = pyrax.cloudfiles

#create the container (will create if does not exist
container = cf.create_container(container_name)

#Make CDN
container.make_public(ttl=900)

#Set meta data (set the uploaded file name as the index)
#X-Container-Meta-Web-Index
container.set_metadata({'Web-Index' : file_name},clear = False, prefix = None)

## Upload the index file
chksum = pyrax.utils.get_checksum(index_file_path)
#print chksum
#induce corrupt chksum for testing purposes
#chksum='123ee'
try:
	obj = cf.upload_file(container_name, index_file_path, etag=chksum)
except:
	sys.exit("File Upload Failure")

print "Index Was set to: ", file_name
print "Access URL: ", container.cdn_uri
