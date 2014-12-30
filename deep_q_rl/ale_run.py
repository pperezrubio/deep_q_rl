"""This script launches all of the processes necessary to train a
deep Q-network on an ALE game.

All unrecognized command line arguments will be passed on to
rl_glue_ale_agent.py
"""
import subprocess
import sys
import os
import argparse

DefaultBaseROMPath = "/usr/src/machinelearning/Arcade-Learning-Environment/roms/"
DefaultROM = 'breakout.bin'
DefaultPort = 4096


def main(args):
    # Check for glue_port command line argument and set it up...
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-r', '--rom', dest="rom", default=DefaultROM,
                        help='ROM to run (default: %(default)s)')
    parser.add_argument('--glue-port', dest="glue_port", type=int, default=DefaultPort,
                        help='rlglue port (default: %(default)s)')
    parameters, unknown = parser.parse_known_args(args)

    my_env = os.environ.copy()
    my_env["RLGLUE_PORT"] = str(parameters.glue_port)

    full_rom_path = os.path.join(DefaultBaseROMPath, parameters.rom)

    # Start the necessary processes:
    p1 = subprocess.Popen(['rl_glue'], env=my_env, close_fds=True)
    p2 = subprocess.Popen(['ale', '-game_controller', 'rlglue', '-frame_skip', '1', full_rom_path],
                          env=my_env, close_fds=True)
    p3 = subprocess.Popen(['./rl_glue_ale_experiment.py'], env=my_env, close_fds=True)
    p4 = subprocess.Popen(['./dummy_agent.py'] + sys.argv[1:], env=my_env, close_fds=True)

    p1.wait()
    p2.wait()
    p3.wait()
    p4.wait()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
