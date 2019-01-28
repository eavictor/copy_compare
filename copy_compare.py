import argparse
import os
import filecmp
import shutil
import subprocess
import logging


str_fmt = '[%(asctime)s] %(levelname)-8s %(filename)-20s line: %(lineno)-10d func: %(funcName)-30s msg: %(message)s'
logging.basicConfig(filename='copy_compare.log', level=logging.INFO, format=str_fmt)
logger = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Random file generator')
parser.add_argument('number', type=int, nargs=1, help='Integer number of file size')
parser.add_argument('unit', type=str, nargs=1, help='File size, accept B(Bytes), KB, MB, GB')
parser.add_argument('sleep_state', type=str, nargs=1, help='Decide which sleep state (S3, S4 or CS)')
parser.add_argument('-P', '--pair', type=int, nargs=1, default=1, help='How many file pairs to run. Default: 1')
parser.add_argument('-C', '--cycle', type=int, nargs=1, default=float('inf'),
                    help='How many cycles to run. Default: run forever until fail')
args = parser.parse_args()


number = args.number[0]
unit = args.unit[0].upper()
sleep_state = args.sleep_state[0].upper()
pair = args.pair[0]
cycle = args.cycle[0]


def remove_create_and_copy(original, copied):
    if os.path.isfile(original):
        logger.info(f'Remove Original file {original}')
        os.remove(original)
    if os.path.isfile(copied):
        logger.info(f'Remove Copied file {copied}')
        os.remove(copied)
    file_size = 1
    if unit == 'B':
        file_size = number
    elif unit == 'KB':
        file_size = number * 1024
    elif unit == 'MB':
        file_size = number * 1024 ** 2
    elif unit == 'GB':
        file_size = number * 1024 ** 3
    else:
        # break operation if getting unknown
        logger.warning(f'Unknown file unit {unit}. ({file_size} {unit})')
        subprocess.run('pause')
        subprocess.run('exit')  # exit cmd
        return

    with open(original, 'wb+') as file:
        logger.info('Creating file')
        file.write(os.urandom(file_size))

    logger.info('Copying file')
    shutil.copy2(original, copied)


def compare(original, copied):
    logger.info(f'Comparing if contents in {original} and {copied} are equal.')
    return filecmp.cmp(original, copied, shallow=False)  # shallow=False means compare file content


def s3_sleep():
    logger.info('Call Microsoft pwrtest.exe for S3 Sleep')
    subprocess.run(['pwrtest.exe', '/sleep', '/s:3', '/c:1', '/d:10', '/p:30'])


def s4_hibernate():
    logger.info('Call Microsoft pwrtest.exe for S4 Hibernate')
    subprocess.run(['pwrtest.exe', '/sleep', '/s:4', '/c:1', '/d:10', '/p:30'])


def cs_modern_standby():
    logger.info('Call Microsoft pwrtest.exe for CS Modern Standby')
    subprocess.run(['pwrtest.exe', '/cs', '/c:1', '/d:10', '/p:30'])


def main():
    iteration = 0

    # Step 0: Check Parameters are logical valid
    if number < 1:
        logger.warning(f'File Size must >= 1, you entered {number}')
        subprocess.run('pause')
        subprocess.run('exit')
        return
    if unit not in ['B', 'KB', 'MB', 'GB']:
        logger.warning(f'File Unit must be one of B, KB, MB or GB, you entered {unit}')
        subprocess.run('pause')
        subprocess.run('exit')
        return
    if sleep_state not in ['S3', 'S4', 'CS']:
        logger.warning(f'Sleep State must be one of S3, S4 or CS, you entered {sleep_state}')
        subprocess.run('pause')
        subprocess.run('exit')
        return
    if pair < 1:
        logger.warning(f'File Pair must >= 1, you entered {pair}')
        subprocess.run('pause')
        subprocess.run('exit')
        return
    if cycle < 1:
        logger.warning(f'Iteration Cycle must >= 1, you entered {cycle}')
        subprocess.run('pause')
        subprocess.run('exit')
        return

    while True:
        logger.info(f'Iteration {iteration} START')
        # Step 1: Handle file pairs
        for i in range(pair):
            original = f'RAND_{i}.bin'
            copied = f'RAND_COPY_{i}.bin'

            # Case 1: Initial setup, only create file
            if not os.path.isfile(original) and not os.path.isfile(copied):
                logger.info(f'Create file pair {original} and {copied} (Initial state)')
                remove_create_and_copy(original=original, copied=copied)

            # Case 2: Missing original file
            elif not os.path.isfile(original) and os.path.isfile(copied):
                logger.critical(f'Missing file {original}, stop iteration.')
                subprocess.run('pause')
                subprocess.run('exit')
                break

            # Case 3: Missing copied file
            elif os.path.isfile(original) and not os.path.isfile(copied):
                logger.critical(f'Missing file {copied}, stop iteration.')
                subprocess.run('pause')
                subprocess.run('exit')
                break

            # Case 4: Both original file and copied file exist, start compare
            else:
                logger.info(f'Compare {original} and {copied}')
                if compare(original=original, copied=copied):  # compare file content, not only meta
                    logger.info(f'Compare results equal, delete and re-create file pair ({original} and {copied})')
                    remove_create_and_copy(original=original, copied=copied)
                else:
                    logger.critical(f'Compare {original} and {copied} results NOT equal, stop iteration.')
                    subprocess.run('pause')
                    subprocess.run('exit')
                    break

        # Step 2: Sleep
        if sleep_state == 'S3':
            logger.info(f'Enter S3 (Sleep) for 30 seconds.')
            s3_sleep()
        elif sleep_state == 'S4':
            logger.info(f'Enter S4 (Hibernate) for 30 seconds.')
            s4_hibernate()
        elif sleep_state == 'CS':
            logger.info(f'Enter CS (Modern Standby) for 30 seconds.')
            cs_modern_standby()
        else:
            logger.critical(f'Sleep State {sleep_state} not recognized, only accept S3, S4 and CS')
            subprocess.run('pause')
            subprocess.run('exit')
            break

        # Step 3: Check if reached user defined iteration cycle.
        if iteration > cycle:
            logger.info(f'Reached user defined iteration cycle ({cycle} times), stop copy compare.')
            # Remove all files
            for i in range(pair):
                original = f'RAND_{i}.bin'
                copied = f'RAND_COPY{i}.bin'
                if os.path.exists(original):
                    os.remove(original)
                if os.path.exists(copied):
                    os.remove(copied)
            subprocess.run('pause')
            subprocess.run('exit')
            break

        # Step 4: If everything goes well, increase iteration by 1
        logger.info(f'Iteration {iteration} COMPLETE.')
        iteration += 1


if __name__ == '__main__':
    main()
