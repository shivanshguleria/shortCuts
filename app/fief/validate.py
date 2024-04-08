import validators


# text = "https://www.ibm.com/docs/en/rational-clearquest/9.0.1?topic=tags-meta-characters-in-regular-expressions"


def validate_link(link: str):
    if not link: 
        return False
    if link[:4] == "/esc":
        return True
    if validators.url(link):
        return True 
    else:
        return False

