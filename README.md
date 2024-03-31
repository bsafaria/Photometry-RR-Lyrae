<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#resources">Resources</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Note: This is not necessarily a reproducible experiment, as the data collected and operation were done using the Trottier Observatory at Simon Fraser University which is available only by special permission. The original data has since been lost to time. The data input takes the form of [Flexible Image Transport System](https://docs.astropy.org/en/stable/io/fits/) (FITS) files specific to the hardware and collection method at the Trottier Observatory.

This project uses sky calibration and aperture photometry methods to measure the periodic magnitude fluctuation (known as a light curve) of a cepheid variable star, RR Leo, in the class of RR Lyrae stars. With the star's light curve measured out, one can then calculate for parameters of interest, such as brightness fluctuation period, peak brightness, and distance to name a few. An RR Lyrae star was chosen due to its relatively rapid periodicity, allowing an overnight observation to wholly describe the fluctuations.

Because the observations were done on the ground, the [Charge-Coupled Device](https://en.wikipedia.org/wiki/Charge-coupled_device) CCD image sensor picks up systematic sources of noise that must be accounted for. These sources are dark currents, offset bias, sky brightness, pixel-to-pixel variations in sensitivity, quantum efficiency, atmospheric absorption and dust. The purpose of the code in Observation.py is to correct these.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[<img src="https://www.astropy.org/images/astropy_word.svg" alt="Astropy.svg" width="300" height="100">][Astropy-url]
[<img src="https://numpy.org/images/logo.svg" alt="Numpy.svg" width="300" height="100">][Numpy-url]
[<img src="https://matplotlib.org/_static/logo_light.svg" alt="Numpy.svg" width="300" height="100">][Matplotlib-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Behzad Safarian Kashani - [LinkedIn](https://www.linkedin.com/in/bsk00/) - bsafariak@gmail.com

Project Link: [https://github.com/bsafaria/Photometry-RR-Lyrae](https://github.com/bsafaria/Photometry-RR-Lyrae)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to thank [Dr. Joanna Woo](https://www.sfu.ca/physics/people/faculty/jwa304.html) from Simon Fraser University, the Director of the Trottier Observatory in April 2021, for approving the overnight observation and operation.

## Resources

* [Introducing Variable Stars](https://www.rasc.ca/variable-stars)
* [International Variable Star Index](https://www.aavso.org/vsx/index.php?view=detail.top&oid=17041)
* [Nightwatch: A Practical Guide to Viewing the Universe](https://nightwatchbook.com/)
* [Stellarium](https://stellarium.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
[Astropy.svg]: https://www.astropy.org/images/astropy_word.svg
[Astropy-url]: https://www.astropy.org/
[Numpy.svg]: https://numpy.org/images/logo.svg
[Numpy-url]: https://numpy.org/
[Matplotlib.svg]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Matplotlib-url]: https://matplotlib.org/
