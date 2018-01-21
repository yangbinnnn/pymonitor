#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : Yang
# Creadted  : 2017-04-17 23:33:26

import os
import time

if __name__ == '__main__':
    try:
        while True:
            print "[time]: %s." % time.ctime()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
