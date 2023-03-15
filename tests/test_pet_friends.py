import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)

    assert status == 200
    assert len(result['pets']) > 0


# Test 1
@pytest.mark.mine
def test_add_new_pet_simple(name='Змеюка', animal_type='змея', age='124'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_update_self_pet_info(name='Мурзик', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Test 2
@pytest.mark.mine
def test_add_photo_to_pet(pet_photo='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    assert status == 200


def test_add_new_pet_with_valid_data(name='Кэт', animal_type='кот', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# Test 3
@pytest.mark.mine
def test_get_api_key_for_invalid_mail_password(email=invalid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа на несуществующие email и пароль возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# Test 4
@pytest.mark.mine
def test_get_api_key_for_invalid_mail(email=invalid_email, password=valid_password):
    """ Проверяем, что запрос api ключа на некорректный email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# Test 5
@pytest.mark.mine
def test_get_api_key_for_invalid_mail(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа с указанием только email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403


# Test 6
@pytest.mark.mine
def test_add_new_pet_with_not_numerical_age(name='Кэт', animal_type='кот', age='hy', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректным типом данных для поля 'возраст'"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key_n = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key_n, name, animal_type, age, pet_photo)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 7
@pytest.mark.mine
def test_add_new_pet_with_age_negative(name='Кэт', animal_type='кот', age='-14', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key_n = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key_n, name, animal_type, age, pet_photo)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 8
@pytest.mark.mine
def test_add_new_pet_without_name(name='', animal_type='кот', age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с не указанным именем"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key_n = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key_n, name, animal_type, age, pet_photo)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 9
@pytest.mark.mine
def test_add_new_pet_without_type(name='Кузьма', animal_type='', age='2', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с не указанным типом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key_n = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key_n, name, animal_type, age, pet_photo)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 9
@pytest.mark.mine
def test_add_new_pet_simple_without_name(name='', animal_type='змея', age='124'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 10
@pytest.mark.mine
def test_add_new_pet_simple_without_type(name='Кобра', animal_type='', age='124'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 11
@pytest.mark.mine
def test_add_new_pet_simple_with_age_negative(name='Кобра', animal_type='змея', age='-124'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403


# Test 12
@pytest.mark.mine
def test_update_self_pet_info_with_age_negative(name='Мурзик', animal_type='Кот', age=-55):
    """Обновление информации о питомце, возраст отрицательный"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

    if status != 403:
        print("\n\n******************\n\nБаг!\n\n******************")

    assert status == 403
    assert result['name'] == name

