"""Parse sys/errno.h and Errors.h and create Estr resource"""

import re
import macfs
import string
from Carbon import Res
import os

READ = 1
WRITE = 2
smAllScripts = -3

ERRNO_PROG="#define[ \t]+" \
		   "([A-Z0-9a-z_]+)" \
		   "[ \t]+" \
		   "([0-9]+)" \
		   "[ \t]*/\*[ \t]*" \
		   "(.*)" \
		   "[ \t]*\*/"
		   
ERRORS_PROG="[ \t]*" \
			"([A-Z0-9a-z_]+)" \
			"[ \t]*=[ \t]*" \
			"([-0-9]+)" \
			"[, \t]*/\*[ \t]*" \
			"(.*)" \
			"[ \t]*\*/"
		   
ERRORS_PROG_2="[ \t]*" \
			"([A-Z0-9a-z_]+)" \
			"[ \t]*=[ \t]*" \
			"([-0-9]+)" \
			"[, \t]*"

def Pstring(str):
	if len(str) > 255:
		raise ValueError, 'String too large'
	return chr(len(str))+str
	
def writeestr(dst, edict):
	"""Create Estr resource file given a dictionary of errors."""
	
	os.unlink(dst.as_pathname())
	Res.FSpCreateResFile(dst, 'RSED', 'rsrc', smAllScripts)
	output = Res.FSpOpenResFile(dst, WRITE)
	Res.UseResFile(output)
	for num in edict.keys():
		res = Res.Resource(Pstring(edict[num][0]))
		res.AddResource('Estr', num, '')
		res.WriteResource()
	Res.CloseResFile(output)
	
def writepython(fp, dict):
	k = dict.keys()
	k.sort()
	for i in k:
		fp.write("%s\t=\t%d\t#%s\n"%(dict[i][1], i, dict[i][0]))
	

def parse_errno_h(fp, dict):
	errno_prog = re.compile(ERRNO_PROG)
	for line in fp.readlines():
		m = errno_prog.match(line)
		if m:
			number = string.atoi(m.group(2))
			name = m.group(1)
			desc = string.strip(m.group(3))
			
			if not dict.has_key(number):
				dict[number] = desc, name
			else:
				print 'DUPLICATE', number
				print '\t', dict[number]
				print '\t', (desc, name)
								
def parse_errors_h(fp, dict):
	errno_prog = re.compile(ERRORS_PROG)
	errno_prog_2 = re.compile(ERRORS_PROG_2)
	for line in fp.readlines():
		match = 0
		m = errno_prog.match(line)
		m2 = errno_prog_2.match(line)
		if m:
			number = string.atoi(m.group(2))
			name = m.group(1)
			desc = string.strip(m.group(3))
			match=1
		elif m2:
			number = string.atoi(m2.group(2))
			name = m2.group(1)
			desc = name
			match=1
		if match:
			if number > 0: continue
			
			if not dict.has_key(number):
				dict[number] = desc, name
			else:
				print 'DUPLICATE', number
				print '\t', dict[number]
				print '\t', (desc, name)
				if len(desc) > len(dict[number][0]):
					print 'Pick second one'
					dict[number] = desc, name
			
def main():
	dict = {}
	fss, ok = macfs.PromptGetFile("Where is GUSI sys/errno.h?")
	if not ok: return
	fp = open(fss.as_pathname())
	parse_errno_h(fp, dict)
	fp.close()
	
	fss, ok = macfs.PromptGetFile("Select cerrno (MSL) or cancel")
	if not ok: return
	fp = open(fss.as_pathname())
	parse_errno_h(fp, dict)
	fp.close()
	
	fss, ok = macfs.PromptGetFile("Where is MacErrors.h?")
	if not ok: return
	fp = open(fss.as_pathname())
	parse_errors_h(fp, dict)
	fp.close()
	
	if not dict:
		return
		
	fss, ok = macfs.StandardPutFile("Resource output file?", "errors.rsrc")
	if ok:
		writeestr(fss, dict)
	
	fss, ok = macfs.StandardPutFile("Python output file?", "macerrors.py")
	if ok:
		fp = open(fss.as_pathname(), "w")
		writepython(fp, dict)
		fp.close()
		fss.SetCreatorType('Pyth', 'TEXT')

	fss, ok = macfs.StandardPutFile("Text output file?", "errors.txt")
	if ok:
		fp = open(fss.as_pathname(), "w")
		
		k = dict.keys()
		k.sort()
		for i in k:
			fp.write("%d\t%s\t%s\n"%(i, dict[i][1], dict[i][0]))
		fp.close()

	
if __name__ == '__main__':
	main()
	
