"""
This script generates then iterates through a mzML file, binning a specified number of spectra
CHANGELOG:
    ---4.2
"""

from pythoms.mzml import mzML
from pythoms.xlsx import XLSX
from pythoms.scripttime import ScriptTime


def sumspectra(filename, start=None, end=None, save=True):
    """
    Sums spectra from raw file and outputs to excel file

    :param filename: raw or mzML filename
    :param start: start scan (None will default to 1)
    :param end: end scan (None will default to the last scan)
    :param save: whether to save into an excel document (if a string is provided, that filename will be used)
    :return: paired x, summed y lists
    """

    st = ScriptTime()
    st.printstart()
    mzml = mzML(filename)  # create mzML object
    if start is None:
        start = mzml.functions[1]['sr'][0] + 1
    if end is None:
        end = mzml.functions[1]['sr'][1] + 1
    x, y = mzml.sum_scans(start=start, end=end)
    if save is not False:
        if type(save) == str:  # if a filename was provided for the Excel file
            xlfile = XLSX(save, create=True)
        else:  # otherwise use the mzML filename
            xlfile = XLSX(filename, create=True)
        xlfile.writespectrum(  # write the spectrum to file
            x,
            y,
            'summed spectra (scans %d-%d)' % (start, end)
        )
        xlfile.save()
    st.printend()
    return x, y  # return if specified


if __name__ == '__main__':
    fn = input('Filename to sum: ')  # ask user for filename
    startscan = input('Start scan (if no value is specified, default to 1): ')
    if len(startscan) == 0:
        startscan = None
    endscan = input('End scan (if no value is specified, default to last): ')
    if len(endscan) == 0:
        endcan = None
    sumspectra(
        # 'LY-2015-01-20 02',
        fn,  # raw filename to use
        start=startscan,  # start scan number
        end=endscan,  # end scan number
        save=True,  # save in an Excel workbook
    )
