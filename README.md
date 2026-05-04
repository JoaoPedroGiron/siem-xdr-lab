# 🛡️ Laboratório SIEM/XDR — Blue Team 2026

![Status](https://img.shields.io/badge/Status-Em%20Andamento-yellow?style=flat-square)
![Framework](https://img.shields.io/badge/MITRE%20ATT%26CK-v14-red?style=flat-square)
![SIEM](https://img.shields.io/badge/SIEM-Wazuh%204.7-blue?style=flat-square)
![AD](https://img.shields.io/badge/Active%20Directory-lab.local-blueviolet?style=flat-square)
![Licença](https://img.shields.io/badge/Licença-MIT-green?style=flat-square)

---

## Overview

Este projeto é um laboratório de segurança ofensiva e defensiva hospedado localmente em ambiente virtualizado, simulando uma infraestrutura corporativa real. O objetivo é praticar detecção e resposta a ameaças utilizando um SIEM (Wazuh) para coletar e correlacionar logs de todos os hosts do ambiente, enquanto técnicas de ataque mapeadas no framework **MITRE ATT&CK** são executadas para validar a capacidade de detecção.

O projeto foi implementado com as seguintes tecnologias:

- **Wazuh:** Utilizado como plataforma SIEM/XDR para coleta, correlação e visualização de alertas de segurança.
- **Docker:** Utilizado para containerizar o stack Wazuh (Manager, Indexer e Dashboard), garantindo um ambiente consistente e fácil de recriar.
- **Sysmon:** Utilizado nos endpoints Windows para capturar telemetria avançada de processos, conexões de rede e acessos a arquivos.
- **Active Directory:** Utilizado para simular um ambiente corporativo real com domínio, usuários e políticas de grupo.
- **Winlogbeat:** Utilizado para forwarding de eventos Windows para o SIEM.
- **Kali Linux:** Utilizado como plataforma de simulação de ataques Red Team.
- **Python:** Utilizado para automação de alertas via integração com a API REST do Wazuh.

---

## Tecnologias Utilizadas

- **SIEM/XDR:** Wazuh 4.7 (Manager, Indexer, Dashboard)
- **Endpoints:** Windows 11, Windows Server 2022
- **Telemetria:** Sysmon 15.x, Winlogbeat 8.x, Auditd
- **Infraestrutura:** Docker, VirtualBox
- **Active Directory:** Windows Server 2022 — domínio `lab.local`
- **Red Team:** Kali Linux, Atomic Red Team
- **Automação:** Python 3.x + API REST Wazuh
- **Framework:** MITRE ATT&CK v14, NIST SP 800-61

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                     REDE DO LABORATÓRIO                         │
│                      192.168.1.0/24                             │
│                                                                 │
│  ┌─────────────────┐      ┌──────────────────────────────────┐ │
│  │   RED TEAM      │      │         SIEM / MONITORAMENTO     │ │
│  │                 │      │                                  │ │
│  │  Kali Linux     │      │  Ubuntu Server                   │ │
│  │  192.168.1.x    │      │  192.168.1.103                   │ │
│  │                 │      │  Wazuh Manager + Indexer +       │ │
│  └────────┬────────┘      │  Dashboard (Docker)              │ │
│           │               └──────────────┬───────────────────┘ │
│           │ ataca                        │ recebe logs          │
│           ▼                              │                      │
│  ┌─────────────────────────────────────┐│                      │
│  │           ENDPOINTS                 ││                      │
│  │                                     ││                      │
│  │  Windows 11 (host físico)           ││                      │
│  │  192.168.1.101                      ├┘                      │
│  │  Wazuh Agent + Sysmon              │                        │
│  │                                     │                       │
│  │  Windows Server 2022 (AD)          │                        │
│  │  192.168.1.105                      │                       │
│  │  Wazuh Agent + Sysmon + Winlogbeat │                        │
│  │                                     │                       │
│  │  Ubuntu Server (App Web)           │                        │
│  │  192.168.1.x                        │                       │
│  │  Wazuh Agent + Auditd              │                        │
│  └─────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Telemetria

```
[Windows 11]      --Wazuh Agent + Sysmon-->    [Wazuh Manager :1514]
[Windows Server]  --Wazuh Agent + Winlogbeat--> [Wazuh Manager :1514]
[Ubuntu Server]   --Syslog + Auditd-------->    [Wazuh Manager :514]
[Wazuh Manager]   --Indexação-------------->    [Wazuh Indexer :9200]
[Wazuh Indexer]   --Visualização---------->     [Wazuh Dashboard :443]
[Wazuh API]       --Webhook--------------->     [Discord / Telegram]
```

---

## Descrição dos Componentes

**Wazuh Manager**
Responsável por receber os logs de todos os agentes, aplicar decoders e rules de detecção, e gerar alertas de segurança. É o cérebro do SIEM.

**Wazuh Indexer**
Baseado em OpenSearch, armazena e indexa todos os eventos coletados, permitindo buscas e correlações em tempo real.

**Wazuh Dashboard**
Interface de visualização e investigação dos alertas. Permite criar dashboards customizados, consultar eventos por técnica MITRE ATT&CK e analisar o comportamento dos agentes.

**Sysmon**
Instalado nos endpoints Windows com a configuração de Olaf Hartong, mapeada ao MITRE ATT&CK. Captura eventos críticos como criação de processos (EID 1), conexões de rede (EID 3), carregamento de DLLs (EID 7) e acesso ao processo LSASS (EID 10).

**Winlogbeat**
Responsável pelo forwarding dos eventos do Windows Event Log para o Wazuh Manager, incluindo logs de segurança, sistema e PowerShell.

**Active Directory (lab.local)**
Simula um ambiente corporativo real com Domain Controller, usuários e políticas de grupo — alvo de técnicas como Pass-the-Hash, Lateral Movement e Kerberoasting.

**Kali Linux**
Plataforma de simulação de ataques Red Team. Utilizado com ferramentas como Nmap, Impacket, Evil-WinRM e Atomic Red Team para executar técnicas do MITRE ATT&CK de forma controlada.

---

## Cobertura MITRE ATT&CK

| Técnica | Nome | Detecção |
|---------|------|----------|
| T1059.001 | PowerShell | Sysmon EID 1 + filtro encoded command |
| T1059.004 | Bash Script | Auditd + Wazuh rules |
| T1110 | Brute Force | Decoder SSH + frequência de eventos |
| T1003.001 | LSASS Memory Dump | Sysmon EID 10 (ProcessAccess) |
| T1021.002 | SMB/WinRM | Detecção de PsExec + EID 7045 |
| T1550.002 | Pass-the-Hash | EID 4624 Logon Type 3 NTLM |
| T1547.001 | Registry Run Keys | Sysmon EID 13 + FIM |
| T1027 | Obfuscação | Filtro Base64/FromBase64String |

---

## Status de Implementação

| Fase | Descrição | Status |
|------|-----------|--------|
| Fase 0 | Arquitetura e topologia de rede | ✅ Concluída |
| Fase 1 | Wazuh + agentes + Sysmon + AD | ✅ Concluída |
| Fase 2 | Decoders e rules customizados | 🔄 Em andamento |
| Fase 3 | Cenários de ataque (MITRE ATT&CK) | 🔄 Em andamento |
| Fase 4 | Dashboards de monitoramento | ⏳ Pendente |
| Fase 5 | Automação Python + Webhooks | ⏳ Pendente |
| Cloud | Integração AWS / Azure | ⏳ Roadmap |

---

## Estrutura do Repositório

```
siem-xdr-lab/
├── docs/           → Guia técnico completo (Blue Team Handbook)
├── infrastructure/ → Docker Compose e configs de rede
├── wazuh/          → Decoders e rules customizados
├── sysmon/         → sysmonconfig.xml (Olaf Hartong)
├── scripts/        → Hardening CIS e automação Python
└── cloud/          → Próximos passos: AWS / Azure
```

---

## Referências

- [Documentação Wazuh](https://documentation.wazuh.com)
- [Sysmon Modular — Olaf Hartong](https://github.com/olafhartong/sysmon-modular)
- [Atomic Red Team — Red Canary](https://github.com/redcanaryco/atomic-red-team)
- [MITRE ATT&CK](https://attack.mitre.org)
- [NIST SP 800-61 Rev2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [Wazuh Docker — Repositório Oficial](https://github.com/wazuh/wazuh-docker)

---

> ⚠️ **Aviso Legal:** Todas as simulações de ataque documentadas neste repositório são realizadas exclusivamente em ambiente de laboratório isolado, sem conectividade com redes de produção. O uso não autorizado dessas técnicas é crime conforme a **Lei 12.737/2012** e o **art. 154-A do Código Penal Brasileiro**.
