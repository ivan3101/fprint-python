#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfprint
import os.path
DIR = "/tmp/fps"

pyfprint.fp_init()
devs = pyfprint.discover_devices()
dev = devs[0]
dev.open()

names = []
fps = []

for name in os.listdir(DIR):
	fps.append(pyfprint.Fprint(open(DIR + "/" + name, 'br').read()))
	names.append(name)

print ("ready to match fingers!")

while True:
	
	fp, img = dev.enroll_finger()
	i = pyfprint.identify(fp, fps)

	if i is None:
		print ("no match found")

	else:
		print ("identified " + names[i] + "!")

dev.close()
pyfprint.fp_exit()
