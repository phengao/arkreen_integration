import os
import shutil

def check_and_copy_directory(source, destination):
    if os.path.exists(destination):
        overwrite = input(f"Directory {destination} already exists. Do you want to overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled.")
            return False
    shutil.copytree(source, destination, dirs_exist_ok=True)
    return True

def main():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    core_dir = os.path.join(parent_dir, 'core')

    if not os.path.exists(core_dir):
        print("Error: The 'core' directory does not exist in the parent directory.")
        print("Please copy the current folder to the same level as the Home Assistant's 'core' directory.")
        print("错误：父目录中不存在 'core' 目录。")
        print("请将当前文件夹复制到与 Home Assistant 的 'core' 目录同一级目录下。")
        return

    config_dir = os.path.join(core_dir, 'config')
    custom_components_source = os.path.join(current_dir, 'custom_components')
    www_source = os.path.join(current_dir, 'www')

    if os.path.exists(custom_components_source):
        custom_components_dest = os.path.join(config_dir, 'custom_components')
        if not check_and_copy_directory(custom_components_source, custom_components_dest):
            return

    if os.path.exists(www_source):
        www_dest = os.path.join(config_dir, 'www')
        if not check_and_copy_directory(www_source, www_dest):
            return

    configuration_yaml_path = os.path.join(config_dir, 'configuration.yaml')
    arkreen_config = """
arkreen:

panel_custom:
  - name: arkreen-plant-panel
    sidebar_title: "Arkreen Plant"
    sidebar_icon: mdi:solar-power-variant-outline
    url_path: arkreen-plant-panel
    module_url: /local/arkreen-plant-panel.js  
"""

    if os.path.exists(configuration_yaml_path):
        with open(configuration_yaml_path, 'r') as file:
            content = file.read()
        if "arkreen:" not in content:
            with open(configuration_yaml_path, 'a') as file:
                file.write(arkreen_config)
    else:
        with open(configuration_yaml_path, 'w') as file:
            file.write(arkreen_config)

if __name__ == "__main__":
    main()




