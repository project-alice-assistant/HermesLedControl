#!/usr/bin/env bash

systemctl stop snipsledcontrol
git stash
git reset --hard HEAD
git clean -f
git checkout master
git stash apply
cp snipsledcontrol.service /etc/systemd/system
systemctl daemon-reload
systemctl start snipsledcontrol