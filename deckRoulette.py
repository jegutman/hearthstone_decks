import random

distro = [
    ('raza', 6),
    ('highroll', 4),
    ('evolve', 1),
    ('murloc', 4),
]

total = sum([i[1] for i in distro])
weights = []
running = 0
for i,j in distro:
    w = float(j) / float(total)
    running += w 
    weights.append([i, running])
    
value = random.random()
print value
for i,j in weights:
    if value < j:
        print i
        break
