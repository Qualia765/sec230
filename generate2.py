import os

replacements = {
    "Section 230" : '<img src="img/section230_mini.png" alt="Section 230" style="height:14px;transform:translate(0,2px)">'
}

def generate_html_files():
    # Initialize variables
    PAGE = 0
    SECTION = ""
    TEXT = []
    
    # Ensure hosted directory exists
    if not os.path.exists('hosted'):
        os.makedirs('hosted')
    
    # Read template.html
    try:
        with open('template.html', 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print("Error: template.html not found")
        return
    
    # Read and process info.txt
    try:
        with open('info.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Error: info.txt not found")
        return
    
    for line in lines:
        line = line.rstrip('\n\r')  # Remove line breaks
        
        if line.startswith('!'):
            # Create HTML file
            create_html_file(PAGE, SECTION, TEXT, template_content, line[1:].strip())
            PAGE += 1
            TEXT = []  # Reset TEXT list
            
        elif line.startswith('~'):
            # Update SECTION
            SECTION = line[1:].strip()
            
        else:
            for replacement in replacements:
                line = line.replace(replacement, replacements[replacement])
            # Regular text line - append to TEXT
            if line.strip():  # Only add non-empty lines
                TEXT.append(line)
    
    create_html_file(PAGE, SECTION, ["More coming soon!"], template_content, "TODO.gif", False)

def create_html_file(page_num, section, text_list, template, image_src, next_link=True):
    # Determine filename
    if page_num == 0:
        filename = 'hosted/index.html'
    else:
        filename = f'hosted/{page_num}.html'
    
    # Build the replacement content
    replacement_content = f'<h1>{section}</h1>\n'
    replacement_content += '<div class="content">\n'
    replacement_content += f'      <img src="img/{image_src}">\n'
    
    # Add paragraph for each text item
    for text in text_list:
        replacement_content += f'      <p>{text}</p>\n'
    
    replacement_content += '</div>\n'
    if next_link:
        replacement_content += '<div class="next">\n'
        replacement_content += f'      > <a href="{page_num + 1}.html">==></a>\n'
        replacement_content += '</div>\n'
    
    # Add "Go Back" link logic
    if page_num == 0:
        # No "Go Back" link for page 0
        pass
    elif page_num == 1:
        replacement_content += '<a href="index.html">Go Back</a>\n'
    else:
        replacement_content += f'<a href="{page_num - 1}.html">Go Back</a>\n'
    
    # Replace $$$$$ in template with our content
    final_content = template.replace('$$$$$', replacement_content)
    
    # Write the file
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Created: {filename}")
    except Exception as e:
        print(f"Error creating {filename}: {e}")

if __name__ == "__main__":
    generate_html_files()
    print("HTML generation complete!")
