# ![vixen logo](/assets/vixen_logo_md.png) Vixen Shell Project

## Linux Desktop Environment

The [Vixen Shell](https://github.com/vixen-shell) project represents an initiative aimed at creating a user-friendly desktop environment for Linux users, focused on development. Built upon the [Hyprland](https://github.com/hyprwm/Hyprland) window manager, this project stands out for its use of Python for the backend and web technologies like JavaScript, HTML, and CSS for the user interface (front-end).

# ![vixen logo](/assets/vixen_logo_md.png) Vixen API

## API for communication between interfaces and the system

This project is an essential component of the Vixen Shell's back-end. It implements an API developed in Python using the FastAPI library, enabling Vixen Shell's front-end to communicate with Hyprland (window manager) and the Linux operating system. Through this API, we notably have the ability to retrieve the event stream coming from Hyprland's UNIX socket via a WebSocket.

> **Note :** This is a development project that has just emerged from its proof of concept phase and is still in its alpha version.