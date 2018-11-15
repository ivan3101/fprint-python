# encoding=utf-8
#
# Copyright (C) 2008 by Lukas Sandström                                 #
# luksan@gmail.com                                                      #
# Copyright (C) 2014 by Francisco Demartino                             #
# demartino.francisco@gmail.com                                         #
#
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 2 of the License, or     #
# (at your option) any later version.                                   #
#
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, write to the                         #
# Free Software Foundation, Inc.,                                       #
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
#

from .pyfprint_cffi import C, ffi

# TODO:
#	exceptions, especially for RETRY_* errors
#	constants for fingers
#	tests
#	documentation
#	for x in y => map ?
#	Image(img) for devices which don't support imaging? Is img NULL?

ENROLL_COMPLETE=C.FP_ENROLL_COMPLETE
ENROLL_FAIL=C.FP_ENROLL_FAIL
ENROLL_PASS=C.FP_ENROLL_PASS
ENROLL_RETRY=C.FP_ENROLL_RETRY
ENROLL_RETRY_TOO_SHORT=C.FP_ENROLL_RETRY_TOO_SHORT
ENROLL_RETRY_CENTER_FINGER=C.FP_ENROLL_RETRY_CENTER_FINGER
ENROLL_RETRY_REMOVE_FINGER=C.FP_ENROLL_RETRY_REMOVE_FINGER
VERIFY_NO_MATCH=C.FP_VERIFY_NO_MATCH
VERIFY_MATCH=C.FP_VERIFY_MATCH
VERIFY_RETRY=C.FP_VERIFY_RETRY
VERIFY_RETRY_TOO_SHORT=C.FP_VERIFY_RETRY_TOO_SHORT
VERIFY_RETRY_CENTER_FINGER=C.FP_VERIFY_RETRY_CENTER_FINGER
VERIFY_RETRY_REMOVE_FINGER=C.FP_VERIFY_RETRY_REMOVE_FINGER

_init_ok = False

class FprintException(Exception):
    pass
class FprintIOException(FprintException, IOError):
    pass

def _dbg(*arg):
    # print ("pyfprint-cffi: " + str(arg))
    pass


def fp_init():
    """Call this before doing anything else."""
    _init_ok = (C.fp_init() == 0)
    if not _init_ok:
        raise FprintException("fprint initialization failed.")


def fp_exit():
    """pyfprint can't be used after this is called."""
    C.fp_exit()
    _init_ok = False

def debug(level):
    C.fp_set_debug(level)

class Device:

    """Provides access to a fingerprint reading device. Don't construct this
    directly, use discover_devices() instead."""

    def __init__(self, dev_ptr=None, dscv_ptr=None, DscvList=None):
        """For internal use only."""
        self.dev = dev_ptr
        self.dscv = dscv_ptr
        self.DscvList = DscvList
        if dscv_ptr and DscvList == None:
            raise FprintException("Programming error? Device contructed with dscv without DscvList.")

    def close(self):
        """Closes the device. No more methods, except open(), may be called after this."""
        if self.dev:
            C.fp_dev_close(self.dev)
        self.dev = None

    def open(self):
        """Connects to the device."""
        if self.dev:
            raise FprintIOException("Device already open")
        self.dev = C.fp_dev_open(self.dscv)
        if not self.dev:
            raise FprintIOException("Device open failed")

    def driver(self):
        """
        Return a Driver instance.

        open() is not required before this method.
        """
        if self.dev:
            return Driver(C.fp_dev_get_driver(self.dev))
        if self.dscv:
            return Driver(C.fp_dscv_dev_get_driver(self.dscv))

    def devtype(self):
        """
        Return an integer representing the type of device.

        open() is not required before this method.
        """
        if self.dev:
            return C.fp_dev_get_devtype(self.dev)
        if self.dscv:
            return C.fp_dscv_dev_get_devtype(self.dscv)

    def nr_enroll_stages(self):
        """
        Return how many times enroll_finger needs to be called
        before the finger is successfully enrolled.
        """
        if self.dev:
            return C.fp_dev_get_nr_enroll_stages(self.dev)
        raise FprintIOError("device not open")

    def is_compatible(self, fprint):
        """
        Checks whether the passed fprint is compatible with the device.

        open() is not required before this method.
        """
        if self.dev:
            if fprint.data_ptr:
                return C.fp_dev_supports_print_data(self.dev, fprint.data_ptr) == 1
            if fprint.dscv_ptr:
                return C.fp_dev_supports_dscv_print(self.dev, fprint.dscv_ptr) == 1
            raise FprintException("No fingerprint found")
        if self.dscv:
            if fprint.data_ptr:
                return C.fp_dscv_dev_supports_print_data(self.dscv, fprint.data_ptr) == 1
            if fprint.dscv_ptr:
                return C.fp_dscv_dev_supports_dscv_print(self.dscv, fprint.dscv_ptr) == 1
            raise FprintException("No fingerprint found")
        raise FprintIOException("No device found")

    def supports_imaging(self):
        """If true, the device can return an image of the finger."""
        if self.dev:
            return C.fp_dev_supports_imaging(self.dev) == 1
        raise FprintIOException("Device not open")

    def img_width(self):
        """Return the width of the images scanned by the device, in pixels."""
        if self.dev:
            return C.fp_dev_get_img_width(self.dev)
        raise FprintIOException("Device not open")

    def img_height(self):
        """Return the height of the images scanned by the device, in pixels."""
        if self.dev:
            return C.fp_dev_get_img_height(self.dev)
        raise FprintIOException("Device not open")

    def capture_image(self, wait_for_finger):
        """
        Captures an image from the device. Return None if imaging isn't supported.
        wait_for_finger controls if the device should wait for a finger to be placed
        on the sensor before image capture.
        """
        if not self.dev:
            raise FprintIOException("Device not open")

        if not self.supports_imaging():
            return None

        unconditional = 1
        if wait_for_finger == True:
            unconditional = 0

        img = ffi.new("struct fp_img **")
        r = C.fp_dev_img_capture(self.dev, unconditional, img)
        img = Image(img[0])
        if r != 0:
            raise FprintException("image_capture failed. error: %i" % r)
        return img

    def enroll_finger(self, reopen_on_retry=False):
        """Enroll a finger

        Returns
        -------
        fprint : Fprint
            the enrolled fingerprint
        img : Image
            the enrolled image
        """
        if not self.dev:
            raise FprintIOException("Device not open")

        while True:
            _dbg("enrolling finger...")
            fprint = ffi.new("struct fp_print_data **")
            img = ffi.new("struct fp_img **")

            r = C.fp_enroll_finger_img(self.dev, fprint, img)

            if r < 0:
                raise FprintException("Internal I/O error while enrolling: %i" % r)

            img = Image(img[0])

            if r == C.FP_ENROLL_COMPLETE:
                _dbg("enroll complete")
                return Fprint(data_ptr=fprint[0]), img

            messages = {
                C.FP_ENROLL_FAIL: "FAIL",
                C.FP_ENROLL_PASS: "PASS",
                C.FP_ENROLL_RETRY: "RETRY",
                C.FP_ENROLL_RETRY_TOO_SHORT: "RETRY_SHORT",
                C.FP_ENROLL_RETRY_CENTER_FINGER: "RETRY_CENTER",
                C.FP_ENROLL_RETRY_REMOVE_FINGER: "RETRY_REMOVE",
            }
            _dbg("enroll " + messages[r])

            # Workaround my uru4000 hangs after fp_enroll_finger_img returns RETRY
            if r>=C.FP_ENROLL_RETRY and reopen_on_retry:
                self.close()
                self.open()

        return None, img

    def verify_finger(self, fprint):
        """
        Compare the finger on the device with the supplied Fprint.

        Parameters
        ----------
        fprint : Fprint
            The fingerprint to match

        Returns
        -------
        verified : bool
            true if the finger and the Fprint match
        """
        if not self.dev:
            raise FprintIOException("Device not open")
        while True:
            img = ffi.new("struct fp_img **")
            r = C.fp_verify_finger_img(self.dev, fprint._get_print_data_ptr(), img)
            img = Image(img[0])
            if r < 0:
                raise FprintException("verify error: %i" % r)
            if r == C.FP_VERIFY_NO_MATCH:
                return False, img
            if r == C.FP_VERIFY_MATCH:
                return True, img
            if r == C.FP_VERIFY_RETRY:
                pass
            if r == C.FP_VERIFY_RETRY_TOO_SHORT:
                pass
            if r == C.FP_VERIFY_RETRY_CENTER_FINGER:
                pass
            if r == C.FP_VERIFY_RETRY_REMOVE_FINGER:
                pass
        return False, None

    def supports_identification(self):
        """Return True if the device supports the identify_finger method."""
        if not self.dev:
            raise FprintIOException("Device not open")
        return C.fp_dev_supports_identification(self.dev) == 1

    def identify_finger(self, fprints):
        """
        FIXME: error handling

        Match the finger on the reader against a list of Fprints.

        Return a tuple: (list_offset, Fprint, Image, state) if a match is found,
        (None, None, Image, state) otherwise.

        Image is None if the device doesn't support imaging.
        """

        if not self.dev:
            raise FprintIOException("Device not open")

        for x in fprints:
            if not self.is_compatible(x):
                raise FprintException("Can't verify uncompatible print")

        print_gallery = ffi.new("struct fp_print_data * [%d]" % (len(fprints)+1))

        for i, x in enumerate(fprints):
            print_gallery[i] = x._get_print_data_ptr()

        offset = ffi.new("size_t *")
        img = ffi.new("struct fp_img **")
        r = C.fp_identify_finger_img(self.dev, print_gallery, offset, img)
        img = Image(img[0])
        offset = offset[0]

        if r < 0:
            raise FprintException("Identification error")
        if r == C.FP_VERIFY_NO_MATCH:
            return (None, None, img, r)
        if r == C.FP_VERIFY_MATCH:
            return (offset, fprints[offset], img, r)
        if r == C.FP_VERIFY_RETRY:
            pass
        if r == C.FP_VERIFY_RETRY_TOO_SHORT:
            pass
        if r == C.FP_VERIFY_RETRY_CENTER_FINGER:
            pass
        if r == C.FP_VERIFY_RETRY_REMOVE_FINGER:
            pass

        return (None, None, None, r)

    def load_print_from_disk(self, finger):
        """
        Load a stored fingerprint from the users home directory.

        - finger should be a value from Fingers.

        Return a Fprint.
        """
        if not self.dev:
            raise FprintIOException("Device not open")
        print_ptr= ffi.new("struct fp_print_data **")
        r = C.fp_print_data_load(self.dev, finger, print_ptr)
        if r != 0:
            raise FprintIOException("Could not load print from disk")
        return Fprint(data_ptr=print_ptr[0])

    def delete_stored_finger(self, finger):
        """
        Delete a fingerprint stored in the users home directory

        - finger should be a value from Fingers.
        """
        if not self.dev:
            raise FprintIOException("Device not open")
        r = C.fp_print_data_delete(self.dev, finger)
        if r != 0:
            raise FprintException("Delete failed")

class Minutia:
    """A single point of interest in a fingerprint."""

    def __init__(self, minutia_ptr, img):
        # We need to keep a reference to the image,
        # since the pointer we're referring to might
        # be free'd otherwise
        self.img = img
        self.data = minutia_ptr[0]


class Image:

    """An image returned from the fingerprint reader."""

    def __init__(self, img_ptr, bin=False):
        """Private method."""
        self._img = img_ptr
        self._bin = bin
        self._std = False
        self._minutiae = None

    def __del__(self):
        if self._img:
            C.fp_img_free(self._img)

    def height(self):
        """The height of the image in pixels."""
        return C.fp_img_get_height(self._img)

    def width(self):
        """The width of the image in pixels."""
        return C.fp_img_get_width(self._img)

    def data(self):
        """
        Return a string containing one byte per pixel, representing a grayscale image.
        """
        data=C.fp_img_get_data(self._img)
        return ffi.string(data)[:-1] if data else ""

    def rgb_data(self):
        """
        Return a string containing three bytes per pixel, representing a gray RGB image.
        """
        return C.pyfp_img_get_rgb_data(self._img)

    def save_to_file(self, filename):
        """Save the image as a pgm file."""
        r = C.fp_img_save_to_file(self._img, filename.encode())
        if r != 0:
            raise FprintException("Save failed")

    def standardize(self):
        """Normalize orientation and colors of the image."""
        if self._std:
            return

        C.fp_img_standardize(self._img)

        self._std = True

    def binarize(self):
        """
        Return the image converted to a black/white binary image of the print.
        The returned Image is a copy of the original. The old image remains
        un-binarized.

        This will standardize() the image, if it isn't already so.
        """
        if self._bin:
            return

        self.standardize()

        bimg = C.fp_img_binarize(self._img)

        i = Image(img_ptr=bimg, bin=True)

        i._minutiae = self._minutiae

        return i


    def minutiae(self):
        """
        Return a list of the minutiae found in the image.

        This method will fail on a binarized image.
        """
        if self._minutiae:
            return self._minutiae
        if self._bin:
            raise FprintException("Cannot find minutiae in binarized image")
        if not self._std:
            self.standardize()

        nr = ffi.new("int *")
        min_list = C.fp_img_get_minutiae(self._img, nr)
        nr = nr[0]
        l = []
        for n in range(nr):
            l.append(Minutia(img=self, minutia_ptr=min_list[n]))
        self._minutiae = l
        return l


class Driver:

    """Provides access to some information about a libfprint driver."""

    def __init__(self, swig_drv_ptr):
        """Private."""
        self.drv = swig_drv_ptr

    def __del__(self):
        # FIXME: free drv?
        pass

    def name(self):
        """Return the driver name."""
        data=C.fp_driver_get_name(self.drv)
        return ffi.string(data).decode() if data else ""

    def full_name(self):
        """A longer, more desciptive version of the driver name."""
        data=C.fp_driver_get_full_name(self.drv)
        return ffi.string(data).decode() if data else ""

    def driver_id(self):
        """Return an integer uniqly identifying the driver."""
        return C.fp_driver_get_driver_id(self.drv)


class Fprint:

    def __init__(self, data_bytes=None, data_ptr=None, dscv_ptr=None, DscvList=None):
        """
        The only parameter that should be used is serial_data, which
        should be data previously aquired from data(), in the form of a string.
        All other parameters are for internal use only.
        """
        # data_ptr is a SWIG pointer to a struct pf_print_data
        # dscv_ptr is a SWIG pointer to a struct pf_dscv_print
        # DscvList is a class instance used to free the allocated pf_dscv_print's
        #          with pf_dscv_prints_free when they're all unused.
        # serial_data is a 'bytes' as returned by data()

        self.data_ptr = data_ptr
        self.dscv_ptr = dscv_ptr
        self.DscvList = DscvList


        if data_bytes:
            l = len(data_bytes)
            s = ffi.new("char[%d]" % l, bytes(data_bytes))

            self.data_ptr = C.fp_print_data_from_data(s, l)
            return

        if dscv_ptr != None and DscvList == None:
            raise FprintException("Programming error: Fprint constructed with dscv_prt with DscvList == None")

    # def __del__(self):
    #     if self.data_ptr:
    #         C.fp_print_data_free(ffi.cast("struct fp_print_data *", self.data_ptr))
    #     # The dscv_ptr is freed when all the dscv prints have been garbage
        # collected

    def _get_print_data_ptr(self):
        if not self.data_ptr:
            self._data_from_dscv()
        return self.data_ptr

    def driver_id(self):
        """Return an integer identifing the driver used to scan this print."""
        if self.data_ptr:
            return C.fp_print_data_get_driver_id(self.data_ptr)
        elif self.dscv_ptr:
            return C.fp_dscv_print_get_driver_id(self.dscv_ptr)
        raise FprintException("No fingerprint")

    def devtype(self):
        """Return an integer representing the type of device used to scan this print."""
        if self.data_ptr:
            return C.fp_print_data_get_devtype(self.data_ptr)
        elif self.dscv_ptr:
            return C.fp_dscv_print_get_devtype(self.dscv_ptr)
        raise FprintException("No fingerprint")

    def _data_from_dscv(self):
        if self.data_ptr:
            return
        if not self.dscv_ptr:
            raise FprintException("No fingerprint")
        (r, ptr) = C.fp_print_data_from_dscv_print(self.dscv_ptr)
        if r != 0:
            raise FprintException("print data from dscv failed")
        self.data_ptr = ptr

    def data(self):
        """
        Return a serialized dataset representing the fprint.
        This data could be stored away, and later passed to the
        contructor of Fprint.
        """
        if not self.data_ptr:
            raise FprintException("No fingerprint")

        s = ffi.new("unsigned char **")
        l = C.fp_print_data_get_data(self.data_ptr, s)

        if not l:
            raise FprintException("Serialization failed")

        sd = s[0]
        b = ffi.buffer(sd, l)
        return b
    def save(self, finger):
        """
        Save a fingerprint to the users home directory.

        - finger should be a value from Fingers.

        Return a True on SUCCESS, False otherwise
        """
        data=self._get_print_data_ptr()
        return 0 == C.fp_print_data_save(data, finger)


class DiscoveredDevices(list):

    """A list of available devices."""

    def __init__(self, dscv_devs_list):

        self.swig_list_ptr = dscv_devs_list

        i = 0

        while True:
            x = dscv_devs_list[i]

            if x == ffi.NULL:
                break

            self.append(Device(dscv_ptr=x, DscvList=self))
            i += 1

    def __del__(self):
        C.fp_dscv_devs_free(self.swig_list_ptr)

    def find_compatible(self, fprint):
        """
        Return a Device that is compatible with the fprint,
        or None if no compatible device is found.
        """
        for n in self:
            if n.is_compatible(fprint):
                return n
        return None


def discover_devices():
    """Return a list of available devices."""
    if not _init_ok:
        fp_init()

    devs = C.fp_discover_devs()

    if not devs:
        raise FprintIOException("Device discovery failed")

    return DiscoveredDevices(devs)

def identify(newfp, fprints):
    """Identifies a fingerprint from a list of fingerprints"""

    THRESHOLD = 40

    fprint_gallery = ffi.new("struct fp_print_data * [%d]" % (len(fprints) + 1))

    for i, fp in enumerate(fprints):
        fprint_gallery[i] = fp._get_print_data_ptr()

    offset = ffi.new("size_t *")

    try:
        r = C.fp_img_compare_print_data_to_gallery(newfp._get_print_data_ptr(), fprint_gallery, THRESHOLD, offset);
    except AttributeError:
        raise FprintException("libfprint does not export fp_img_compare_print_data_to_gallery!")
    offset = offset[0]

    if r == C.FP_VERIFY_NO_MATCH:
        return None

    if r == C.FP_VERIFY_MATCH:
        return offset
