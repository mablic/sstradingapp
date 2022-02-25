#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class BackTester:

    # BackTester takes different strategy fromt the strategy class.
    def __init__(self, strategy):
        self.strategy = strategy

    def run_back_tester(self):
        return self.strategy.run_back_tester()

if __name__ == '__main__':

    pass
