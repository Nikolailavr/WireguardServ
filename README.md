## Wireguarg

Приложение для быстрой настройки Wireguarg VPN

Для запуска понадобится Python v3.9

## Начало работы
<!-- termynal -->

```
sudo apt update && sudo apt upgrade -y
sudo apt install qrencode git wireguard python3-venv -y
git copy git@github.com:Nikolailavr/TestCopy.git
cd TestCopy
sh install.sh
```

## Запуск
<!-- termynal -->

```
source venv/bin/activate
python3 main.py data -o
```

