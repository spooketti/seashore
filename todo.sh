cd "Programming/CLI/todo/.venv"
source bin/activate
cd ../
case $# in 
   2) 
      case $1 in 
      	"addCol")
	python main.py --addCol "$2"
	;;
        "rmCol")
	python main.py --rmCol "$2"
        ;;
      esac
      ;;
   3)
      case $1 in
        "write")
        python main.py --write "$2" --content "$3"
        ;;
        "erase")
        python main.py --erase "$2" --content "$3"
        ;;
      esac
      ;;
   *) 
      python main.py
      ;;
esac

