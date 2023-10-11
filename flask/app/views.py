from app import app
from flask import Flask, request, send_file, render_template
import random
import string
import os
import subprocess as sp
import shutil as sh

@app.route("/index.html", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():

    # Use os.getenv("key") to get environment variables
    app_name = os.getenv("APP_NAME")

    if app_name:
        #return open("./app/html/index.html", "r").read()
        return render_template('index.html')

    return "Hello from Flask"

@app.route('/contacts.html')
def contacts():
    # Contacts page
    return render_template("contacts.html")

@app.route('/help.html')
def help():
    # Help page
    return render_template("help.html")

@app.route('/start.html', methods=['GET', 'POST'])
def start():
    # Start page

    def fill_startbase(data_dic):

        # Open the start.sh file in write mode
        with open("./start.sh", "w") as start:
            
            # Write the shebang line
            start.write("#!/bin/bash" + '\n\n')

            if data_dic['wlm'] == 'slurm':

                start.write("#SBATCH --job-name=PA_proc_start" + '\n')
                start.write("#SBATCH --output=general.out" + '\n')
                start.write("#SBATCH --error=general.err" + '\n')
                start.write("#SBATCH --nodes=1" + '\n')
                start.write("#SBATCH --ntasks=1" + '\n')
                start.write("#SBATCH --cpus-per-task=1" + '\n')
                start.write("#SBATCH --mem=5GB" + '\n')
                start.write("#SBATCH --time=01:00:00" + '\n')
                start.write("#SBATCH --partition=" + data_dic['serial_part'] + '\n\n')
            
            start.write(open("../bases/start_base.txt").read().format(data_dic['inputpath'],
                                                                      data_dic['threads'],
                                                                      data_dic['python_executable'],
                                                                      data_dic['reference']))
            start.close()
        
        if data_dic['wlm'] == 'htcondor':

            with open("start.sub") as sub:
                header =  "universe=" + data_dic['HTC_universe_name'] + '\n' \
                        + "output=start.out" + '\n' \
                        + "error=start.err" + '\n' \
                        + "log=start.log" + '\n' \
                        + "executable=/bin/bash" + '\n' \
                        + "arguments=start.sh" + '\n' \
                        + "request_cpus=1" +'\n' \
                        + "request_memory=1GB" + '\n' \
                        + "queue" + "\n"
                sub.write(header)
                sub.close()

    def fill_readbase(data_dic):

        wlm_header = ""

        if data_dic['wlm'] == 'slurm':

            wlm_header =  "#SBATCH --account=" + data_dic['account_name'] + '\n' \
                        + "#SBATCH --partition=" + data_dic['parallel_part'] + '\n' \
                        + "#SBATCH --nodes=1" + '\n' \
                        + "#SBATCH --ntasks-per-node=1" + '\n' \
                        + "#SBATCH --time=" + data_dic['time'] + ":00:00" + '\n' \
                        + "#SBATCH --mem=" + data_dic['memory_per_process'] + 'GB' + '\n' \
                        + "#SBATCH --output=general.out" + '\n' \
                        + "#SBATCH --error=general.err" + '\n'
            
        elif data_dic['wlm'] == 'htcondor':

            wlm_header =  "universe=" + data_dic['HTC_universe_name'] + '\n' \
                        + "output=general.out" + '\n' \
                        + "error=general.err" + '\n' \
                        + "log=general.log" + '\n' \
                        + "executable=/bin/bash" + '\n' \
                        + "arguments=script.sh" + '\n' \
                        + "request_cpus=" + data_dic['threads'] + '\n' \
                        + "request_memory=" + data_dic['memory_per_process'] + "GB" + '\n' \
                        + "queue" + "\n"

        elif data_dic['wlm'] == 'None':
            pass
        
        with open("./read.py", 'w') as read:

            read.write(open("../bases/read_base.txt").read().format(data_dic["inputpath"],
                                                                    data_dic["reference"],
                                                                    data_dic["python_executable"],
                                                                    data_dic["bed_file"],
                                                                    data_dic["splicing_file"],
                                                                    data_dic["omopolymeric_file_r"],
                                                                    data_dic["additional_options"],
                                                                    data_dic["threads"],
                                                                    data_dic["wlm"],
                                                                    wlm_header.replace("\n", "\\n"),
                                                                   ))
            read.close()
    
    def fill_controlscriptbase(data_dic):

        # Open the control_script.sh file in write mode
        with open("./control_script.sh", "w") as control:
            # Write the shebang line
            control.write("#!/bin/bash\n\n")

            if data_dic['wlm'] == 'slurm':
                
                control.write("#SBATCH --job-name=PA_proc-control" + '\n')
                control.write("#SBATCH --output=control.out" + '\n')
                control.write("#SBATCH --error=control.err" + '\n')
                control.write("#SBATCH --nodes=1" + '\n')
                control.write("#SBATCH --ntasks=1" + '\n')
                control.write("#SBATCH --cpus-per-task=1" + '\n')
                control.write("#SBATCH --mem=5GB" + '\n')
                control.write("#SBATCH --time=01:00:00" + '\n')
                control.write("#SBATCH --partition=" + data_dic['serial_part'] + '\n\n')

                # Open the controlscript_base.txt file in read mode
                with open("../bases/controlscript_base.txt", "r") as f:
                    # Read the contents of controlscript_base.txt and format it with "sbatch"
                    base = f.read().format("sbatch", "control_script.sh")
                    # Write the formatted contents to control_script.sh
                    control.write(base)
                    f.close()
            
            elif data_dic['wlm'] == 'htcondor':
                # Open the controlscript_base.txt file in read mode
                with open("../bases/controlscript_base.txt", "r") as f:
                    # Read the contents of controlscript_base.txt and format it with "bash"
                    base = f.read().format("condor_submit", "control_script.sub")
                    # Write the formatted contents to control_script.sh
                    control.write(base)
                    f.close()

            else:
                # Open the controlscript_base.txt file in read mode
                with open("../bases/controlscript_base.txt", "r") as f:
                    # Read the contents of controlscript_base.txt and format it with "bash"
                    base = f.read().format("bash", "control_script.sh")
                    # Write the formatted contents to control_script.sh
                    control.write(base)
                    f.close()

            control.close()


    if request.method == 'POST':
        
        tmp_dir = 'tmp_' + ''.join(random.choices(string.ascii_lowercase, k=10))

        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        data_dic = dict()
        
        data_dic['tmp_system_path'] = tmp_dir
        
        
        data_dic['wlm'] = request.form.get('workload_manager').lower()
        data_dic['python_executable'] = "None"
        
        if data_dic['wlm'] == 'slurm':
            data_dic['account_name'] = request.form.get('Slurm_account_name')
            data_dic['serial_part'] = request.form.get('Slurm_serial_part')
            data_dic['parallel_part'] = request.form.get('Slurm_parallel_part')
            data_dic['threads'] = request.form.get('Slurm_Nthreads')
            data_dic['time'] = request.form.get('Slurm_time')
            data_dic['memory_per_process'] = request.form.get('Slurm_Mprocess')

        elif data_dic['wlm'] == 'htcondor':
            data_dic['HTC_universe_name'] = request.form.get('HTC_universe_name')
            data_dic['HTC_scheduler_name'] = request.form.get('HTC_scheduler_name')
            data_dic['HTC_accounting_group'] = request.form.get('HTC_accounting_group')
            data_dic['python_executable'] = request.form.get('HTC_python_executable')
            data_dic['threads'] = request.form.get('HTC_Nthreads')
            data_dic['time'] = request.form.get('HTC_time')
            data_dic['memory_per_process'] = request.form.get('HTC_Mprocess')
        else:
            data_dic['wlm'] = 'None'
            data_dic['threads'] = request.form.get('threads')
        
        data_dic['inputpath']           = request.form.get('ID_path')
        data_dic['python_executable']   = request.form.get('EX_path')
        data_dic['reference']           = request.form.get('REF_path')
        data_dic['bed_file']            = request.form.get('BED_path')
        data_dic['splicing_file']       = request.form.get('SP_path')
        data_dic['omopolymeric_file_r'] = request.form.get('OMO_path')
        data_dic['additional_options']  = request.form.get('add_options')
        
        
        fill_startbase(data_dic)
        fill_readbase(data_dic)
        fill_controlscriptbase(data_dic)

        sp.run("chmod +x start.sh && chmod +x read.py && chmod +x control_script.sh", shell=True)
        sp.run("cp ../time_calculator.py .", shell=True)
        sp.run("tar -cf hpc-reditools.tar read.py start.sh control_script.sh time_calculator.py", shell=True)

        tar = open("./hpc-reditools.tar", "r")
        tar.seek(0)

        os.chdir("../")
        sh.rmtree(tmp_dir)

        return send_file(tar, as_attachment=True, attachment_filename='hpc-reditools.tar', mimetype='text/plain')
    
    return render_template("start.html")

@app.route('/architecture.html')
def architecture():
    # Help page
    return render_template("architecture.html")


@app.route('/download.html')
def download():
    # Help page
    return render_template("download.html")
