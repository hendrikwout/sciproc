from datetime import datetime, timedelta

def dtrange(*args):
    # purpose: alternative for range() that works with datetimes
    if len(args) != 3:
        return range(*args)
    start, stop, step = args
    if start < stop:
        cmp = lambda a, b: a < b
        inc = lambda a: a + step
    else:
        cmp = lambda a, b: a > b
        inc = lambda a: a - step
    #output = [start]
    output = []
    while cmp(start, stop):
        output.append(start)
        start = inc(start)

    return output
