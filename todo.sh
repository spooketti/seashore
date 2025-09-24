cd "Programming/CLI/todo/.venv"
source bin/activate
cd ../

confirm() {
    local prompt="$1"
    while true; do
        read -rp "$prompt [y/n] " yn
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            *) echo "No trolling, type y or n." ;;
        esac
    done
}

case "$1" in
  clear)
    confirm "This will delete the entire sheet, continue?" &&
      python main.py --clear
    ;;

  lsTable)  python main.py --lsTable ;;
  help)     python main.py --help ;;
  addCol)   python main.py --addCol "$2" ;;
  getTable) python main.py --getTable "$2" ;;
  rmCol)    python main.py --rmCol "$2" ;;
  addTable) python main.py --addTable "$2" ;;
  rmTable)
    confirm "This will delete the table, continue?" &&
      python main.py --rmTable "$2"
    ;;
  setTable) python main.py --setTable "$2" ;;
  color)    python main.py --color "$2" --index "$3" --content "$4" ;;
  write)    python main.py --write "$2" --content "$3" ;;
  erase)    python main.py --erase "$2" --index "$3" ;;
  editCol)  python main.py --editCol "$2" --content "$3" ;;
  edit)     python main.py --edit "$2" --index "$3" --content "$4" ;;
  *)
    python main.py "$@"
    ;;
esac
