# Microchip PIC32: development platform for [PlatformIO](http://platformio.org)
[![Build Status](https://travis-ci.org/platformio/platform-microchippic32.svg?branch=develop)](https://travis-ci.org/platformio/platform-microchippic32)
[![Build status](https://ci.appveyor.com/api/projects/status/r1gu34suxrbgfjp9/branch/develop?svg=true)](https://ci.appveyor.com/project/ivankravets/platform-microchippic32/branch/develop)

Microchip's 32-bit portfolio with the MIPS microAptiv or M4K core offer high performance microcontrollers, and all the tools needed to develop your embedded projects. PIC32 MCUs gives your application the processing power, memory and peripherals your design needs!

* [Home](http://platformio.org/platforms/microchippic32) (home page in PlatformIO Platform Registry)
* [Documentation](http://docs.platformio.org/page/platforms/microchippic32.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](http://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](http://docs.platformio.org/page/projectconf.html) file:

## Stable version

```ini
[env:stable]
platform = microchippic32
board = ...
...
```

## Development version

```ini
[env:development]
platform = https://github.com/platformio/platform-microchippic32.git
board = ...
...
```

# Configuration

Please navigate to [documentation](http://docs.platformio.org/page/platforms/microchippic32.html).
