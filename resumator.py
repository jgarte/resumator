import sys
import os
import getopt
import json
from datetime import datetime
import jinja2
from jinja2 import Template
import mistune
from bs4 import BeautifulSoup

def parse_markdown(in_file):
    '''Read resume data from markdown file'''
    with open(in_file, 'r') as file:
        file_text = file.read();
        file_html = mistune.html(file_text)
    # print(file_html)
    soup = BeautifulSoup(file_html, 'html.parser')
    print(soup)
    md_data = {
        'name': soup.h1.text.strip(),
        'sections': []
    }
    # loop through info section
    for line in soup.find_all('p'):
        if 'PHONE' in line.text:
            md_data['phone'] = line.text[6:].strip()
        elif 'EMAIL' in line.text:
            md_data['email'] = line.text[6:].strip()
        elif 'WEBSITE' in line.text:
            md_data['website'] = line.text[8:].strip()
        elif 'LINKEDIN' in line.text:
            md_data['linkedin'] = line.text[9:].strip()
    # loop through each h2 header
    for section in soup.find_all('h2'):
        section_data = {
            'title': section.text.strip(),
        }
        # loop till the next section
        print(section)
        next_sib = section.h2.next_sibling()
        while next_sib.name != 'h2':
            # skip subtitles
            if next_sib.name != 'h4':
                entry_data = {
                    'title': next_sib.text
                }
                # include subtitle if present
                subtitle = next_sib.next_sibling()
                if subtitle.name == 'h4':
                    entry_data['subtitle'] = subtitle.text
                # read info list
                info_list = section.find_next('ul')
                # entry_info = []
                for el in entry_info.children:
                    if 'LOCATION' in el.text:
                        entry_data['location'] = line.text[9:].strip()
                    elif 'DATES' in el.text:
                        entry_data['dates'] = line.text[6:].strip()
                    else:
                        entry_data['info'].append(el.text)
                

            next_sib = next_sib.next_sibling()
        md_data['sections'].append(section_data)

    print(md_data)

def parse_json(in_file):
    '''Read resume data from JSON file'''
    with open(in_file, 'r') as file:
        # data = json.loads(file.read())
        # print(data)
        # return data
        return json.loads(file.read())
        
def output_to_tex(filename, data):
    '''Write resume to new tex file'''
    now = datetime.now().strftime('-%Y-%d-%m_%H:%M:%S')
    full_filename = filename + now + '.tex'
    with open(os.path.abspath(os.path.join('latex',full_filename)), 'w') as output:
        output.write(data)
    return full_filename

def output_to_pdf(filename):
    '''Print resume to new pdf file'''
    os.system('latexmk -pdf latex/' + filename)
    os.system('latexmk -C')
    os.system('mv ' + filename[:-3] + 'pdf pdf')
    os.system('rm Resume-*')

def resumator(in_file, data):
    '''Fill Latex resume template'''
    latex_env = jinja2.Environment(
        block_start_string = '\BLOCK{',
        block_end_string = '}',
        variable_start_string = '\VAR{',
        variable_end_string = '}',
        comment_start_string = '\#{',
        comment_end_string = '}',
        line_statement_prefix = '%%',
        line_comment_prefix = '%#',
        trim_blocks = True,
        autoescape = False,
        loader = jinja2.FileSystemLoader(os.path.abspath('templates/'))
    )
    template = latex_env.get_template('template1.tex')
    renderer = template.render(**data)
    # print(renderer)
    tex_out = output_to_tex('Resume',renderer)
    output_to_pdf(tex_out)

def main():
    # read and process command line args
    in_file = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:],':h',['help'])
    except getopt.GetoptError:
        print('Usage: python3 resumator.py [OPTIONS]')
        print('    Use -h for more options')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('Usage: python3 wiki_scraper.py [OPTIONS]')
            print('    -h,--help: open help menu')
            sys.exit(2)
        else:
            in_file = arg
    data = {
        'name':'Calvin Huang',
        'cell':'(513) 693-5266)',
        'var':1
    }
    # resumator(in_file, data)
    parse_markdown('Sample.md')
    # parse_json('Sample.json')

if __name__ == '__main__':
    main()