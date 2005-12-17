#ifndef Py_ASDL_H
#define Py_ASDL_H

typedef PyObject * identifier;
typedef PyObject * string;
typedef PyObject * object;

typedef enum {false, true} bool;

/* It would be nice if the code generated by asdl_c.py was completely
   independent of Python, but it is a goal the requires too much work
   at this stage.  So, for example, I'll represent identifiers as
   interned Python strings.
*/

/* XXX A sequence should be typed so that its use can be typechecked. */

/* XXX We shouldn't pay for offset when we don't need APPEND. */

typedef struct {
    int size;
    int offset;
    void *elements[1];
} asdl_seq;

asdl_seq *asdl_seq_new(int size, PyArena *arena);
void asdl_seq_free(asdl_seq *);

#ifdef Py_DEBUG
#define asdl_seq_GET(S, I) (S)->elements[(I)]
#define asdl_seq_SET(S, I, V) { \
        int _asdl_i = (I); \
        assert((S) && _asdl_i < (S)->size); \
        (S)->elements[_asdl_i] = (V); \
}
#define asdl_seq_APPEND(S, V) { \
        assert((S) && (S)->offset < (S)->size); \
        (S)->elements[(S)->offset++] = (V); \
}
#else
#define asdl_seq_GET(S, I) (S)->elements[(I)]
#define asdl_seq_SET(S, I, V) (S)->elements[I] = (V)
#define asdl_seq_APPEND(S, V) (S)->elements[(S)->offset++] = (V)
#endif
#define asdl_seq_LEN(S) ((S) == NULL ? 0 : (S)->size)

#endif /* !Py_ASDL_H */
