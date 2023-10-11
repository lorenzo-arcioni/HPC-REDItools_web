document.addEventListener("DOMContentLoaded", function () {
    initPage();
});

function initPage() {
    toggleConfigurationPanel();
    var advanced_options = document.getElementById("advanced_options");
    advanced_options.style.display = "none";

    // Verifica se l'elemento con l'id "sub_B" esiste prima di aggiungere l'event listener
    var sub_B_v = document.getElementById("sub_B");
    if (sub_B_v) {
        sub_B_v.addEventListener("click", validateForm);
    }

    // Esegui una verifica simile per gli altri elementi
    var help_add_options_v = document.getElementById("help_add_options");
    if (help_add_options_v) {
        help_add_options_v.addEventListener("click", help_add_options);
    }

    var help_redi_v = document.getElementById("help_redi");
    if (help_redi_v) {
        help_redi_v.addEventListener("click", help_redi);
    }

    var help_workload_v = document.getElementById("help_workload");
    if (help_workload_v) {
        help_workload_v.addEventListener("click", help_workload);
    }
}

function toggleConfigurationPanel() {
    var slurmConfPanel = document.getElementById("slurmConfPanel");
    var htcondorConfPanel = document.getElementById("htcondorConfPanel");
    var noneConfPanel = document.getElementById("noneConfPanel");
    var python_exec_path = document.getElementsByName("EX_path");

    var slurmRadio = document.getElementById("slurm");
    var htcondorRadio = document.getElementById("htcondor");
    var noneRadio = document.getElementById("none");

    if (slurmRadio && slurmRadio.checked) {
        slurmConfPanel.style.display = "block";
        noneConfPanel.style.display = "none";
        htcondorConfPanel.style.display = "none";
        for (var i = 0; i < python_exec_path.length; i++) {
            python_exec_path[i].style.display = "none";
        }
    } else if (noneRadio && noneRadio.checked) {
        slurmConfPanel.style.display = "none";
        noneConfPanel.style.display = "block";
        htcondorConfPanel.style.display = "none";
        for (var i = 0; i < python_exec_path.length; i++) {
            python_exec_path[i].style.display = "none";
        }
    } else if (htcondorRadio && htcondorRadio.checked) {
        slurmConfPanel.style.display = "none";
        noneConfPanel.style.display = "none";
        htcondorConfPanel.style.display = "block";
        for (var i = 0; i < python_exec_path.length; i++) {
            python_exec_path[i].style.display = "block";
        }
    }
}
function toggleAdvancedoptions() {
    var advanced_options = document.getElementById("advanced_options");
    var check_advanced = document.getElementById("show_advanced_options");

    if (check_advanced && check_advanced.checked) {
        advanced_options.style.display = "block";
    } else {
        advanced_options.style.display = "none";
    }
}

// Check if all fields are filled
function validateForm(){
    var form = document.querySelector("form");
    var inputs = form.querySelectorAll("input, select");
    var isValid = true;

    for (var i = 0; i < inputs.length; i++) {
        var input = inputs[i];
        var forbiddenIds = ["add_options", "OMO_path", "BED_path", "SP_path"];

        if (input.offsetParent !== null && input.value.trim() === "" && !forbiddenIds.includes(input.id)){
            isValid = false;
            input.style.backgroundColor = "#BDBDBD";
        }
        else{
            input.style.backgroundColor = ""
        }
    }

    if (!isValid){
        event.preventDefault();
        window.alert("Please fill all field!");
        exit(0)
    }
}

function help_add_options(){
    window.alert("In note, only options related to computation are accepted. Please see the \"Help\" page for more information.");
}

function help_workload(){
    window.alert("In this section, you can configure the workload manager you wish to use, or you can choose not to use any workload manager.");
}

function help_redi(){
    window.alert("In this section, you can set the configuration of REDItools software. It is necessary to provide the input directory (absolute) path, the reference genome (absolute) path.");
}