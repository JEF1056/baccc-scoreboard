home_dir="PATH-TO-REPO"
cert="PATH-TO-FULLCHAIN.PEM"
key="PATH-TO-PRIVKEY.PEM"
password="USER-PASSWORD"

cd $home_dir
git reset --hard
git pull
tmux kill-server
tmux new-session -d -n serve
tmux send-keys -t serve "sudo fuser -k 443/tcp" Enter
tmux send-keys -t serve $password Enter
sleep 1
tmux send-keys -t serve "cd $home_dir" Enter
tmux send-keys -t serve "sudo -H pip3 install -U -r requirements.txt" Enter
tmux send-keys -t serve "sudo gunicorn --certfile=$cert --keyfile=$key main:app --bind 0.0.0.0:443" Enter