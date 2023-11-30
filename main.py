

# configparser user to read initialization file(default config.ini)
import configparser
def integrate():
    try:
        # open file in the read mode
        fin = open("modules/app_init.py", "r")
        # read file content
        app_init = fin.read()
        # close file after read
        fin.close()

        fin = open("modules/web.py", "r")
        web_file = fin.read()
        fin.close()

        fin = open("modules/common.py", "r")
        common_file = fin.read()
        fin.close()

        fin = open("modules/login.py", "r")
        web_login = fin.read()
        fin.close()

        fin = open("modules/app_run.py", "r")
        app_run = fin.read()
        fin.close()

        # Create combine file of content of all the python files
        # Note: app_run should be at last
        combine_file = app_init + web_file + web_login +  common_file + app_run

        # Created new app file to run the app
        fout = open("employee.py", 'w')
        fout.write(combine_file)
        fout.close()

    except Exception as e:
        print(f"Exception in integrating code = {e}")
        raise Exception("Exception in integrating code")
    
# ==============================================================================  

try:
    # Create object of Config Parser class which is available in configparser module
    config_object = configparser.ConfigParser()
    config_object.read("default_config.ini")

    with open('config.py', 'w') as f:
        # Read DEFAULT section from the Default_config.ini
        for key in config_object['DEFAULT']:
            # Write each line in config.py file
            f.write(f"{key.upper()} = {config_object['DEFAULT'][key]}\n")

    integrate()
except Exception as e:
    print(f"Exception Occured = {e}")