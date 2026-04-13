#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc
sshd
sleep 2
python -u ~/anggira.py >> ~/anggira.log 2>&1 &
sleep 3
python -u ~/dashboard.py >> ~/dashboard.log 2>&1 &
sleep 2
~/watchdog.sh &
