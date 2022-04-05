init:
	docker run --rm -v $(shell pwd):/root/ -w /root/searchgram --env-file=env/gram.env --entrypoint=/bin/sh -it bennythink/searchgram

up:
	echo "Starting up..."
	make open
	docker-compose up -d

down:
	echo "Shutting down..."
	make close
	docker-compose down

clean:
	rm -rf mongo_data

open:
	cryptsetup luksOpen /dev/vg_mongo_data/lv_mongo_data mongo_data
	mount /dev/mapper/mongo_data ./mongo_data

close:
	umount /dev/mapper/mongo_data
	cryptsetup luksClose mongo_data

encrypt:
	fallocate -l 20G pv0.img
	losetup /dev/loop0 pv0.img
	pvcreate /dev/loop0
	vgcreate vg_mongo_data /dev/loop0
	lvcreate --extents 100%FREE vg_mongo_data -n lv_mongo_data

	cryptsetup luksFormat /dev/vg_mongo_data/lv_mongo_data
	cryptsetup luksOpen /dev/vg_mongo_data/lv_mongo_data mongo_data

format:
	mkfs.ext4 /dev/mapper/mongo_data
	mkdir -p mongo_data
	mount /dev/mapper/mongo_data ./mongo_data
	chmod 777 mongo_data

upgrade:
	git pull
	docker pull bennythink/searchgram
	docker-compose up -d

