INSTALL_DIR=/usr/local/bin
SYSTEMD_UNIT_DIR=/lib/systemd/system
CONFIG_DIR=/etc/nmd

requirements:
	apt install -y libmariadb3 libmariadb-dev
	pip3 -q install -r requirements.txt

install:
	install -m 755 nmd.py $(INSTALL_DIR)/nmd

uninstall:
	rm -rf $(INSTALL_DIR)/nmd
	rm -rf $(SYSTEMD_UNIT_DIR)/nmd.service
	rm -rf $(CONFIG_DIR)