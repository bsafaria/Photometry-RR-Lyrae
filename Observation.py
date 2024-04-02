import numpy as np
from astropy.io import fits
import sep
import matplotlib.pyplot as plt
from astropy.table import Table
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs import WCS
import glob
import warnings
from astropy.visualization import ZScaleInterval, ImageNormalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
from datetime import datetime
#%%

def readImageData(f):  # The argument f is a string that contains the file name to be read
    ''' Inputs .fits files and extracts relevant float data of the sky'''
    hdu = fits.open(f)  # Open the file
    image_data = hdu[0].data  # get the data, and assign to image_data (after calibration they're already floats)
    image_data = image_data.byteswap(
        inplace=True).newbyteorder()  # This line is need for SEP; otherwise it produces an error

    return hdu, image_data


def subtractSky(image_data, index, filter_size, box_size):
    ''' Inputs image_data and its index within the iterable.
        filter_size is the filter width and height in pixels
        box_size is the size of background boxes in pixels
        
        The function subtracts the sky noise from the frame'''
    
    sky = sep.Background(image_data, fw=filter_size, fh=filter_size, bh=box_size,
                         bw=box_size)  # use SEP to determine the background sky level
    sky_data = sky.back()  # This is the 2D array containing the sky level in each pixel (ADUs)

    image_data_nosky = image_data - sky_data  # Subtract the sky data from the image data and assign the result to image_data_sub

    if index == 0: # I just want to see the plot of one of the images
        makeplots(image_data, sky_data, image_data_nosky)  # Call the function makeplots defined below

    return sky_data, image_data_nosky, sky.globalrms


def makeplots(image_data, sky_data, image_data_nosky):
    fig, ax = plt.subplots(1, 3, figsize=[12, 4])

    norm = ImageNormalize(image_data, interval=ZScaleInterval())  # scales the image by same 'zscale' algorithm as ds9
    im0 = ax[0].imshow(image_data, origin='lower', cmap='gray', norm=norm)
    ax[0].set_title('Original')

    im1 = ax[1].imshow(sky_data, origin='lower', cmap='gray')  # linear.  no need for zscale
    ax[1].set_title('Sky')

    norm = ImageNormalize(image_data_nosky,
                          interval=ZScaleInterval())  # scales the image by same 'zscale' algorithm as ds9
    im2 = ax[2].imshow(image_data_nosky, origin='lower', cmap='gray', norm=norm)
    ax[2].set_title('After sky subtraction')

    # Remove the ticks and tick labels
    for a in ax:
        a.xaxis.set_visible(False)
        a.yaxis.set_visible(False)

    # Add colour bars to all three panels (not as simple when using subplots; calls function below)
    colourbar(im0, ax[0])
    colourbar(im1, ax[1])
    colourbar(im2, ax[2])
    fig.tight_layout()
    fig.savefig('test_sky_subtraction.png')


def colourbar(sc, ax):
    # This function is complete.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size="5%", pad=0.05)
    cbar = plt.colorbar(sc, cax=cax, orientation='vertical')

def computeNoise(image_data_nosky, sky_data, texp):
    ''' This function computes the total noise in units of ADUs.  Aside from the image data and sky data, you will also need:
      - gain
      - read noise
      - dark current
        The total noise is the sum (in quadrature) of 4 sources of noise: the read noise, the dark noise, the sky noise and the data noise '''

    # 1. Declare the gain and read noise (in electrons)
    gain = 1.5
    noise_read = 19.

    # 2. Read the master dark data and compute the Poisson noise (in electrons)
    hdu = fits.open('MasterDark.fit')
    MasterDark = hdu[0].data
    noise_dark = np.mean(np.sqrt(gain * np.abs(MasterDark)))

    # 3. Compute the Poisson noise of the sky in electrons
    noise_sky = np.sqrt(gain * np.abs(sky_data))

    # 4. Compute the Poisson noise of the sky-subtracted image in electrons
    noise_image = np.sqrt(gain * np.abs(image_data_nosky))

    # 5. Total noise: add the image noise, sky noise, dark noise and read noise in quadrature.  Note that the dark noise defined above
    # is the dark noise per second.  Make sure to scale it up by the exposure time.
    noise = np.sqrt(noise_image ** 2 + noise_sky ** 2 + texp * noise_dark ** 2 + noise_read ** 2)

    # 6. Turn the noise back into units of ADU
    noise /= gain

    return noise  # Return the noise in units of ADU


def sourceExtraction(image_data_nosky, skyrms):
    
    ''' Use sep.extract to find all the objects in image_data_nosky that are 2-sigma above the background,
     where sigma (err) is the skyrms '''
    
    objects = sep.extract(image_data_nosky, 20., err=skyrms)

    # Get the dimensions of image_data_nosky
    ny, nx = np.shape(image_data_nosky)

    # We are going to keep only those objects whose light-weighted centres are more than 30 pixels
    # away from the edge of the image.  objects['x'] and objects['y'] are the pixel coordinates of
    # the light-weighted centres.  The following illustrates how masks are used to select a subset
    # of an array or table.
    mask = (objects['x'] > 30) & (objects['x'] < nx - 30) & (objects['y'] > 30) & (objects['y'] < ny - 30)
    objects = objects[mask]  # Here we've overwritten "objects" with a subset that fulfill the above criteria

    return objects  # Return the structured array of objects


# %%
# The first task is to gather all the raw data and get the calibrated science frame for each file
# The master dark and master bias calibrations are found from the night of the observation

raw_filelist = glob.glob('RR_Leo_a_11.03.21/RR*') + glob.glob('RR_Leo_b_11.03.21/RR*')  # creates a list of the .fit files

# importing the master calibrations
hdu = fits.open('MasterBias.fit')  # open the master bias file
MasterBias = hdu[0].data.astype('float')  # take the data, convert to floats, and assign it to MasterBias
hdu = fits.open('MasterDark.fit')  # open the master dark file
MasterDark = hdu[0].data.astype('float')  # take the data, convert to floats, and assign it to MasterDark
hdu = fits.open('MasterFlat_PhotV.fits')  # open master flat for photV
MasterFlat = hdu[0].data.astype('float')  # take the data, convert to floats, and assign it to MasterFlat

for f in raw_filelist:
    hdu = fits.open(f)  # open the file f
    rawdata = hdu[0].data.astype('float')  # get the data, convert to float, and assign to rawdata
    texp = hdu[0].header['EXPTIME']  # get the exposure time

    # Use the calibration equation to calibrate the data
    calibrated_data = (rawdata - texp * MasterDark - MasterBias) / MasterFlat

    # modify the hdu file, but save it in the calibrated directory
    hdu[0].data = calibrated_data
    hdu[0].header['CLBRATED'] = (True, 'Calibrated from file ' + f)
    hdu[0].header['BZERO'] = 0
    hdu[0].header['BSCALE'] = 1.0

    filename = f[18:]  # strip the file name of the leading directory in the full path
    hdu.writeto('RR_Leo_11.03.21_calibrated/' + filename, overwrite=True)


#%%
# Now we do sky subtraction on our calibrated frames

# import the calibrated files
calibrated_filelist = glob.glob('RR_Leo_11.03.21_calibrated/*')

for f, index in zip(calibrated_filelist, range(len(calibrated_filelist))):
    # Call the function to read the file
    hdu, image_data = readImageData(f)

    sky_data, image_data_nosky, skyrms = subtractSky(image_data, index, filter_size=10, box_size=64)

    # Once you're happy with the sky subtraction, save the sky data and sky-subtracted image into new files
    filename = f[26:]
    hdu[0].header['GLOBLRMS'] = skyrms
    hdu[0].data = sky_data  # Re-use the header information from the old hdu, but overwrite the data with the sky data
    hdu.writeto('RR_Leo_11.03.21_calibrated_sky/' + filename, overwrite=True)  # save the hdu as new file

    hdu[
        0].data = image_data_nosky  # Re-use the header information from the old hdu, but overwrite the data with the sky-subtracted image
    hdu.writeto('RR_Leo_11.03.21_calibrated_nosky/' + filename, overwrite=True)  # save the hdu as new file


#%%

nosky_filelist = glob.glob('RR_Leo_11.03.21_calibrated_nosky/*')
sky_filelist = glob.glob('RR_Leo_11.03.21_calibrated_sky/*')

airmass = []
mags = []
mag_errors = []
sn = []
time = []
for fnosky, fsky in zip(nosky_filelist, sky_filelist):
    # initializing data
    hdu_nosky, hdu_sky = fits.open(fnosky), fits.open(fsky)  # Open the file f
    image_data_nosky, sky_data = hdu_nosky[0].data, hdu_sky[0].data
    image_data_nosky, sky_data = image_data_nosky.byteswap(inplace=True).newbyteorder(), sky_data.byteswap(inplace=True).newbyteorder()

    texp = hdu_nosky[0].header['EXPTIME']  # get the exposure time
    timestring = hdu_nosky[0].header['DATE-OBS']
    t = datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S')
    time.append(t)

    am = hdu_nosky[0].header['AIRMASS']  # get the air mass from the header
    airmass.append(am)  # append am to the airmass list

    noise = computeNoise(image_data_nosky, sky_data, texp)

    skyrms = hdu_sky[0].header['GLOBLRMS']

    # perform aperture photometry

    objects = sourceExtraction(image_data_nosky, skyrms)

    kronrad, krflag = sep.kron_radius(image_data_nosky, objects['x'], objects['y'], objects['a'], objects['b'],
                                      objects['theta'], 6.0)
    flux_radius = 2.5 * kronrad * objects['b']

    # This line measures the flux within 2.5*Kron radius
    flux, fluxerr, flag = sep.sum_ellipse(image_data_nosky, objects['x'], objects['y'], objects['a'], objects['b'],
                                          objects['theta'],
                                          2.5 * kronrad, subpix=5, err=noise)


    # we want to find the extinction coefficient, so we have to find which flux corresponds to RR Leo
    # this is easy to find manually since the telescope is centered on the object and its pretty isolated

    idx = np.where((objects['x'] > 900) & (objects['x'] < 1300) & (objects['y'] > 925) & (objects['y'] < 1120))[0][0]
    print(idx) # to make sure only RR Leo is indexed

    flux_RRLeo = flux[idx]
    fluxerr_RRLeo = fluxerr[idx]
    sn.append(flux_RRLeo/ fluxerr_RRLeo)

    # We need to use the reference star and find its instrumental magnitude
    # the reference star is GSC 1968:912
    x_GSC, y_GSC = 508, 1089  # rough coordinates of the star, although it changes.

    distances_to_GSC = np.sqrt((objects['x'] - x_GSC) ** 2 + (objects['y'] - y_GSC) ** 2)
    GSC_index = np.argmin(distances_to_GSC)
    flux_GSC = flux[GSC_index]
    fluxerr_GSC = fluxerr[GSC_index]

    mag_instrument_GSC = -2.5 * np.log10(flux_GSC / texp)

    mag_offset = 11.02 - mag_instrument_GSC

    # Determine the instrumental magnitude from flux_pick; This is the Pogson equation with C=0
    mag_instrument_RRLeo = -2.5 * np.log10(flux_RRLeo / texp)  # instrumental magnitude
    mag_instrument_error_RRLeo = 2.5 * fluxerr_RRLeo / (flux_RRLeo * np.log(
        10))  # determine the error on the magnitude using error propagation through a function

    standard_mag = mag_instrument_RRLeo + mag_offset
    # Append mag_instrument to the mags list
    mags.append(standard_mag)

    # Append mag_err to the mag_errors list
    mag_errors.append(mag_instrument_error_RRLeo)


# convert airmass, mags, mag_errors to numpy arrays

mags = np.array(mags)
mag_errors = np.array(mag_errors)
airmass = np.array(airmass)
sn = np.array(sn)
#%%
# now we plot our obtained values

plt.plot(mags, 'o')
time_labels = ["%s:%s" % (i.hour, i.minute) for i in time] # this creates a label for our times we can plot on the x-axis
positions = range(len(mags))
plt.gca().invert_yaxis()
plt.gcf().autofmt_xdate()
plt.xticks(positions[::30], time_labels[::30]) # x ticks every 30 exposures
plt.ylabel('Apparent Magnitude')
plt.xlabel('Time (UCT)')
plt.hlines(11.019140085443993, 0, 219, 'r', linestyles='dashed')
plt.text(20, 10.99, f'Peak minimum = {np.round(np.max(mags), 3)} ± {np.round(mag_errors[np.argmax(mags)], 3)}')
plt.savefig('RRLeo_magnitude.pdf')
plt.show()
