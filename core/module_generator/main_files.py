# core/module_generator/main_files.py
from pathlib import Path
from utils.file_utils import write_file, read_file

def generate_main_and_build_files(base_path: Path, module_name: str):
    m = module_name
    # Legge il template main da "templates/py_templates/main_template.py"
    main_template_path = Path("templates/py_templates/main_template.py")
    main_content = read_file(main_template_path).replace("{module_name}", m)
    write_file(base_path / 'main.py', main_content)
    
    webpack_config = """const path = require('path');

module.exports = {
  mode: 'production',
  entry: './ui/static/js/script.js',
  output: {
    filename: 'script.min.js',
    path: path.resolve(__dirname, 'ui/static/js')
  }
};
"""
    write_file(base_path / 'webpack.config.js', webpack_config)
    package_json = f"""{{
  "name": "{m}",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {{
    "webpack": "^5.0.0",
    "webpack-cli": "^4.0.0"
  }}
}}
"""
    write_file(base_path / 'package.json', package_json)
