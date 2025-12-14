import json
import os
import sys
from pathlib import Path

def sanitize_name(name):
    """Remove invalid characters for folder/file names"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip()

def save_request_txt(item, folder_path, name):
    """Save request details to a TXT file"""
    if 'request' not in item:
        return
        
    request = item['request']
    filename = f"{name}.txt"
    filepath = os.path.join(folder_path, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"API Endpoint: {name}\n")
            f.write("=" * 50 + "\n")
            f.write(f"Method: {request.get('method', 'N/A')}\n")
            f.write(f"URL: {request.get('url', {}).get('raw', 'N/A')}\n\n")
            
            description = request.get('description', '').strip()
            if description:
                f.write("Description:\n")
                f.write(description + "\n\n")
                
            # Headers
            headers = request.get('header', [])
            if headers:
                f.write("Headers:\n")
                for header in headers:
                    key = header.get('key', '')
                    value = header.get('value', '')
                    f.write(f"  {key}: {value}\n")
                f.write("\n")
                
            # Body (if present)
            body = request.get('body')
            if body:
                f.write("Body:\n")
                if body.get('mode') == 'raw':
                    f.write(body.get('raw', '') + "\n")
                f.write("\n")
                
        print(f"Saved TXT: {name}")
    except Exception as e:
        print(f"Error saving TXT {name}: {str(e)}")

def save_request_json(item, folder_path, name):
    """Save request details to a JSON file"""
    filename = f"{name}.json"
    filepath = os.path.join(folder_path, filename)
    
    try:
        # Pretty print the entire item
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(item, f, indent=2, ensure_ascii=False)
        print(f"Saved JSON: {name}")
    except Exception as e:
        print(f"Error saving JSON {name}: {str(e)}")

def save_request_md(item, folder_path, name):
    """Save request details to a Markdown file"""
    if 'request' not in item:
        return
        
    request = item['request']
    filename = f"{name}.md"
    filepath = os.path.join(folder_path, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n")
            f.write(f"**Method:** `{request.get('method', 'N/A')}`  \n")
            f.write(f"**URL:** `{request.get('url', {}).get('raw', 'N/A')}`\n\n")
            
            description = request.get('description', '').strip()
            if description:
                f.write(f"## Description\n{description}\n\n")
                
            # Headers
            headers = request.get('header', [])
            if headers:
                f.write("## Headers\n")
                f.write("| Key | Value |\n|-----|-------|\n")
                for header in headers:
                    key = header.get('key', '')
                    value = header.get('value', '')
                    f.write(f"| {key} | {value} |\n")
                f.write("\n")
                
            # Body (if present)
            body = request.get('body')
            if body:
                f.write("## Body\n")
                if body.get('mode') == 'raw':
                    raw_body = body.get('raw', '')
                    f.write("```json\n")
                    f.write(raw_body + "\n")
                    f.write("```\n")
                f.write("\n")
                
        print(f"Saved MD: {name}")
    except Exception as e:
        print(f"Error saving MD {name}: {str(e)}")

def process_item(item, current_path, format_type):
    """Process a collection item (folder or request)"""
    name = sanitize_name(item.get('name', 'unnamed'))
    
    if 'item' in item:
        # This is a folder
        folder_path = os.path.join(current_path, name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {name}")
            
        # Process children
        for child in item['item']:
            process_item(child, folder_path, format_type)
    else:
        # This is a request
        # Save in the specified format only
        if format_type == 'txt':
            save_request_txt(item, current_path, name)
        elif format_type == 'json':
            save_request_json(item, current_path, name)
        elif format_type == 'md':
            save_request_md(item, current_path, name)

def show_help():
    print("Postman Collection Converter (Single Format)")
    print("Usage: python single_format_converter.py [collection_file] [output_dir] [format]")
    print("")
    print("Arguments:")
    print("  collection_file  Path to the Postman collection JSON file (default: d:/printify_postman_collection.json)")
    print("  output_dir       Output directory path (default: ./output)")
    print("  format           Output format: txt, json, or md (default: txt)")
    print("")
    print("Examples:")
    print("  python single_format_converter.py")
    print("  python single_format_converter.py d:/my_collection.json")
    print("  python single_format_converter.py d:/my_collection.json ./api_docs md")
    print("  python single_format_converter.py d:/my_collection.json ./api_docs json")

def convert_collection(collection_file, output_dir, format_type):
    """Main conversion function"""
    print(f"Converting '{collection_file}' to '{output_dir}'")
    print(f"Format: {format_type} (single format only)")
    print("-" * 50)
    
    # Load collection
    try:
        with open(collection_file, 'r', encoding='utf-8') as f:
            collection = json.load(f)
    except FileNotFoundError:
        print(f"Error: Collection file '{collection_file}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in collection file: {str(e)}")
        return False
        
    collection_name = collection.get('info', {}).get('name', 'PostmanCollection')
    print(f"Loaded collection: {collection_name}")
    
    # Create main output directory
    main_output_dir = os.path.join(output_dir, sanitize_name(collection_name))
    Path(main_output_dir).mkdir(parents=True, exist_ok=True)
    print(f"Created main directory: {os.path.basename(main_output_dir)}")
        
    # Process items
    if 'item' in collection:
        for item in collection['item']:
            process_item(item, main_output_dir, format_type)
            
    print("-" * 50)
    print("Conversion completed successfully!")
    return True

if __name__ == "__main__":
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        sys.exit(0)
    
    # Default values
    collection_file = "d:/printify_postman_collection.json"
    output_dir = "./output"
    format_type = "txt"  # Default to TXT format
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        collection_file = sys.argv[1]
        
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
        
    if len(sys.argv) > 3:
        # Parse format argument
        format_arg = sys.argv[3].lower()
        if format_arg in ['txt', 'json', 'md']:
            format_type = format_arg
        else:
            print(f"Warning: Unknown format '{format_arg}', using 'txt' instead.")
            format_type = "txt"
    
    # Convert the collection
    success = convert_collection(collection_file, output_dir, format_type)
    sys.exit(0 if success else 1)