

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

        # ========================================================================

        # create Leave management combine file
        fin = open("modules/manage_leave/web/manage_leave.py", "r")
        web_manage_leave = fin.read()
        fin.close()

        fin = open("modules/manage_leave/api/manage_leave.py", "r")
        api_manage_leave = fin.read()
        fin.close()

        fin = open("modules/manage_leave/common/manage_leave.py", "r")
        common_manage_leave = fin.read()
        fin.close()
        
        manage_leave = web_manage_leave + api_manage_leave + common_manage_leave

        # ========================================================================

        # create employee management combine file
        fin = open("modules/manage_employee/web/manage_employee.py", "r")
        web_manage_emplyoee = fin.read()
        fin.close()

        fin = open("modules/manage_employee/api/manage_employee.py", "r")
        api_manage_employee = fin.read()
        fin.close()

        fin = open("modules/manage_employee/common/manage_employee.py", "r")
        common_manage_employee = fin.read()
        fin.close()
        
        manage_employee = web_manage_emplyoee + api_manage_employee + common_manage_employee

        # ==========================================================================

        # create Leave management combine file
        fin = open("modules/manage_resources/web/manage_resources.py", "r")
        web_manage_resources = fin.read()
        fin.close()

        fin = open("modules/manage_resources/api/manage_resources.py", "r")
        api_manage_resources = fin.read()
        fin.close()

        fin = open("modules/manage_resources/common/manage_resources.py", "r")
        common_manage_resources = fin.read()
        fin.close()
        
        manage_resources = web_manage_resources + api_manage_resources + common_manage_resources

        # ===========================================================================

        # create Leave management combine file
        fin = open("modules/manage_attendance/web/manage_attendance.py", "r")
        web_manage_attendance = fin.read()
        fin.close()

        fin = open("modules/manage_attendance/api/manage_attendance.py", "r")
        api_manage_attendance = fin.read()
        fin.close()

        fin = open("modules/manage_attendance/common/manage_attendance.py", "r")
        common_manage_attendance = fin.read()
        fin.close()
        
        manage_attendance = web_manage_attendance + api_manage_attendance + common_manage_attendance

        # ========================================================================

        # Create combine file of content of all the python files
        # Note: app_run should be at last
        combine_file = app_init + web_file + web_login +  common_file + manage_leave + manage_employee + manage_resources + manage_attendance + app_run

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