# -------------------------------
# AUTHOR
# -------------------------------
# Pavol Holes
# 2024
#
# -------------------------------
# DESCRIPTION
# -------------------------------
# This PowerShell script is intended to be used on the Web server where it will deploy new IIS Application pool and new WebApp to be used by application running on Python.
#
# Prerequisite software
#   - install IIS Web server role with below additional features to the default installation:
#       - Web server > Common HTTP Features > HTTP Redirection
#       - Web Server > Performance > Dynamic Content Compression
#       - Web Server > Security > Basic Authentication; Windows Authentication
#       - Web Server > Application Development > .NET Extensibility 4.6; ASP.NET 4.6; CGI; ISAPI Extensions; ISAPI Filters
#   - install httpPlatformHandler to IIS from: [https://www.iis.net/downloads/microsoft/httpplatformhandler]
#   - install Python from: [https://www.python.org/downloads/windows/]
#
# Installation procedure:
#   - copy directory for the Python application to a custom location i.e: [d:\scripts\NGO_Naruc\ngo_naruc_project_be]
#   - open CMD, navigate to the application directory created in previous step i.e. [d:\scripts\NGO_Naruc\ngo_naruc_project_be] and run:
#       pip install -r requirements.txt
#   - open PowerShell x64 as Administrator and execute this PS script to deploy a new IIS Application Pool and IIS Application under the Default Web Site
#   - Update the environment parameters in [.env] file (PowerShell variable [$WebAppName] in this script has to be same as env. variable [API_ROOT] with leading slash i.e. 'ngo_naruc_project_be' == '/ngo_naruc_project_be').
#   - open Swagger UI: [http://localhost/ngo_naruc_project_be/api/v1/ui]
#
# Notes:
#   - Runtime process is:
#     - Opening [http://localhost/ngo_naruc_project_be/] starts the IIS Application Pool [ngo_naruc_project_be] which starts IIS Application [ngo_naruc_project_be].
#     - Application [ngo_naruc_project_be] starts the IIS module [httpPlatformHandler] with dynamic port and it will automatically handle the mapping to the port 80.
#     - IIS module [httpPlatformHandler] starts the Python and handover the dynamic port number to it.
#     - Python starts the Waitress server on the dynamic port only for the localhost machine so the authorization can be handled by IIS and can't be overcome.
#     - Waitress server starts the Flask application from file app.py.
#     - App start API and Swagger UI.
#   - Troubleshooting:
#     - If Python fails to start (because of i.e. database connection error) it will not log anything to the log files and IIS will result in HTTP 502 Error.
#     - For troubleshooting (to see the error) you can manualy start the app by command [python d:\scripts\NGO_Naruc\ngo_naruc_project_be\app.py].
#     - After python code change it's needed to Recycle the IIS Application Pool [ngo_naruc_project_be].
#
# ===============================
# CONFIGURATION VARIABLES
# ===============================
#
# WebApplication name
$WebAppName = "ngo_naruc_project_be"
# allow longer GET urls "system.webServer/security/requestFiltering/maxQueryString" (default 2048)
$maxQueryStringValue = 4096

#--------- DO NOT EDIT BELOW THIS LINE -----------
try {
    $ErrorActionPreference="Stop"
    Set-ExecutionPolicy Bypass -Scope Process

    # Function for logging to file 
    function log {
        Param(
            [Parameter(Mandatory=$True, HelpMessage="log text", ValueFromPipeline)] $lt,
            [Switch] $h, #header
            [Switch] $d  #no date
        )
        $high = ""
        if ($h){
            $strg = "["+(get-date).tostring("yyyy-MM-dd HH:mm:ss")+"]     " + $lt + "     "
            for ($i = 0; $i -lt $strg.length; $i++){$high = $high + "-"}
            $strg = "`r`n"+ $high +"`r`n"+ $strg + "`r`n"+ $high + "`r`n"
        } elseif ($d) {
            $strg = $lt
        } else {
            $strg = "["+(get-date).tostring("HH:mm:ss")+"]     " + $lt
        }
        Write-Host $strg
        Add-Content $global:logpath $strg

        $global:ilog += $strg+"`r`n"
    }

    # Function to remove all custom variables 
    function RemoveAllCustomVariables {
        Param()
        # Invoke a new instance of PowerShell, get the built-in variables, then remove everything else that doesn't belong.
        $ps = [PowerShell]::Create()
        $ps.AddScript('Get-Variable | Select-Object -ExpandProperty Name') | Out-Null
        $builtIn = $ps.Invoke()
        $ps.Dispose()
        $builtIn += "profile","psISE","psUnsupportedConsoleApplications" # keep some ISE-specific stuff
    }
    
    # Function to test if the current process is run as administrator
    function Test-ProcessElevated() {
        Param(        
        )
        $identity  = [System.Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object System.Security.Principal.WindowsPrincipal($identity)
        return $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    
    if (-not (Test-ProcessElevated)) {
        throw 'This PowerShell script must be run from a PowerShell process that is running as administrator.'
    } 

    # Get the script path
    $ScriptPath = Switch ($Host.name){
        "Visual Studio Code Host" { split-path $psEditor.GetEditorContext().CurrentFile.Path }
        "Windows PowerShell ISE Host" {  Split-Path -Path $psISE.CurrentFile.FullPath }
        "ConsoleHost" { $PSScriptRoot }
    }

    # Logging to file
    $global:ilog=""
    $global:logPath = ($ScriptPath + "\" + $PSScriptBaseName + "-debug.log")
    
    #rename .log to .old.log when it reach 3MB. Note: this will overwrite .old.log file so all will be automaintained.
    if (((Get-Item $logPath -ErrorAction SilentlyContinue).length/1Mb) -gt 3) { Move-Item $logPath -Destination "$PSScriptBaseName-debug.old.log" -Force }

    log "$WebAppName install script execution has started" -h

    log "[INFO] Script location: [$ScriptPath]"
    log "[INFO] Script name: [$PSScriptBaseName]"
    $workingDir = $(pwd).Path
    log "[INFO] Current working directory: [$workingDir]"
    if ($workingDir -ne $ScriptPath) {
        log "[INFO] Changing PowerShell work directory from [$workingDir] to [$ScriptPath]."
        try {
            & cd $ScriptPath
        } catch {
            throw
        }
        $workingDir = $(pwd).Path
        if ($workingDir -ne $ScriptPath) {
            throw "Failed to change PowerShell work directory from [$workingDir] to [$ScriptPath]!"
        } else {
            log "[INFO] Current working directory: [$workingDir]"
        }
    }

    log "[INFO] Creating new IIS Application Pool [$WebAppName]..."
    $newWebAppPool = New-WebAppPool -Name $WebAppName
    log "[INFO] Done."

    log "[INFO] Creating new WebApplication [$WebAppName] under site [Default Web Site] with path [$ScriptPath] and using Application Pool [$($newWebAppPool.name)]..."
    $newWebApp = New-WebApplication -Name $WebAppName -Site "Default Web Site" -PhysicalPath $ScriptPath -ApplicationPool $($newWebAppPool.name)
    log "[INFO] Done."

    try {
        log "[INFO] Changing attribute [maxQueryString] for [$WebAppName]..."
        $requestLimits = Get-IISConfigSection -CommitPath "Default Web Site/$WebAppName" -SectionPath "system.webServer/security/requestFiltering" | Get-IISConfigElement -ChildElementName "requestLimits"
        $maxQueryString_oldValue = $requestLimits.RawAttributes.maxQueryString
        log "[INFO]   maxQueryString old value: [$maxQueryString_oldValue]"
        Set-IISConfigAttributeValue -ConfigElement $requestLimits -AttributeName "maxQueryString" -AttributeValue $maxQueryStringValue
        $maxQueryString_newValue = $requestLimits.RawAttributes.maxQueryString
        log "[INFO]   maxQueryString new value: [$maxQueryString_newValue]"
        if ($maxQueryString_newValue -eq $maxQueryStringValue) {
            log "[INFO] Attribute maxQueryString for [$WebAppName] successfully changed from [$maxQueryString_oldValue] to [$maxQueryString_newValue]."
        } else {            
            throw "Exception message:`r`n $($_.Exception.ToString())"
        }
    } catch {
        log "[ERROR] Failed to set attribute [maxQueryString] for [$WebAppName]!"
    }

    log "$WebAppName install script finished successfully" -h

} catch {
    log "[ERROR] SCRIPT ERROR!"
    log "Returned error message:`r`n $($_.Exception.ToString())" -d
    log "Script finished with error" -h
    break
} Finally {
    RemoveAllCustomVariables
}

