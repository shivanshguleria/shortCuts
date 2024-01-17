is_dev = False
def handle_print(args):
    if is_dev:
        print(args)
    else:
        print("IN Prod")