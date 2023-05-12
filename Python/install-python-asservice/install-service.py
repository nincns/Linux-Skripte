import os
import subprocess

def check_for_service(service_name):
    try:
        output = subprocess.check_output(
            ["systemctl", "is-active", f"{service_name}"],
            universal_newlines=True
        )
        if 'inactive' in output or 'failed' in output:
            return False
        else:
            return True
    except Exception as e:
        return False

def install_service(service_name, script_path):
    service_content = f"""
    [Unit]
    Description={service_name}

    [Service]
    ExecStart=/usr/bin/python3 {script_path}
    Restart=always

    [Install]
    WantedBy=multi-user.target
    """

    with open(f'/etc/systemd/system/{service_name}.service', 'w') as service_file:
        service_file.write(service_content)

    subprocess.check_output(["systemctl", "daemon-reload"])
    subprocess.check_output(["systemctl", "enable", service_name])
    subprocess.check_output(["systemctl", "start", service_name])
    print(f'Service {service_name} installed and started.')

def remove_service(service_name):
    subprocess.check_output(["systemctl", "stop", service_name])
    subprocess.check_output(["systemctl", "disable", service_name])
    os.remove(f'/etc/systemd/system/{service_name}.service')
    subprocess.check_output(["systemctl", "daemon-reload"])
    print(f'Service {service_name} removed.')

def main():
    scripts = [f for f in os.listdir() if f.endswith('.py') and f != os.path.basename(__file__)]
    for index, script in enumerate(scripts, start=1):
        service_name = f'{script[:-3]}_service'
        print(f"{index}. {script} - {'Installed' if check_for_service(service_name) else 'Not installed'}")

    print("\nSelect the script number to install/uninstall or 0 to exit:")
    selection = int(input("> "))
    if selection == 0:
        return
    elif selection > 0 and selection <= len(scripts):
        script = scripts[selection-1]
        service_name = f'{script[:-3]}_service'
        if check_for_service(service_name):
            print(f"Uninstalling service for {script}...")
            remove_service(service_name)
        else:
            print(f"Installing service for {script}...")
            install_service(service_name, os.path.join(os.getcwd(), script))
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
