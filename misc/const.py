SERVER_CONF = """
[Interface]
Address = 172.16.0.1/24
ListenPort = 51830
PrivateKey = {ServPrivateKey}
SaveConfig = false
PostUp = iptables -I FORWARD -i %i -j ACCEPT
PostUp = iptables -I FORWARD -o %i -j ACCEPT
{PostUp}
PostDown = iptables -D FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -o %i -j ACCEPT
{PostDown}
Table = off
"""

POSTUP = "PostUp = ip route add 192.168.{num}.0/24 via 172.16.0.{num} dev %i"
POSTDOWN = "PostDown = ip route delete 192.168.{num}.0/24 via 172.16.0.{num} dev %i"

PEER_CONF = """
[Peer]
PublicKey = {PeerPublicKey}
AllowedIPs = 172.16.0.{IP}/32,192.168.{IP}.0/24
"""

CLIENT_CONF = """
[Interface]
PrivateKey = {PeerPrivateKey}
Address = 172.16.0.{IP}/24
DNS = 8.8.8.8

[Peer]
PublicKey = {ServPublicKey}
Endpoint = {ServerIP}:51830
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""

ACTIONS = """
Выберете что нужно сделать:
1 - Создать файлы конфигурации
2 - Скопировать файлы
3 - Инициализация сервера
4 - Показать QR код для клиента
5 - Restart server
6 - Stop server
exit - Exit
"""