from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем API ключ и сохраняем в переменную auth_key. Далее используя этоn ключ
       запрашиваем список всех питомцев и проверяем, что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер', age='4', pet_photo='images/cat1.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
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


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Test 1
def test_add_pet_with_valid_data_without_photo(name='Фунтик_без_фото', animal_type='Кот', age='1'):
    """Проверяем возможность добавления нового питомца без фото"""
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name

# Test 2
def test_add_photo_at_pet(pet_photo='images/Funtik.jpg'):
    """Проверяем возможность добавления фотографии питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception('Питомцы отсутствуют')

# Test 3
def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='Собака', age='1', pet_photo='images/Karlson.jpg'):
    """Проверяем возможность добавления питомца с пустым значением в переменной name.
    Тест не будет пройден, если питомец будет добавлен в приложение с пустым значением в поле "Имя"."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] != '', 'Питомец добавлен в приложение с пустым значением в поле "Имя"'

# Test 4
def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='Кот', age='2', pet_photo='images/Karlson.jpg'):
    """Проверка с негативным сценарием.
    Добавления питомца с именем, которое превышает 10 слов.
    Тест не будет пройден если питомец будет добавлен в приложение с именем состоящим из более 10 слов"""

    name = 'Рыжик Пушок Снежок Ласка Василий Шнырь Профессор Киса Шибзик Пират'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с именем больше 10 слов'

# Test 5
def test_add_pet_with_a_lot_of_symbol_in_variable_name(animal_type='Кошка', age='0', pet_photo='images/Karlson.jpg'):
    """Добавления питомца с именем, которое имеет слишком длинное значение.
    Тест не будет пройден, если питомец будет добавлен в приложение с именем состоящим из 35 символов."""

    name = 'asnfHKrQJWSSWRSwSayyDFJxafmWIsutgdn'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    symbol_count = len(list_name)

    assert status == 200
    assert symbol_count < 10, 'Питомец добавлен с именем больше 35 символов.'

# Test 6
def test_add_pet_with_a_lot_of_age_in_variable_age(name='Karlson', animal_type='Кошка', pet_photo='images/Karlson.jpg'):
    """Добавления очень взрослого питомца с большим возрастом.
    Тест не будет пройден, если питомец будет добавлен в приложение с возрастом старше 15 лет."""

    age = '400'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = result['age'].split()
    age_count = len(age)

    assert status == 200
    assert age_count <= 15, 'Питомец добавлен с возрастом старше 15 лет.'

# Test 7
def test_add_pet_with_special_characters_in_variable_animal_type(name='Кашак', age='3', pet_photo='images/Karlson.jpg'):
    """Проверка с негативным сценарием.
    Добавление питомца с использованием специальных символов вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен в приложение со специальными символами вместо букв в поле "Порода"."""

    animal_type = 'Cat%@'
    symbols = '#$%^&*{}|?/><=+_~@'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] not in result['animal_type'], 'Питомец добавлен с недопустимыми специальными символами.'

# Test 8
def test_add_pet_with_numbers_in_variable_animal_type(name='Karlson', animal_type='89123', age='0', pet_photo='images/Karlson.jpg'):
    """Проверка с негативным сценарием.
    Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден, если питомец будет добавлен в приложение с цифрами вместо букв в поле "Порода"."""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен в приложение с цифрами вместо букв в поле "Порода".'

# Test 9
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Малыш', age='2', pet_photo='images/cat_snowshoe.jpg'):
    """Проверка с негативным сценарием.
    Добавления питомца с полем "Породы", которое превышает 10 слов.
    Тест не будет пройден, если питомец будет добавлен в приложение с названием породы состоящим из более 10 слов."""

    animal_type = 'Абиссинская Американская жесткошерстная Азиатская Австралийский Мист Балийская Турецкий Ван Шантильи-тиффани Сноу-шу'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен в приложение с названием породы больше 10 слов.'

# Test 10
def test_add_pet_with_a_lot_of_symbol_in_variable_animal_type(name='Karlson', age='2', pet_photo='images/Karlson.jpg'):
    """Добавления питомца с полем "Породы", которое имеет слишком длинное значение.
    Тест не будет пройден, если питомец будет добавлен в приложение с названием породы состоящим из 50 символов."""

    animal_type = 'QypIGnMnhFepDelGzbBbuEzxfrPHUvdKsPKlCrApxHSCnchktC'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    symbol_count = len(list_animal_type)

    assert status == 200
    assert symbol_count < 9, 'Питомец добавлен в приложение с названием породы из 50 символов.'

# Test 11
def test_get_api_key_with_correct_mail_and_wrong_passwor(email=valid_email, password=invalid_password):
    """Проверяем запрос с валидным e-mail и c невалидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Test 12
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    """Проверяем запрос с невалидным e-mail и с валидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

# Test 13
def test_get_api_key_with_wrong_email_and_wrong_password(email=invalid_email, password=invalid_password):
    """Проверяем запрос с невалидным e-mail и с невалидным паролем.
    Проверяем нет ли ключа в ответе."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result