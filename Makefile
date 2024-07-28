init:
	docker run --rm -v $(shell pwd)/sg_data/session:/SearchGram/searchgram/session --env-file=env/gram.env --entrypoint=/bin/sh -it bennythink/searchgram

up:
	echo "Starting up..."
	make open
	docker-compose up -d

down:
	echo "Shutting down..."
	make close
	docker-compose down

clean:
	rm -rf sg_data

open:
	cryptsetup luksOpen /dev/vg_sg_data/lv_sg_data sg_data
	mount /dev/mapper/sg_data ./sg_data

close:
	umount /dev/mapper/sg_data
	cryptsetup luksClose sg_data

encrypt:
	fallocate -l 20G pv0.img
	losetup /dev/loop0 pv0.img
	pvcreate /dev/loop0
	vgcreate vg_sg_data /dev/loop0
	lvcreate --extents 100%FREE vg_sg_data -n lv_sg_data

	cryptsetup luksFormat /dev/vg_sg_data/lv_sg_data
	cryptsetup luksOpen /dev/vg_sg_data/lv_sg_data sg_data

format:
	mkfs.ext4 /dev/mapper/sg_data
	mkdir -p sg_data
	mount /dev/mapper/sg_data ./sg_data
	chmod 777 sg_data

upgrade:
	git pull
	docker pull bennythink/searchgram
	docker-compose up -d

