import aiohttp
from models import Pet


PWD = 'true_secret_key'

# используй смайлики в ответе

CAT_PROMPT = "Напиши небольшое объявление на 4 или 6 предложений в приют о _animal_, котор_ending_ ищет хозяина на основе описания. Не указывай контактные данные и адрес приюта, не используй хештеги:"
DOG_PROMPT = "Напиши небольшое объявление на 4 или 6 предложений в приют о собаке, которая ищет хозяина на основе описания. Не указывай контактные данные и адрес приюта, не используй хештеги:"

DOG_1 = """
    new_description
🐶 Прекрасный мальчик ищет своего пушистого компаньона! 💕

🌟 Этот очаровательный песик - маленький коричневый красавчик, который обожает играть в мячик и гулять на прогулках! 🎾🏞️

✨Он уже приучен к лотку и будет отличным другом для целой семьи! Мягкий, дружелюбный и полон любви 🤗

👪Если вы хотите предоставить дому и душевное тепло этому замечательному малышу, пожалуйста, свяжитесь с нами! 📞📧

💐Он ждет искренней любви и заботы! Помогите этой чудесной собачке найти долгожданное счастье! 🏡💖
"""

CAT_1 = """
🐱❤️ Объявление! Ищем дом для нашего замечательного котика! 🏠🏡

Этот милый мальчик - настоящая находка! Он очень ласковый и дружелюбный 😻💕, готов стать верным другом на всю жизнь. К тому же, он уже приучен к лотку 🚽, так что проблем с уходом за ним не будет. 

Котик имеет коричневую шерсть, которая выглядит просто потрясающе! 🍂🌰 Уверены, что его окрас подчеркнет уют и теплоту вашего дома.

Если вы ищете нового пушистого члена семьи, который будет радовать вас своей прекрасной личностью, то этот котик - идеальный выбор! 💖

Обязательно приходите в наш приют и встретьтесь с этим прекрасным питомцем. Он ждет искреннего и заботливого хозяина, который даст ему свою любовь и ласку. 🏠❤️

Помните, что истинное счастье может начаться с нашего маленького котика. Уверены, что он станет вашим настоящим другом! 🐾😊
"""


def _get_prompt(pet: Pet):
    if pet.pet_type == 'cat':
        if pet.gender in ['мальчик', 'мужской']:
            prompt = CAT_PROMPT.replace('_animal_', 'коте')
            prompt = prompt.replace('_ending_', 'ый')
        else:
            prompt = CAT_PROMPT.replace('_animal_', 'кошке')
            prompt = prompt.replace('_ending_', 'ая')
    else:
        prompt = DOG_PROMPT

    # prompt = prompt + f' пол: {pet.gender}, ' 
    # if pet.name is not None:
    #     prompt += f' кличка {pet.name}, '
    # if pet.age is not None:
    #     prompt += f' возраст {pet.age}, '
        

    prompt = prompt + pet.prompt
        #prompt = CAT_PROMPT + '\n' + user_prompt
    # else:
    #     if pet.gender in ['мальчик', 'мужской']:
    #         prompt = CAT_PROMPT.replace('_animal_', 'собаке')
    #         prompt = prompt.replace('_ending_', 'ый')
    #     else:
    #         prompt = CAT_PROMPT.replace('_animal_', 'собаке')
    #         prompt = prompt.replace('_ending_', 'ая')

    print(f'PROMPT = {prompt}')
    return prompt


def get_prompt(pet: Pet):
    template = "Напиши небольшое объявление в приют о __animal__ на основе описания. Не указывай контактные данные, адрес приюта и имя животного, не используй хештеги: __gender__"
    if pet.pet_type == 'cat':
        if pet.gender == 'мальчик':  
            prompt = template.replace('__animal__', 'коте').replace('__gender__', 'хороший мальчик')
        else:
            prompt = template.replace('__animal__', 'кошке').replace('__gender__', 'хорошая девочка')
    else:
        if pet.gender == 'мальчик': 
            prompt = template.replace('__animal__', 'собаке').replace('__gender__', 'хороший мальчик')
        else:
            prompt = template.replace('__animal__', 'собаке').replace('__gender__', 'хорошая девочка')
    print(f'PROMPT = {prompt}')
    print('\n')
    prompt = prompt + ' ' + pet.prompt
    return prompt

# async def make_description(user_prompt: str, pet_type: str, smiles: bool = True):
async def make_description(pet: Pet, smiles: bool = True):
    # return DOG_1
    URL = 'http://162.248.227.166:4000/get_gpt_response'
    try:
        prompt = get_prompt(pet)
        async with aiohttp.ClientSession() as session:
            async with session.post(URL, json={"prompt": prompt, 'password': PWD}) as response:
                json = await response.json()
                if int(json.get('status')) == 200:
                    return json.get('description').replace('\n\n', '\n')
                else:
                    return None
                
    except Exception as e:
        print(f'Exception: {e}')
        if pet.pet_type == 'cat':
            prompt = CAT_1
        else:
            prompt = DOG_1

        return prompt