#!/usr/bin/python

# Small cgi-wrapper for memcache atomic increment decrement for Pure Data http calls
# Copyright 2009, Chris McCormick <chris@mccormick.cx>
# GPLv3 License

import cgitb
cgitb.enable(format="text")

from os import environ
from urllib import unquote_plus

import memcache

m = memcache.Client(['127.0.0.1:11211'])
prefix = "incrdecr.cgi_"

print "Content-type: text/plain"
print

if environ.has_key("QUERY_STRING"):
	parts = unquote_plus(environ['QUERY_STRING']).split(" ")
	if len(parts) == 1 and parts[0]:
		# get a key
		try:
			print "incrdecr " + parts[0] + " " + (str(int(m.get(prefix + parts[0]))) or "") + ";"
		except ValueError:
			print "incrdecr not-an-int;"
		except TypeError:
			print "incrdecr no-such-key;"
	elif len(parts) == 2:
		# add it if we don't have it yet
		m.add(prefix + parts[0], 0)
		# set a key, incr a key, decr a key
		if parts[1] == "incr":
			print "incrdecr " + parts[0] + " " + str(m.incr(prefix + parts[0])) + ";"
		elif parts[1] == "decr":
			print "incrdecr " + parts[0] + " " + str(m.decr(prefix + parts[0])) + ";"
		else:
			try:
				m.set(prefix + parts[0], int(parts[1]))
				print "incrdecr " + parts[0] + " " + parts[1] + ";"
			except ValueError:
				print "incrdecr bad-argument;"
	elif len(parts) > 2:
		print "incrdecr too-many-args;"
	else:
		print "incrdecr no-key;"
else:
	print "incrdecr no-request;"
