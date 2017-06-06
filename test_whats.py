#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from whats import whats


def test_tellme():
    assert whats.tellme('美妙的新世界')
