#! /usr/bin/env python

"""Non-terminal symbols of Python grammar (from "graminit.h")."""

#  This file is automatically generated; please don't muck it up!
#
#  To update the symbols in this file, 'cd' to the top directory of
#  the python source tree after building the interpreter and run:
#
#    python Lib/symbol.py

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
augassign = 268
print_stmt = 269
del_stmt = 270
pass_stmt = 271
flow_stmt = 272
break_stmt = 273
continue_stmt = 274
return_stmt = 275
yield_stmt = 276
raise_stmt = 277
import_stmt = 278
import_as_name = 279
dotted_as_name = 280
dotted_name = 281
global_stmt = 282
exec_stmt = 283
assert_stmt = 284
compound_stmt = 285
if_stmt = 286
while_stmt = 287
for_stmt = 288
try_stmt = 289
except_clause = 290
suite = 291
test = 292
and_test = 293
not_test = 294
comparison = 295
comp_op = 296
expr = 297
xor_expr = 298
and_expr = 299
shift_expr = 300
arith_expr = 301
term = 302
factor = 303
power = 304
atom = 305
listmaker = 306
lambdef = 307
trailer = 308
subscriptlist = 309
subscript = 310
sliceop = 311
exprlist = 312
testlist = 313
dictmaker = 314
classdef = 315
arglist = 316
argument = 317
list_iter = 318
list_for = 319
list_if = 320
#--end constants--

sym_name = {}
for _name, _value in globals().items():
    if type(_value) is type(0):
        sym_name[_value] = _name


def main():
    import sys
    import token
    if len(sys.argv) == 1:
        sys.argv = sys.argv + ["Include/graminit.h", "Lib/symbol.py"]
    token.main()

if __name__ == "__main__":
    main()
