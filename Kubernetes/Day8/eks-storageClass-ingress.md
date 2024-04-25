# Kubernetes Hands-on Day-2 : StorageClass - Ingress


## Prerequisites

1. AWS CLI 

2. kubectl 

3. eksctl --------> [Installing or upgrading eksctl.](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)


## Part 1 - Installing kubectl and eksctl on Amazon Linux 2

### Install kubectl

```bash
sudo yum update -y
```

- Download the Amazon EKS vended kubectl binary.

```bash
curl -o kubectl https://s3.us-west-2.amazonaws.com/amazon-eks/1.22.6/2022-03-09/bin/linux/amd64/kubectl
```

- Apply execute permissions to the binary.

```bash
chmod +x ./kubectl
```

- Copy the binary to a folder in your PATH. If you have already installed a version of kubectl, then we recommend creating a $HOME/bin/kubectl and ensuring that $HOME/bin comes first in your $PATH.

```bash
mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
```

- (Optional) Add the $HOME/bin path to your shell initialization file so that it is configured when you open a shell.

```bash
echo 'export PATH=$PATH:$HOME/bin' >> ~/.bashrc
```

- After you install kubectl , you can verify its version with the following command:

```bash
kubectl version --short --client
```

### Install eksctl

- Download and extract the latest release of eksctl with the following command.

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
```

- Move the extracted binary to /usr/local/bin.

```bash
sudo mv /tmp/eksctl /usr/local/bin
```

- Test that your installation was successful with the following command.

```bash
eksctl version
```

## Part 2 - Creating the Kubernetes Cluster on EKS

- If needed create ssh-key with commnad `ssh-keygen -f ~/.ssh/id_rsa`

- Configure AWS credentials. Or you can attach `AWS IAM Role` to your EC2 instance.

```bash
aws configure
```

- Create an EKS cluster via `eksctl`. It will take a while.

```bash
eksctl create cluster \
 --name my-cluster \
 --region us-east-1 \
 --zones us-east-1a,us-east-1b,us-east-1c \
 --nodegroup-name my-nodes \
 --node-type t2.small \
 --nodes 2 \
 --nodes-min 2 \
 --nodes-max 3 \
 --ssh-access \
 --ssh-public-key  ~/.ssh/id_rsa.pub \
 --managed \
 --version 1.22
```

or 

```bash
eksctl create cluster --region us-east-1 --zones us-east-1a,us-east-1b,us-east-1c --node-type t2.medium --nodes 2 --nodes-min 2 --nodes-max 3 --name my-cluster
```

- Explain the deault values. 

```bash
eksctl create cluster --help
```

## Part 3 - Volume Provisionining

- Firstly, check the StorageClass object in the cluster. 

```bash
kubectl get sc

kubectl describe sc/gp2
```

- Create a StorageClass with the following settings.

```bash
vi storage-class.yaml
```

```yaml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: aws-standard
provisioner: kubernetes.io/aws-ebs
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: gp2
  fsType: ext4           
```


```bash
kubectl apply -f storage-class.yaml
```

- Explain the default storageclass

```bash
kubectl get storageclass
```

- Create a persistentvolumeclaim with the following settings and show that new volume is created on aws management console.

```bash
vi devops-pv-claim.yaml
```
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: devops-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
  storageClassName: aws-standard
```

```bash
kubectl apply -f devops-pv-claim.yaml
```

- List the pv and pvc and explain the connections.

```bash
kubectl get pv,pvc
```
- You will see an output like this because binding mode is WaitForFirstConsumer

NAME                                    STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/devops-pv-claim   Pending                                      aws-standard   44s

- Create a pod with the following settings.

```bash
vi pod-with-dynamic-storage.yaml
```
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-aws
  labels:
    app : web-nginx
spec:
  containers:
  - image: nginx:latest
    ports:
    - containerPort: 80
    name: test-aws
    volumeMounts:
    - mountPath: /usr/share/nginx/html
      name: aws-pd
  volumes:
  - name: aws-pd
    persistentVolumeClaim:
      claimName: devops-pv-claim
```

```bash
kubectl apply -f pod-with-dynamic-storage.yaml
```

- Enter the pod and see that ebs is mounted to  /usr/share/nginx/html path.

```bash
kubectl exec -it test-aws -- bash
```
- You will see an output like this
- 
```bash
df -h
lsblk
```

- Delete the storageclass that we create.

```bash
kubectl get storageclass
```

```bash
kubectl delete storageclass aws-standard
```

```bash
kubectl get storageclass
```

- Delete the pod

```bash
kubectl delete -f pod-with-dynamic-storage.yaml
```

## Part 4 - Ingress

Let's check the state of the cluster and see that everything works fine.

```bash
kubectl cluster-info
kubectl get node
```

- Let's check the MongoDB `service`.

```bash
cat db-service.yaml
```
- You will see an output like this

```yaml
apiVersion: v1
kind: Service
metadata:
  name: db-service
  labels:
    name: mongo
    app: todoapp
spec:
  selector:
    name: mongo
  type: ClusterIP
  ports:
    - name: db
      port: 27017
      targetPort: 27017
```


```bash
cat web-service.yaml
```
- You will see an output like this

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
  labels:
    name: web
    app: todoapp
spec:
  selector:
    name: web 
  type: LoadBalancer
  ports:
   - name: http
     port: 3000
     targetPort: 3000
     protocol: TCP
```

Check the web application `Deployment` file.
```bash
cat web-deployment.yaml
```
- You will see an output like this

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      name: web
  template:
    metadata:
      labels:
        name: web
        app: todoapp
    spec:
      containers: 
        - image: eagle79/todo
          imagePullPolicy: Always
          name: myweb
          ports: 
            - containerPort: 3000
          env:
            - name: "DBHOST"
              value: "db-service:27017"
          resources:
            limits:
              cpu: 100m
            requests:
              cpu: 80m
```

Let's deploy the to-do application.

```bash
kubectl apply -f .
```
Note that we can use `directory` with `kubectl apply -f` command.

- Check the pods.
```bash
kubectl get pods
```

- Check the services.
  
```bash
kubectl get svc
```

- We can visit xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.us-east-2.elb.amazonaws.com:3000 and access the application.


We see the home page. You can add to-do's.

- Now deploy the second application

```bash
cd php/
cat php-apache.yaml
```
- You will see an output like this

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  replicas: 1
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: k8s.gcr.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 100m
          requests:
            cpu: 80m
---
apiVersion: v1
kind: Service
metadata:
  name: php-apache-service
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache 
  type: LoadBalancer	
```

Note how the `Deployment` and `Service` `yaml` files are merged in one file. 

- Deploy this `php-apache` file.

```bash
kubectl apply -f php-apache.yaml 
```

- Get the pods.

```bash
kubectl get po
```
- Get the services.

```bash
kubectl get svc
```


Let's check what web app presents us.

- On opening browser (xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.us-east-2.elb.amazonaws.com ) we see

```text
OK!
```


## Ingress

Briefly explain ingress and ingress controller. For additional information a few portal can be visited like;

- https://kubernetes.io/docs/concepts/services-networking/ingress/
  
- https://banzaicloud.com/blog/k8s-ingress/
  
- Open the offical [ingress-nginx]( https://kubernetes.github.io/ingress-nginx/deploy/ ) explain the `ingress-controller` installation steps for different architecture.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.2.0/deploy/static/provider/cloud/deploy.yaml

```

- Now, check the contents of the `ingress-service`.

```bash
 cat ingress-service.yaml
```
- You will see an output like this

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-service
  annotations:
    kubernetes.io/ingress.class: 'nginx'
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port: 
                  number: 3000
          - path: /load
            pathType: Prefix
            backend:
              service:
                name: php-apache-service
                port: 
                  number: 80
```

- Explain the rules part.

```bash
kubectl apply -f ingress-service.yaml
```


```bash
kubectl get ingress
```


On browser, type this  ( xxxxxxxxxxxxxxxxxxxxxxxxxxxxx.elb.eu-central-1.amazonaws.com ), you must see the to-do app web page. If you type `xxxxxxxxxxxxxxxxxxxxxxx.elb.eu-central-1.amazonaws.com/load`, then the apache-php page, "OK!". Notice that we don't use the exposed ports at the services.

- Delete the cluster

```bash
eksctl get cluster --region us-east-1
```
- You will see an output like this

```text
NAME            REGION
my-cluster      us-east-2
```
```bash
eksctl delete cluster my-cluster --region us-east-1
```

- Do no forget to delete related ebs volumes.
