import random
def find_priority(role):
    '''
    Given role of the user, this function will find priority of that particular user
    '''
    return random.randint(1,3)

def find_priority_of_request(reqID,username):
    pr = 0
    if username == "admin":
        pr += 5
    pr += reqID
    return pr    