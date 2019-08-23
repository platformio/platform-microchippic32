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

from os.path import join

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Builder, Default,
                          DefaultEnvironment)

env = DefaultEnvironment()
board_config = env.BoardConfig()

env.Replace(
    AR="pic32-ar",
    AS="pic32-as",
    CC="pic32-gcc",
    CXX="pic32-g++",
    OBJCOPY="pic32-objcopy",
    RANLIB="pic32-ranlib",
    SIZETOOL="pic32-size",

    ARFLAGS=["rc"],

    SIZEPROGREGEXP=r"^(?:\.reset|\.startup|\.init|\.fini|\.ctors|\.dtors|\.header_info|\.dinit|\.text\S*|\.rodata\S*|\.romdata\S*|\.data)\s+([0-9]+).*",
    SIZEDATAREGEXP=r"^(?:\.dbg_data|\.ram_exchange_data|\.sdata|\.sbss|\.data\S*|\.stack|\.bss\S*|\.eh_frame|\.jcr|\.libc\S*|\.heap)\s+([0-9]+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    UPLOADER="pic32prog",
    UPLOADERFLAGS=[
        "-d", '"$UPLOAD_PORT"',
        "-b", "$UPLOAD_SPEED"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS $SOURCES',

    PROGSUFFIX=".elf"
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

# append LD script manually
if "LDSCRIPT_PATH" in env:
    del env['LDSCRIPT_PATH']

env.Append(
    ASFLAGS=[
        "-O2",
        "-Wa,--gdwarf-2",
        "-mprocessor=$BOARD_MCU"
    ],

    CFLAGS=["-std=gnu11"],

    CCFLAGS=[
        "-w",
        "-O2",
        "-mdebugger",
        "-mno-smart-io",
        "-mprocessor=$BOARD_MCU",
        "-ffunction-sections",
        "-fdata-sections",
        "-Wcast-align",
        "-fno-short-double",
        "-ftoplevel-reorder"
    ],

    CXXFLAGS=[
        "-fno-exceptions",
        "-std=gnu++11"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU"),
        ("MPIDEVER", "16777998"),
        ("MPIDE", "150")
    ],

    LINKFLAGS=[
        "-w",
        "-Os",
        "-mdebugger",
        "-mprocessor=$BOARD_MCU",
        "-mno-peripheral-libs",
        "-nostartfiles",
        "-Wl,--gc-sections"
    ],

    LIBS=["m"],

    BUILDERS=dict(
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "pic32-bin2hex",
                "-a", "$SOURCES"
            ]), "Building $TARGET"),
            suffix=".hex"
        ),
        ElfToEep=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-j",
                ".eeprom",
                '--set-section-flags=.eeprom="alloc,load"',
                "--no-change-warnings",
                "--change-section-lma",
                ".eeprom=0",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".eep"
        ),
    )
)

if int(board_config.get("upload.maximum_ram_size", 0)) < 65535:
    env.Append(
        ASFLAGS=["-G1024"],
        CCFLAGS=["-G1024"]
    )

#
# Target: Build executable and linkable firmware
#

target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_elf = join("$BUILD_DIR", "${PROGNAME}.elf")
    target_firm = join("$BUILD_DIR", "${PROGNAME}.hex")
else:
    target_elf = env.BuildProgram()

    env.Append(LINKFLAGS=[
        "-Wl,--script=%s" % board_config.get("build.ldscript", ""),
        "-Wl,--script=chipKIT-application-COMMON%s.ld" %
        ("-MZ" if "MZ" in board_config.get("build.mcu", "") else "")
    ])

    target_firm = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.Alias(
    "size", target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Target: Upload firmware
#

target_upload = env.Alias(
    "upload", target_firm,
    [env.VerboseAction(env.AutodetectUploadPort, "Looking for upload port..."),
     env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")])
AlwaysBuild(target_upload)

#
# Default targets
#

Default([target_buildprog, target_size])
