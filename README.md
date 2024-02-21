docker build -t pet_bot .
docker run --name pet_bot_container -d --rm pet_bot
docker kill pet_bot_container