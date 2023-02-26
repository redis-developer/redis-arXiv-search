set -eux

pwd0=$(pwd)  # initial working dir
DOCKER_COMPOSE=${DOCKER_COMPOSE:-docker compose}  # on some Mac machines, it's docker-compose
$DOCKER_COMPOSE -f docker-local-redis.yml up --detach --wait redis-vector-db
function stop() { $DOCKER_COMPOSE -f $pwd0/docker-local-redis.yml down ;}
trap stop EXIT  # stop containers when finish

cd ./backend/vecsim_app
export DEPLOYMENT="dev"
export REDIS_HOST="localhost"
export REDIS_PORT=6379
export REDIS_PASSWORD="testing123"
export REDIS_DB=0
./entrypoint.sh
