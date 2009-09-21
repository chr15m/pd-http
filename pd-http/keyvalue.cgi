#!/usr/bin/python

# Small cgi-wrapper for memcache key-value pairs of Pure Data lists
# Copyright 2009, Chris McCormick <chris@mccormick.cx>
# GPLv3 License

import cgitb
cgitb.enable(format="text")

from os import environ
from urllib import unquote_plus

import memcache

m = memcache.Client(['127.0.0.1:11211'])
prefix = "keyvalue.cgi_"

print "Content-type: text/plain"
print

if environ.has_key("QUERY_STRING"):
	parts = unquote_plus(environ['QUERY_STRING']).split(" ")
	if len(parts) == 1 and parts[0]:
		# get a key
		print parts[0] + " " + (m.get(prefix + parts[0]) or "") + ";"
	elif len(parts) >= 2:
		# set a key
		m.set(prefix + parts[0], " ".join(parts[1:]))
		print "keyvalue set %s;" % " ".join(parts)
	else:
		print "keyvalue no-key;"
else:
	print "keyvalue no-request;"

