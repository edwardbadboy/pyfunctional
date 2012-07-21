from funCompose import fcp
from operator import pow, gt, add, mul
from itertools import count as icount
from itertools import imap, ifilter, takewhile, izip


def f1(x):
    return x * 2


def f2(x):
    return x + 2


def f3(x):
    return x ** 2


# function composition example
print f3(f2(f1(3)))
F = (fcp() * f3 * f2 * f1)
print F(3)
print
# the result of the above two computation must be the same

# function composition and currying example
F = fcp() * $mul(2) * $add(1)
print F(2)
print


def isOdd(x):
    return (x % 2) != 0


def takeN(N, it):
    i = 0
    while i < N:
        yield it.next()
        i += 1


def flip(f):
    return lambda a, b: f(b, a)


# sophisticated currying example
pow2 = flip(pow)
R = fcp() * $takewhile($gt(1000)) * $ifilter(isOdd) * $imap($pow2(2)) * icount
for i in R(1):
    print i
print

# a bit more sophisticated currying example
R = (fcp() *
     $takewhile($gt(1000)) * $ifilter(isOdd) *
     $imap($(flip(pow))(2)) * icount)
for i in R(1):
    print i
print

# generator alternative
R = (pow(i, 2) for i in icount(1) if pow(i, 2) % 2 != 0 and pow(i, 2) < 1000)
# but it won't stop
# for i in R:
    # print i


def dotProduct(addOp, mulOp, *vectors):
    f = fcp() * $reduce(addOp) * $imap(mulOp)
    return f(*vectors)


print dotProduct(add, mul, [1, 2, 3], [4, 5, 6])
print 1 * 4 + 2 * 5 + 3 * 6
print


def f3arg(a, b, c):
    return a + b + c


F = $($f3arg(1))(2)
print F(3)
print
