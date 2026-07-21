from esp_pylib.excepthook import install_exception_reporting

from .nvs_partition_gen import main

if __name__ == '__main__':
    install_exception_reporting()
    main()
