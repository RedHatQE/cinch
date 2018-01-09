import os
import unittest

from cinch.bin.wrappers import call_ansible, command_handler


class CinchCLI(unittest.TestCase):

    def test_exit_code_zero(self):
        # full path to the playbook and inventory must be specified in order to
        # avoid path issues with the BASE variable in wrappers.py
        playbook = os.path.join(os.getcwd(), 'tests/playbook.yml')
        inventory = os.path.join(os.getcwd(), 'tests/inventory.ini')

        # valid inventory and playbook files
        self.assertEqual(call_ansible(inventory, playbook), 0)

    def test_exit_code_one(self):
        # inventory and playbook files that do not exist
        self.assertEqual(call_ansible('junk.ini', 'junk.yml'), 1)

    def test_exit_code_255(self):
        # invalid data given to plumbum which should return exit code 255
        self.assertEqual(command_handler('invalid_command',
                                         'invalid_arg'), 255)
