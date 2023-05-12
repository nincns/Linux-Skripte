#!/bin/bash

install_service() {
  service_name=$1
  script_path=$2
  service_file="/etc/systemd/system/${service_name}.service"

  echo "[Unit]
Description=${service_name}

[Service]
ExecStart=/bin/bash ${script_path}
Restart=always

[Install]
WantedBy=multi-user.target
" > ${service_file}

  systemctl daemon-reload
  systemctl enable ${service_name}
  systemctl start ${service_name}
  echo "Service ${service_name} installed and started."
}

remove_service() {
  service_name=$1
  service_file="/etc/systemd/system/${service_name}.service"
  
  systemctl stop ${service_name}
  systemctl disable ${service_name}
  rm ${service_file}
  systemctl daemon-reload
  echo "Service ${service_name} removed."
}

check_for_service() {
  service_name=$1
  service_status=$(systemctl is-active ${service_name})
  
  if [[ ${service_status} == "active" ]]; then
    return 0
  else
    return 1
  fi
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ${SCRIPT_DIR}
SCRIPTS=$(ls ${SCRIPT_DIR}/*.sh | grep -v install-service.sh)

index=1
declare -A script_map
for script in ${SCRIPTS}; do
  script_name=$(basename ${script} .sh)
  service_name=${script_name}_service
  if check_for_service ${service_name}; then
    status="Installed"
  else
    status="Not installed"
  fi
  echo "${index}. ${script_name} - ${status}"
  script_map[${index}]=${script_name}
  index=$((index+1))
done

echo -n "Select the script number to install/uninstall or 0 to exit: "
read selection
if ((selection == 0)); then
  exit
elif ((selection > 0 && selection < index)); then
  script_name=${script_map[${selection}]}
  service_name=${script_name}_service
  if check_for_service ${service_name}; then
    echo "Uninstalling service for ${script_name}..."
    remove_service ${service_name}
  else
    echo "Installing service for ${script_name}..."
    install_service ${service_name} ${SCRIPT_DIR}/${script_name}.sh
  fi
else
  echo "Invalid selection."
fi
