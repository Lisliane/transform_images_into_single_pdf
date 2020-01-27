import sys
import constant
from bin.copydir import CopyDir


def main():
    """
      Main
    """

    copydir = CopyDir()
    copydir.run(constant.PATCH_SOURCE, constant.PATCH_DESTINY)


if __name__ == '__main__':
    sys.exit(main())
