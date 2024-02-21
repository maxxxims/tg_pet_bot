import phonenumbers


def validate_phone_number(phone_number: str):
    try:
        phone_number = phone_number.replace(' ', '')
        phone_number_with_code = '+7'
        if phone_number.startswith('8'):
            phone_number_with_code += phone_number[1:]
        else:
            phone_number_with_code = phone_number
        
        number = phonenumbers.parse(phone_number_with_code)
        is_correct = phonenumbers.is_possible_number(number)
        
        return is_correct

    except Exception as e:
        return False