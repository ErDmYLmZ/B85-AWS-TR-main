# Kubernetes Networking Sample Hands-on

## Using Service and Selector for Pod Labels

### Outline

In this task there is a service of NodePort type. There are 2 versions of a web application. First initial version is deployed in the K8S cluster. Then the newer version is deployed. Web service selector is used to enable either pods/application.

### Create the service

- Create a yaml file and apply it using "kubectl apply -f .." command

map-service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: map-webapp-svc

spec:
  # This defines which pods are going to be represented by this Service
  # The service becomes a network endpoint for either other services
  # or maybe external users to connect to (eg browser)
  selector:
    app: webapp
    

  ports:
    - name: http
      port: 80
      nodePort: 30080

  type: NodePort
```
- create the yaml file for the web application, then apply it using "kubectl apply -f ..." command

map1.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: map-webapp
  labels:
    app: webapp
    
spec:
  containers:
  - name: webapp
    image: richardchesterwood/k8s-fleetman-webapp-angular:release0
```

- now, as the service is NodePort, we can view the application that broadcasts on the service port. 

- check the services and get the port number

```bash
kubectl get svc
```

- use the worker node publicIP to view the app on browser.

workernode PublicIP:Nodeport

- now see which endpoints are attached to the service

```bash
kubectl describe svc servicenameofmapapp
```

- you should see only one IP that belongs to the pod running the app.

- now create another yaml file for the second version of the map app.

map2.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: map-webapp-r0-5
  labels:
    app: webapp
    release: "0-5"
spec:
  containers:
  - name: webapp
    image: richardchesterwood/k8s-fleetman-webapp-angular:release0-5
```

- run yaml file using

```bash
kubectl apply -f map2.yaml
```

- now check the endpoints in the service description

```bash
kubectl describe svc servicenameofmapapp
```

- you will notice 2 endpoints now, this is because the second app label matches the service label selector.

- now we will modify service label selector, adding one more label.

- edit the existing file

map-service.yaml 

```yaml
apiVersion: v1
kind: Service
metadata:
  name: map-webapp-svc

spec:
  # This defines which pods are going to be represented by this Service
  # The service becomes a network endpoint for either other services
  # or maybe external users to connect to (eg browser)
  selector:
    app: webapp
    release: "0-5"

  ports:
    - name: http
      port: 80
      nodePort: 30080

  type: NodePort
```
- After the new label we added the service will match the pods having both labels

- now check the endpoints in service description

```bash
kubectl describe svc servicenameofmapapp
```

- you see one endpoint, whose IP is it? To find out see the pods details

```bash
kubectl get pods -o wide
```

- now go to the browser to see the new version of the app

### In this sample task, service object matched the pods with the labels in service labels selector. In case there are more than 1, only the pods that have all the selected labels are matched.

Congratulations! Lab is finished!
