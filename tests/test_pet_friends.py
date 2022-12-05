# (200, {'key': '7d221932ca53f6c09807110a47d3df83d9d0b94fc26983110c26d758'})
import os.path
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()

def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    # Тест получения auth_key с валидными данными пользователя
    status, result = pf.get_api_key(email, password)
    # Проверка того что статус ответа апи возвращает код 200 (т.к. данные валидны) и в результате содержится слово key
    assert status == 200
    assert 'key' in result
    print(result)

def test_get_api_key_invalid_user(email=invalid_email, password=invalid_password):
    # Тест получени auth_key с не валидными данными пользователя
    status, result = pf.get_api_key(email, password)
    # Проверяем статус ответа(должен быть 403, т.к. введены некорректные почта и пароль)
    # и в результате не содержится слово key
    assert status == 403
    assert 'key' not in result
    print(status, result)

def test_get_all_pets_with_valid_key(filter = ''):
    # Тест получения списка всех питомцев сайта при вводе валидного auth_key
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    #Проверяем что статус ответа 200 и что запрос всех питомцев возвращает не пустой список
    assert status == 200
    assert len(result['pets']) > 0
    print(result)

def test_get_all_pets_with_invalid_key(filter = ''):
    # Тест получения списка всех питомцев сайта при вводе не валидного апи ключа
    # Запрос auth_key, сохранение в переменную и добавление питомца
    auth_key = {'key': str(range(56))}
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Проверяем статус ответа(должен быть 403, т.к. введен не верный auth_key). Выводим текст ошибки
    assert status == 403
    print(result)

def test_post_new_pet_with_photo_valid_data(name = "Ktulh", animal_type = "hton", age = "6", pet_photo = "images/ktulha.jpg"):
    # Тест добавлеия питомца с фото с корректными данными
    # Получение полного пути к фотографии питомца и сохранение в перременную
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрос auth_key и сохранение в переменную
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление питомца
    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    # Проверяем статус ответа(ожидается 200 т.к. данные валидны) и получаем ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_with_photo_invalid_pet_photo_format(name = "Fluffy", animal_type = "hton", age = "0", pet_photo = "images/Fluffy.pdf"):
    # Тест добавлеия питомца с фото в неверном формате
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    # Проверяем статуса ответа(должен быть 400 - т.к. введенные данные не верны(фотография питомца в недопустимом формате))
    # и полученного ответа с ожидаемым результатом. Если тест pass, значит недопустимый формат фотографии не вызвал ошибки
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_without_photo_valid_data(name = "Bun", animal_type = "kitten", age = "20"):
    # Проверка добавления питомца пост запросом без добавления фото с корректными данными
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем статуса ответа(ожидается 200 т.к. данные валидны) и получение ответа с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_without_photo_no_data(name = "", animal_type = "", age = ""):
    # Проверка добавления питомца пост запросом без добавления фото с пустыми значениями данных питомца
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем статус ответа(должен быть 400 - т.к. введенные данные не верны(заданы пустые строки))
    # и получение ответа с ожидаемым результатом. Если тест pass, значит пустые значения не вызвали ошибки
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_without_photo_negative_age(name = "Bon-bon", animal_type = "kitten", age = "-100"):
    # Проверка добавления питомца пост-запросом без добавления фото с отрицательным возрастом(невозможное значение)
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем статус ответа(должен быть 400 - т.к. введенные данные не верны(отрицательный возраст))
    # и получение ответа с ожидаемым результатом. Если тест pass, значит отрицательный возраст питомца не вызвали ошибки
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_without_photo_wrong_age(name = "Banana ", animal_type = "villain", age = "десять"):
    # Проверка добавления питомца пост запросом без добавления фото с возрастом написанном словами
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем статус ответа(должен быть 400 - т.к. введенные данные не верны(отрицательный возраст)) и получение ответа
    # с ожидаемым результатом. Если тест pass, значит возраст питомца записанный словами не вызвали ошибки
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_new_pet_without_photo_impossibly_old(name = "Banshy ", animal_type = "villain", age = "90000000000000"):
    # Проверка добавления питомца пост запросом без добавления фото с невозможно большим для питомца возрастом
    # Запрос auth_key, сохранение в переменную и добавление питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet_without_photo(auth_key, name, animal_type, age)
    # Проверяем статус ответа(должен быть 400 - т.к. введенные данные не верны(слишком большой возраст)) и получение
    # ответа с ожидаемым результатом. Если тест pass, значит слишком большой возраст питомца не вызвали ошибки
    assert status == 200
    assert result['name'] == name
    print(result)

def test_post_adding_photo_to_the_last_added_pet_valid_data_and_id(pet_photo = "images/Fluffy.jpg"):
    # Проверка добавления к последнему своему питомцу фотографии корректного формата по ID
    # Получение полного пути к фотографии питомца и сохранение в перременную
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Получаем auth_key и списка собственных питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берем id последнего добавленного питомца(будет первым в списке) и осуществляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_adding_photo_to_the_last_added_pet(auth_key, pet_id, pet_photo)
    # Проверяем статус ответа(должен быть равен 200, т.к. данные верны) и полученного ответа с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != 0
    print(result)

def test_delete_pet_valid_id():
    # Проверка возможности удаления собственных питомцев
    # Получаем auth_key и список собственных питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список питомцев пуст - добавляем нового и снова запрос списка
    if len(my_pets['pets']) == 0:
        pf.post_new_pet_with_photo(auth_key, "Ktulh", "hton", "666", "images/ktulha.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берем id последнего добавленного питомца(будет первым в списке) и осуществляем запрос на его удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Повторный запрос списка питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем статус ответа(должен быть равен 200, т.к. данные верны) и что в списке питомцев нет id удаленного питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_not_mine_pet():
    # Проверка возможность удаления питомца который не является собственным питомцем пользователя
    # Получаем auth_key и запрашиваем список питомцев(в целом по сайту, не только своих)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, filt = pf.get_list_of_pets(auth_key, "")
    # Берем id последнего добавленного питомца(будет первым в списке) и осуществляем запрос на его удаление
    pet_id = filt['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Повторный запрос списка питомцев
    _, filt = pf.get_list_of_pets(auth_key, "")
    # Проверяем статус ответа(должен быть 403. По документации - данный код ошибки возникает если применен неверный
    # auth_key,если я не являюсь владельцем карточки питомца - мой ключ должен восприниматься как неверный) и что в
    # списке питомцев нет id удаленного питомца. Если тест pass, значит сайт позволяет удалять не принадлежащие
    # пользователю карточки питомцев
    assert status == 200
    assert pet_id not in filt.values()

def test_update_pet_info_valid_id(name = "Ktulh", animal_type = "котик", age = "666"):
    # Проверка возможности обновления информации о питомце
    # Получаем auth_key и список собственных питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список питомцев не пустой - пробуем обновить информацию о питомце
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверка статуса ответа(должен быть 200, т.к. данные верны) и что имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пуст то должно вывестись исключение с текстом о том что собственных питомцев нет
        raise Exception("There is no my pets")
    print(result)

