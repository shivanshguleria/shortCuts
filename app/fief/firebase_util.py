def create_cred_dict(obj, objkeys):
    cred = dict()
    for i in range(len(objKeys)):
        cred[objKeys[i]] = obj[i]
    return cred
