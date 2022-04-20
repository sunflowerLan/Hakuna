import json

dd = {
    'name': 'zhangsan',
    'age': 23
}

print('dict: ', dd, type(dd))

sd = str(dd)
print('str: ', sd, type(sd))


dictTostr = json.dumps(dd)
print('dictTostr: ', dictTostr, type(dictTostr))

strTodict1 = json.loads(json.dumps(dd))
print('strTodict1: ', strTodict1, type(strTodict1))


eval_s = eval(sd)
print('eval_s:', eval_s, type(eval_s))

strTodict2 = json.loads(json.dumps(eval(sd)))
print('strTodict2: ', strTodict2, type(strTodict2))


tt = {
    "name": "zhangsan",
    "age": 23
}

print('tt: ', tt, type(tt))