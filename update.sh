#!/usr/bin/env bash

systemctl stop snipsledcontrol
git stash
git reset --hard HEAD
git clean -f
git pull
git stash apply
chown -R pi ~/snipsLedControl
systemctl start snipsledcontrol