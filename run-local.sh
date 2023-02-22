docker-compose -f docker-local-redis.yml up -d redis-vector-db
function stop() { docker-compose -f docker-local-redis.yml down ;}
trap stop EXIT

cd ./backend/vecsim_app
export DEPLOYMENT="dev"
export REDIS_HOST="localhost"
export REDIS_PORT=6379
export REDIS_PASSWORD="testing123"
export REDIS_DB=0
.//entrypoint.sh