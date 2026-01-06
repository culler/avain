ICON_NAME="Avain"

# This should be a 1024x1024 png image with an 832x832 rounded
# rectangle icon background.  The icon image is allowed to extend
# outside of the rounded rectangle.
PNG_FILE="${ICON_NAME}_icon.png"
ICONSET_DIR="${ICON_NAME}.iconset

sips -z 16 16 ${PNG_FILE} --out ${ICONSET_DIR}/icon_16x16.pn
sips -z 32 32 ${PNG_FILE} --out ${ICONSET_DIR}/icon_16x16@2x.png
sips -z 32 32 ${PNG_FILE} --out ${ICONSET_DIR}/icon_32x32.png
sips -z 64 64 ${PNG_FILE} --out ${ICONSET_DIR}/icon_32x32@2x.png
sips -z 128 128 ${PNG_FILE} --out ${ICONSET_DIR}/icon_128x128.png
sips -z 256 256 ${PNG_FILE} --out ${ICONSET_DIR}/icon_128x128@2x.png
sips -z 256 256 ${PNG_FILE} --out ${ICONSET_DIR}/icon_256x256.png
sips -z 512 512 ${PNG_FILE} --out ${ICONSET_DIR}/icon_256x256@2x.png
sips -z 512 512 ${PNG_FILE} --out ${ICONSET_DIR}/icon_512x512.png
cp ${PNG_FILE} ${ICONSET_DIR}/icon_512x512@2x.png
iconutil -c icns ${ICONSET_DIR}
