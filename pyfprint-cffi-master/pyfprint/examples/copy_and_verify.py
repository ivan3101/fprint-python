#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pyfprint

pyfprint.fp_init()
devs = pyfprint.discover_devices()
dev = devs[0]
dev.open()
print("enroll, finger please")
fp, _ = dev.enroll_finger()

print("getting data")
b = fp.data()

print("got data buffer:")
print(b)

print("fp copied")
fp2 = pyfprint.Fprint(b)

print("verify original, finger please")
print(dev.verify_finger(fp))

print("verifying copy, finger please")
print(dev.verify_finger(fp2))

dev.close()
pyfprint.fp_exit()
