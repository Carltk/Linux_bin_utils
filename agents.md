# AGENTS.md

## Directory Overview

This directory, `/home/carl/bin`, contains a comprehensive collection of personal command-line utilities and scripts designed to enhance productivity and streamline various computing tasks. These scripts span multiple categories including clipboard management, file operations, media manipulation, system administration, development workflows, and communication tools.

## Script Categories and Key Utilities

### Clipboard Management
- **copy**: Cross-platform clipboard copy utility supporting macOS (pbcopy), Linux (xclip), and fallback to /tmp/clipboard
- **pasta**: Cross-platform clipboard paste utility with platform detection and fallback mechanisms
- **pastas**: Continuously monitors clipboard changes and outputs new content
- **cpwd**: Copies current working directory to clipboard

### File Management
- **trash**: Safe file deletion using system trash (cross-platform macOS/Linux support)
- **mksh**: Creates executable shell scripts with proper shebang and opens in editor
- **extract**: Universal archive extraction utility
- **rn**: File renaming utility
- **length**: Returns string length (character count)

### Text Processing
- **line**: Extracts specific line numbers from input streams
- **scratch**: Opens temporary editor buffer for quick notes
- **straightquote**: Converts smart quotes to straight quotes
- **markdownquote**: Adds markdown blockquote formatting
- **jsonformat**: Pretty-prints JSON input
- **uppered/lowered**: Case conversion utilities
- **nato**: Converts text to NATO phonetic alphabet
- **csv2md**: Converts CSV to markdown format

### Development Tools
- **serveit**: Cross-platform HTTP server with fallbacks (PHP → Python3 → Python2 → Ruby)
- **git-init**: Initializes git repo, creates initial commit, and sets up GitHub remote under Carltk
- **git-fzf-checkout**: Interactive git branch selection using fzf
- **vimplug**: Vim plugin management utility

### Media and Multimedia
- **getsong**: Downloads audio from YouTube/SoundCloud using yt-dlp
- **getpod**: Downloads content for podcast listening
- **getsubs**: Extracts subtitles from videos
- **tunes**: Audio player using mpv
- **pix**: Image viewer using mpv
- **radio**: Internet radio streaming utility
- **shrinkvid**: Video compression using ffmpeg
- **ffmpeg-smallest**: Optimizes video for minimal file size
- **removeexif**: Removes EXIF data from images
- **ocr**: Optical character recognition from images
- **movs2mp4s**: Converts MOV files to MP4 format
- **transcribe**: Audio transcription utility

### System Utilities
- **timer**: Countdown timer with sound and notification alerts
- **stopwatch**: Timer/stopwatch utility
- **clock**: Time display utility
- **notify**: Cross-platform system notifications (Linux notify-send/macOS osascript)
- **theme**: System theme switching (dark/light mode)
- **sleepybear**: System sleep utility
- **wifi**: WiFi network management
- **myip**: Displays current IP address
- **flushdns**: Clears DNS cache
- **ds-destroy**: Removes .DS_Store files recursively

### Process Management
- **running**: Process listing with simplified output
- **murder**: Gradual process termination (SIGTERM → SIGINT → SIGHUP → SIGKILL)
- **waitfor**: Waits for process completion
- **bb**: Background process execution
- **tryna/trynafail**: Retry utilities until success/failure

### Internet and Network
- **url**: URL parsing and analysis
- **pingbing**: Network connectivity testing
- **pingen**: Ping generation utility
- **httpstatus**: HTTP status code reference
- **duck/duckl**: DuckDuckGo search utilities

### Communication
- **send-email**: Email sending via mutt with SMTP configuration
- **speak**: Text-to-speech conversion with markdown stripping

### Reference and Lookup
- **emoji**: Emoji search and lookup
- **alphabet**: Displays alphabet (upper/lowercase)
- **u+**: Unicode character lookup
- **extensions**: File extension reference
- **list-colors**: Color palette display
- **httpstatus**: HTTP status code reference

### Data and Math
- **math**: Mathematical calculations
- **uuid**: UUID generation
- **bytedump**: Hexadecimal file analysis
- **catbin**: Displays binary file content

### Productivity and Utilities
- **snippet/snippets**: Text snippet management
- **each**: Alternative to xargs for command execution
- **prettypath**: Formatted PATH display
- **view**: File viewing utility
- **g**: Quick grep/search utility
- **f**: File finding utility
- **l/la**: Directory listing alternatives
- **cls**: Clear screen utility
- **hoy**: Current date in ISO format
- **datesort**: Date-based sorting
- **emoji**: Emoji lookup
- **sfx**: Sound effects player

## Development Conventions

### Shell Scripts
- Most bash scripts use `#!/usr/bin/env bash` shebang
- Standard safety headers: `set -e`, `set -u`, `set -o pipefail`
- Cross-platform compatibility with command existence checks (`hash` command)
- Fallback mechanisms for different operating systems

### Python Scripts
- Use `argparse` for command-line argument parsing
- Follow PEP 8 style guidelines
- Include proper error handling and exit codes

### Cross-Platform Support
- Platform detection using `hash` command for tool availability
- Conditional logic for macOS vs Linux differences
- Fallback implementations when primary tools aren't available

### Dependencies
Key external dependencies include:
- **xclip**: Linux clipboard operations
- **ffmpeg**: Media processing and conversion
- **yt-dlp**: Media downloading from internet sources
- **mpv**: Media playback
- **mutt**: Email client for send-email utility
- **gh**: GitHub CLI for git operations
- **fzf**: Fuzzy finding for interactive selections
- **notify-send**: Linux notifications
- **osascript**: macOS notifications

## Environment Configuration

### Email Configuration
The `send-email` utility requires these environment variables:
- `DEFAULT_ADMIN_EMAIL`: Default sender/recipient email
- `SCRIPT_SMTP_SERVER`: SMTP server address
- `SCRIPT_SMTP_PORT`: SMTP port number
- `SCRIPT_SMTP_LOGIN`: SMTP authentication username
- `SCRIPT_SMTP_KEY`: SMTP authentication password/app password

### GitHub Integration
The `git-init` script requires:
- `gh` GitHub CLI tool installed and authenticated
- Creates repositories under the `Carltk` GitHub account

## Usage Examples

### Clipboard Operations
```bash
# Copy command output
ls -la | copy

# Paste clipboard content
pasta > clipboard_content.txt

# Copy current directory
cpwd
```

### File Operations
```bash
# Safe deletion
trash unwanted_file.txt

# Create shell script
mksh new_script.sh

# Extract archive
extract archive.tar.gz
```

### Development Workflow
```bash
# Start local server
serveit 8080

# Initialize git repo with GitHub remote
git-init

# Interactive git checkout
git-fzf-checkout
```

### Media Operations
```bash
# Download audio
getsong https://youtube.com/watch?v=example

# Play music
tunes --shuffle ~/music/

# Extract subtitles
getsubs https://youtube.com/watch?v=example
```

### System Management
```bash
# Set 5-minute timer
timer 5m

# Send notification
notify "Task Complete" "Your backup has finished"

# Check running processes
running python
```

## Installation and Setup

1. Add `/home/carl/bin` to `$PATH` environment variable
2. Install required dependencies based on intended usage
3. Configure email environment variables for send-email functionality
4. Install and authenticate GitHub CLI for git operations
5. Set up notification tools for your platform

## Script Architecture

The collection follows a modular design philosophy:
- Single-purpose utilities that do one thing well
- Composable tools that work together via pipes
- Consistent command-line interfaces where possible
- Extensive cross-platform compatibility
- Robust error handling and user feedback

This collection represents a comprehensive personal toolkit optimized for daily development, system administration, and productivity tasks.