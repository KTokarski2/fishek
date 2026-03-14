#!/bin/bash
set -e

VERSION="1.0.0"
APP_NAME="fishek"
RPM_BUILD_DIR="$HOME/rpmbuild"

echo "Files are copied to rpmbuild/SOURCES..."
mkdir -p "$RPM_BUILD_DIR/SOURCES/$APP_NAME"
cp -r dist/fishek/* "$RPM_BUILD_DIR/SOURCES/$APP_NAME/"
cp assets/icon.png "$RPM_BUILD_DIR/SOURCES/icon.png"

echo "Copying spec..."
cp fishek.spec.rpm "$RPM_BUILD_DIR/SPECS/fishek.spec"

echo "Building RPM..."
rpmbuild -bb "$RPM_BUILD_DIR/SPECS/fishek.spec"

echo "Done! RPM is located in:"
ls "$RPM_BUILD_DIR/RPMS/x86_64/"