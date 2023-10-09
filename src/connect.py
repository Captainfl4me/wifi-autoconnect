# pylint: disable=too-many-arguments
"""
    Auto send request to URL when connected to specific Wi-Fi
    
    Author: THIERRY Nicolas - 2023
"""

from json import load
from enum import Enum
from subprocess import check_output
from re import findall, RegexFlag
from os import path
from time import sleep
from requests import post, get, Response


class UrlMethod(Enum):
    """
    URL method enum
    """
    POST = "POST"
    GET = "GET"


def json_decoder(json_dict: dict):
    """
    JSON decoder
    :param json_dict:
    :return:
    """
    if "method" in json_dict:
        json_dict["method"] = UrlMethod(json_dict["method"])
    if "name" in json_dict:
        return Connector(
            json_dict["name"],
            json_dict["url"],
            json_dict["SSID"],
            json_dict["method"],
            json_dict["body"],
            json_dict["delay"] if "delay" in json_dict else 0,
        )
    return json_dict


class Connector:
    """
    Connector class representing a connector to a Wi-Fi with a URL to send a request to
    """

    def __init__(
        self, name: str, url: str, ssid: str, method: UrlMethod, body: dict, delay: int = 0
    ) -> None:
        self._name = name
        self._url = url
        self._ssid = ssid
        self._method = method
        self._body = body
        self._delay = delay

    @property
    def name(self) -> str:
        """
        Get name of connector
        return: str
        """
        return self._name

    def does_match_current_wifi(self) -> bool:
        """
        Check if the current connected Wi-Fi is the same as this one
        :return: bool
        """
        netsh_interfaces = check_output("netsh wlan show interfaces").decode("cp850")
        ssid_match = findall(
            r"^\s*SSID\s*.:\s([^\n\r]+)",
            netsh_interfaces,
            RegexFlag.MULTILINE | RegexFlag.DOTALL,
        )
        ssid = ssid_match[0] if len(ssid_match) > 0 else None
        return ssid is not None and ssid == self._ssid

    def send_request(self) -> Response | None:
        """
        Send request to URL with body
        :return:
        """
        sleep(self._delay)
        if self._method is UrlMethod.POST:
            return post(self._url, self._body, timeout=60)
        if self._method is UrlMethod.GET:
            return get(self._url, self._body, timeout=60)

        return None


def main() -> None:
    """
    Main function
    :return: None
    """

    # Read config file
    if not path.isfile("config.json"):
        print("Config file not found")
        return

    with open("config.json", mode="r", encoding="UTF-8") as config_file:
        config = load(config_file, object_hook=json_decoder)

    # Get all sections
    for connector in config["sections"]:
        connector: Connector = connector
        if connector.does_match_current_wifi():
            print(f"Section {connector.name} matches current Wi-Fi")
            res = connector.send_request()
            if res is not None:
                print(res.status_code)
                return
            print("No request configure or error sending one!")
        print("No section matches current Wi-Fi")


if __name__ == "__main__":
    main()
