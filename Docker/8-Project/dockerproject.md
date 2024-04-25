# Hands-on Docker-Compose: Docker Compose practice


## Part 1 & 2 - Launch a Docker Machine Instance and Connect with SSH

- Launch a Docker machine on Amazon Linux 2 AMI with security group allowing SSH connections.
* User Data:
```bash
#! /bin/bash

yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
sudo yum install git -y
```
* Security:
```bash
 SSH 22 Anywhere
 HTTP 80 Anywhere
 Custom TCP 8080 Anywhere
```
- Connect to your instance with SSH.


## Part 3 - Building a Web Application using Docker Compose

- Clone the following from given adress: https://github.com/talfik2/devopsproject.git and set directory inside it.
  
```bash
git clone https://github.com/talfik2/devopsproject.git
cd devopsproject
```

- Create a file called `app.py` in your project folder and paste the following python code in it. In this example, the application uses the Flask framework and maintains a hit counter in Redis, and  `redis` (redis bir catch DB. Yani bilgisayar acilip kapanana kadar butun bilgileri hafizasinda tutuyor; 6379 da calisir.)is the hostname of the `Redis container` on the application’s network. We use the default port for Redis, `6379`.
```bash
nano app.py
```

```python
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
import joblib

app = Flask(__name__, template_folder = 'template')#main klasörüm bu
model = joblib.load('model.pkl')
#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')#İlk göreceğimiz şey index.html olsun

@app.route('/predict',methods=['POST', 'GET'])
def predict():
    '''
    For rendering results on HTML
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]

    prediction = model.predict(final_features)

    def final_countdown(prediction):
        if final_features == 0:
            return ("to buy")
        else:
            return ("not to buy")
    deneme1 = final_countdown(prediction)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text = 'For the given values, this customer is more likely  {} the desired product of the bank'.format(deneme1))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
```

- Create a file called `model.py` in your project folder and paste the following python code in it.

```bash
nano model.py
```

```python
# Save Model Using Pickle
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


banking = ".\banking.csv"

dataframe = pd.read_csv(banking)
# y = pd.read_csv(Y)

# Splitting data into train & test sets
X_train, X_test, y_train ,y_test = train_test_split(
    banking.drop(columns = "y"),
    banking["Company"],
    test_size=0.25,
    random_state=42,
    stratify=banking["y"]
)

# Defining stacking estimator

from sklearn.base import BaseEstimator, TransformerMixin, is_classifier
from sklearn.utils import check_array
class StackingEstimator(BaseEstimator, TransformerMixin):

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y=None, **fit_params):

        self.estimator.fit(X, y, **fit_params)
        return self

    def transform(self, X):

        X = check_array(X)
        X_transformed = np.copy(X)
        # add class probabilities as a synthetic feature
        if is_classifier(self.estimator) and hasattr(self.estimator, 'predict_proba'):
            y_pred_proba = self.estimator.predict_proba(X)
            # check all values that should be not infinity or not NAN
            if np.all(np.isfinite(y_pred_proba)):
                X_transformed = np.hstack((y_pred_proba, X))

        # add class prediction as a synthetic feature
        X_transformed = np.hstack((np.reshape(self.estimator.predict(X), (-1, 1)), X_transformed))
        return X_transformed

# Creating our pipeline

from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
st = StackingEstimator(estimator=DecisionTreeClassifier(max_depth=10,
                                                   min_samples_leaf=11,
                                                   min_samples_split=4,
                                                   random_state=42))
gnb = GaussianNB()

pipeline = make_pipeline(st, gnb)

# Fit the model on training set
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)


# save the model to disk with joblib
filename = 'model.pkl'
joblib.dump(pipeline, 'model.pkl')


# some time later...

#load the model from disk with joblib
pipeline = joblib.load('model.pkl')
```


- Create another file called `requirements.txt` in your project folder, add `flask` and `redis` as package list.
 
- TR`requirements.txt` birden fazla `pip install` komutunun birlestirilip dosya formatina donmus halidir.

```bash
echo '
redis
Flask
joblib
numpy
pandas
scikit-learn
sklearn
sklearn-utils

' > requirements.txt
```

- requirements.txt

```bash
echo '
FROM ubuntu
RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
WORKDIR /app
CMD python3 ./app.py
' > Dockerfile
```
### Image Building
- Log in creditentials:
```bash
docker login
```

- Build Docker image from Dockerfile locally, tag it as `<Your_Docker_Hub_Account_Name>/<Your_Image_Name>:<Tag>` and explain steps of building. Note that repo name is the combination of `<Your_Docker_Hub_Account_Name>/<Your_Image_Name>`.

```bash
docker build -t "talfik2/devopsproject" -f ./Dockerfile .
# The -f, --file, option lets you specify the path to an alternative file to use instead.
docker image ls
```
### Running the Image & Binding Volume

- Create a volume named as `projectvolume`

```bash
docker volume create projectvolume
```

- Inspect the `projectvolume`

```bash
docker volume inspect projectvolume
```
- Bind the volume to the container named `welcome` 

- Run the newly built image as container in detached mode, connect host `port 80` to container `port 80`, and name container as `welcome`. Then list running containers and connect to EC2 instance from the browser to show the Flask app is running.
- Bind the `projectvolume` to the container named `welcome` 

```bash
docker run -it --name welcome -p 80:5000 -v projectvolume:/app talfik2/devopsproject
# Check the 80 port
read escape sequence
```
- Create a container derived from(turetilen) `nginx:latest` image and name it as `alcon`

```bash
docker run -it --name alcon -v projectvolume:/alternativemounting nginx bash
```

- Check whether the file(s) we copied exists or not.

```bash
ls
cd alternativemounting
```

### Pushing Image to Docker Hub
- Push newly built image to Docker Hub, and show the updated repo on Docker Hub.

```bash
docker push talfik2/devopsproject
```
### Networking

* Create a bridge network `projectnet`.

```bash
docker network create --driver bridge projectnet
```

- List all networks available  , and explain types of networks.

```bash
docker network ls
```

- Show the details of `projectnet`, and show that there is no container yet.
```bash
docker network inspect projectnet
```

- Run 2 alpine containers with interactive shell, in detached mode, name the containers as techpro1st, techpro2nd and add command to run alpine shell. Here, 1st and 2nd containers should be in techpronet.

```bash
docker run -d -it --network projectnet --name techpro1st alpine sh
docker run -d -it --network projectnet --name techpro2nd alpine sh
```

- Show the details of `projectnet`, and explore newly added containers.

```bash
docker network inspect projectnet
```
- Show the details of default network bridge.

```bash
docker network inspect bridge
```

- Connect to the `techpro1st` container.

```bash
docker attach techpro1st
```

- Ping `techpro2nd `, `welcome` and `alcon` containers by its IP four times to show the connection.

```bash
ping -c 3 <techpro2ndIPv4>
ping -c 3 <welcomeIPv4>
ping -c 3 <alconIPv4> 
# -c yi koymazsak sonsuza kadar calisir
```

- Disconnect from `techpro1st` with `exit`
```bash
exit
```


- Delete `projectnet` network

```bash
docker network rm projectnet
```

- Delete image with `image id` locally.

```bash
docker image rm 497
```
