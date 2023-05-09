INSTALL_DIR=/usr/local/bin
SCRIPTS_DIR=/usr/local/src/nmd
CONFIG_DIR=/etc/nmd

install:
	install -m 755 bin/measure.sh $(INSTALL_DIR)
