#!/bin/sh

ROOTFS_DIR=/home/container

export PATH=$PATH:~/.local/usr/bin

PROOT_VERSION="5.3.0"
ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
  ARCH_ALT=amd64
elif [ "$ARCH" = "aarch64" ]; then
  ARCH_ALT=arm64
else
  printf "Unsupported CPU architecture: ${ARCH}"
  exit 1
fi

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
echo "#######################################################################################"
echo "#                                                                                     #"
echo "#                                    > thefeziak <                                    #"
echo "#                                                                                     #"
echo "#                                      FREE VPS                                       #"
echo "#                                                                                     #"
echo "#                                                                                     #"
echo "#######################################################################################"

  echo ""
  echo "* [0] Debian"
  echo "* [1] Ubuntu"
  echo "* [2] Alpine"

  read -p "Enter OS (0-2): " input

  case $input in

    0)
      wget --no-hsts -O /tmp/rootfs.tar.xz \
      "https://github.com/termux/proot-distro/releases/download/v3.18.1/debian-${ARCH}-pd-v3.18.1.tar.xz"
      apt download xz-utils
      deb_file=$(find "$ROOTFS_DIR" -name "*.deb" -type f)
      dpkg -x "$deb_file" ~/.local/
      rm "$deb_file"
      tar -xJf /tmp/rootfs.tar.xz -C "$ROOTFS_DIR"
      mkdir $ROOTFS_DIR/home/container/ -p

      wget -O $ROOTFS_DIR/home/container/installer.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/private.sh"
      wget -O $ROOTFS_DIR/home/container/.bashrc \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/.bashrc"
      wget -O $ROOTFS_DIR/home/container/style.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/style.sh"
      ;;

    1)
      wget --no-hsts -O /tmp/rootfs.tar.gz \
      "http://cdimage.ubuntu.com/ubuntu-base/releases/20.04/release/ubuntu-base-20.04.4-base-${ARCH_ALT}.tar.gz"
      tar -xf /tmp/rootfs.tar.gz -C "$ROOTFS_DIR"
      mkdir $ROOTFS_DIR/home/container/ -p

      wget -O $ROOTFS_DIR/home/container/installer.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/private.sh"
      wget -O $ROOTFS_DIR/home/container/.bashrc \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/.bashrc"
      wget -O $ROOTFS_DIR/home/container/style.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/style.sh"
      ;;

    2)
      wget --no-hsts -O /tmp/rootfs.tar.gz \
      "https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-minirootfs-3.18.3-${ARCH}.tar.gz"
      tar -xf /tmp/rootfs.tar.gz -C "$ROOTFS_DIR"
      mkdir $ROOTFS_DIR/etc/profile.d/ -p
      
      wget -O $ROOTFS_DIR/home/container/installer.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/private.sh"
      wget -O $ROOTFS_DIR/home/container/.bashrc \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/.bashrc"
      wget -O $ROOTFS_DIR/home/container/style.sh \
      "https://github.com/abdalla435/VPS-Pterodactyl-EGG/raw/main/style.sh"
      ;;

    *)
      echo "Invalid selection. Exiting."
      exit 1
      ;;
  esac
fi

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    mkdir -p "$ROOTFS_DIR/usr/local/bin"
    wget --no-hsts -O "$ROOTFS_DIR/usr/local/bin/proot" "https://github.com/proot-me/proot/releases/download/v${PROOT_VERSION}/proot-v${PROOT_VERSION}-${ARCH}-static"
    chmod 755 "$ROOTFS_DIR/usr/local/bin/proot"
fi

if [ ! -e "$ROOTFS_DIR/.installed" ]; then
    printf "nameserver 1.1.1.1\nnameserver 1.0.0.1" > "${ROOTFS_DIR}/etc/resolv.conf"
    rm -rf /tmp/rootfs.tar.xz /tmp/sbin
    touch "$ROOTFS_DIR/.installed"
fi

"$ROOTFS_DIR/usr/local/bin/proot" \
--rootfs="${ROOTFS_DIR}" \
-0 -w "/root" -b /dev -b /sys -b /proc -b /etc/resolv.conf --kill-on-exit \
/bin/bash
