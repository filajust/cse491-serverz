import jinja2
import sys

def render(filename, var_dict={}):
    # sets up jinja2 to load templates
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    # filename to render
    # print >>sys.stderr, '** Rendering"', filename

    # print >>sys.stderr, '** Using vars dictionary:', var_dict

    template = env.get_template(filename)
    return template.render(var_dict)
