from test import test_support
import StringIO

# SF bug 480215:  softspace confused in nested print
f = StringIO.StringIO()
class C:
    def __str__(self):
        print('a', file=f)
        return 'b'

print(C(), 'c ', 'd\t', 'e', file=f)
print('f', 'g', file=f)
# In 2.2 & earlier, this printed ' a\nbc  d\te\nf g\n'
test_support.vereq(f.getvalue(), 'a\nb c  d\te\nf g\n')
