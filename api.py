import json.decoder

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends: # указан базовый url
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

# задаем валидные данные для входа в аккаунт в приложение с апи ключом на выходе
    def get_api_key(self, email: str, password: str) -> json:
        # Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным
        # ключом пользователя, найденного по указанным емейл и паролю
        headers = {
            'email' : email,
            'password' : password
        }
        res = requests.get(self.base_url+'api/key', headers = headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# запрос с валидным апи ключом для получения списка питомцев на выходе
    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        # Метод делает напро к FPI сервера и возвращает статус запроса и результат в формате JSON со списком найденных
        # питомцев совпадающих с фильтром, который может иметь или пустое значение или 'my_pets' - тоесть список
        # собственных питомцев

        headers = {'auth_key' : auth_key['key']}
        filter = {'filter' : filter}

        res = requests.get(self.base_url+'api/pets', headers = headers, params = filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_new_pet_with_photo(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        # Метод публикует на сервере данные о добавленном питомце и возвращает статус запроса  на сервер и результат
        # в формате JSON с данными добавленного питомца.
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers = headers, data = data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def post_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        # Метод публикует на сервере данные о добавленном питомце за исключением его фотографии и возвращает статус запроса на сервер
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def post_adding_photo_to_the_last_added_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        # Метод добавления фотографии к последнему добавленному своему питомцу по id
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers = headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        # Метод отправдлет на сервер запрос на удаление питомца по указанному ID и возращает статус запроса
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers = headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
    # Метод отправляет запрос на обновление информации о питомце по указанному ID и возвращает статус запроса
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers = headers, data = data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result