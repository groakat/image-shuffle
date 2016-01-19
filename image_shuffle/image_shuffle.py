import numpy as np
import pandas as pd
import os
import shutil
import glob

def parse_folder(folder, glob_pattern=('*.jpg', '*png', '*.gif', '*.tiff', '*.jpeg')):
    files = []
    for pattern in glob_pattern:
        match = glob.glob(os.path.join(os.path.realpath(folder), pattern))
        if match:
            files += match

    return files


def rename_files(file_list, new_basenames):
    """ renames files

    Args:
        file_list (list(str): full path of file
        new_basenames (list(str)): new basename of files (without folder)
    """
    for f, new_basename in zip(file_list, new_basenames):

        folder = os.path.dirname(f)
        shutil.move(f, os.path.join(folder, new_basename))


def generate_random_names(file_list):
    """
    generates a list of basenames with zero-padded numbers and the correct
    file extension
    """

    numbers = np.random.permutation(range(len(file_list)))
    zero_pad = np.floor(len(file_list) / 10.0).astype(np.int)

    new_basenames = []

    for f, number in zip(sorted(file_list), numbers):
        basename = os.path.basename(f)
        ext = basename.split('.')[-1]

        new_basename = '{number:0{zp}d}.{ext}'.format(number=number,
                                                      zp=zero_pad,
                                                      ext=ext)

        new_basenames += [new_basename]

    return new_basenames

def basenames_to_full_path(basenames, folder):
    return [os.path.join(folder, x) for x in basenames]

def save_key(org_basenames, new_basenames, folder):
    df = pd.DataFrame(zip(org_basenames, new_basenames), columns=['original names', 'new names'])

    df.to_csv(os.path.join(folder, 'key.csv'))

def retrieve_key(folder):
    df = pd.read_csv(os.path.join(folder, 'key.csv'))

    org_basenames = df['original names'].tolist()
    new_basenames = df['new names'].tolist()

    return org_basenames, new_basenames

def save_observation_table(folder, new_basenames):
    df = pd.DataFrame(zip(new_basenames, [None for x in new_basenames]),
                       columns=['filename', 'observation'])
    df.sort_values(by='filename', inplace=True)

    df.to_excel(os.path.join(folder, 'observations.xlsx'), index=False)


def resolve_observation_table(folder, org_basenames, new_basenames):
    df = pd.read_excel(os.path.join(folder, 'observations.xlsx'))

    df['filename'].replace(new_basenames, org_basenames, inplace=True)
    df.sort_values(by='filename', inplace=True)

    df.to_excel(os.path.join(folder, 'observations.xlsx'), index=False)


def test_if_shuffled(folder):
    if os.path.exists(os.path.join(folder, 'key.csv')):
        return True
    else:
        return False

def remove_keys(folder):
    if os.path.exists(os.path.join(folder, 'key.csv')):
        os.remove(os.path.join(folder, 'key.csv'))


def shuffle(folder):
    org_files = parse_folder(folder)
    new_basenames = generate_random_names(org_files)

    rename_files(org_files, new_basenames)

    org_basenames = [os.path.basename(x) for x in org_files]
    save_key(org_basenames, new_basenames, folder)
    save_observation_table(folder, new_basenames)


def unshuffle(folder):
    org_basenames, new_basenames = retrieve_key(folder)
    new_files = basenames_to_full_path(new_basenames, folder)
    rename_files(new_files, org_basenames)
    resolve_observation_table(folder, org_basenames, new_basenames)

def main():
    import argparse
    import textwrap
    parser = argparse.ArgumentParser(\
    formatter_class=argparse.RawDescriptionHelpFormatter,\
    description=textwrap.dedent(\
    """
    Program to shuffle images in a folder by conceiling their original filename.

     The association between original filename and the newly generated filenames
     are stored in the key.csv file.

     The program automatically creates a new observation.xlsx file which can be
     used to record observations in the shuffled images.

     The un-shuffling process restores the original filenames and changes the
     place-holder filenames in observation.xlsx with the real filenames. It keeps
     the association between the user data and the images.
    """),
    epilog=textwrap.dedent(\
    """
    ============================================================================
    Written and tested by Peter Rennert in 2015 as part of his PhD project at
    University College London.

    You can contact the author via p.rennert@cs.ucl.ac.uk

    I did my best to avoid errors and bugs, but I cannot provide any liability
    with respect to software or hardware or data (including fidelity and potential
    data-loss), nor any issues it may cause with your experimental setup.

    <Licence missing>
    """))
    #
    # parser.add_argument('-c', '--shuffle',
    #             help="path to file containing configuration")

    parser.add_argument('mode', choices=['shuffle', 'unshuffle'],
                        help="Select either shuffling or unshuffling mode")

    parser.add_argument("target_folder", type=str,
                        help="target folder containing the images to be processed",
                        default='.')

    args = parser.parse_args()

    folder = args.target_folder

    if args.mode == 'shuffle':
        shuffle(folder)
    elif args.mode == 'unshuffle':
        unshuffle(folder)


if __name__ == "__main__":
    main()





