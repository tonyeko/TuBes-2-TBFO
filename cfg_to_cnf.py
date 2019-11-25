'''
CFG to CNF Algorithm v.1
Created by Yonatan Viody.
'''
import sys
import itertools

def prods_more_than_two(prod):
    if (len(prod) > 2):
        found = False
        a = prods_more_than_two(prod[1:])
        for cnf in cnfs:
            if (' '.join(a) == cnf.split(' -> ')[1]):
                found = True
                newvar = cnf.split(' -> ')[0]
                break
        if not(found):
            newvar = 'a' + str(i[0])
            it = i[0] + 1
            i.pop(0)
            i.append(it)
            res = a
            cnfs.append(newvar+" -> "+res[0]+" "+res[1])
        return [prod[0], newvar]
    else:
        return prod

def parsing_cfg_prod(prod):
    x = list(filter(None,map(lambda x: x.replace(' ', '').replace('\n',''), prod.split(" "))))
    prods_res_local = []
    if (len(x) == 2):
        for j in range(len(x)):
            found = False
            if ("'" == x[j][0]):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    cnfs.append('a'+str(i[0])+" -> '"+x[j][1:-1]+"'")
                    x[j] = 'a'+str(i[0])
                    it = i[0] + 1
                    i.pop(0)
                    i.append(it)
        prods_res_local += [' '.join(x)]
    elif (len(x) == 1):
        if (x[0][0] != "'"):
            for j in range(len(cfgs)):
                if (cfgs[j].find(x[0]) == 0):
                    break
            desc = cfgs[j].split("->")
            symbol = desc[0]
            prods = desc[1].split("|")
            for prod in prods:
                prods_res_local += parsing_cfg_prod(prod)
        else:
            prods_res_local += x
    else:
        for j in range(len(x)):
            found = False
            if ("'" == x[j][0]):
                for cnf in cnfs:
                    if (x[j] == cnf.split(" -> ")[1]):
                        found = True
                        x[j] = cnf.split(" ")[0]
                        break
                if not(found):
                    cnfs.append('a'+str(i[0])+" -> '"+x[j][1:-1]+"'")
                    x[j] = 'a'+str(i[0])
                    it = i[0] + 1
                    i.pop(0)
                    i.append(it)
        prods_res_local += [' '.join(prods_more_than_two(x))]
    return prods_res_local

def parsing_cfg(cfg):
    desc = cfg.split("->")
    symbol = desc[0].replace(' ','')
    prods = desc[1].split("|")
    prods_res = []
    for prod in prods:
        prods_res += parsing_cfg_prod(prod)
    return symbol + ' -> ' + ' | '.join(list(dict.fromkeys(prods_res)))

def remove_epsilon_rec(symbol, x, prods2):
    if (x != []):
        z = 0
        a = x.copy()
        while (z < len(a)):
            if (a[z] == symbol):
                a.pop(z)
                prods2 = remove_epsilon_rec(symbol, a, prods2)
                prods2.append(' '.join(a))
                a = a[:z] + [symbol]  + a[z:] 
            z += 1
    return prods2

def remove_epsilon_prod(cfg):
    desc = cfg.split("->")
    symbol = desc[0].replace(' ','')
    prods = list(map(lambda x: x.replace('\n', '').replace('\r',''), desc[1].split("|")))
    for j in range(len(prods)):
        if ('EEE' in prods[j]):
            break
    prods.pop(j)
    cfgs[cfgs.index(cfg)] = symbol + ' -> ' + ' | '.join(list(dict.fromkeys(prods)))
    for j in range(len(cfgs)):
        if (symbol in cfgs[j]):
            desc = cfgs[j].split("->")
            symbol2 = desc[0].replace(' ','')
            prods2 = list(map(lambda x: x.replace('\n', '').replace('\r',''), desc[1].split("|")))
            for k in range(len(prods2)):
                if (symbol in prods2[k]):
                    x = list(filter(None,map(lambda x: x.replace(' ', '').replace('\n',''), prods2[k].split(" "))))
                    if (len(x) > 1):
                        z = 0
                        a = x.copy()
                        while (z < len(a)):
                            if (a[z] == symbol):
                                a.pop(z)
                                prods2 = remove_epsilon_rec(symbol, a, prods2)
                                prods2.append(' '.join(a))
                                a = a[:z] + [symbol] + a[z:] 
                            z += 1
                        cfgs[j] = symbol2 + ' -> ' + ' | '.join(list(dict.fromkeys(prods2)))
                    else:
                        prods2.append('EEE')
                        for z in range(len(prods2)):
                            if (symbol in prods2[z] and len(list(filter(None,prods2[z].split(" ")))) == 1):
                                break
                        prods2.pop(z)
                        cfgs[j] = symbol2 + ' -> ' + ' | '.join(list(dict.fromkeys(prods2)))
                        remove_epsilon_prod(cfgs[j])

def searchSym(symbol, cfg, visited):
    if (' '+symbol in cfg):
        return True
    elif (len(visited) == len(cfgs)):
        return False
    else:
        desc2 = cfg.split("->")
        symbol2 = desc2[0].replace(' ','')
        prods2 = list(map(lambda x: x.replace('\n', '').replace('\r','').split(' '), desc2[1].split("|")))
        vars_only = list(dict.fromkeys(filter(None, map(lambda x: x.replace(' ',''), [k for j in prods2 for k in j]))))
        for j in vars_only:
            if ("'" in j):
                vars_only.remove(j)
        found = False
        for var in vars_only:
            if (found):
                break
            if (var != symbol2):
                for cfg2 in cfgs:
                    if (cfg2.split("->")[0].replace(' ','').replace('\n','') == var and not(cfg2 in visited)):
                        found = searchSym(symbol,cfg2,visited+[cfg2])
                        break
        return found

def remove_useless_prod(cfg):
    desc = cfg.split("->")
    symbol = desc[0].replace(' ','')
    prods = desc[1].split("|")
    found = searchSym(symbol, cfgs[0],[cfgs[0]])
    if not(found):
        j = cfgs.index(cfg)
        cfgs.pop(j)

def help():
    print("Use: python cfg_to_cnf.py <filename> <flags>")
    print("-e <mode>   | default mode is on, use mode 'off' to deactive epsilon production removal")
    print("-u <mode>   | default mode is on, use mode 'off' to deactive useless production removal")

i = [0]
if (len(sys.argv) > 1):
    try:
        cfgs = list(filter(None,map(lambda x: x.replace('\n','').replace('\r',''),open(sys.argv[1],'r').readlines())))
    except:
        help()
    cnfs = []
    if ('-e' in sys.argv and sys.argv.index('-e') != 1 or not('-e' in sys.argv)):
        try:
            a = sys.argv.index('-e')
        except:
            a = 0
        if (a != len(sys.argv)-1):
            if (sys.argv[a+1] != 'off' or a == 0):
                for cfg in cfgs:
                    if ('EEE' in cfg):
                        remove_epsilon_prod(cfg)
                print('\n'.join(cfgs))
        else:
            help()
            exit()
    if ('-u' in sys.argv and sys.argv.index('-u') != 1 or not('-u' in sys.argv)):
        try:
            a = sys.argv.index('-u')
        except:
            a = 0
        if (a != len(sys.argv)-1 or a == 0):
            if (sys.argv[a+1] != 'off'):
                for cfg in cfgs[1:]:
                    remove_useless_prod(cfg)
                print('\n'.join(cfgs))
        else:
            help()
            exit()
    cnfs = [parsing_cfg(cfgs[0])] + cnfs
    for cfg in cfgs[1:]:
        #print(cfg)
        #print(cnfs)
        cnfs.append(parsing_cfg(cfg))
    cnfs = list(map(lambda x: x+ '\n', cnfs))
    '''
    for i in range(len(cnfs)):
        if ('S ' == cnfs[i][:2]):
            break
    start = [cnfs[i]]
    cnfs.pop(i)
    cnfs = start + cnfs
    '''
    open('grammar/chowsky','w').writelines(cnfs)