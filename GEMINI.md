# GEMINI.md

## Directory Overview

This directory, `/home/carl/bin`, contains a collection of personal command-line scripts and utilities. These scripts are designed to simplify and automate various tasks, from clipboard management and file operations to media manipulation and system administration. The scripts are written in a mix of `bash` and `python`.

## Key Files

The most important file in this directory is `README.md`, which provides a comprehensive overview of each script, its purpose, and usage examples. Other key files are the scripts themselves, which are designed to be executed from the command line.

*   `send-email`: A shell script to send emails from the command line using `mutt`. It supports specifying the recipient, subject, body, and an attachment.
*   `git-init`: A shell script to initialize a git repository, add all files, make an initial commit, and set up a GitHub remote repository under the user `Carltk`.

## Building and Running

The scripts in this directory do not require a build process. They are intended to be run directly from the command line. For ease of use, it is recommended to add this directory to your system's `$PATH` environment variable.

For example, to run the `copy` script, you would simply type:

```bash
echo "hello world" | copy
```

### Dependencies

Many of the scripts in this directory rely on external command-line tools. Some of the key dependencies include:

*   `xclip`: For clipboard operations on Linux.
*   `ffmpeg`: For video and audio manipulation.
*   `yt-dlp`: For downloading media from the internet.
*   `mpv`: For playing audio and video files.

Please refer to the `README.md` file for more details on the dependencies for each script.

## Development Conventions

The scripts in this directory follow a set of conventions that promote robustness and maintainability:

*   **Shell Scripts**: Most `bash` scripts start with `#!/usr/bin/env bash` and include `set -e` and `set -u` to ensure that the script will exit immediately if a command fails or if it tries to use an uninitialized variable.
*   **Python Scripts**: Python scripts use the `argparse` module to parse command-line arguments.
*   **Cross-Platform Support**: Many scripts are designed to work on both macOS and Linux by checking for the existence of platform-specific commands and providing fallbacks.
*   **Documentation**: The `README.md` file serves as the primary documentation for all the scripts in this directory.
