docker-compose -f docker-compose.yml up -d --build rabbitmq

docker-compose -f docker-compose.yml up -d --build bot_database

DATABASE_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' bot_database) 

echo $DATABASE_IP

DATABASE_IP=$DATABASE_IP docker-compose -f docker-compose.yml up -d --build birthday_manager

DATABASE_IP=$DATABASE_IP docker-compose -f docker-compose.yml up -d --build monster_game

docker-compose -f docker-compose.yml up -d --build discord_listener