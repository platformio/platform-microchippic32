# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import isdir, join

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinomicrochippic32")
BUILD_CORE = env.BoardConfig().get("build.core")
assert isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=[
        ("ARDUINO", 10808),
        "ARDUINO_ARCH_PIC32",
        ("IDE", "Arduino")
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE)
    ],

    LIBPATH=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ],

    LINKFLAGS=[
        join(FRAMEWORK_DIR, "cores", BUILD_CORE, "cpp-startup.S")
    ],

    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Process USB flags
#

cpp_flags = env.Flatten(env.get("CPPDEFINES", []))
if any(str(f).startswith("PIO_ARDUINO_ENABLE_USB") for f in cpp_flags):
    env.Append(
        CPPDEFINES=[
            "__USB_ENABLED__",
            "__SERIAL_IS_USB__"
        ]
    )
if "PIO_ARDUINO_ENABLE_USB_SERIAL" in cpp_flags:
    env.Append(CPPDEFINES=["__USB_CDCACM__"])
elif "PIO_ARDUINO_ENABLE_USB_HID" in cpp_flags:
    env.Append(CPPDEFINES=["__USB_CDCACM_KM__"])

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants",
                 env.BoardConfig().get("build.variant"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", env.BoardConfig().get("build.variant"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores", BUILD_CORE)
))

env.Prepend(LIBS=libs)
