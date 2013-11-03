

def thread_start(target=None, args=()):
    if args:
        t = Thread(target=target, args=args)
    else:
        t = Thread(target=target)
    t.daemon = True
    t.start()
    return t


