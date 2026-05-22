

git config user.name "Mikhail Baltin"
git config user.email "balmikh2803@gmail.com"


docker network create freelance_network


docker rm -f freelance_db
docker run --name freelance_db \
    -p 7432:5432 \
    -e POSTGRES_USER=guest \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=freelance \
    --network=freelance_network \
    --volume pg-freelance-data:/var/lib/posgresql/data \
    -d postgres:16 \


docker rm -f freelance_cache
docker run --name freelance_cache \
    -p 8379:6379 \
    --network=freelance_network \
    -d redis:7.4 \

docker run --name freelance_rabbitmq \
    -p 5673:5672 \
    -p 15673:15672 \
    --network=freelance_network \
    -d rabbitmq:3-management


docker run --name freelance_back \
    -p 1337:8000 \
    --network=freelance_network \
    exchange_image


docker ps | grep rabbitmq


docker rm freelance_celery_worker
docker run --name freelance_celery_worker \
    --network=freelance_network \
    exchange_image \
    celery --app=src.celery_tasks.celery_app:celery_instance worker -l INFO