import sys
import os
import getopt
import jinja2
from jinja2 import Template

def resumator(in_file):
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
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    template = latex_env.get_template('template1.tex')
    print(template.render(section1='Long Form', section2='Short Form'))

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
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    template = latex_env.get_template('template1.tex')
    print(template.render())

if __name__ == '__main__':
    main()