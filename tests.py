#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 16:47:26 2020

@author: dale
"""

import expparams


def main():
    frameName14 = "burn_5ms_000002.cbf"
    reader = expparams.CbfReader(frameName=frameName14)
    detector = reader.getDetector()
    print(detector)
    return

if __name__ == "__main__":
    main()