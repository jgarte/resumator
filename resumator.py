import sys
import os
import getopt
from datetime import datetime
import jinja2
from jinja2 import Template
import mistune

def parse_markdown(in_file):
    '''Read resume data from markdown file'''
    with open(in_file, 'r') as file:
        file_text = file.read();
        file_html = mistune.html(file_text)
    print(file_html)
        
def output_to_tex(filename, data):
    '''Write resume to new tex file'''
    now = datetime.now().strftime('-%Y-%d-%m_%H:%M:%S')
    full_filename = filename + now + '.tex'
    with open(os.path.abspath(os.path.join('latex',full_filename)), 'w') as output:
        output.write(data)
    return full_filename

def output_to_pdf(filename):
    '''Print resume to new pdf file'''
    os.system('pdflatex latex/' + filename)

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
    resumator(in_file, data)
    parse_markdown('Sample.md')

if __name__ == '__main__':
    main()