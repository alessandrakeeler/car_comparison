NAME?=sloats

all:

images:
	- docker images | grep ${NAME}

ps:
	- docker ps -a | grep ${NAME}

build-db:
	docker pull redis:6

build-api:
	docker build -t ${NSPACE}/${APP}-api:${VER} \
		     -f docker/Dockerfile.api \
		     ./
build-wrk:
	docker build -t ${NSPACE}/${APP}-wrk:${VER} \
		     -f docker/Dockerfile.wrk \

run-db: build-db
	docker run --name ${NSPACE}-db \
		   -p ${NSPACE}-api \
		   -d \
		   -u ${UID}:${GID} \
		   -v ${PWD}/data/:/data \
		   redis:6 \
		   --save 1 1

run-api: build-api
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-api \
		   --env REDIS_IP=$${RIP} \
		   -p ${FPORT}:5000 \
		   -d \
		   ${NSPACE}/${APP}-api:${VER}

run-api: build-api
	RIP=$$(docker inspect ${NSPACE}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NSPACE}-api \
		   --env REDIS_IP=$${RIP} \
		   -d \
		   ${NSPACE}/${APP}-api:${VER}

stop-db:
	docker stop ${NSPACE}-db && docker rm -f ${NSPACE}-db || true


stop-api:
	docker stop ${NSPACE}-api && docker rm -f ${NSPACE}-api || true


stop-wrk:
	docker stop ${NSPACE}-wrk && docker rm -f ${NSPACE}-wrk || true

push-api:
	docker push ${NSPACE}/${APP}-api:${VER}

push-wrk:
	docker push ${NSPACE}/${APP}-wrk:${VER}

push-all: push-api push-wrk

stop-all: stop-db stop-api stop-wrk


