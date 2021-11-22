How to build PlatformIO based project
=====================================

1. [Install PlatformIO Core](http://docs.platformio.org/page/core.html)
2. Download [development platform with examples](https://github.com/platformio/platform-microchippic32/archive/develop.zip)
3. Extract ZIP archive
4. Run these commands:

```shell
# Change directory to example
$ cd platform-microchippic32/examples/arduino-blink

# Build project
$ pio run

# Upload firmware
$ pio run --target upload

# Build specific environment
$ pio run -e chipkit_mx3

# Upload firmware for the specific environment
$ pio run -e chipkit_mx3 --target upload

# Clean build files
$ pio run --target clean
```
