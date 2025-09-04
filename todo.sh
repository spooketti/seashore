cd "Programming/CLI/todo/.venv"
source bin/activate
cd ../
case $# in 
   2) 
      case $1 in 
      	"addCol")
	python main.py --addCol $2
	;;
        "rmCol")
	python main.py --rmCol $2
        ;;
      esac
      ;;
   3)
      echo 3
      ;;
   *) 
      python main.py
      ;;
esac

