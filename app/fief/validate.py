import re



# text = "https://www.ibm.com/docs/en/rational-clearquest/9.0.1?topic=tags-meta-characters-in-regular-expressions"


def validate(link: str):
    print(re.match(r"(https://|http://)\w+\.\w+\.\w", link))
    if re.match(r"(https://|http://)\w+\.\w+\.\w", link):
        return True 
    else:
        return False