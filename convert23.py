#! /usr/local/bin/python3
#
# convert23 - convert from Python 2 to Python without changing line ends.
# Copyright © 2018  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#
# Essentially, this program wrappers the 2to3 script that is part of the
# Python3 distribution. It's main purpose is to maintain the line ending
# used by the file being converted. The 2to3 script does not
# handle this issue very gracefully.
#

import sys
import subprocess
import os


def help():
    print("")
    print("Convert a file from Python2 to Python3.")
    print("The file is converted in place with the dominant line end being maintained.")
    print("The 2to3 conversion program is used for the actual conversion.")
    print("")
    print("Usage:")
    print("\tpython3 convert23.py filename")
    print("Arguments:")
    print("\tfilename - the name of the file to be converted.")
    print("")


def main(args):
    """
    Main program for converting from Python 2 to Python 3
    :param args: Command line args
    :return:
    """
    filename = args[1]

    # Determine line ending of source file
    lf_count = 0
    crlf_count = 0

    fh = open(filename, "rb")
    line = fh.readline()
    while line:
        crlf = line.endswith(b"\r\n")
        if crlf:
            crlf_count += 1
        else:
            lf_count += 1
        line = fh.readline()
    # The larger count wins
    crlf = crlf_count >= lf_count
    fh.close()

    print("Dominant line ending is:", crlf)
    print("CRLF count:", crlf_count)
    print("LF count:", lf_count)

    # convert the file
    # The options are write and no backup
    subprocess.run(["2to3", "-w", "-n", filename])

    # What is the new line ending in the converted file
    # Likely, the converted file has LF line ending
    fh = open(filename, "rb")
    line = fh.readline()
    new_crlf = line.endswith(b"\r\n")
    fh.close()
    print("New line ending is:", new_crlf)

    # Fix line endings if necessary
    if crlf != new_crlf:
        # Fix line endings by writing a new file (.tmp suffix)
        # with correct line ends, removing the converted file
        # with incorrect line ends and renaming the .tmp
        # file to the original file name.
        print("Fixing line ends")
        rfh = open(filename, "r", newline=None)
        if crlf:
            wfh = open(filename + ".tmp", "w", newline="\r\n")
        else:
            wfh = open(filename + ".tmp", "w", newline="\n")
        line = rfh.readline()
        while line:
            wfh.writelines(line)
            line = rfh.readline()
        # Delete/rename
        os.remove(filename)
        os.rename(filename + ".tmp", filename)


#
# Run the conversion
#
if __name__ == "__main__":
    # Checks
    if sys.version_info < (3, 6):
        print("Python version 3.6+ required")
        exit(1)
    if len(sys.argv) < 2:
        help()
        exit(2)
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        help()
        exit(0)

    main(sys.argv)

    print("Conversion with line end repair complete")
    exit(0)