INSTALL_DIR=/usr/local/bin
CONFIG_DIR=/etc/nmd

requirements:
	apt install -y libmariadb3 libmariadb-dev
	pip3 -q install -r requirements.txt

install:
	install -m 755 nmd.py $(INSTALL_DIR)/nmd
