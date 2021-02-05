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
    # print(soup.prettify())
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
    prev_tag = 'h2'
    h2_index = -1
    h3_index = -1
    for section in soup.find_all(['h2','h3','h4','ul']):
        if 'h2' in str(section):
            h2_index += 1
            section_data = {
                'title': section.text.strip(),
                'entries': []
            }
            md_data['sections'].append(section_data)
            h3_index = -1
        elif 'h3' in str(section):
            entry_data = {
                'title': section.text.strip()
            }
            md_data['sections'][h2_index]['entries'].append(entry_data)
            h3_index += 1
        elif 'h4' in str(section):
            md_data['sections'][h2_index]['entries'][h3_index]['subtitle'] = section.text.strip()
        elif 'ul' in str(section):
            md_data['sections'][h2_index]['entries'][h3_index]['info'] = []
            for line in section.find_all('li'):
                if 'LOCATION' in line.text:
                    md_data['sections'][h2_index]['entries'][h3_index]['location'] = line.text[9:].strip()
                elif 'DATES' in line.text:
                    md_data['sections'][h2_index]['entries'][h3_index]['dates'] = line.text[6:].strip()
                else:
                    md_data['sections'][h2_index]['entries'][h3_index]['info'].append(line.text)
    # print(json.dumps(md_data,indent=4))
    return md_data

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
    os.system('latexmk -pdf -silent -quiet latex/' + filename)
    os.system('latexmk -C -silent -quiet')
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
    template = latex_env.get_template(in_file)
    renderer = template.render(**data)
    # print(renderer)
    tex_out = output_to_tex('Resume',renderer)
    output_to_pdf(tex_out)

def main():
    # read and process command line args
    in_file = ""
    template_file = ""
    file_type = 'markdown'
    resume_data = {}
    try:
        opts, args = getopt.getopt(sys.argv[1:],':hi:jt:',['help','input','json','template'])
    except getopt.GetoptError:
        print('Usage: python3 resumator.py [FILE] [OPTIONS]')
        print('    Use -h for more options')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('Usage: python3 resumator.py [FILE] [OPTIONS]')
            print('    -h,--help: open help menu')
            print('    -j,--json: use JSON file type')
            print('    -t,--template: latex template file name')
            sys.exit(2)
        elif opt in ('-i','--input'):
            in_file = arg
        elif opt in ('-j','--json'):
            file_type = 'json'
        elif opt in ('-t','--template'):
            template_file = arg
    
    template_file = template_file if template_file[-4:] == '.tex' else template_file + '.tex'

    if file_type == 'markdown':
        # add file extension if not provided
        in_file = in_file if in_file[-3:] == '.md' else in_file + '.md'
        resume_data = parse_markdown(in_file)
    else:
        # add file extension if not provided
        in_file = in_file if in_file[-5:] == '.json' else in_file + '.json'
        resume_data = parse_json(in_file)
    # try:
    #     print(template_file)
    #     resumator(template_file, resume_data)
    # except:
    #     print("Error: could not template LaTeX file.")
    resumator(template_file, resume_data)

if __name__ == '__main__':
    main()