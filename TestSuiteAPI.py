import os
from api import PetFriends
from settings import email, password

pet_friends = PetFriends()


def test_get_api(email=email, password=password):
    """Проверка получения ключа API"""
    status, result = pet_friends.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_list(filter='my_pets'):
    """Проверка получения списка питомцев с фильтром 'мои питомцы'"""
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.get_list_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    assert len('my_pets') > 0


def test_post_new_pet(name='Charlie', animal_type='хаски', age='11', pet_photo='images/huski1.jpg'):
    """Проверка возможности добавить нового питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pet_friends.get_api_key(email, password)
    status, result = pet_friends.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status is 200
    assert result['name'] == name


def test_delete_pet():
    """Проверка удаления существующего питомца по его id"""
    _, auth_key = pet_friends.get_api_key(email, password)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    # if len(my_pets['pets']) == 0:
    #     pet_friends.post_new_pet(auth_key, 'Жулька', 'crocodile', '22', 'images/husk2.jpeg')
    #     _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pet_friends.delete_pet(auth_key, pet_id)

    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    print(my_pets['pets'])
    assert status is 200
    assert pet_id not in my_pets.values()

# получение id и name моих питомцев
# def test_get_my_list(filter='my_pets'):
#     _, auth_key = pet_friends.get_api_key(email, password)
#     _, my_pets = pet_friends.get_list_pets(auth_key, filter)
#     pets = my_pets.get('pets')
#     for el in pets:
#         print(el['name'], el['id'])


def test_update_info(name='Мурзилка', animal_type='дикая чеширская', age='22'):
    """Проверка обновления информации о питомце по его id"""
    _, auth_key = pet_friends.get_api_key(email, password)
    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][-1]['id']
    if len(my_pets['pets']) > 0:
        status, result = pet_friends.update_info(auth_key, pet_id, name, animal_type, age)

    _, my_pets = pet_friends.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name
