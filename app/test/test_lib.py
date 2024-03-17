import os,requests,pprint,json, random, string

os.system("")


pointer_for_is_preview = True
def newbody(token, uid): 
    global pointer_for_is_preview
    update_body = {
    "token": token,
    "unique_id": uid,
    "link": "https://robohash.org/" + genrate_random_string(30),
    "short_link": genrate_random_string(10),
    "is_preview": True if pointer_for_is_preview else False 
}
    pointer_for_is_preview = False if pointer_for_is_preview else True
    return update_body

def genrate_random_string(k = 5):
    return "".join(random.sample(string.ascii_letters, k = k))

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    GET = '\033[34m'
    MAGENTA = '\033[35m'
    POST = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'



class Test:
    def __init__(self,url, path="") -> any:
        self.path = path
        self.url = url
    def send_req(self, path, type=0):
        if type:
            print("       "+  style.GET + "Sent GET req at: " + style.BLACK + self.url[:-4] + path)
            print(style.RESET)
            response = requests.get(self.url[:-4] + path)
        else:
            print( "       " + style.GET + "Sent GET req at: " + style.BLACK + self.url + path)
            print(style.RESET)
            response = requests.get(self.url + path)
        return response
    
    def send_post_req(self, path="", **kwargs):
        print(style.GREEN+ "[INFO] " + style.MAGENTA + "Sending Link creation request with " + style.YELLOW + "Request Body: " + style.RESET + "\n")
        pprint.pprint(kwargs , width=80, indent=4)
        print()
        print(style.GREEN+ "[INFO] " + style.POST + "Sent POST req at: " + style.BLACK + self.url + path)
        print(style.RESET)
        response = requests.post(self.url + path, data=json.dumps(kwargs))
        if response.status_code == 201:
            return {
                "status": response.status_code,
                "json": response.json()
            }
        else:
            return {"err": response.json()}
    def send_dummy_req(self, code:str):
        print(style.GREEN+ "[INFO] " + style.MAGENTA + "Sending Dummy Request" + style.RESET)
        res = self.send_req("/"+code, type=1)
        return res.ok
    
    def get_count(self, **kwargs):
        print(style.GREEN+ "[INFO] " +  style.MAGENTA + "Sending Count Request" + style.RESET)
        response = self.send_req("/count/" + kwargs["token"] + "/" + kwargs["uid"])
        return {
                "status": response.status_code,
                "json": response.json()
            }
    def create_token(self):
        print(style.GREEN+ "[INFO] " +  style.MAGENTA + "Sending Token Creation Request" + style.RESET)
        response = self.send_req(path="/token")


        return {
                "status": response.status_code,
                "json": response.json()
            }

    def delete_link(self, **kwargs):
        print(style.GREEN+ "[INFO] " +  style.MAGENTA + "Sending Link Deletion Request" + style.RESET)
        res = requests.delete(self.url + "/delete", data=json.dumps(kwargs))
        return res.status_code
    def update_link(self, **kwargs):
        print(style.GREEN+ "[INFO] " +  style.MAGENTA + "Sending Updation Request with " + style.YELLOW + "Request Body: " + style.RESET + "\n")
        pprint.pprint(kwargs["data"] , width=80, indent=4)
        print(style.RESET)
        res = requests.put(self.url + "/update", data=json.dumps(kwargs['data']))
        # print(res.json())
        return res.status_code
    # def create_link(self, link, token, short_link="", is_preview=False, schedule_delete=""):
    #     self.create_link(path="/link", token=token, short_link=)
