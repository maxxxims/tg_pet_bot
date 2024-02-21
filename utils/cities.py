
cities_array = []
city_id2name = {}

with open('utils/cities.txt', 'r', encoding='utf-8') as file:
    for i, city in enumerate(file.read().split('\n')):
        corrected_city_name = city.replace('-', '').replace(' ', '').lower()
        cities_array.append(corrected_city_name)
        city_id2name[corrected_city_name] = city

# print(cities_array[100])
# town = 'Электросталь'.lower()
# print(town in cities_array)
        

def validate_city(city: str):
    if not isinstance(city, str):
        return False
    correct_city = city.replace('-', '').replace(' ', '').lower()
    if correct_city in cities_array:
        return True
    else:
        return False


def get_corrected_city(city: str):
    if not isinstance(city, str):
        return ''
    correct_city = city.replace('-', '').replace(' ', '').lower()
    if correct_city in cities_array:
        return city_id2name[correct_city]
    else:
        return ''


def get_city_id(city: str) -> int:
    if not isinstance(city, str):
        return -1
    correct_city = city.replace('-', '').replace(' ', '').lower()
    if correct_city in cities_array:
        return city_id2name[correct_city]
    else:
        return -1
    


def get_city_by_id(id: int) -> int:
    if id < 0 or len(cities_array):
        return ''
    
    else:
        return cities_array[i]
    


if __name__ == "__main__":
    s = 'москва'

    res = get_corrected_city(s)

    print(f'res = {res}')