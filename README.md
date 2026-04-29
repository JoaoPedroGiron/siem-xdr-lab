# 🛡️ SIEM / XDR Laboratory 2026

> **Blue Team Handbook** — Implementação de um laboratório moderno de detecção e resposta a ameaças utilizando Wazuh + Elastic Stack, com simulação de ataques via MITRE ATT&CK.

![Status](https://img.shields.io/badge/Status-Em%20Construção-yellow?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-MITRE%20ATT%26CK%20v14-red?style=flat-square)
![Stack](https://img.shields.io/badge/Stack-Wazuh%204.x%20%2B%20ELK%208.x-blue?style=flat-square)
![Nível](https://img.shields.io/badge/Nível-Intermediário%2FAvançado-orange?style=flat-square)
![Licença](https://img.shields.io/badge/Licença-MIT-green?style=flat-square)

---

## 📋 Sobre o Projeto

Este repositório documenta a construção de um laboratório de **SIEM (Security Information and Event Management)** e **XDR (Extended Detection and Response)** voltado para estudo e desenvolvimento de habilidades de Blue Team.

O lab foi projetado para rodar em hardware pessoal com recursos limitados (**16GB RAM**), utilizando uma arquitetura em fases onde as VMs são ligadas conforme necessário — sem precisar rodar tudo ao mesmo tempo.

### 🎯 Objetivos

- Implantar e configurar um stack SIEM/XDR completo com Wazuh 4.x e Elasticsearch 8.x
- Implementar telemetria avançada via Sysmon (config de Olaf Hartong), Winlogbeat e Auditd
- Desenvolver decoders e rules customizados mapeados ao MITRE ATT&CK
- Simular técnicas de ataque com Atomic Red Team e Kali Linux
- Criar dashboards de monitoramento no Kibana e automações de alerta em Python
- Expandir futuramente para cenários em nuvem (AWS/Azure/GCP)

---

## 🏗️ Arquitetura do Laboratório

### Topologia de Rede (VLANs)

```
┌─────────────────────────────────────────────────────────────┐
│  VLAN 10 - MGMT/SIEM (192.168.10.0/24)                     │
│  ├── wazuh-manager    192.168.10.10  (Wazuh All-in-One)    │
│  └── elastic-node     192.168.10.11  (ELK Stack)           │
├─────────────────────────────────────────────────────────────┤
│  VLAN 20 - ENDPOINTS (192.168.20.0/24)                      │
│  ├── WIN-DC01         192.168.20.10  (Windows Server AD)   │
│  └── HOST FÍSICO      192.168.20.20  (Windows 11 - Vítima) │
├─────────────────────────────────────────────────────────────┤
│  VLAN 30 - SERVERS (192.168.30.0/24)                        │
│  └── ubuntu-webserver 192.168.30.10  (Ubuntu App Web)      │
├─────────────────────────────────────────────────────────────┤
│  VLAN 40 - ATTACK (192.168.40.0/24)                         │
│  └── kali-attacker    192.168.40.10  (Kali Linux)          │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo de Telemetria

```
[Windows Host/AD]  --Wazuh Agent + Winlogbeat-->  [Wazuh Manager :1514]
[Ubuntu Server]    --Syslog + Filebeat---------->  [Wazuh Manager :514]
[Wazuh Manager]    --Forwarding API------------->  [Elasticsearch :9200]
[Elasticsearch]    --Query--------------------->   [Kibana :5601]
[Wazuh API]        --Webhook------------------->   [Discord / Telegram / Slack]
```

### ⚙️ Arquitetura em Fases (Hardware Limitado - 16GB RAM)

Como o lab roda em hardware pessoal, as VMs são divididas em fases para respeitar os 16GB de RAM disponíveis. O **Windows 11 host físico** é usado diretamente como endpoint vítima — tornando os eventos capturados reais.

| Fase | VMs Ativas | RAM Usada | Quando Usar |
|------|-----------|-----------|-------------|
| **A - SIEM Core** | Ubuntu + Wazuh Docker | ~6GB | Sempre que estudar |
| **B - Cenário AD** | Wazuh + Windows Server | ~10GB | Estudos de Active Directory |
| **C - Red Team** | Wazuh + Kali + Ubuntu Web | ~10GB | Simulação de ataques |

> **Nota:** O Wazuh Agent instalado no Windows 11 host captura eventos reais do sistema, incluindo todos os eventos do Sysmon — o que torna o aprendizado muito mais próximo de um ambiente corporativo real.

---

## 🛠️ Stack Tecnológico

| Componente | Versão | Função |
|-----------|--------|--------|
| Wazuh Manager | 4.7+ | SIEM core: coleta, correlação e alertas |
| Wazuh Indexer | 4.7+ | Armazenamento baseado em OpenSearch |
| Wazuh Dashboard | 4.7+ | Interface de visualização e investigação |
| Elasticsearch | 8.x | Indexação e busca de alto desempenho |
| Kibana | 8.x | Dashboards e visualizações avançadas |
| Logstash | 8.x | Pipeline de ingestão e enriquecimento |
| Sysmon | 15.x | Telemetria avançada de endpoints Windows |
| Winlogbeat | 8.x | Forwarding de eventos Windows |
| Atomic Red Team | latest | Simulação de técnicas ATT&CK |
| Kali Linux | 2024.x | Plataforma de simulação de ataques |

---

## 📁 Estrutura do Repositório

```
siem-xdr-lab/
├── README.md                        ← Este arquivo
├── docs/
│   └── blue-team-handbook.md        ← Guia técnico completo
├── infrastructure/
│   ├── network/                     ← Diagramas e configs de VLAN
│   └── docker/                      ← docker-compose do Wazuh
├── wazuh/
│   ├── decoders/                    ← Decoders XML customizados
│   └── rules/                       ← Rules mapeadas ao ATT&CK
├── sysmon/
│   └── sysmonconfig.xml             ← Config Olaf Hartong (ATT&CK)
├── scripts/
│   ├── hardening-host.sh            ← Hardening CIS Ubuntu
│   └── wazuh_alert_bot.py          ← Bot de alertas via webhook
└── cloud/                           ← (Em breve: AWS / Azure / GCP)
    └── README.md
```

---

## 🚀 Fases de Implementação

### ✅ Fase 0 — Arquitetura
Topologia de rede com isolamento de VLANs, mapeamento de IPs, regras de firewall e fluxo de logs documentados.

### 🔄 Fase 1 — Hardening e Configuração
- Hardening CIS do OS host (Ubuntu)
- Instalação do Wazuh via Docker Compose
- Instalação do agente Windows (host físico + Windows Server AD)
- Configuração avançada do Sysmon com template ATT&CK de Olaf Hartong
- Configuração do Winlogbeat e Auditd no Ubuntu

### 🔄 Fase 2 — Enriquecimento de Dados
- Decoders customizados para SSH Brute Force e Lateral Movement
- Rules mapeadas ao MITRE ATT&CK (T1110, T1003.001, T1059.001, T1550.002)
- Pipeline de enriquecimento via Logstash

### 🔄 Fase 3 — Cenário de Ataque Prático (T1059)
- Reconhecimento com Nmap/enum4linux
- Comprometimento inicial via Bash reverse shell
- Execução PowerShell com encoded command (Atomic Red Team)
- Lateral Movement para Active Directory (Impacket/Evil-WinRM)
- Dump de credenciais NTLM

### 🔄 Fase 4 — Monitoramento e Resposta
- Dashboard Kibana com KQL queries para 8 cenários de ameaça
- Playbook de Resposta a Incidentes (NIST SP 800-61)
- Active Response automatizado via Wazuh API

### 🔄 Fase 5 — Automação
- Script Python com integração à API do Wazuh
- Notificações ricas via Discord, Telegram e Slack
- Execução como serviço systemd

---

## 🎯 Cobertura MITRE ATT&CK

| Técnica | Nome | Detecção |
|---------|------|----------|
| T1059.001 | PowerShell | Sysmon EID 1 + Rule 100030 |
| T1059.004 | Bash Script | Auditd + Wazuh rules |
| T1110 | Brute Force | Decoder SSH + Rule 100001 |
| T1003.001 | LSASS Memory | Sysmon EID 10 + Rule 100020 |
| T1021.002 | SMB/WinRM | Rule 100010 (PsExec) |
| T1550.002 | Pass-the-Hash | EID 4624 Logon Type 3 NTLM |
| T1547.001 | Registry Run Keys | Sysmon EID 13 + FIM |
| T1027 | Obfuscation | Filtro Base64/FromBase64 |

---

## 📦 Requisitos de Hardware

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| CPU | 4 cores | 6+ cores (Ryzen 5600G ✅) |
| RAM | 16GB | 32GB |
| Disco | 100GB SSD | 200GB+ SSD |
| GPU | Não necessária | — |

> Este lab foi otimizado para rodar em **16GB RAM** utilizando a arquitetura em fases descrita acima.

---

## 🔮 Roadmap

- [x] Estrutura inicial do repositório
- [ ] Fase 0 — Documentação da arquitetura
- [ ] Fase 1 — Scripts de instalação e hardening
- [ ] Fase 2 — Decoders e rules customizados
- [ ] Fase 3 — Cenários de ataque documentados
- [ ] Fase 4 — Dashboards Kibana
- [ ] Fase 5 — Bot de alertas Python
- [ ] Cloud — Integração com AWS (CloudTrail + GuardDuty)
- [ ] Cloud — Integração com Azure Sentinel
- [ ] Cloud — Integração com GCP Security Command Center

---

## 📚 Referências

- [Documentação Wazuh](https://documentation.wazuh.com)
- [Sysmon Config - Olaf Hartong](https://github.com/olafhartong/sysmon-modular)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
- [MITRE ATT&CK Matrix](https://attack.mitre.org)
- [NIST SP 800-61 Rev2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)

---

## ⚠️ Aviso Legal

Todas as simulações de ataque documentadas neste repositório devem ser realizadas **exclusivamente em ambiente de laboratório isolado**, sem conectividade com redes de produção. O uso dessas técnicas em sistemas sem autorização é crime conforme a **Lei 12.737/2012** e o **art. 154-A do Código Penal Brasileiro**.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

<div align="center">

**Construa. Detecte. Responda. Aprenda.**

*Blue Team Handbook — SIEM/XDR Lab 2026 | v2.0*

</div>
