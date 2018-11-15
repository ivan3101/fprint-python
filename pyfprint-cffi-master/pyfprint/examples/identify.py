#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfprint

pyfprint.fp_init()
devs = pyfprint.discover_devices()
dev = devs[0]
dev.open()
fps = []

for i in range(2):
	print("enroll #%d, finger please" % i)
	fp, img = dev.enroll_finger()
	print("got", fp, img)
	fps.append(fp)

while True:
	print("finger to identify, please")
	i, fp, img, r = dev.identify_finger(fps)
	print (i, fp, img, r)


dev.close()
pyfprint.fp_exit()
