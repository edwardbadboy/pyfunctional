from functools import partial


class _compFun(partial):
    def __mul__(self, y):
        f = lambda *args, **kwargs: self.func(y(*args, **kwargs))
        return _compFun(f)


def fcp():
    return _compFun(lambda arg: arg)
