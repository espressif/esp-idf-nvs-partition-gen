# NVS Partition Generator Utility

## Introduction

The utility `esp-idf-nvs-partition-gen/nvs_partition_gen.py` creates a binary file, compatible with the NVS architecture defined in [Non-Volatile Storage Library](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_flash.html), based on the key-value pairs provided in a CSV file.

Install with `pip install esp-idf-nvs-partition-gen`, then run `nvs-partition-gen generate sample.csv sample.bin 0x3000`.

This utility is ideally suited for generating a binary blob, containing data specific to ODM/OEM, which can be flashed externally at the time of device manufacturing. This allows manufacturers to generate many instances of the same application firmware with customized parameters for each device, such as a serial number.

## Documentation

See more in [NVS Partition Generator Utility ESP-IDF docs](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/storage/nvs_partition_gen.html).
