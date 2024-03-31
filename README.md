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
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Note: This is not a reproducible experiment, as the data collected and operation were done using the Trottier Observatory at Simon Fraser University which is available only by special permission.

This project uses sky calibration and aperture photometry methods to measure the periodic magnitude fluctuation (known as a light curve) of a cepheid variable star, RR Leo, in the class of RR Lyrae stars. With the star's light curve measured out, one can then calculate for parameters of interest, such as brightness fluctuation period, peak brightness, and distance to name a few. An RR Lyrae star was chosen due to its relatively rapid periodicity, allowing an overnight observation to wholly describe the fluctuations.

Because the observations were done on the ground, the CCD image sensor picks up systematic sources of noise that must be accounted for. These sources are dark currents, offset bias, sky brightness, pixel-to-pixel variations in sensitivity, quantum efficiency, atmospheric absorption and dust. The purpose of the code in Observation.py is to correct these.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[<img src="https://www.astropy.org/images/astropy_word.svg" alt="Astropy.svg" width="300" height="100">][Astropy-url]
[<img src="https://numpy.org/images/logo.svg" alt="Numpy.svg" width="300" height="100">][Numpy-url]
[<img src="https://matplotlib.org/_static/logo_light.svg" alt="Numpy.svg" width="300" height="100">][Matplotlib-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Behzad Safarian Kashani - [LinkedIn](https://www.linkedin.com/in/bsk00/) - bsafariak@gmail.com

Project Link: [https://github.com/bsafaria/Photometry-RR-Lyrae](https://github.com/bsafaria/Photometry-RR-Lyrae)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

I would like to thank [Dr. Joanna Woo](https://www.sfu.ca/physics/people/faculty/jwa304.html) from Simon Fraser University, the Director of the Trottier Observatory in April 2021, for approving the overnight observation and operation.

Resources of Interest:

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
