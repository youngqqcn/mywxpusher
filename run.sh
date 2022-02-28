nohup python monitor.py > /var/log/monitor.log  2>&1 &
nohup python server.py > /var/log/server.log  2>&1 &

# just keep this script running
while [[ true ]]; do
    sleep 1
done