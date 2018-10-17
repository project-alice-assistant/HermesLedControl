#!/usr/bin/env bash

systemctl stop snipsledcontrol
git reset --hard
git pull
cp snipsledcontrol.service /etc/systemd/system
systemctl daemon-reload
systemctl start snipsledcontrol