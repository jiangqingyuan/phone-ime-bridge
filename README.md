# Phone IME Bridge

Use your phone's keyboard or voice input to type text into the current focused Linux Wayland application.

Built for users who want to use phone's input method (with voice input ) on Linux desktops such as Niri, Hyprland, Sway, and other wlroots-based compositors.

## Features

- Use input method of phone
- Supports Chinese and other Unicode text
- Works through a local web page
- Uses `wtype` for Wayland text injection
- No Bluetooth required

## Requirements

- Linux Wayland session
- `wtype`
- Python 3
- Phone and computer on the same LAN

On Arch Linux:

```bash
sudo pacman -S wtype python
```

## Usage

Start the server:

```bash
python server.py
```


Find your computer IP:

```bash
ip -4 addr | grep inet
```

Open this on your phone:

```
http://YOUR_COMPUTER_IP:8765
```

Put your cursor in any input field on your computer, type or use voice input on your phone, then press send.

## Tested on
Arch Linux Niri
Android

