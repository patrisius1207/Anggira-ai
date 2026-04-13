#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc

while true; do
    if ! pgrep -f anggira.py > /dev/null; then
        echo "$(date) - Anggira mati, restart..." >> ~/watchdog.log
        python -u ~/anggira.py >> ~/anggira.log 2>&1 &
    fi
    sleep 30
done
