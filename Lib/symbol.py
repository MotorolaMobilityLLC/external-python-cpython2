#! /usr/bin/env python
#
#  Non-terminal symbols of Python grammar (from "graminit.h")
#
#  This file is automatically generated; please don't muck it up!
#
#  To update the symbols in this file, 'cd' to the top directory of
#  the python source tree after building the interpreter and run:
#
#    PYTHONPATH=Lib:Modules ./python Lib/symbol.py
#
#  (this path allows the import of string.py, token.py, and regexmodule.so
#  for a site with no installation in place)

#--start constants--
single_input = 256
file_input = 257
eval_input = 258
funcdef = 259
parameters = 260
varargslist = 261
fpdef = 262
fplist = 263
stmt = 264
simple_stmt = 265
small_stmt = 266
expr_stmt = 267
print_stmt = 268
del_stmt = 269
pass_stmt = 270
flow_stmt = 271
break_stmt = 272
continue_stmt = 273
return_stmt = 274
raise_stmt = 275
import_stmt = 276
dotted_name = 277
global_stmt = 278
exec_stmt = 279
compound_stmt = 280
if_stmt = 281
while_stmt = 282
for_stmt = 283
try_stmt = 284
except_clause = 285
suite = 286
test = 287
and_test = 288
not_test = 289
comparison = 290
comp_op = 291
expr = 292
xor_expr = 293
and_expr = 294
shift_expr = 295
arith_expr = 296
term = 297
factor = 298
power = 299
atom = 300
lambdef = 301
trailer = 302
subscriptlist = 303
subscript = 304
sliceop = 305
exprlist = 306
testlist = 307
dictmaker = 308
classdef = 309
arglist = 310
argument = 311
#--end constants--

names = dir()
sym_name = {}
for name in names:
    number = eval(name)
    if type(number) is type(0):
	sym_name[number] = name


def main():
    import sys
    import token
    if len(sys.argv) == 1:
	sys.argv = sys.argv + ["Include/graminit.h", "Lib/symbol.py"]
    token.main()

if __name__ == "__main__":
    main()

#
#  end of file
