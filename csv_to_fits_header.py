
import numpy as np
from astropy.io import fits
import os
import pandas as pd



#
# function for checking whether string can be converted to numeric or not.
# 参考)https://note.nkmk.me/python-str-num-determine/
#
def is_num(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

#
# and int or not
#
def is_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True

    
def csv_to_fits_header(ifname_csv, data_fits, ofname_fits):


    # Setting HDU
    hdu_out = fits.PrimaryHDU(data_fits)

    # Header #
    header = hdu_out.header

    #
    # Extracting values from CSV attribute
    #
    df = pd.read_csv(ifname_csv) #, names=('Keyword','Value','Comment'))
    df_values = df.values

    # adding each line to fits header attribute
    for i in range(len(df.values)):

        keyword=df_values[i,0]
        if (keyword != 'NAXIS   '
            and keyword != 'NAXIS1  '
            and keyword != 'NAXIS2  '
            and keyword != 'XTENSION'
            #and keyword != 'PCOUNT  '
            #and keyword != 'GCOUNT  '
            #and keyword != 'EXTNAME '
            #and keyword != 'EXTVER  '
            and keyword != 'BITPIX  '):

            #print(df_values[i,1], is_num(df_values[i,1]))

            # confirming value is number or string #
            if is_num(df_values[i,1]):
                if is_int(df_values[i,1]):
                    header.append( (keyword,int(df_values[i,1]), df_values[i,2] ) )
                else:
                    header.append( (keyword,float(df_values[i,1]), df_values[i,2] ) )
            else:
                out_str = str(df_values[i,1])
                out_str = out_str.replace("'","")
                out_str = out_str.replace("   ","")
                out_str = out_str.replace("  ","")
                header.append( (keyword, out_str, df_values[i,2] ) )

    hdulist = fits.HDUList([hdu_out])
    hdulist.writeto('./sample.fits',overwrite=True)

if __name__ == '__main__':

    ifname_csv = "./hyb2_onc_20180921_025306_tvf_l2c.csv"
    data_fits = np.zeros((100,100),dtype=float)
    ofname_fits = "./sample.fit"

    csv_to_fits_header(ifname_csv,data_fits, ofname_fits)
