# Setup and getting started

## The easy way

If you trust me (Why would you??), and accept my 100% assurance that I didn't (would never) hide any trojan horsies ready to jump on your home network and wreak havoc, you can use the disk image .iso from the link below.

1. [Download the .iso.zip file](https://drive.google.com/file/d/1x0tPy3iFA8inaSVATO7jO8zQiFyFZLPC/view?usp=sharing) to a local directory (you don't need to unzip)
1. Open .iso.zip file with [Balena Etcher](https://www.balena.io/etcher/)
1. Insert an SSD card >= 16GB into your computer and "Select drive" in Etcher
1. Flash!

When Etcher finishes flashing and verifying -- it will take a while, it may eject the SSD on Mac. Remount (unplug and replug) SDD card so you can see the "boot" folder in Explorer.

In the /boot folder on the SSD, add a file named `wpa_supplicant.conf` with the following information replacing "YOUR\_..." with your wifi name and password:

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="YOUR_WIFI_SID"
    psk="YOUR_PASSWORD"
    id_str="home"
    scan_ssid=1
}
```

If you have multiple networks, you can add additional `network={...}` blocks as long as they have unique `id_str`.

Eject the card from your computer, insert it into the Raspberry Pi 4 and power to the Pi!

Once the pi boots, and joins your network, you should be able to connect to it using ssh as the user `pi`. Like,

```
ssh pi@raspberrypi.local
```

When prompted, enter the password `raspberry`

**Warning** The default password is very well known. After signing in via SSH, use `passwd` command to change the pi users password.

Thats it! The github repo is already cloned in the pi user's home dir.

```
cd scatbot-edge-ai-shootout
./benchmark.py
```

## The hard(er) way

So you want to know all of the things and see them installing in all their glories? Are you the type of person that likes watching long builds? We've got just the thing for you!

I've tried to script out the setup and install that I went through to get all of the ML frameworks working. I cannot guarantee that it still works. As things change, new minor versions of dependent libs break; developers of libraries make changes that break other libraries.... But you probably know about all of that.

Start with Raspian Bullseye OS LITE 64 without desktop. When installing without the desktop, be sure to go into the config of Raspbery Pi Imager and enable SSL and setup your wifi.

<img src="https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/docs/images/raspberry%20pi%20imager.png"
     alt="Raspberry Pi Imager"
     style="float: left; margin-right: 10px;" />

Once you've signed in via ssh to your newly built Raspbian Bullseye OS,

```
sudo apt-get update
sudo apt-get -y upgrade

sudo apt install -y git
git clone https://github.com/littlebee/scatbot-edge-ai-shootout.git
cd scatbot-edge-ai-shootout
./setup.sh
```

...to install all of the things. This will take a while. Go watch an episode of The Expanse.

https://github.com/littlebee/scatbot-edge-ai-shootout/blob/main/setup.sh
