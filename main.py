from src import encryption
from argparse import ArgumentParser
import os

if __name__ == '__main__':

    #Declare CLI Args
    parser = ArgumentParser()
    parser.add_argument(
        'datatablePath',
        type=str,
        help='Path to datatable folder'
    )
    # parser.add_argument(
    #     'songId',
    #     type=str,
    #     help='Song id'
    # )


    #parse args
    args = parser.parse_args()

    #decrypt datatable
    if not os.path.isdir(args.datatablePath):
        raise Exception('Datatable folder does not exist')

    encryption.type = encryption.Keys.Datatable
    for path, subdirs, files in os.walk(args.datatablePath):
        for name in files:
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                encryption.save_file(
                    file=full_path,
                    outdir=full_path,
                    encrypt=False,
                )


