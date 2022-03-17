dep:
	@pip3 install -r requirements.txt

clean:
	@docker rm monitor001 server001
	@docker rmi `docker images -q`

start:
	@docker-compose up --force-recreate --build -d
	
stop:
	@docker-compose stop

