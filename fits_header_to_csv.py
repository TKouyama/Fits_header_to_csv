#
# Converting fits header lines to a csv file.
#

import numpy as np
from astropy.io import fits

import os
import pandas as pd

def fits_header_to_csv(ifname_fits,ofname_csv,extension=0):
    #
    # check HDU ##
    #
    hdulist_onc=fits.open(ifname_fits)
    hdulist_onc.info()  
    hdu_onc=hdulist_onc[extension]

    # header read
    header_onc=hdu_onc.header

    ##
    ## At first, output Header lines in a work file
    ##
    tmp_header_output = './.tmp.txt'
    with open(tmp_header_output, 'w') as f:
        print(repr(header_onc),file=f)

    ##
    ## Then, read again the lines from the work file.
    ##
    # Read a file witout "/n"
    with open(tmp_header_output, 'r') as f:
        cards = f.read().splitlines()

    ## Dividing each line into keyword, value, and comment ##
    keywords = []
    values = []
    comments = []
    for i, card in enumerate(cards):
    
        if card[0:8] != "COMMENT " and card[0:8] != "HISTORY ":
            keywords.append(card[0:8])
            ## Read value part within nominal length. ##
            value = card[9:31]

            ## for the case the length of the value expression is longer than nominal (8-32) ##
            value_and_comment = card[31:]

            ## spliting string at "/"
            tmp = value_and_comment.split('/')
            s_pos = value_and_comment.find('/')

            if s_pos >= 1:
                values.append(value+value_and_comment[0:s_pos-1])
                comments.append(value_and_comment[s_pos+1:])
            else:
                values.append(value)
                if len(tmp) >= 2:
                    comments.append(value_and_comment[1:])
                else:
                    comments.append('')
                    
    ## Output CSV ##
    out_csv = {"Keywords": keywords,
               "Values": values,
               "Comments": comments}
    df = pd.DataFrame(out_csv)
    df.to_csv(ofname_csv,index=False)

    ## Delete the work file.
    os.remove(tmp_header_output)

    
if __name__ == '__main__':
    # sample 1
    ifname_onc = "./hyb2_onc_20180921_025306_tvf_l2c.fit"
    ofname_csv = "./hyb2_onc_20180921_025306_tvf_l2c.csv"
    
    fits_header_to_csv(ifname_onc,ofname_csv)

