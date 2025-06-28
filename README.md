# GB_APU_simu
Some scripts used to demonstrate how the GameBoy APU works

## Dependencies

- python3
- tkinter
- matplotlib
- numpy
- sounddevice
- soundfile

### Debian packages

The installation of the latest python3 is not shown below.
This section exists only to show some debian specific packages needed by the python packages.
It also shows how to use a `venv` to install python packages
(`pip` cannot be used on debian...).

```sh
sudo apt install python3-tk portaudio19-dev
python3 -m venv .venv
.venv/bin/pip3 install numpy matplotlib sounddevice soundfile scipy
```

