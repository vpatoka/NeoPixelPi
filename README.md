# Update Your Pi and Python

Run the standard updates:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-pip
```

and upgrade setuptools:

```
sudo apt install --upgrade python3-setuptools
```

Python2 support has been dropped, so you will need to either use pip3 and python3 as commands or set Python 3 as the default python install.

You may need to reboot prior to installing Blinka. The raspi-blinka.py script will inform you if it is necessary.

If you are installing in a virtual environment, the installer may not work correctly since it requires sudo. We recommend using pip to manually install it in that case.

# Setup Virtual Environment

If you are installing on the Bookworm version of Raspberry Pi OS, you will need to install your python modules in a virtual environment. You can find more information in the [Python Virtual Environment Usage on Raspberry Pi](https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi) guide. To Install and activate the virtual environment, use the following commands:

```
sudo apt install python3.11-venv
python -m venv env --system-site-packages
```

You will need to activate the virtual environment every time the Pi is rebooted. To activate it:

```
source env/bin/activate
```

To deactivate, you can use `deactivate`, but leave it active for now.

# Automated Install

Creators put together a script to easily make sure your Pi is correctly configured and install Blinka. It requires just a few commands to run. Most of it is installing the dependencies.

```
cd ~
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

If you are installing on an earlier version such as Bullseye of Raspberry Pi OS, you can call the script like:

```
sudo python3 raspi-blinka.py
```



It may take a few minutes to run. When it finishes, reboot the Raspberry Pi



Once it reboots, the connection will close. After a couple of minutes, you can reconnect.

# Check I2C and SPI

The script will automatically enable I2C and SPI. You can run the following command to verify:


```
ls /dev/i2c* /dev/spi*
```

You should see the response

```
/dev/i2c-1 /dev/spidev0.0 /dev/spidev0.1
```





# Blinka Test

Create a new file called **blinkatest.py** with **nano** or your favorite text editor and put the following in:

```python
import board
import digitalio
import busio

print("Hello blinka!")

# Try to great a Digital input
pin = digitalio.DigitalInOut(board.D4)
print("Digital IO ok!")

# Try to create an I2C device
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

# Try to create an SPI device
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")

print("done!")
```

Save it and run at the command line with:



```
python3 blinkatest.py
```

You should see its goes through, indicating digital i/o, I2C and SPI all worked.

# Python Installation of NeoPixel Library

As Adafruit_Blinka library has been installed, it is time to install NeoPixel:

- `source env/bin/activate`

- `pip3 install rpi_ws281x adafruit-circuitpython-neopixel`

  

If all this steps are done, we could connect WS281x strip to Raspberry PI, using +5V and Ground pins for the power and Pin D18 for Data
*(!)* NOTE - We have to use LED Signal Amplifier to avoid direct connection of LED to Raspberry PI. I am using `SP901E` model.

There is few effects included to the code. Also it has a logic to start the show 30 minutes after sunset and stop it 30 minutes before the sunrise.

# Make Python code to run as a service

To make live easier, we have to create custom service to run it every time we boot the Raspberry PI host

- `systemctl edit --force --full led_controller.service`

  The content could be something like this:
  

  **`[Unit]`**
  **`Description=Led Controller Service`**
  **`Wants=network.target`**
  **`After=network.target`**

  **`[Service]`**
  **`ExecStartPre=/bin/sleep 10`**
  **`ExecStart=/usr/local/bin/led_controller.py`**
  **`Restart=always`**

  **`[Install]`**
  **`WantedBy=multi-user.target`**

  

- `systemcrl list`

- `systemctl status led_controller.service`

- `systemctl enable led_controller.service`

- `systemctl enable led_controller.service`

  

