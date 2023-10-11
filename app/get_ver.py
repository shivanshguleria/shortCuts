import requests

def get_version():
    headers =  {
    'User-agent': "shivanshguleria"
  }
    r = requests.get('https://api.github.com/repos/shivanshguleria/shortCuts/git/ref/heads/dev',headers=headers)
    body = r.json()
    if r.status_code == 200:
        r = requests.get(body.get("object").get("url"), headers=headers)
        if r.status_code == 200:
            body = r.json()
            res = body.get('message').split('\n')
            return res[0]
    else:
        return ":("

print(get_version())