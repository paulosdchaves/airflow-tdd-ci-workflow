# Airflow DAG development using TDD with tests + CI/CD github actions
(project &amp; tutorial) dag using TDD + tests + ci/cd setup

[![CI](https://github.com/paulosdchaves/airflow-tdd-ci-workflow/workflows/CI/badge.svg?branch=master)](https://github.com/paulosdchaves/airflow-tdd-ci-workflow/actions?query=workflow:CI)

## The project

Projeto voltado para a comunidade de dados usando as melhores práticas de desenvolvimento junto com a técnica TDD(Test Driven Development) para a criação dos componentes, features e DAGS e CI/CD para deploy automatizado.

**Projeto em construção (Project under construction)**

# Executando Airflow localmente

![local_desktop_airflow.png](/docs/local_desktop_airflow.png)

Para rodar o Airflow localmente você precisará de:

- Pelo menos 3G de RAM disponíveis
- Banda larga para baixar imagens Docker

### Dependências?
Docker, docker-compose and makefile.

### Como rodar?

O comando abaixo configurará o ambiente usando o docker-compose para o Airflow inicializar suas configurações internas, criação das credenciais e conexões.
```bash
make setup
```
Ao executar o comando acima, é possível acessar o Airflow em `localhost: 8080`. 
Um usuário de testes é criado user: admin / password: admin.
O comando abaixo roda os testes:
```bash
make testing
```