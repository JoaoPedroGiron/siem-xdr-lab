# Laboratório SIEM/XDR — Blue Team

## O que é esse projeto?

Esse repositório documenta um laboratório de segurança que montei para aprender na prática como funcionam as plataformas SIEM. A ideia foi subir um ambiente virtualizado que simulasse uma rede corporativa real, coletar os logs gerados por essa infraestrutura e ver o que seria possível detectar.

Para o SIEM, escolhi o Wazuh, que foi uma indicação pela facilidade de uso e implementação, e se mostrou uma boa escolha para quem está começando.

## Por que montei isso?

Estou me especializando em cibersegurança com foco em SOC, e quis construir algo prático que me ajudasse a entender como esse ambiente funciona de verdade. Usei o framework MITRE ATT&CK como referência para simular ataques controlados e testar se o SIEM conseguia detectá-los, e o NIST SP 800-61 para orientar como organizar o processo de detecção e resposta.

## O que foi montado

O laboratório roda localmente em máquinas virtuais. O Wazuh foi containerizado com Docker e fica acessível pelo navegador. Os agentes instalados nos endpoints enviam os logs para ele via rede local, e tudo é visualizado em um dashboard centralizado.

Os endpoints monitorados foram um Windows 11, um Windows Server com Active Directory, e um Ubuntu Server. Para simular os ataques, usei um Kali Linux separado na mesma rede.

## O que foi testado

Com o ambiente no ar, simulei algumas técnicas de ataque de forma controlada para ver se o SIEM conseguia identificá-las. Testei coisas como execução de comandos via PowerShell, tentativas de força bruta, dump de memória, movimentação lateral na rede e ofuscação de código. Em todos os casos o objetivo foi validar se os alertas eram gerados corretamente.

## O que aprendi

A maior dificuldade foi subir toda a infraestrutura: configurar as máquinas virtuais, fazer os agentes se comunicarem com o servidor do Wazuh, liberar as portas certas e garantir que os logs chegassem de ponta a ponta. Mas o que ficou de conhecimento real foi entender como um SIEM funciona por baixo dos panos, como os logs chegam, como as regras de detecção são aplicadas e como um analista de SOC usaria essa ferramenta no dia a dia.

## Estrutura do repositório

```
siem-xdr-lab/
├── docs/           → Documentação técnica do projeto
├── infrastructure/ → Docker Compose e configurações de rede
├── wazuh/          → Regras e decoders customizados
├── sysmon/         → Configuração do Sysmon
└── scripts/        → Scripts de automação em Python
```

## Referências

- [Documentação Wazuh](https://documentation.wazuh.com)
- [MITRE ATT&CK](https://attack.mitre.org)
- [NIST SP 800-61](https://www.nist.gov/publications/computer-security-incident-handling-guide)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)

> ⚠️ Todas as simulações de ataque foram realizadas exclusivamente em ambiente de laboratório isolado, sem conexão com redes de produção.
