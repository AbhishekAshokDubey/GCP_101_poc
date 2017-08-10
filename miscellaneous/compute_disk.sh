https://cloud.google.com/compute/docs/disks/add-persistent-disk#create_disk

lsblk

mkdir /mnt/phm-disk
sudo mkfs.ext4 -m 0 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb
#sudo mkfs.ext4 -a /dev/sdb

sudo mount -o discard,defaults /dev/sdb /mnt/phm-disk

lsblk

sudo mkdir /mnt/phm-disk/phm-data
sudo gsutil cp -r gs://abhi-ml/data/phm_unzipped_data /mnt/phm-disk/phm-data


#sudo chmod a+w /mnt/phm-disk

sudo python # when we writing to disk, this refer to diff python, in case you have one on your profile
sudo pip

pip show pandas
sudo pip show pandas
