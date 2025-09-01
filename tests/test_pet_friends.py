from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_add_new_pet_without_photo(name='Бося', animal_type='такса', age='6'):
    """Проверяем что можно добавить питомца с корректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_successful_add_pet_photo(pet_photo='images/P1040103.jpg'):
    """Проверяем возможность добавления фото для питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Бося", "такса", "6")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert result['name'] == my_pets['pets'][0]['name']

def test_add_pet_invalid_photo_format(pet_photo='images/Cat2.bmp'):
    """Проверяем что нельзя добавить фото для питомца формата отличного от JPG, JPEG"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Бося", "такса", "6")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 400

def test_add_new_pet_with_invalid_name(name='"""@#"""', animal_type='такса', age='6'):
    """Проверяем что нельзя добавить питомца с некорректными данными в поле name """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400

def test_add_new_pet_with_invalid_animal_type(name='Бося', animal_type='!!<<>>@@#', age='6'):
    """Проверяем что нельзя добавить питомца с некорректными данными в поле animal_type """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400

def test_add_new_pet_with_negative_age(name='Бося', animal_type='такса', age='-4000'):
    """Проверяем, что нельзя добавить питомца с отрицательным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400

def test_get_api_key_for_invalid_user(email='user1@mail.com', password="12345"):
    """ Проверяем что запрос api ключа возвращает статус 403 при передаче несуществующего юзера"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

def test_get_all_pets_with_invalid_authkey(filter=''):
    """ Проверяем что запрос всех питомцев с невалидным токеном возвращает 403 ошибку.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее изменяем этот ключ
    запрашиваем список всех питомцев и проверяем что нам возвращается."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = auth_key.pop('key')[1::]
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403

def test_get_all_pets_with_invalid_filter(filter='my-pets'):
    """ Доступное значение параметра filter - 'my_pets' либо ''. Проверяем недопустимые значения поля фильтр
    """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_update_pet_info_with_invalid_pet_id(name='Тося', animal_type='шпиц', age=2):
    """Проверяем возможность обновления информации о питомце c невалидным pet_id"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, "123", name, animal_type, age)

        assert status == 400
    else:
        raise Exception("There is no my pets")

