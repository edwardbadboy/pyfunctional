from functools import partial
from operator import pow, gt, add, mul
from itertools import count as icount
from itertools import imap, ifilter, takewhile


class _compFun(partial):
    def __add__(self, y):
        f = lambda *args, **kwargs: self.func(y(*args, **kwargs))
        return _compFun(f)


def fcp():
    return _compFun(lambda arg: arg)


def f1(x):
    return x * 2


def f2(x):
    return x + 2


def f3(x):
    return x ** 2


print f3(f2(f1(3)))
print (fcp() + f3 + f2 + f1)(3)

F = fcp() + $mul(2) + $add(1)
print F(2)


def isOdd(x):
    return (x % 2) != 0


def takeN(N, it):
    i = 0
    while i < N:
        yield it.next()
        i += 1


def flip(f):
    return lambda a, b: f(b, a)


pow2 = flip(pow)

R = fcp() + $takewhile($gt(100)) + $ifilter(isOdd) + $imap($pow2(2)) + icount

# can stop
for i in R(1):
    print i


R = (pow(i, 2) for i in icount(1) if pow(i, 2) % 2 != 0 and pow(i, 2) < 100)

# won't stop
for i in R:
    print i
