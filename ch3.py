#!/usr/bin/python
#Challenge 3

import pyrax
import sys
import os


def usage():
	sys.exit("USAGE : ./ch3.py directory container")
	
#ARG parsing
if len(sys.argv[1:]) == 2 :
	directory, container = sys.argv[1:]
else:
	usage()

#Validations
if not os.access(directory, os.F_OK):
	sys.exit("Path non existent. Please verify the directory path : " + directory)
		
##Auth	
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('SYD')
pyrax.set_credentials('denzelfernando', 'blah')

#cloud file handler
cf = pyrax.cloudfiles

#This will create the container if non existent	
#key, bytes = cf.upload_folder(directory, container=""+container+"")
key, bytes = cf.upload_folder(directory, container=container)
print "Upload Key: {0} , Total Bytes: {1}".format(key, bytes)