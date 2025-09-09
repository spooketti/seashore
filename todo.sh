cd "Programming/CLI/todo/.venv"
source bin/activate
cd ../
case $# in 
   1)
   case $1 in
     "clear")
     while true; do
         read -p "This will delete the entire sheet, continue? " yn
         case $yn in
            [Yy]* ) python main.py --clear; break;;
            [Nn]* ) exit;;
            * ) echo "No trolling, type y or n.";;
         esac
      done
     ;;
     "lsTable")
     python main.py --lsTable
     ;;
     "help")
     python main.py --help
     ;;
     esac
   ;;
   2) 
      case $1 in 
      	"addCol")
	python main.py --addCol "$2"
	;;
   "getTable")
     python main.py --getTable "$2"
     ;;
        "rmCol")
	python main.py --rmCol "$2"
        ;;
        "addTable")
	python main.py --addTable "$2"
	;;
        "rmTable")
	python main.py --rmTable "$2"
        ;;
        "setTable")
	python main.py --setTable "$2"
	;;
        *)
        warn "Unknown command"
      esac
      ;;
   3)
      case $1 in
        "write")
        python main.py --write "$2" --content "$3"
        ;;
        "erase")
        python main.py --erase "$2" --index "$3"
        ;;
        "editCol")
        python main.py --editCol "$2" --content "$3"
        ;;
      esac
      ;;
   4) 
   case $1 in
        "edit")
        python main.py --edit "$2" --index "$3" --content "$4"
        ;;
      esac
      ;;
   *) 
      python main.py
      ;;
esac

