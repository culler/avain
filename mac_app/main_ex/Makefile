DEV_ID := $(shell source ../IDs.sh && echo $$DEV_ID)
ARCH := $(shell uname -m)
ifeq ($(ARCH),x86_64)
CFLAGS = -mmacosx-version-min=10.15
else
CFLAGS = -mmacosx-version-min=11.0
endif
all: Avain.c
	gcc $(CFLAGS) -o Avain -framework CoreFoundation Avain.c
	codesign -v -s $(DEV_ID) --timestamp --options runtime --force Avain
