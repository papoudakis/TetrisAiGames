p1 = 0
p2 = 0
d = 0 
while True:
    try:
        a = raw_input()
    except:
        print p1
        print p2
        print d
        exit()
    if a not in ['\n', '\r\n']:
        if a == 'player1':
            p1 = p1 + 1
        elif a == 'player2':
            p2 = p2 + 1
        elif a == 'draw':
            d = d + 1
