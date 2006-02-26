/* File automatically generated by Parser/asdl_c.py */

#include "asdl.h"

typedef struct _mod *mod_ty;

typedef struct _stmt *stmt_ty;

typedef struct _expr *expr_ty;

typedef enum _expr_context { Load=1, Store=2, Del=3, AugLoad=4, AugStore=5,
                             Param=6 } expr_context_ty;

typedef struct _slice *slice_ty;

typedef enum _boolop { And=1, Or=2 } boolop_ty;

typedef enum _operator { Add=1, Sub=2, Mult=3, Div=4, Mod=5, Pow=6, LShift=7,
                         RShift=8, BitOr=9, BitXor=10, BitAnd=11, FloorDiv=12 }
                         operator_ty;

typedef enum _unaryop { Invert=1, Not=2, UAdd=3, USub=4 } unaryop_ty;

typedef enum _cmpop { Eq=1, NotEq=2, Lt=3, LtE=4, Gt=5, GtE=6, Is=7, IsNot=8,
                      In=9, NotIn=10 } cmpop_ty;

typedef struct _comprehension *comprehension_ty;

typedef struct _excepthandler *excepthandler_ty;

typedef struct _arguments *arguments_ty;

typedef struct _keyword *keyword_ty;

typedef struct _alias *alias_ty;


struct _mod {
        enum { Module_kind=1, Interactive_kind=2, Expression_kind=3,
               Suite_kind=4 } kind;
        union {
                struct {
                        asdl_seq *body;
                } Module;
                
                struct {
                        asdl_seq *body;
                } Interactive;
                
                struct {
                        expr_ty body;
                } Expression;
                
                struct {
                        asdl_seq *body;
                } Suite;
                
        } v;
};

struct _stmt {
        enum { FunctionDef_kind=1, ClassDef_kind=2, Return_kind=3,
               Delete_kind=4, Assign_kind=5, AugAssign_kind=6, Print_kind=7,
               For_kind=8, While_kind=9, If_kind=10, Raise_kind=11,
               TryExcept_kind=12, TryFinally_kind=13, Assert_kind=14,
               Import_kind=15, ImportFrom_kind=16, Exec_kind=17,
               Global_kind=18, Expr_kind=19, Pass_kind=20, Break_kind=21,
               Continue_kind=22 } kind;
        union {
                struct {
                        identifier name;
                        arguments_ty args;
                        asdl_seq *body;
                        asdl_seq *decorators;
                } FunctionDef;
                
                struct {
                        identifier name;
                        asdl_seq *bases;
                        asdl_seq *body;
                } ClassDef;
                
                struct {
                        expr_ty value;
                } Return;
                
                struct {
                        asdl_seq *targets;
                } Delete;
                
                struct {
                        asdl_seq *targets;
                        expr_ty value;
                } Assign;
                
                struct {
                        expr_ty target;
                        operator_ty op;
                        expr_ty value;
                } AugAssign;
                
                struct {
                        expr_ty dest;
                        asdl_seq *values;
                        bool nl;
                } Print;
                
                struct {
                        expr_ty target;
                        expr_ty iter;
                        asdl_seq *body;
                        asdl_seq *orelse;
                } For;
                
                struct {
                        expr_ty test;
                        asdl_seq *body;
                        asdl_seq *orelse;
                } While;
                
                struct {
                        expr_ty test;
                        asdl_seq *body;
                        asdl_seq *orelse;
                } If;
                
                struct {
                        expr_ty type;
                        expr_ty inst;
                        expr_ty tback;
                } Raise;
                
                struct {
                        asdl_seq *body;
                        asdl_seq *handlers;
                        asdl_seq *orelse;
                } TryExcept;
                
                struct {
                        asdl_seq *body;
                        asdl_seq *finalbody;
                } TryFinally;
                
                struct {
                        expr_ty test;
                        expr_ty msg;
                } Assert;
                
                struct {
                        asdl_seq *names;
                } Import;
                
                struct {
                        identifier module;
                        asdl_seq *names;
                } ImportFrom;
                
                struct {
                        expr_ty body;
                        expr_ty globals;
                        expr_ty locals;
                } Exec;
                
                struct {
                        asdl_seq *names;
                } Global;
                
                struct {
                        expr_ty value;
                } Expr;
                
        } v;
        int lineno;
};

struct _expr {
        enum { BoolOp_kind=1, BinOp_kind=2, UnaryOp_kind=3, Lambda_kind=4,
               Dict_kind=5, ListComp_kind=6, GeneratorExp_kind=7, Yield_kind=8,
               Compare_kind=9, Call_kind=10, Repr_kind=11, Num_kind=12,
               Str_kind=13, Attribute_kind=14, Subscript_kind=15, Name_kind=16,
               List_kind=17, Tuple_kind=18 } kind;
        union {
                struct {
                        boolop_ty op;
                        asdl_seq *values;
                } BoolOp;
                
                struct {
                        expr_ty left;
                        operator_ty op;
                        expr_ty right;
                } BinOp;
                
                struct {
                        unaryop_ty op;
                        expr_ty operand;
                } UnaryOp;
                
                struct {
                        arguments_ty args;
                        expr_ty body;
                } Lambda;
                
                struct {
                        asdl_seq *keys;
                        asdl_seq *values;
                } Dict;
                
                struct {
                        expr_ty elt;
                        asdl_seq *generators;
                } ListComp;
                
                struct {
                        expr_ty elt;
                        asdl_seq *generators;
                } GeneratorExp;
                
                struct {
                        expr_ty value;
                } Yield;
                
                struct {
                        expr_ty left;
                        asdl_seq *ops;
                        asdl_seq *comparators;
                } Compare;
                
                struct {
                        expr_ty func;
                        asdl_seq *args;
                        asdl_seq *keywords;
                        expr_ty starargs;
                        expr_ty kwargs;
                } Call;
                
                struct {
                        expr_ty value;
                } Repr;
                
                struct {
                        object n;
                } Num;
                
                struct {
                        string s;
                } Str;
                
                struct {
                        expr_ty value;
                        identifier attr;
                        expr_context_ty ctx;
                } Attribute;
                
                struct {
                        expr_ty value;
                        slice_ty slice;
                        expr_context_ty ctx;
                } Subscript;
                
                struct {
                        identifier id;
                        expr_context_ty ctx;
                } Name;
                
                struct {
                        asdl_seq *elts;
                        expr_context_ty ctx;
                } List;
                
                struct {
                        asdl_seq *elts;
                        expr_context_ty ctx;
                } Tuple;
                
        } v;
        int lineno;
};

struct _slice {
        enum { Ellipsis_kind=1, Slice_kind=2, ExtSlice_kind=3, Index_kind=4 }
               kind;
        union {
                struct {
                        expr_ty lower;
                        expr_ty upper;
                        expr_ty step;
                } Slice;
                
                struct {
                        asdl_seq *dims;
                } ExtSlice;
                
                struct {
                        expr_ty value;
                } Index;
                
        } v;
};

struct _comprehension {
        expr_ty target;
        expr_ty iter;
        asdl_seq *ifs;
};

struct _excepthandler {
        expr_ty type;
        expr_ty name;
        asdl_seq *body;
};

struct _arguments {
        asdl_seq *args;
        identifier vararg;
        identifier kwarg;
        asdl_seq *defaults;
};

struct _keyword {
        identifier arg;
        expr_ty value;
};

struct _alias {
        identifier name;
        identifier asname;
};


mod_ty Module(asdl_seq * body, PyArena *arena);
mod_ty Interactive(asdl_seq * body, PyArena *arena);
mod_ty Expression(expr_ty body, PyArena *arena);
mod_ty Suite(asdl_seq * body, PyArena *arena);
stmt_ty FunctionDef(identifier name, arguments_ty args, asdl_seq * body,
                    asdl_seq * decorators, int lineno, PyArena *arena);
stmt_ty ClassDef(identifier name, asdl_seq * bases, asdl_seq * body, int
                 lineno, PyArena *arena);
stmt_ty Return(expr_ty value, int lineno, PyArena *arena);
stmt_ty Delete(asdl_seq * targets, int lineno, PyArena *arena);
stmt_ty Assign(asdl_seq * targets, expr_ty value, int lineno, PyArena *arena);
stmt_ty AugAssign(expr_ty target, operator_ty op, expr_ty value, int lineno,
                  PyArena *arena);
stmt_ty Print(expr_ty dest, asdl_seq * values, bool nl, int lineno, PyArena
              *arena);
stmt_ty For(expr_ty target, expr_ty iter, asdl_seq * body, asdl_seq * orelse,
            int lineno, PyArena *arena);
stmt_ty While(expr_ty test, asdl_seq * body, asdl_seq * orelse, int lineno,
              PyArena *arena);
stmt_ty If(expr_ty test, asdl_seq * body, asdl_seq * orelse, int lineno,
           PyArena *arena);
stmt_ty Raise(expr_ty type, expr_ty inst, expr_ty tback, int lineno, PyArena
              *arena);
stmt_ty TryExcept(asdl_seq * body, asdl_seq * handlers, asdl_seq * orelse, int
                  lineno, PyArena *arena);
stmt_ty TryFinally(asdl_seq * body, asdl_seq * finalbody, int lineno, PyArena
                   *arena);
stmt_ty Assert(expr_ty test, expr_ty msg, int lineno, PyArena *arena);
stmt_ty Import(asdl_seq * names, int lineno, PyArena *arena);
stmt_ty ImportFrom(identifier module, asdl_seq * names, int lineno, PyArena
                   *arena);
stmt_ty Exec(expr_ty body, expr_ty globals, expr_ty locals, int lineno, PyArena
             *arena);
stmt_ty Global(asdl_seq * names, int lineno, PyArena *arena);
stmt_ty Expr(expr_ty value, int lineno, PyArena *arena);
stmt_ty Pass(int lineno, PyArena *arena);
stmt_ty Break(int lineno, PyArena *arena);
stmt_ty Continue(int lineno, PyArena *arena);
expr_ty BoolOp(boolop_ty op, asdl_seq * values, int lineno, PyArena *arena);
expr_ty BinOp(expr_ty left, operator_ty op, expr_ty right, int lineno, PyArena
              *arena);
expr_ty UnaryOp(unaryop_ty op, expr_ty operand, int lineno, PyArena *arena);
expr_ty Lambda(arguments_ty args, expr_ty body, int lineno, PyArena *arena);
expr_ty Dict(asdl_seq * keys, asdl_seq * values, int lineno, PyArena *arena);
expr_ty ListComp(expr_ty elt, asdl_seq * generators, int lineno, PyArena
                 *arena);
expr_ty GeneratorExp(expr_ty elt, asdl_seq * generators, int lineno, PyArena
                     *arena);
expr_ty Yield(expr_ty value, int lineno, PyArena *arena);
expr_ty Compare(expr_ty left, asdl_seq * ops, asdl_seq * comparators, int
                lineno, PyArena *arena);
expr_ty Call(expr_ty func, asdl_seq * args, asdl_seq * keywords, expr_ty
             starargs, expr_ty kwargs, int lineno, PyArena *arena);
expr_ty Repr(expr_ty value, int lineno, PyArena *arena);
expr_ty Num(object n, int lineno, PyArena *arena);
expr_ty Str(string s, int lineno, PyArena *arena);
expr_ty Attribute(expr_ty value, identifier attr, expr_context_ty ctx, int
                  lineno, PyArena *arena);
expr_ty Subscript(expr_ty value, slice_ty slice, expr_context_ty ctx, int
                  lineno, PyArena *arena);
expr_ty Name(identifier id, expr_context_ty ctx, int lineno, PyArena *arena);
expr_ty List(asdl_seq * elts, expr_context_ty ctx, int lineno, PyArena *arena);
expr_ty Tuple(asdl_seq * elts, expr_context_ty ctx, int lineno, PyArena *arena);
slice_ty Ellipsis(PyArena *arena);
slice_ty Slice(expr_ty lower, expr_ty upper, expr_ty step, PyArena *arena);
slice_ty ExtSlice(asdl_seq * dims, PyArena *arena);
slice_ty Index(expr_ty value, PyArena *arena);
comprehension_ty comprehension(expr_ty target, expr_ty iter, asdl_seq * ifs,
                               PyArena *arena);
excepthandler_ty excepthandler(expr_ty type, expr_ty name, asdl_seq * body,
                               PyArena *arena);
arguments_ty arguments(asdl_seq * args, identifier vararg, identifier kwarg,
                       asdl_seq * defaults, PyArena *arena);
keyword_ty keyword(identifier arg, expr_ty value, PyArena *arena);
alias_ty alias(identifier name, identifier asname, PyArena *arena);

PyObject* PyAST_mod2obj(mod_ty t);
