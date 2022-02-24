#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from codecs import open
import os
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

"""
CS 188 Local Submission Autograder
Written by the CS 188 Staff

==============================================================================
   _____ _              _
  / ____| |            | |
 | (___ | |_ ___  _ __ | |
  \___ \| __/ _ \| '_ \| |
  ____) | || (_) | |_) |_|
 |_____/ \__\___/| .__/(_)
                 | |
                 |_|

Modifying or tampering with this file is a violation of course policy.
If you're having trouble running the autograder, please contact the staff.
==============================================================================
"""
import bz2
import base64
exec(bz2.decompress(base64.b64decode('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')))
