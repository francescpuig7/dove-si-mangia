import json
from random import randint


def get_messages(ppal, key):
    f = open('reply_text.json')
    data = json.load(f)
    data = data[ppal]
    val = data.pop(key, 'Ops! Messagio non trovato')
    f.close()
    return val


def get_list_restaurants():
    f = open('reply_text.json')
    data = json.load(f)
    data = data['restaurants']
    f.close()
    return data


def get_random_restaurant(last_key):
    f = open('reply_text.json')
    data = json.load(f)
    data = data['restaurants'][last_key]
    key = randint(1, len(data))
    val = data.pop(str(key), 'Ops! Messagio non trovato')
    f.close()
    return val


def update_json_new_restaurant(new_restaurant, username):
    f = open('reply_text.json')
    data = json.load(f)
    key = str(len(data['restaurants']) + 1)
    if "https://goo.gl/maps/" not in new_restaurant and 'maps.app.goo.gl' not in new_restaurant:
        print(new_restaurant)
        return "Ops! Link non valido, devi fornire un link con formato https://goo.gl/maps/<id>"
    f.close()
    data['restaurants'][key] = new_restaurant
    print(data)
    with open('reply_text.json', 'w') as outfile:
        json.dump(data, outfile)

    return "Ok, ho capito, grazie per farmi imparare nuovi posti!"
