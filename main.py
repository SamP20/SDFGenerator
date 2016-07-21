from fontTools.ttLib import TTFont
import sys

if __name__ == '__main__':
    argv = sys.argv
    font = TTFont(argv[1])
    
