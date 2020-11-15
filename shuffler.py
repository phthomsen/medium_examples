import random
import os
import gzip


def shuffler(infile, outfile, tempdir, nf=200):

    # count total number of rows in the file
    nr = 0
    with open(infile, encoding='utf-8') as f:
        for _ in f:
            nr += 1

    # number of rows to write in one tmp file
    nrf = int(nr / nf)

    # counts rows of current file
    cr = 1
    # counts number of files
    cf = 1

    # keep files in memory before writing them in a file
    cache = []

    os.system('mkdir ' + tempdir)

    filename = tempdir + 'tempfile_' + str(cf)
    fw = open(filename, 'a', newline='\n')

    # list of all tmp files
    files = [filename]

    # store data in temp files
    with open(infile, encoding='utf-8') as f:

        for line in f:

            cache.append(line)
            # if condition is true, stop collecting and start writing
            if cr == nrf:

                # shuffle the block internally
                random.shuffle(cache)

                for row in cache:
                    fw.write(row)

                cache = []

                cf += 1

                # close tmp file
                fw.close()

                # make sure to only create nf files
                if cf <= nf:
                    # change file name and open new tempfile
                    filename = tempdir + 'tempfile_' + str(cf)

                    # collect file name for later processing
                    files.append(filename)

                    fw = open(filename, 'a', newline='\n')

                    # set counter to zero and empty cache to collect data for the next file
                    cr = 0

                # break the loop if max number of tmp files is reached
                else:
                    break

            cr += 1

    fw.close()

    # create random array that specifies the order of files to write into the output file
    random.shuffle(files)

    ctw = 0
    # open the file to write to
    with gzip.open(outfile, 'at', newline='\n') as fw:

        # open up the tmp files and read
        for path in files:
            with open(path, encoding='utf-8') as fr:
                for line in fr:
                    # write to the output file
                    fw.write(line)

                    ctw += 1
            os.system('rm ' + path)

    # remove the tmp directory
    os.system('rm -r ' + tempdir)

