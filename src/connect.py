from configparser import SectionProxy, ConfigParser
from enum import Enum
from subprocess import check_output
from re import findall, RegexFlag


class UrlMethod(Enum):
    POST = "POST"


class Connector:
    def __init__(self, section: SectionProxy) -> None:
        self._section = section

    def check_integrity(self) -> bool:
        """
        Check if the section has all the required fields
        :return: bool
        """
        integrity = ('SSID' in self._section
                     and 'URL' in self._section
                     and 'METHOD' in self._section
                     and 'USERNAME' in self._section
                     and 'PASSWORD' in self._section)

        integrity = integrity and (self._section["SSID"] != '')
        integrity = integrity and (self._section["URL"] != '')
        integrity = integrity and (self._section["METHOD"] != '' and self._section["METHOD"] in UrlMethod.__members__)
        return integrity

    def does_match_current_wifi(self) -> bool:
        """
        Check if the current connected Wi-Fi is the same as this one
        :return: bool
        """
        netsh_interfaces = check_output('netsh wlan show interfaces').decode("cp850")
        ssid_match = findall(r'^\s*SSID\s*.:\s([^\n\r]+)', netsh_interfaces, RegexFlag.MULTILINE | RegexFlag.DOTALL)
        ssid = ssid_match[0] if len(ssid_match) > 0 else None
        return ssid is not None and ssid == self._section["SSID"]


def main() -> None:
    """
    Main function
    :return: None
    """

    # Read config file
    config = ConfigParser()
    if not config.read('config.ini'):
        print("Config file not found! Please create a config.ini file.")
        exit(1)

    # Get all sections
    sections = config.sections()
    for section in sections:
        connector = Connector(config[section])
        if connector.check_integrity():
            if connector.does_match_current_wifi():
                print(f"Section {section} matches current Wi-Fi")
        else:
            print(f"Section {section} is invalid")


if __name__ == "__main__":
    main()
