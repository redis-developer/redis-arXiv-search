.PHONY: deploy

deploy:
	docker compose -f docker-local-redis.yml up
