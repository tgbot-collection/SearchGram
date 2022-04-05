# SearchGram

A telegram Bot that can search for CJK and other languages.

# Introduction

Telegram has bad search experience for CJK languages because those languages are not separated by spacing.

Bug issues were submitted years ago but never fixed.

* https://github.com/tdlib/td/issues/1004
* https://bugs.telegram.org/c/724

I'm not planning to be sitting ducks, so I create a bot that can search for CJK languages.

# Theory

1. Telegram allows multiple sessions, maximum is 10 clients.
2. We create a hidden session
3. We use this session to store all your incoming and outgoing text messages to ElasticSearch
4. We create another bot to use the fulltext search of ElasticSearch
5. We return the whole sentense, so you could use Telegram's built-in buggy search feature.

# Screenshots

![](assets/1.jpeg)

# Installation

**Because chat history is very important and that should be kept privately always, so I don't offer any public bots.**

## 1. Prepare environment and clone this repository

Install docker and docker-compose on your server, clone this repository to any directory you want.

## 2. (Optional) Prepare Encryption data volume

It's highly recommend to use encrypted data volume. You can use LUKS.

Here there is an example of using loop+LVM+LUKS, you can also use simple make commands:

```shell
make encrypt
make format
```

### 2.1 Create loop device

```shell
# create loop file and loop device
fallocate -l 1G pv1.img
losetup /dev/loop0 pv1.img
# verify loop device
fdisk -l /dev/loop0
Disk /dev/loop0: 1 GiB, 1073741824 bytes, 2097152 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

```

### 2.2 create LVM

```shell
pvcreate /dev/loop0
vgcreate vg_es_data /dev/loop0
# use vgdisplay to confirm Volume Group
vgdisplay

# create logical volume
lvcreate --extents 100%FREE vg_es_data -n lv_es_data

# You should have device here 
file /dev/vg_es_data/lv_es_data
```

### 2.3 luks

```shell
# format lucks and input your password
cryptsetup luksFormat /dev/vg_es_data/lv_es_data
# open device
cryptsetup luksOpen /dev/vg_es_data/lv_es_data es_data
# you should see /dev/mapper/es_data
file /dev/mapper/es_data
cryptsetup status es_data
```

### 2.4 format and mount

```shell
mkfs.ext4 /dev/mapper/es_data
mkdir -p es_data
mount /dev/mapper/es_data ./es_data
```

### 2.5 unmount and remove

```shell
umount /dev/mapper/es_data
cryptsetup luksClose es_data
````

## 3. Prepare APP_ID, APP_HASH and bot token

1. You can get APP_ID and APP_HASH from https://core.telegram.org/
2. Talk to @BotFather to get your bot token
3. Talk to @blog_update_bot to get your user id

## 4. Modify env file

```shell
# vim env/gram.env
TOKEN=3token
APP_ID=id
APP_HASH=hash
OWNER_ID=your user_id

```

## 5. Login to client

```shell
make init
```

And then you'll be dropped into a container shell.

```shell
python client.py
```

Follow the instruction to log in to your account.

When you finish, Ctrl + D to exit. You should find session file under `session/client.session`.

## 6. Up and running

```shell
docker-compose up -d
```

Now you can talk to your friends and search in your bot.

# Roadmap and TODOs

- [ ] import chat history

# License

This project is LICENSED under the GNU GENERAL PUBLIC LICENSE Version 3.