import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def parse(content):
    text = parse_headers(content)
    text = parse_bold(text)
    text = format_list(text)
    text = add_br_to_newlines(text)
    text = remove_hyphens_except_in_style(text)
    text = remove_asterisks(text)
    text = replace_double_quotes_with_single(text)
    return text


def parse_headers(text):
    for i in range(6, 0, -1):
        text = re.sub(r'{} (.+)'.format('#' * i), r'<h{0}>\1</h{0}>'.format(i), text)
    return text


def parse_bold(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def format_list(text):
    text = text.replace('\t', '    ')
    
    def replace_line(match):
        line = match.group(0)
        
        leading_spaces = len(line) - len(line.lstrip())
        
        indent_level = leading_spaces // 4
        
        line_content = line.lstrip('- ').strip()
        
        return f'<span style="display: block; margin-left: {indent_level * 30}px;">{line_content}</span>'

    formatted_text = re.sub(r'^\s*- .+', replace_line, text, flags=re.MULTILINE)
    
    return formatted_text


def add_br_to_newlines(text):
    def replace_newline(match):
        newlines_count = len(match.group(0))
        if newlines_count > 1:
            return '<br>' * 2
        else:
            return '<br>'
    
    text_with_br = re.sub(r'(\n{2,})', replace_newline, text)
    
    text_with_br = re.sub(r'(<h[1-6]>.*?</h[1-6]>)\s*<br>\s*<br>', r'\1<br>', text_with_br)

    text_with_br = re.sub(r'(<br>\s*){3,}', '<br><br>', text_with_br)
    
    return text_with_br


def remove_asterisks(text):
    return text.replace('*', '')


def replace_double_quotes_with_single(text):
    return text.replace('"', "'")


def remove_hyphens_except_in_style(text):
    def preserve_style(match):
        return match.group(0)

    preserved_style_text = re.sub(r'style="[^"]*"', preserve_style, text)
    
    cleaned_text = re.sub(r'-(?![^<]*>)', '', preserved_style_text)
    
    return cleaned_text


root = Tk()
root.withdraw()  
content = ""

file_path = askopenfilename(title="Select a file")


if file_path:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    

parsed_content = parse(content)

with open('content.html', 'w') as html_file:
    html_file.write(parsed_content)