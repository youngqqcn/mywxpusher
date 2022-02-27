dep:
	@pip3 install -r requirements.txt

start:
	@docker-compose up --force-recreate --build -d
	
stop:
	@docker-compose stop
