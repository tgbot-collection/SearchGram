> This document will help you to go through the entire process of running this utility.


# 1. Prepare environment and clone this repository

Install docker and docker-compose on your server, clone this repository to any directory you want.

# 2. (Optional) Prepare Encryption data volume

It's highly recommend to use encrypted data volume. You can use LUKS.

Here there is an example of using loop+LVM+LUKS, you can also use simple make commands:

```shell
make encrypt
make format
```

## 2.1 Create loop device

```shell
# create loop file and loop device
fallocate -l 1G pv0.img
losetup /dev/loop0 pv0.img
# verify loop device
fdisk -l /dev/loop0
Disk /dev/loop0: 1 GiB, 1073741824 bytes, 2097152 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

```

## 2.2 create LVM

```shell
pvcreate /dev/loop0
vgcreate vg_mongo_data /dev/loop0
# use vgdisplay to confirm Volume Group
vgdisplay

# create logical volume
lvcreate --extents 100%FREE vg_mongo_data -n lv_mongo_data

# You should have device here 
file /dev/vg_mongo_data/lv_mongo_data
```

## 2.3 luks

```shell
# format lucks and input your password
cryptsetup luksFormat /dev/vg_mongo_data/lv_mongo_data
# open device
cryptsetup luksOpen /dev/vg_mongo_data/lv_mongo_data mongo_data
# you should see /dev/mapper/mongo_data
file /dev/mapper/mongo_data
cryptsetup status mongo_data
```

## 2.4 format and mount

```shell
mkfs.ext4 /dev/mapper/mongo_data
mkdir -p mongo_data
mount /dev/mapper/mongo_data ./mongo_data
chmod 777 mongo_data
```

## 2.5 unmount and remove

```shell
umount /dev/mapper/mongo_data
cryptsetup luksClose mongo_data
````

# 3. Prepare APP_ID, APP_HASH and bot token

1. You can get APP_ID and APP_HASH from https://core.telegram.org/
2. Talk to @BotFather to get your bot token
3. Talk to @blog_update_bot to get your user id and your bot's id

# 4. Modify env file

```shell
# vim env/gram.env
TOKEN=token
APP_ID=id
APP_HASH=hash
OWNER_ID=your user_id
BOT_ID=your bot_id
```

# 5. Login to client

```shell
make init
```

And then you'll be dropped into a container shell.

```shell
python client.py
```

Follow the instruction to log in to your account.

When you see 'started xxx handlers', Ctrl + D to exit. You should find session file
under `searchgram/session/client.session`.

# 6. (optional)setup sync id

If you would like to sync all the chat history for any user, group or channel, you can configure sync id.

First thing you need is obtaining chat peer, it could be integer or username. Use https://t.me/blog_update_bot to get
what
you want.

Secondly, you'll have to manually edit `sync.ini`
**Please use username as much as possible. 
If you want to use user_id, please talk to the person immediately after starting `client.py`. You have 30s to do so.**

```ini
[chat]
123456 = true # will sync this chat
789 = false # won't sync this
BennyThink # will sync this
```

# 6. Up and running

```shell
docker-compose up -d
```

Now you can talk to your friends and search in your bot.

If you configure sync id, you can monitor sync status in Saved Messages.
