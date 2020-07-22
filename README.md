# resumator

A simple python-automated resume using jinja2 templating. The idea is to simplify the formatting process and make dynamic changes using the minimalistic Markdown format that are carried over to a finalized LaTeX-generated pdf.
This module defaults to scraping data from a markdown file named "Resume.md" that can be used to input information. It can also be configured to read from a JSON file of the resume information.

## Usage

Note: This module uses `latexmk` instead of `pdflatex` to output pdf files. Many linux distros already have this installed, but if not, you can run `sudo apt install latexmk` or `pacman -S latexmk`.
You may also have to install your prefered latex distribution, such as `pdflatex`.

To run the resumator, simply edit the Markdown file to your liking and run `./resumator`.

To clear all generated resumes (both .tex and .pdf files), run `./clear`

## Markdown Schema

It is recommneded that you use a fully functional Markdown editor such as Typora or Zettlr as an interface to edit your resume.
```
# Name

PHONE: <phone>
EMAIL: <email>
WEBSITE: <website url>
LINKEDIN: <linkedin url>

## Section Name

### Section entry

#### Entry subtitle

- <entry information>
...
- LOCATION: <location>
- DATES: <dates>

```
For a full example, take a look at Sample.md.


## JSON Schema

```
{
  "name": <name>,
  "phone": <phone>,
  "email": <email>,
  "website": <website url>,
  "linkedin": <linkedin url>,
  "sections": [
    {
      "title": <section title>,
      "entries": [
        {
          "title": <entry title>,
          "subtitle": <entry subtitle>,
          "info": [<bullet point 2>, <bullet point 2>],
          "location": <location>,
          "dates": <dates>
        }
      ]
    }
    ...
  ]
}
```