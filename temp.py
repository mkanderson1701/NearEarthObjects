from itertools import islice

def limit(iterator, n=None):
    if n == None or n == 0:
        return iterator
    count = 0
    while count < n:
        try: 
            count += 1
            yield next(iterator)
        except StopIteration:
            count = n
            
def limit_two(iterator, n=None):
    if n == 0:
        n = None
    for item in islice(iterator, 0, None):
        yield item
 
shit = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
#shitit = iter(shit)
bullshit = limit_two(shit, n=15)

for num in bullshit:
    print(num)