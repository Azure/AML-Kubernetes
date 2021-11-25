# Define helper functions

import sys
import os
import re
import json
import platform
import shlex
import shutil
import datetime
import time
import random
import string

from subprocess import Popen, PIPE
from IPython.display import Markdown

# # Define log_result function to log test results to the /results/results.json file
# def log_result(test_name, test_result, execution_time):
#     results_file = './results/results.json'
#     with open(results_file,'r') as json_file:
#         data = json.load(json_file)
#         results = data['results']
#         results.append({"test_name":test_name, "test_result":test_result, "execution_time":execution_time})
#     with open(results_file,'w') as json_file_write:
#         json.dump(data,json_file_write)

# Define log_result function to log test results to the /results.json file
def log_result(test_name, test_result, execution_time):
    root_array = []
    test_result = {"test_name":test_name, "test_result":test_result, "execution_time":execution_time}
    file_name= './results/results.json'

    if not os.path.isfile(file_name) or os.path.getsize(file_name) == 0:
        root_array.append(test_result)
        with open(file_name, mode='w') as f:
            f.write(json.dumps(root_array, indent=2))
    else:
        with open(file_name) as test_results_file:
            test_results = json.load(test_results_file)
            test_results.append(test_result)
        with open(file_name, mode='w') as test_results_file:
            test_results_file.write(json.dumps(test_results, indent=2))


# Define `run` function for transient fault handling, suggestions on error, and scrolling updates on Windows
def run(cmd, return_output=False, no_output=False, retry_count=0):
    """Run shell command, stream stdout, print stderr and optionally return output

    NOTES:

    1.  Commands that need this kind of ' quoting on Windows e.g.:

            kubectl get nodes -o jsonpath={.items[?(@.metadata.annotations.pv-candidate=='data-pool')].metadata.name}

        Need to actually pass in as '"':

            kubectl get nodes -o jsonpath={.items[?(@.metadata.annotations.pv-candidate=='"'data-pool'"')].metadata.name}

        The ' quote approach, although correct when pasting into Windows cmd, will hang at the line:
        
            `iter(p.stdout.readline, b'')`

        The shlex.split call does the right thing for each platform, just use the '"' pattern for a '
    """
    MAX_RETRIES = 5
    output = ""
    retry = False

    # When running `azdata sql query` on Windows, replace any \n in """ strings, with " ", otherwise we see:
    #
    #    ('HY090', '[HY090] [Microsoft][ODBC Driver Manager] Invalid string or buffer length (0) (SQLExecDirectW)')
    #
    if platform.system() == "Windows" and cmd.startswith("azdata sql query"):
        cmd = cmd.replace("\n", " ")

    # shlex.split is required on bash and for Windows paths with spaces
    # https://github.com/jrnl-org/jrnl/issues/348
    cmd_actual = shlex.split(cmd, posix="win" not in sys.platform)

    # Store this (i.e. kubectl, python etc.) to support binary context aware retries
    #
    user_provided_exe_name = cmd_actual[0].lower()

    # When running python, use the python in the ADS sandbox ({sys.executable})
    #
    if cmd.startswith("python "):
        cmd_actual[0] = cmd_actual[0].replace("python", sys.executable)

        # On Mac, when ADS is not launched from terminal, LC_ALL may not be set, which causes pip installs to fail
        # with:
        #
        #    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc5 in position 4969: ordinal not in range(128)
        #
        # Setting it to a default value of "en_US.UTF-8" enables pip install to complete
        #
        if platform.system() == "Darwin" and "LC_ALL" not in os.environ:
            os.environ["LC_ALL"] = "en_US.UTF-8"

    # When running `kubectl`, if AZDATA_OPENSHIFT is set, use `oc`
    #
    if cmd.startswith("kubectl ") and "AZDATA_OPENSHIFT" in os.environ:
        cmd_actual[0] = cmd_actual[0].replace("kubectl", "oc")

    # To aid supportabilty, determine which binary file will actually be executed on the machine
    #
    which_binary = None

    # Special case for CURL on Windows.  The version of CURL in Windows System32 does not work to
    # get JWT tokens, it returns "(56) Failure when receiving data from the peer".  If another instance
    # of CURL exists on the machine use that one.  (Unfortunately the curl.exe in System32 is almost
    # always the first curl.exe in the path, and it can't be uninstalled from System32, so here we
    # look for the 2nd installation of CURL in the path)
    if platform.system() == "Windows" and cmd.startswith("curl "):
        path = os.getenv('PATH')
        for p in path.split(os.path.pathsep):
            p = os.path.join(p, "curl.exe")
            if os.path.exists(p) and os.access(p, os.X_OK):
                if p.lower().find("system32") == -1:
                    cmd_actual[0] = p
                    which_binary = p
                    break

    # Find the path based location (shutil.which) of the executable that will be run (and display it to aid supportability), this
    # seems to be required for .msi installs of azdata.cmd/az.cmd.  (otherwise Popen returns FileNotFound) 
    #
    # NOTE: Bash needs cmd to be the list of the space separated values hence shlex.split.
    #
    if which_binary == None:
        which_binary = shutil.which(cmd_actual[0])

    if which_binary == None:
        raise FileNotFoundError(f"Executable '{cmd_actual[0]}' not found in path (where/which)")
    else:   
        cmd_actual[0] = which_binary

    start_time = datetime.datetime.now().replace(microsecond=0)

    print(f"START: {cmd} @ {start_time} ({datetime.datetime.utcnow().replace(microsecond=0)} UTC)")
    print(f"       using: {which_binary} ({platform.system()} {platform.release()} on {platform.machine()})")
    print(f"       cwd: {os.getcwd()}")

    # Command-line tools such as CURL and AZDATA HDFS commands output
    # scrolling progress bars, which causes Jupyter to hang forever, to
    # workaround this, use no_output=True
    #

    # Work around a infinite hang when a notebook generates a non-zero return code, break out, and do not wait
    #
    wait = True 

    try:
        p = Popen(cmd_actual, stdout=PIPE, stderr=PIPE)
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                line = line.decode()
                if return_output:
                    output = output + line
                else:
                    if cmd.startswith("azdata notebook run"): # Hyperlink the .ipynb file
                        regex = re.compile('  "(.*)"\: "(.*)"') 
                        match = regex.match(line)
                        if match:
                            if match.group(1).find("HTML") != -1:
                                display(Markdown(f' - "{match.group(1)}": "{match.group(2)}"'))
                            else:
                                display(Markdown(f' - "{match.group(1)}": "[{match.group(2)}]({match.group(2)})"'))

                                wait = False
                                break # otherwise infinite hang, have not worked out why yet.
                    else:
                        pass
                
                if not no_output: 
                    print(line, end='')

        if wait:
            p.wait()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Executable '{cmd_actual[0]}' not found in path (where/which)") from e

    exit_code_workaround = 0 # WORKAROUND: azdata hangs on exception from notebook on p.wait()

    if not no_output:
        for line in iter(p.stderr.readline, b''):
            try:
                line_decoded = line.decode()
            except UnicodeDecodeError:
                # NOTE: Sometimes we get characters back that cannot be decoded(), e.g.
                #
                #   \xa0
                #
                # For example see this in the response from `az group create`:
                #
                # ERROR: Get Token request returned http error: 400 and server 
                # response: {"error":"invalid_grant",# "error_description":"AADSTS700082: 
                # The refresh token has expired due to inactivity.\xa0The token was 
                # issued on 2018-10-25T23:35:11.9832872Z
                #
                # which generates the exception:
                #
                # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xa0 in position 179: invalid start byte
                #
                print("WARNING: Unable to decode stderr line, printing raw bytes:")
                print(line)
                line_decoded = ""
                pass
            else:

                # azdata emits a single empty line to stderr when doing an hdfs cp, don't
                # print this empty "ERR:" as it confuses.
                #
                if line_decoded == "":
                    continue
                
                print(f"STDERR: {line_decoded}", end='')

                if line_decoded.startswith("An exception has occurred") or line_decoded.startswith("ERROR: An error occurred while executing the following cell"):
                    exit_code_workaround = 1


    elapsed = datetime.datetime.now().replace(microsecond=0) - start_time

    # WORKAROUND: We avoid infinite hang above in the `azdata notebook run` failure case, by inferring success (from stdout output), so
    # don't wait here, if success known above
    #
    if wait: 
        if p.returncode != 0:
            raise SystemExit(f'Shell command:\n\n\t{cmd} ({elapsed}s elapsed)\n\nreturned non-zero exit code: {str(p.returncode)}.\n')
    else:
        if exit_code_workaround !=0 :
            raise SystemExit(f'Shell command:\n\n\t{cmd} ({elapsed}s elapsed)\n\nreturned non-zero exit code: {str(exit_code_workaround)}.\n')
    
    if return_output:
        return output

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

def randFolderName():
    return randStr(chars=string.ascii_lowercase, N=5)+"_"+randStr(chars=string.ascii_letters+string.digits, N=8)

def currentTimeStr(format="%Y%m%d%H%M%S"):
    current = datetime.datetime.now()
    currentStr = current.strftime(format)
    return currentStr