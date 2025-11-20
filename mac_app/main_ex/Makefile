DEV_ID := $(shell source ../IDs.sh && echo $$DEV_ID)
CFLAGS = -arch arm64 -arch x86_64 -mmacosx-version-min=10.15

all: Avain.c
	gcc $(CFLAGS) -o Avain -framework CoreFoundation Avain.c
	codesign -v -s $(DEV_ID) --timestamp --options runtime --force Avain
