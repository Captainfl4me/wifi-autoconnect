import configparser


class Connector:
    def __init__(self, section: configparser.SectionProxy) -> None:
        self._section = section

    def check_integrity(self) -> bool:
        """
        Check if the section has all the required fields
        :return: bool
        """
        integrity = (hasattr(self._section, 'url')
                     and hasattr(self._section, 'username')
                     and hasattr(self._section, 'password'))
        return integrity


def main() -> None:
    """
    Main function
    :return: None
    """

    # Read config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get all sections
    sections = config.sections()
    for section in sections:
        connector = Connector(config[section])
        print(connector.check_integrity())


if __name__ == "__main__":
    main()
