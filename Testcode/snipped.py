import time
refreshlist_tempreader = list(range(0,61,5))
refreshlist_weather = list(range(0,61,1))


print(refreshlist_weather, refreshlist_tempreader)

while True:

    if int(time.strftime('%S')) in refreshlist_tempreader:
        print(f'refreshing {int(time.strftime("%S"))}')

    if int(time.strftime('%M')) in refreshlist_weather and int(time.strftime('%S')) == 1:
        print(f"refreshing minute {int(time.strftime('%M'))}")
    


    time.sleep(0.8)
