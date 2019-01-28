from __future__ import unicode_literals
from textx import metamodel_from_file
from textx.export import metamodel_export
import fnmatch
import os
from os.path import sep,join,dirname, exists

def main(path=None, debug=False):
    if path is None:
        path = join(dirname(__file__), "..", "..")

    print("render_all_grammars.py - example program")
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.tx'):
            matches.append((root, filename))
    for m in matches:
        inname = join(m[0],m[1])
        outfname_base = "{}_{}".format(
            m[0].replace(path,'').lstrip(sep).replace(sep,'_'),
            m[1].rstrip('.tx'));
        destpath = join(dirname(__file__),"dot")
        if not exists(destpath): os.mkdir(destpath)
        dest_dot = join(destpath, outfname_base+".dot")

        print(dest_dot)
        mm = metamodel_from_file(inname, debug=debug)
        metamodel_export(mm, dest_dot)

    print("after copying an initial output to out_ref,")
    print(" you may use: diff -Nsaur dot dot_ref |less")

if __name__ == "__main__":
    main()
