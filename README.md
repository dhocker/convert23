# convert23 - convert Python 2 to 3 while maintaining the dominant line ending

Copyright © 2018 by Dave Hocker (email: AtHomeX10@gmail.com)

## Overview
2to3 is a popular app for converting Python 2 to Python 3. Unfortunately,
the converted output always uses the UNIX standard single LF as a line
ending. Input files using CRLF line endings will become 100% changed
after being run through 2to3. This behavior essentially hides the
conversion changes in input files with CRLF line endings.

convert23 gives you a work around to this behavior. Essentially, it
puts a wrapper around 2to3 and attempts to maintain the original
line ending. It determines the dominant line ending by reading the entire
input file and counting line ends (CRLF and LF). The most
frequent line ending is considered to be the dominant line ending.
After convert23 determines the dominant line ending, it passes the input
file to 2to3.

When 2to3 completes its conversion work, convert23 determines the
line ending of the converted file by reading the first line of the
converted file. It then proceeds to "fix" the line endings of the
converted file, as necessary. If the converted file line ending matches the
dominant line ending, no action is taken. If the converted file line
ending does not match the dominant line ending, the converted file
is rewritten using the dominant line ending.

This algorithm is not 100% perfect because it does not accomodate
an input file with mixed line endings (when you want to maintain the mixed
line endings). However, it will normalize
the converted file to the dominant line ending of the input file.
This covers the more typical case where an input file with CRLF line
endings is converted to LF line endings by 2to3.

## License
convert23 is licensed under the GNU General Public License v3 as published
by the Free Software Foundation, Inc..
See the LICENSE.md file for the full text of the license.

## Python Compatibility
convert23 should be run using Python 3. It was tested on Python 3.6.5.

## Source code
The source code is maintained on
[GitHub](https://github.com/dhocker/convert23).