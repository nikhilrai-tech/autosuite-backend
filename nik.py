pip install bardapi
from bardapi import BardCookies

import datetime

cookie_dict={
    "__secure-1PSID": "bgiNas0Ggj5jT103CiGbi0rIJ-YkLt-z0ricoqkLn7HucnSvPl2bv65nw2lM7lLT04slbA.",
    "__secure-1PSIDTS": "ACA-OxONcAK589xU6QRMNRZLidDUSOu9VQX5FQzQ6ki4H2tK5whOVTWFkV4bCHSqoB0bIGl8UDw",
    "__secure-1PSIDCC": "ACA-OxMvTG-YRKvi8RuJDtO4oJAFxuJwAq8GopMQBPcc1AGnVLVyr2aBkCLfFD2tmyhkP_-xG8M",

}

bard=BardCookies(cookie_dict=cookie_dict)

while True: 
    query=input("hjghfhfds")
    reply=bard.get_answer(query)['content']
    print (reply)