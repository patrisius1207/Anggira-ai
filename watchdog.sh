#!/data/data/com.termux/files/usr/bin/bash
source ~/.bashrc

while true; do
    # --- Pantau Anggira AI ---
    if ! pgrep -f "anggira.py" > /dev/null; then
        echo "$(date) - Anggira mati, restart..." >> ~/watchdog.log
        python -u ~/anggira.py >> ~/anggira.log 2>&1 &
    fi

    # --- Pantau Dashboard ---
    if ! pgrep -f "dashboard.py" > /dev/null; then
        echo "$(date) - Dashboard mati, restart..." >> ~/watchdog.log
        python ~/dashboard.py >> ~/dashboard.log 2>&1 &
    fi

    sleep 30
done
