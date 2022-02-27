dep:
	@pip3 install -r requirements.txt
up:
	@docker-compose up --force-recreate --build -d
stop:
	@docker-compose stop
