#!/usr/bin/env python3
import os

def generate_static_site():
    # Directory paths
    template_file = "template.html"
    insert_dir = "insert"
    output_dir = "hosted"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if template file exists
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found!")
        return
    
    # Check if insert directory exists
    if not os.path.exists(insert_dir):
        print(f"Error: Insert directory '{insert_dir}' not found!")
        return
    
    # Read template content
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        return
    
    # Check if template has the placeholder
    if "$$$$$" not in template_content:
        print("Warning: Template file doesn't contain the placeholder '$$$$$'")
    
    # Process each file in the insert directory
    files_processed = 0
    
    for filename in os.listdir(insert_dir):
        if filename.endswith('.html'):
            insert_file_path = os.path.join(insert_dir, filename)
            
            try:
                # Read insert file content
                with open(insert_file_path, 'r', encoding='utf-8') as f:
                    insert_content = f.read()
                
                # Replace placeholder with insert content
                final_content = template_content.replace("$$$$$", insert_content)
                
                # Write to output file
                output_file_path = os.path.join(output_dir, filename)
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                
                print(f"Generated: {output_file_path}")
                files_processed += 1
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    print(f"\nCompleted! Processed {files_processed} files.")

if __name__ == "__main__":
    generate_static_site()
