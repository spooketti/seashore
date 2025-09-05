cd "Programming/CLI/todo/.venv"
source bin/activate
cd ../
case $# in 
   1)
   if [[ $1 == "clear" ]]; then
      while true; do
         read -p "This will delete the entire sheet, continue? " yn
         case $yn in
            [Yy]* ) python main.py --clear; break;;
            [Nn]* ) exit;;
            * ) echo "No trolling, type y or n.";;
         esac
      done
   fi
   ;;
   2) 
      case $1 in 
      	"addCol")
	python main.py --addCol "$2"
	;;
        "rmCol")
	python main.py --rmCol "$2"
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

