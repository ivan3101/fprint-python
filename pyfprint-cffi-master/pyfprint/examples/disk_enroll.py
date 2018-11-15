#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfprint
import os.path
DIR = "/tmp/fps"

pyfprint.fp_init()
devs = pyfprint.discover_devices()
dev = devs[0]
dev.open()

print("enroll finger, please:")
fp, img = dev.enroll_finger()

print("name this fingerprint, please:")
name = input()

b = fp.data()

os.makedirs(DIR, exist_ok=True)

with open(DIR + "/" + name, "wb") as file:
	file.write(bytes(b))

dev.close()
pyfprint.fp_exit()
