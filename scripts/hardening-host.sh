#!/bin/bash
# hardening-host.sh - CIS Ubuntu 22.04 Hardening
# Executar como root na VM Ubuntu Wazuh

# --- 1. Atualizacao do sistema ---
apt-get update && apt-get upgrade -y
apt-get install -y unattended-upgrades fail2ban ufw auditd

# --- 2. Configurar UFW ---
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 1514/tcp
ufw allow 1515/tcp
ufw allow 55000/tcp
ufw allow 9200/tcp
ufw allow 5601/tcp
ufw allow 443/tcp
ufw --force enable

# --- 3. Hardening SSH ---
sed -i "s/#PermitRootLogin yes/PermitRootLogin no/" /etc/ssh/sshd_config
sed -i "s/#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config
sed -i "s/X11Forwarding yes/X11Forwarding no/" /etc/ssh/sshd_config
echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
systemctl restart sshd

# --- 4. Configurar auditd ---
cat >> /etc/audit/rules.d/hardening.rules << EOF
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/sudoers -p wa -k sudoers
-a always,exit -F arch=b64 -S execve -k exec_commands
EOF
service auditd restart

# --- 5. Desabilitar servicos desnecessarios ---
systemctl disable --now avahi-daemon cups bluetooth 2>/dev/null

# --- 6. Configurar fail2ban ---
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOF
systemctl enable --now fail2ban

echo "[OK] Hardening concluido."