import subprocess
import shutil
import os
from dataclasses import dataclass
import requests

import misc.const as const


@dataclass
class Key:
    private: str
    public: str

    def __init__(self, private='', public=''):
        self.private = private
        self.public = public


def generate_wireguard_keys(server: bool = False) -> Key:
    """
    Generate a WireGuard private & public key
    Requires that the 'wg' command is available on PATH
    Returns (private_key, public_key), both strings
    """
    if server:
        os.system("wg genkey | tee /etc/wireguard/server_private_key | wg pubkey | tee /etc/wireguard/server_public_key")
        privkey = subprocess.check_output("cat /etc/wireguard/server_private_key", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"cat /etc/wireguard/server_public_key", shell=True).decode("utf-8").strip()
    else:
        privkey = subprocess.check_output("wg genkey", shell=True).decode("utf-8").strip()
        pubkey = subprocess.check_output(f"echo '{privkey}' | wg pubkey", shell=True).decode("utf-8").strip()
    return Key(private=privkey, public=pubkey)


def get_IP() -> str:
    url = "https://ipwho.is/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('ip')
    except Exception as ex:
        print(ex)


def copy():
    shutil.copy2('wg0.conf', '/etc/wireguard/wg0.conf')
    print(f'Copied /etc/wireguard/wg0.conf')
    if os.path.exists('/etc/wireguard/clients'):
        print('Delete /etc/wireguard/clients...')
        os.system('rm -rf /etc/wireguard/clients')
        print('Deleting is ok!')
    shutil.copytree('clients', '/etc/wireguard/clients')
    print(f'Copied /etc/wireguard/clients')
    os.system('rm -rf clients')
    os.system('rm -rf wg0.conf')


def generate_configs(count_clients: int = 1) -> None:
    if not os.path.exists('clients'):
        os.mkdir('clients')
    server = generate_wireguard_keys(server=True)
    postup = ''
    postdown = ''
    for num in range(count_clients):
        postup += const.POSTUP.format(num=num+2) + '\n'
        postdown += const.POSTDOWN.format(num=num+2) + '\n'
    with open('wg0.conf', 'w') as file:
        text = const.SERVER_CONF.format(ServPrivateKey=server.private, PostUp=postup, PostDown=postdown)
        file.write(text)
        for num in range(count_clients):
            client = generate_wireguard_keys()
            text = const.PEER_CONF.format(PeerPublicKey=client.public, IP=num+2)
            file.write(text)
            with open(f'clients/client_{num+1}.conf', 'w') as client_conf:
                text = const.CLIENT_CONF.format(
                    IP=num+2,
                    PeerPrivateKey=client.private,
                    ServPublicKey=server.public,
                    ServerIP=get_IP()
                )
                client_conf.write(text)


def show_qr(num: str) -> None:
    try:
        os.system(f'qrencode -t ansiutf8 < /etc/wireguard/clients/client_{num}.conf')
    except Exception:
        raise Exception


def interactive():
    while True:
        try:
            os.system('clear')
            temp = input(const.ACTIONS)
            # os.system('clear')
            if temp == '1':
                count = 0
                try:
                    count = int(input('Введите количество клиентов: '))
                except:
                    ...
                generate_configs(count_clients=count)
                print('All Generated')
            elif temp == '2':
                copy()
                print(f'All files is copied')
            elif temp == '3':
                os.system('sh prototypes/start')
            elif temp == '4':
                show_qr(input('Введите номер клиента: '))
            elif temp == '5':
                os.system('sudo systemctl restart wg-quick@wg0')
                os.system('sudo systemctl status wg-quick@wg0')
            elif temp == '6':
                os.system('sudo systemctl stop wg-quick@wg0')
                os.system('sudo systemctl status wg-quick@wg0')
            elif temp == 'exit':
                break
            else:
                print(f'Нет такой команды: {temp}')
            input('Для продолжения нажмите Enter')
        except KeyboardInterrupt:
            break
        except Exception:
            break


if __name__ == '__main__':
    interactive()
    # get_IP()
    # copy()
