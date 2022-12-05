# coding=utf-8

# permission_vs_forgiveness

class BaseClass:
   hello = "world"
   bar = "world"
   baz = "world"

class Foo(BaseClass):
   pass

FOO = Foo()
def test_permission2():
   if hasattr(FOO, "hello") and hasattr(FOO, "bar") and hasattr(FOO, "baz"):
       var = FOO.hello
       var = FOO.bar
       var = FOO.baz


def test_forgiveness2():
   try:
       var = FOO.hello
       var = FOO.bar
       var = FOO.baz
   except AttributeError:
       pass



from itertools import count


def count_numbers():
   for item in count(1):
       if (item % 42 == 0) and (item % 43 == 0):
           return item


def generator():
   return next(item for item in count(1) if (item % 42 == 0) and (item % 43 == 0))


MILLION_NUMBERS = list(range(1_000_000))

def for_loop():
   output = []
   for element in MILLION_NUMBERS:
       if not element % 2:
           output.append(element)
   return output

def list_comprehension():
   return [number for number in MILLION_NUMBERS if not number % 2]

