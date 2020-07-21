# resumator

A simple python-automated resume using jinja2 templating.

## Usage

Note: This module uses `latexmk` instead of `pdflatex` to output pdf files. Many linux distros already have this installed, but if not, you can run `sudo apt install latexmk` or `pacman -S latexmk`.
You may also have to install your prefered latex distribution, such as `pdflatex`.

To run the resumator, simply edit the Markdown file to your liking and run `./resumator`.
