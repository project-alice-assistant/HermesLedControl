#!/usr/bin/env bash

systemctl stop snipsledcontrol
cp snipsledcontrol.service /etc/systemd/system
systemctl daemon-reload
systemctl start snipsledcontrol