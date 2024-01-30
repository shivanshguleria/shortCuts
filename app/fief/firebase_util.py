def create_cred_dict(obj, objkeys):
    cred = dict()
    for i in range(len(objkeys)):
        cred[objkeys[i]] = obj[i]
    return cred
