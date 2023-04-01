> This document provides a step-by-step guide to help you run this utility.

# 1. Prepare the Environment and Download the Appropriate Docker Compose File

To get started, install Docker and Docker Compose on your server.

You can choose to use either the legacy version, which is powered by MongoDB, by using the docker-compose.legacy.yml
file
or the latest version, which is powered by MeiliSearch, by using the docker-compose.yml file.

# 2. (Optional) Prepare the Encrypted Data Volume

For added security, it's highly recommended to use an encrypted data volume.

You can use LUKS for this purpose.

Here's an example of how to use loop+LVM+LUKS to set it up, but you can also use simple make commands:

```shell
make encrypt
make format
```

## 2.1 Create the loop device

Start by creating a loop file and loop device:

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

## 2.2 Create LVM

Create the physical volume and volume group:

```shell
pvcreate /dev/loop0
vgcreate vg_sg_data /dev/loop0
# use vgdisplay to confirm Volume Group
vgdisplay

# create logical volume
lvcreate --extents 100%FREE vg_sg_data -n lv_sg_data

# You should have device here 
file /dev/vg_sg_data/lv_sg_data
```

## 2.3 luks

Format LUKS and enter your password:

```shell
# format lucks and input your password
cryptsetup luksFormat /dev/vg_sg_data/lv_sg_data
# open device
cryptsetup luksOpen /dev/vg_sg_data/lv_sg_data sg_data
# you should see /dev/mapper/sg_data
file /dev/mapper/sg_data
cryptsetup status sg_data
```

## 2.4 Format and Mount

Format and mount the device:

```shell
mkfs.ext4 /dev/mapper/sg_data
mkdir -p sg_data
mount /dev/mapper/sg_data ./sg_data
chmod 777 sg_data
```

## 2.5 Unmount and Remove

Unmount and remove the device:

```shell
umount /dev/mapper/sg_data
cryptsetup luksClose sg_data
````

# 3. Obtain APP_ID, APP_HASH, and Bot Token

To get started with SearchGram, you'll need to

1. obtain your APP_ID and APP_HASH from https://core.telegram.org/,
2. get your bot token by contacting @BotFather
3. get your user ID and bot ID by contacting @blog_update_bot.

# 4. Modify env file

The MEILI_MASTER_KEY is a credential used to access the Web UI of MeiliSearch.

To simplify things, you can use your bot token instead.

```shell
# vim env/gram.env
TOKEN=token
APP_ID=id
APP_HASH=hash
OWNER_ID=your user_id
MEILI_MASTER_KEY=token
```

# 5. Login to client

```shell
make init
```

After running make init, you will be dropped into a container shell.

```shell
python client.py
```

Follow the instruction to log in to your account.

When you see 'started xxx handlers', Ctrl + D to exit. You should find session file
under `searchgram/session/client.session`.

# 6. (optional)setup sync id

To synchronize the chat history for a user, group, or channel, you can configure the sync ID.

This allows you to specify which chats you want to sync the history for.

The first step in configuring the sync ID is to obtain the chat peer, which can be either an integer or a username.

You can obtain the chat peer by using https://t.me/blog_update_bot.

Next, you will need to manually edit the sync.ini file.
**It is recommended to use usernames whenever possible when configuring the sync ID.
If you need to use a user ID instead, it is important to talk to the person immediately after starting `client.py`
because you only have 30 seconds to do so.**

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

Once you have completed the previous steps, you can talk to your friends and search in your bot.

You can also use http://localhost:7700 to access the MeiliSearch Web UI.

If you have configured the sync ID, you can monitor the sync status in the Saved Messages.
