def get_args(string_to_parse):
    pieces = string_to_parse.split(' ')
    max_item = len(pieces)
    i = 0
    res = []
    startFlags = False
    tmp_res = []
    while i < max_item:
        if '--' in pieces[i]:
            if tmp_res:
                res.append(tmp_res)
            tmp_res = [pieces[i]]
            startFlags = True
        elif not startFlags:
            res.append([pieces[i]])
            tmp_res = []
        else:
            tmp_res.append(pieces[i])
        i += 1
    if tmp_res:
        res.append(tmp_res)
    args = []
    flags = {}
    for i in res:
        if len(i) == 1:
            args.append(i[0])
        else:
            flags[i[0].replace('--', '')] = " ".join(i[1:])
    return args, flags
