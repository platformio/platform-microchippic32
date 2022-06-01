# Microchip PIC32: development platform for [PlatformIO](https://platformio.org)

[![Build Status](https://github.com/platformio/platform-microchippic32/workflows/Examples/badge.svg)](https://github.com/platformio/platform-microchippic32/actions)

Microchip's 32-bit portfolio with the MIPS microAptiv or M4K core offer high performance microcontrollers, and all the tools needed to develop your embedded projects. PIC32 MCUs gives your application the processing power, memory and peripherals your design needs!

* [Home](https://registry.platformio.org/platforms/platformio/microchippic32) (home page in the PlatformIO Registry)
* [Documentation](https://docs.platformio.org/page/platforms/microchippic32.html) (advanced usage, packages, boards, frameworks, etc.)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

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

Please navigate to [documentation](https://docs.platformio.org/page/platforms/microchippic32.html).
