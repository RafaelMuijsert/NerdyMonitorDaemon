INSTALL_DIR=/usr/local/bin
SYSTEMD_UNIT_DIR=/lib/systemd/system
CONFIG_DIR=/etc/nmd

requirements:
	apt install -y libmariadb3 libmariadb-dev
	pip3 -qqq install -r requirements.txt

install: requirements
	install -m 755 nmd.py $(INSTALL_DIR)/nmd
	install -Dm 644 config/nmd.service $(SYSTEMD_UNIT_DIR)/nmd.service
	install -Dm 644 config/nmd.ini $(CONFIG_DIR)/nmd.ini

uninstall:
	rm -rf $(INSTALL_DIR)/nmd
	rm -rf $(SYSTEMD_UNIT_DIR)/nmd.service
	rm -rf $(CONFIG_DIR)