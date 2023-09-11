from json import load
from enum import Enum
from subprocess import check_output
from re import findall, RegexFlag
from os import path
from requests import post, Response


class UrlMethod(Enum):
    POST = "POST"


def json_decoder(json_dict: dict):
    """
    JSON decoder
    :param json_dict:
    :return:
    """
    if 'method' in json_dict:
        json_dict['method'] = UrlMethod(json_dict['method'])
    if 'name' in json_dict:
        return Connector(json_dict['name'], json_dict['url'], json_dict['SSID'], json_dict['method'], json_dict['body'])
    return json_dict


class Connector:
    def __init__(self, name: str, url: str, ssid: str, method: UrlMethod, body: dict) -> None:
        self._name = name
        self._url = url
        self._SSID = ssid
        self._method = method
        self._body = body

    @property
    def name(self) -> str:
        return self._name

    def does_match_current_wifi(self) -> bool:
        """
        Check if the current connected Wi-Fi is the same as this one
        :return: bool
        """
        netsh_interfaces = check_output('netsh wlan show interfaces').decode("cp850")
        ssid_match = findall(r'^\s*SSID\s*.:\s([^\n\r]+)', netsh_interfaces, RegexFlag.MULTILINE | RegexFlag.DOTALL)
        ssid = ssid_match[0] if len(ssid_match) > 0 else None
        return ssid is not None and ssid == self._SSID

    def send_request(self) -> Response:
        """
        Send request to URL with body
        :return:
        """
        if self._method is UrlMethod.POST:
            return post(self._url, self._body)


def main() -> None:
    """
    Main function
    :return: None
    """

    # Read config file
    if not path.isfile('config.json'):
        print("Config file not found")
        return

    with open('config.json') as config_file:
        config = load(config_file, object_hook=json_decoder)

    # Get all sections
    for connector in config["sections"]:
        connector: Connector = connector
        if connector.does_match_current_wifi():
            print(f"Section {connector.name} matches current Wi-Fi")
            res = connector.send_request()
            print(res.status_code)
            return
        print("No section matches current Wi-Fi")


if __name__ == "__main__":
    main()
