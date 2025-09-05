cd "Programming/CLI/gradefetch/.venv"
source bin/activate
cd ../
if [[ "$1" == "gb" ]]; then
    python main.py --gradebook --classID "$2"
else
python main.py
fi

