
/* Python version identification scheme.

   When the major or minor version changes, the VERSION variable in
   configure.in must also be changed.

   There is also (independent) API version information in modsupport.h.
*/

/* Values for PY_RELEASE_LEVEL */
#define PY_RELEASE_LEVEL_ALPHA	0xA
#define PY_RELEASE_LEVEL_BETA	0xB
#define PY_RELEASE_LEVEL_GAMMA	0xC     /* For release candidates */
#define PY_RELEASE_LEVEL_FINAL	0xF	/* Serial should be 0 here */
					/* Higher for patch releases */

/* Version parsed out into numeric values */
/*--start constants--*/
#define PY_MAJOR_VERSION	3
#define PY_MINOR_VERSION	1
#define PY_MICRO_VERSION	0
#define PY_RELEASE_LEVEL	PY_RELEASE_LEVEL_GAMMA
#define PY_RELEASE_SERIAL	1

/* Version as a string */
#define PY_VERSION      	"3.1rc1+"
/*--end constants--*/

/* Subversion Revision number of this file (not of the repository) */
#define PY_PATCHLEVEL_REVISION  "$Revision$"

/* Version as a single 4-byte hex number, e.g. 0x010502B2 == 1.5.2b2.
   Use this for numeric comparisons, e.g. #if PY_VERSION_HEX >= ... */
#define PY_VERSION_HEX ((PY_MAJOR_VERSION << 24) | \
			(PY_MINOR_VERSION << 16) | \
			(PY_MICRO_VERSION <<  8) | \
			(PY_RELEASE_LEVEL <<  4) | \
			(PY_RELEASE_SERIAL << 0))
