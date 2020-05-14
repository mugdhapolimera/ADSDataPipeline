
from subprocess import PIPE, Popen

from adsdata.file_defs import data_files


def execute(command, **kwargs):
    print('command = {}'.format(command))
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE, **kwargs)
    out, err = p.communicate()
    return (p.returncode, out, err)


def sort_input_files(root_dir='logs/input/'):
    """the input files sorted in place to compute diffs"""
    # on my laptop, sorting bibcodes.list.can takes 30 seconds
    for x in data_files:
        f = root_dir + '/current/' + data_files[x]['path']
        command = 'sort -o {} {}'.format(f, f)
        execute(command)


def compute_changed_bibcodes(root_dir='logs/input/'):
    """generates a list of changed bibcoces by comparing input files in directory named current to directory named previous

    we use comm to compare the old and new files, then strip changes down to just the canonical bibcodes
    for every input file we create a list of changed bibcodes, then we merge these changed bibcoes files"""
    for x in data_files:
        c = root_dir + '/current/' + data_files[x]['path']
        p = root_dir + '/previous/' + data_files[x]['path']
        changed_bibs = root_dir + '/current/' + data_files[x]['path'] + '.changedbibs'
        #          find changes  | remove comm leading tab|remove blank|only bib| sort bibcodes | filter out non-canonical
        command = "comm -3 {} {} | sed $'s/^[ \t]*//g' | sed '/^$/d' | cut -f 1 | sort --unique | comm -2 -3 - {}  > {}".format(c, p, changed_bibs, root_dir + '/current/' + data_files['canonical']['path'])
        execute(command)


def merge_changed_bibcodes(root_dir='logs/input/'):
    """merge small change bibcode files into a single file"""
    o = root_dir + '/current/' + 'changedBibcodes.txt'
    for x in data_files:
        f = root_dir + '/current/' + data_files[x]['path'] + '.changedbibs'
        command = 'cat {} >> {}'.format(f, o)
        execute(command)
    command = 'sort --unique -o {} {}'.format(o, o)
    execute(command)

