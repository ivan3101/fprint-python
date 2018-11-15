# -*- coding: utf-8 -*-
"""CFFI bindings for libfprint"""

__all__ = [
    "fp_init",
    "fp_exit",
    "Driver",
    "Device",
    "discover_devices",
    "DiscoveredDevices",
    "Fprint",
    "Image",
    "identify",

    "ENROLL_COMPLETE",
    "ENROLL_FAIL",
    "ENROLL_PASS",
    "ENROLL_RETRY",
    "ENROLL_RETRY_TOO_SHORT",
    "ENROLL_RETRY_CENTER_FINGER",
    "ENROLL_RETRY_REMOVE_FINGER",
    "VERIFY_NO_MATCH",
    "VERIFY_MATCH",
    "VERIFY_RETRY",
    "VERIFY_RETRY_TOO_SHORT",
    "VERIFY_RETRY_CENTER_FINGER",
    "VERIFY_RETRY_REMOVE_FINGER",
]

from .pyfprint import *
