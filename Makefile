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
	rm -rf es_data

open:
	cryptsetup luksOpen /dev/vg_es_data/lv_es_data es_data
	mount /dev/mapper/es_data ./es_data

close:
	umount /dev/mapper/es_data
	cryptsetup luksClose es_data

encrypt:
	fallocate -l 20G pv0.img
	losetup /dev/loop0 pv0.img
	pvcreate /dev/loop0
	vgcreate vg_es_data /dev/loop0
	lvcreate --extents 100%FREE vg_es_data -n lv_es_data

	cryptsetup luksFormat /dev/vg_es_data/lv_es_data
	cryptsetup luksOpen /dev/vg_es_data/lv_es_data es_data

format:
	mkfs.ext4 /dev/mapper/es_data
	mkdir -p es_data
	mount /dev/mapper/es_data ./es_data
	chmod 777 es_data

upgrade:
	git pull
	docker pull bennythink/searchgram
	docker-compose up -d