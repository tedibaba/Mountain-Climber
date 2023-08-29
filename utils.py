def av(*args):
    return sum(args)/len(args)

def bezier(*points):
    if len(points) == 1:
        return lambda t: points[0]
    p1 = bezier(*points[:-1])
    p2 = bezier(*points[1:])
    return lambda t: (
        (1-t) * p1(t)[0] + t * p2(t)[0],
        (1-t) * p1(t)[1] + t * p2(t)[1]
    )
