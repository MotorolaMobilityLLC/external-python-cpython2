# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

import string

# Declarations that change for each manager
MACHEADERFILE = 'AppleHelp.h'		# The Apple header file
MODNAME = '_AH'				# The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = 'Ah'			# The prefix for module-wide routines
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects
AHTOCType = Type("AHTOCType", "s")

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <AppleHelp.h>
#else
#include <Carbon/Carbon.h>
#endif

"""

# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)

# Create the generator classes used to populate the lists
Function = OSErrFunctionGenerator

# Create and populate the lists
functions = []
execfile(INPUTFILE)

# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()

