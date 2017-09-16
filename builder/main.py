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

env.Replace(
    AR="pic32-ar",
    AS="pic32-as",
    CC="pic32-gcc",
    CXX="pic32-g++",
    OBJCOPY="pic32-objcopy",
    RANLIB="pic32-ranlib",
    SIZETOOL="pic32-size",

    ARFLAGS=["rc"],

    ASFLAGS=[
        "-g1",
        "-O2",
        "-Wa,--gdwarf-2",
        "-mprocessor=$BOARD_MCU"
    ],

    CCFLAGS=[
        "-w",
        "-g",
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

    CXXFLAGS=["-fno-exceptions"],

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

    SIZEPRINTCMD='$SIZETOOL -B -d $SOURCES',

    UPLOADER="pic32prog",
    UPLOADERFLAGS=[
        "-d", '"$UPLOAD_PORT"',
        "-b", "$UPLOAD_SPEED"
    ],
    UPLOADCMD='$UPLOADER $UPLOADERFLAGS $SOURCES',

    PROGNAME="firmware",
    PROGSUFFIX=".elf"
)

if int(env.BoardConfig().get("upload.maximum_ram_size", 0)) < 65535:
    env.Append(
        ASFLAGS=["-G1024"],
        CCFLAGS=["-G1024"]
    )


env.Append(
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

#
# Target: Build executable and linkable firmware
#
target_elf = None
if "nobuild" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.hex")
else:
    target_elf = env.BuildProgram()

    # Hook: Fix option for LD script
    _new_linkflags = []
    for f in env['LINKFLAGS']:
        if not f.startswith("-Wl,-T"):
            _new_linkflags.append(f)
        else:
            _new_linkflags.append("-Wl,--script=%s" % f[6:])

    env.Replace(LINKFLAGS=_new_linkflags)
    env.Append(LINKFLAGS=[
        "-Wl,--script=chipKIT-application-COMMON%s.ld" %
        ("-MZ" if "MZ" in env.BoardConfig().get("build.mcu", "") else "")
    ])

    target_firm = env.ElfToHex(target_elf)

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
