/* stringlib: fastsearch implementation */

#define STRINGLIB_FASTSEARCH_H

/* fast search/count implementation, based on a mix between boyer-
   moore and horspool, with a few more bells and whistles on the top.
   for some more background, see: http://effbot.org/zone/stringlib.htm */

/* note: fastsearch may access s[n], which isn't a problem when using
   Python's ordinary string types, but may cause problems if you're
   using this code in other contexts.  also, the count mode returns -1
   if there cannot possible be a match in the target string, and 0 if
   it has actually checked for matches, but didn't find any.  callers
   beware! */

#define FAST_COUNT 0
#define FAST_SEARCH 1
#define FAST_RSEARCH 2

#if LONG_BIT >= 128
#define STRINGLIB_BLOOM_WIDTH 128
#elif LONG_BIT >= 64
#define STRINGLIB_BLOOM_WIDTH 64
#elif LONG_BIT >= 32
#define STRINGLIB_BLOOM_WIDTH 32
#else
#error "LONG_BIT is smaller than 32"
#endif

#define STRINGLIB_BLOOM_ADD(mask, ch) \
    ((mask |= (1UL << ((ch) & (STRINGLIB_BLOOM_WIDTH -1)))))
#define STRINGLIB_BLOOM(mask, ch)     \
    ((mask &  (1UL << ((ch) & (STRINGLIB_BLOOM_WIDTH -1)))))


Py_LOCAL_INLINE(Py_ssize_t)
STRINGLIB(fastsearch_memchr_1char)(const STRINGLIB_CHAR* s, Py_ssize_t n,
                                   STRINGLIB_CHAR ch, unsigned char needle,
                                   Py_ssize_t maxcount, int mode)
{
    void *candidate;
    const STRINGLIB_CHAR *found;

#define DO_MEMCHR(memchr, s, needle, nchars) do { \
    candidate = memchr((const void *) (s), (needle), (nchars) * sizeof(STRINGLIB_CHAR)); \
    found = (const STRINGLIB_CHAR *) \
        ((Py_ssize_t) candidate & (~ ((Py_ssize_t) sizeof(STRINGLIB_CHAR) - 1))); \
    } while (0)

    if (mode == FAST_SEARCH) {
        const STRINGLIB_CHAR *_s = s;
        const STRINGLIB_CHAR *e = s + n;
        while (_s < e) {
            DO_MEMCHR(memchr, _s, needle, e - _s);
            if (found == NULL)
                return -1;
            if (sizeof(STRINGLIB_CHAR) == 1 || *found == ch)
                return (found - _s);
            /* False positive */
            _s = found + 1;
        }
        return -1;
    }
#ifdef HAVE_MEMRCHR
    /* memrchr() is a GNU extension, available since glibc 2.1.91.
       it doesn't seem as optimized as memchr(), but is still quite
       faster than our hand-written loop in FASTSEARCH below */
    else if (mode == FAST_RSEARCH) {
        while (n > 0) {
            DO_MEMCHR(memrchr, s, needle, n);
            if (found == NULL)
                return -1;
            n = found - s;
            if (sizeof(STRINGLIB_CHAR) == 1 || *found == ch)
                return n;
            /* False positive */
        }
        return -1;
    }
#endif
    else {
        assert(0); /* Should never get here */
        return 0;
    }

#undef DO_MEMCHR
}

Py_LOCAL_INLINE(Py_ssize_t)
FASTSEARCH(const STRINGLIB_CHAR* s, Py_ssize_t n,
           const STRINGLIB_CHAR* p, Py_ssize_t m,
           Py_ssize_t maxcount, int mode)
{
    unsigned long mask;
    Py_ssize_t skip, count = 0;
    Py_ssize_t i, j, mlast, w;

    w = n - m;

    if (w < 0 || (mode == FAST_COUNT && maxcount == 0))
        return -1;

    /* look for special cases */
    if (m <= 1) {
        if (m <= 0)
            return -1;
        /* use special case for 1-character strings */
        if (n > 10 && (mode == FAST_SEARCH
#ifdef HAVE_MEMRCHR
                    || mode == FAST_RSEARCH
#endif
                    )) {
            /* use memchr if we can choose a needle without two many likely
               false positives */
            unsigned char needle;
            needle = p[0] & 0xff;
#if STRINGLIB_SIZEOF_CHAR > 1
            if (needle != 0)
#endif
                return STRINGLIB(fastsearch_memchr_1char)
                       (s, n, p[0], needle, maxcount, mode);
        }
        if (mode == FAST_COUNT) {
            for (i = 0; i < n; i++)
                if (s[i] == p[0]) {
                    count++;
                    if (count == maxcount)
                        return maxcount;
                }
            return count;
        } else if (mode == FAST_SEARCH) {
            for (i = 0; i < n; i++)
                if (s[i] == p[0])
                    return i;
        } else {    /* FAST_RSEARCH */
            for (i = n - 1; i > -1; i--)
                if (s[i] == p[0])
                    return i;
        }
        return -1;
    }

    mlast = m - 1;
    skip = mlast - 1;
    mask = 0;

    if (mode != FAST_RSEARCH) {

        /* create compressed boyer-moore delta 1 table */

        /* process pattern[:-1] */
        for (i = 0; i < mlast; i++) {
            STRINGLIB_BLOOM_ADD(mask, p[i]);
            if (p[i] == p[mlast])
                skip = mlast - i - 1;
        }
        /* process pattern[-1] outside the loop */
        STRINGLIB_BLOOM_ADD(mask, p[mlast]);

        for (i = 0; i <= w; i++) {
            /* note: using mlast in the skip path slows things down on x86 */
            if (s[i+m-1] == p[m-1]) {
                /* candidate match */
                for (j = 0; j < mlast; j++)
                    if (s[i+j] != p[j])
                        break;
                if (j == mlast) {
                    /* got a match! */
                    if (mode != FAST_COUNT)
                        return i;
                    count++;
                    if (count == maxcount)
                        return maxcount;
                    i = i + mlast;
                    continue;
                }
                /* miss: check if next character is part of pattern */
                if (!STRINGLIB_BLOOM(mask, s[i+m]))
                    i = i + m;
                else
                    i = i + skip;
            } else {
                /* skip: check if next character is part of pattern */
                if (!STRINGLIB_BLOOM(mask, s[i+m]))
                    i = i + m;
            }
        }
    } else {    /* FAST_RSEARCH */

        /* create compressed boyer-moore delta 1 table */

        /* process pattern[0] outside the loop */
        STRINGLIB_BLOOM_ADD(mask, p[0]);
        /* process pattern[:0:-1] */
        for (i = mlast; i > 0; i--) {
            STRINGLIB_BLOOM_ADD(mask, p[i]);
            if (p[i] == p[0])
                skip = i - 1;
        }

        for (i = w; i >= 0; i--) {
            if (s[i] == p[0]) {
                /* candidate match */
                for (j = mlast; j > 0; j--)
                    if (s[i+j] != p[j])
                        break;
                if (j == 0)
                    /* got a match! */
                    return i;
                /* miss: check if previous character is part of pattern */
                if (i > 0 && !STRINGLIB_BLOOM(mask, s[i-1]))
                    i = i - m;
                else
                    i = i - skip;
            } else {
                /* skip: check if previous character is part of pattern */
                if (i > 0 && !STRINGLIB_BLOOM(mask, s[i-1]))
                    i = i - m;
            }
        }
    }

    if (mode != FAST_COUNT)
        return -1;
    return count;
}

