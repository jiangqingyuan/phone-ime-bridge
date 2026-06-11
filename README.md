# Phone IME Bridge

Use your phone's keyboard or voice input to type text into the current focused Linux Wayland application.

Built for users who want to use phone's input method (with voice input ) on Linux desktops such as Niri, Hyprland, Sway, and other wlroots-based compositors.

## Features

- Use input method of phone
- Supports Chinese and other Unicode text
- Works through a local web page
- Uses `wtype or crossmacro` for Wayland to paste text
- No Bluetooth required

## Requirements

- Linux Wayland session
- Phone and computer on the same LAN

On Arch Linux:

```bash
yay -S wtype crossmarco
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
wechat
qq
firefox
edge
chrome
vscode
kitty

## Compatibility Notes

### Direct keyboard simulation

Direct text injection through `wtype text` is not reliable across all Wayland applications.

Observed issues include:

- Some browsers may drop the first CJK character.
- WeChat and QQ may interpret injected text as numbers incorrectly.

For this reason, Phone IME Bridge uses clipboard-based paste by default.

And `wtype` may cause the window to exit unexpectedly.

WeChat and QQ require a different paste backend `crossmacro` for reliable operation.

Phone IME Bridge automatically detects these applications and switches to a compatible paste method.

