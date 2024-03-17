import requests
import datetime
import pprint
import random
from test_lib import Test, genrate_random_string, newbody, style





url = "https://shrk.xyz/api"

response = requests.get(url)
print(response.json())
test1 = Test(url)

print(style.GREEN + "\n[0 : ⏳]\n")
token_req = test1.create_token()
token = token_req["json"]["token"]
print(style.GREEN + "[0]: ✔\n")
if token_req["status"] == 200:
    print(style.GREEN + "[1 : ⏳]" + "\n")
    create_link = test1.send_post_req("/link", link="https://robohash.org/" + genrate_random_string(30), token=token, short_link=genrate_random_string(8), schedule_link= (datetime.datetime.now() + datetime.timedelta(minutes=10)).isoformat())
    # print(res)
    # unique_id= res["json"]["unique_id"]
    # short_link = res["json"]["short_link"]
    if create_link['status'] == 201:
        print(style.GREEN + "[1]: ✔ "+ style.RESET + "Status code " + str(create_link['status']))
        print(style.GREEN + "\n[2 : ⏳]\n")
        for i in range(random.randint(1,10)):
            res = test1.send_dummy_req(create_link["json"]["short_link"])
            if res:
                print(style.GREEN + f"[2 : {i+1}]: ✔ \n" + style.RESET)

            else:
                print(style.RED + "[2]: ✘ " + style.RESET + "Status code " + str(create_link['status']) + "Error Occured " )
        print(style.GREEN + "\n[3 : ⏳]\n")
        get_link_count = test1.get_count(token=token, uid=create_link['json']['unique_id'])
        if get_link_count["status"] == 200:
            print("Response Body: ")
            pprint.pprint(get_link_count["json"] , width=80, indent=10)
            print(style.GREEN + "\n[3]: ✔" + style.RESET)
            print(style.GREEN + "\n[4 : ⏳]\n")
            for   i  in enumerate(range(5 - 2)):
                data = dict(list(newbody(token, create_link["json"]["unique_id"]).items())[:(i[1] + 3)])
                send_update_req = test1.update_link(data = data)
                if send_update_req == 204:
                    print(style.GREEN + f"[4 : {i[1]+1} ]: ✔ " + style.RESET + "\n")

                else:
                    raise Exception(style.RED + "[4]: ✘ " + style.RESET + "Status Code: " +str( send_update_req))
            print(style.GREEN + "[5 : ⏳]\n")
            res = test1.delete_link(token=token, unique_id= create_link["json"]["unique_id"])
            if res == 204:
                print(style.GREEN + "[5] ✔ " + style.RESET + "Deletion Success")
                last_req = test1.send_dummy_req(create_link["json"]["short_link"])
                last_count_req = test1.get_count(token=token, uid=create_link['json']['unique_id'])
                print("Run Exist test")
                print(style.RED + "✘" if not last_req else style.GREEN + "✔")
                print( last_count_req['json']  if  last_count_req['status'] != 200 else style.GREEN + "✔")
            else:
                raise Exception(style.RED + "[5]: ✘ " + style.RESET + "Status Code: " + str(res) )
        else:
            raise Exception(style.RED + "[3]: ✘ " + style.RESET + str(get_link_count["status"]) + "= 200")
    else:
        raise Exception(style.RED + "[1]: ✘" + style.RESET + "Status code " + str(create_link['status']) + "Error Occured " )
else:
    raise Exception(style.RED + "[0]: ✘ " + style.RESET + "Status code " + str(token_req['status']) +f"\nDetails: {str(token_req['json'])}" )+ ""
