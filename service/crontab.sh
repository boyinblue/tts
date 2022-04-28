#!/bin/bash

running=$(systemctl --user status tts | grep running)

if [ "$running" != "" ]; then
  systemctl --user restart tts
fi
