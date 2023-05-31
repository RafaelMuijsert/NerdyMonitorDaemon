INSTALL_DIR=/usr/local/bin
CONFIG_DIR=/etc/nmd

install:
	install -m 755 nmd.py $(INSTALL_DIR)/nmd
