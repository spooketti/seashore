cd "Programming/CLI/gradefetch/.venv"
source bin/activate
cd ../

if [[ "$#" == 3 ]]; then
  case "$1" in

  graph)  python main.py --graph --startDate "$2" --endDate "$3";;
  *)
    exit 1
    ;;
esac
exit 0
fi

case "$1" in

  gb)  python main.py --gradebook --classID "$2";;
  graph) python main.py --graph;;
  *)
    python main.py
    ;;
esac