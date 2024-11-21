
# Projeto Nuvem - Deploy na AWS com EKS

**Autor:** Lucas Lima
**Projeto:** Deploy na AWS usando EKS

**Vídeo de demonstração** [AWS deployment](https://youtu.be/iUxmSB9jtRw)


Este documento detalha o processo de deploy de uma aplicação na AWS usando o Kubernetes (EKS) e outras ferramentas associadas.

## Requisitos

1. **Amazon CLI**: Ferramenta para interagir com os serviços da AWS.
   - Link para instalação: [Amazon CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. **Choco (Chocolatey)**: Gerenciador de pacotes para Windows.
   - Link para instalação: [Chocolatey Installation Guide](https://chocolatey.org/install)

3. **EKSCTL**: Ferramenta para facilitar a configuração e gerenciamento de clusters no EKS.
   - Link para instalação: [EKSCTL Installation Guide](https://eksctl.io/installation/)

4. **kubectl**: Ferramenta para gerenciar clusters Kubernetes.

## Passo a Passo

### 1. Configuração das Credenciais de Acesso

- Acesse o console da AWS para criar as credenciais de acesso necessárias.
- Link de acesso ao IAM: [AWS IAM Console](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-2#/users)

Após criar as credenciais, configure-as localmente usando o comando:
```bash
aws configure
```

### 2. Criação do Cluster

Use o EKSCTL para criar um cluster Kubernetes com as seguintes especificações:

- Nome do cluster: `projeto-nuvem-cluster`
- Região: `sa-east-1`
- Tipo de instância: `t3.medium`
- Número de nós: `2`

Comando para criação do cluster:
```bash
eksctl create cluster --name projeto-nuvem-cluster --region sa-east-1 --nodes 2 --node-type t3.medium
```

Após a criação, configure o `kubeconfig` para se conectar ao cluster:
```bash
aws eks --region sa-east-1 update-kubeconfig --name projeto-nuvem-cluster
```

### 3. Criação dos Arquivos de Deploy

#### Arquivo de Deploy da API (`api-deployment.yaml`)
Este arquivo configura o deployment e o serviço da API no cluster. O serviço é do tipo `LoadBalancer`, expondo a API para acesso externo.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: lucasouzamil/projeto-api-consulta-dolar:v1.0
          env:
            - name: USER
              value: "projeto"
            - name: PASSWORD
              value: "projeto"
            - name: SERVER
              value: "mysql-service"
            - name: PORT
              value: "3306"
            - name: DATABASE_NAME
              value: "projeto"
            - name: SECRET_KEY
              value: "key_super_secreta"
            - name: ALGORITHM
              value: "HS256"
            - name: ACCESS_TOKEN_EXPIRE_MINUTES
              value: "30"
          ports:
            - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  type: LoadBalancer
  ports:
    - port: 8000
      targetPort: 8000
  selector:
    app: api

```

#### Arquivo de Deploy do Banco de Dados (`sql-deployment.yaml`)
Este arquivo configura o deployment e o serviço do banco de dados MySQL.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:9.1.0
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "projeto"
            - name: MYSQL_DATABASE
              value: "projeto"
            - name: MYSQL_USER
              value: "projeto"
            - name: MYSQL_PASSWORD
              value: "projeto"
          ports:
            - containerPort: 3306
---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
spec:
  type: ClusterIP
  ports:
    - port: 3306
      targetPort: 3306
  selector:
    app: mysql

```

### 4. Aplicação dos Arquivos de Deploy

Faça o deploy dos serviços no cluster Kubernetes usando o `kubectl`:

```bash
kubectl apply -f sql-deployment.yaml
kubectl apply -f api-deployment.yaml
```

### 5. Verificação dos Serviços

Verifique os serviços e obtenha os endpoints gerados pelo LoadBalancer:

```bash
kubectl get svc
```

## Considerações

1. Certifique-se de que os arquivos YAML estão corretos e completos.
2. O endpoint da API será gerado automaticamente após o deploy. Use o comando acima para verificá-lo.
