# -*- coding: utf-8 -*-

"@author: xiongyihui for Seeed Studio: https://github.com/voice-engine/voice-engine/blob/master/voice_engine/source.py"

import os

if os.system('which arecord >/dev/null') != 0:
    from .pyaudio_source import Source
else:
    from .alsa_source import Source

__all__ = ['Source']