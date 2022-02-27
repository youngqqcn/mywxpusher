dep:
	@pip3 install -r requirements.txt

start:
	@nohup python3 monitor.py >> logfile.log 2>&1 &

docker-up:
	docker-compose up