# TV Program Challenge

## Arquitetura do Projeto

O projeto está dividido em camadas:

- **Application**: Contém endpoints, cronjobs e outros pontos de entrada
- **Cross**: Dependências gerais e compartilhadas
- **Domain**: Define interfaces, serviços e entidades
- **Infra**: Implementações concretas das interfaces definidas na camada de domínio

*Observação:* Toda a estrutura foi preparada para injeção de dependências, porém esta feature não foi implementada devido a restrições de tempo.

## Implementação Atual

### Características Principais
- Utiliza Redis como banco de dados temporário
- Integração com Amazon S3 para carregamento de arquivos CSV
- Arquitetura flexível para múltiplas implementações de:
  - Conexões com bancos de dados
  - Estratégias de importação de arquivos

## Kubernetes Cluster Setup

### Componentes Principais
**Kong Gateway**:
- Configurado como proxy reverso para o microserviço
- Gerenciamento via Kong Manager:  
  [Acessar Kong Manager](https://kongmanager-test.lh-test.net/)
- Acessar doc fast-api [Acessar Fast api docs](https://kongadmin-test.lh-test.net/docs)

**Aplicação FastAPI**:
- Implantada em pod separado com auto-scaling horizontal
- Job programado para execução diária

### Configurações Especiais:
- Roteamento interno via Kong Gateway
- Namespaces segregados para diferentes componentes
- Infraestrutura auto-escalável


