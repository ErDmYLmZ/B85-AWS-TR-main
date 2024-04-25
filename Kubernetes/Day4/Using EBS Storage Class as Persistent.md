# Using EBS Storage Class as Persistent Volume


PersistentVolume file

ebs-pv.yaml

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: aws-pv
  labels:
    type: aws-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  awsElasticBlockStore:
    volumeID: vol-00f422521aa68a416
    fsType: xfs
```


Persistent Volume Claim file

ebs-pvc.yaml

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: batch85-pv-claim
spec:
  
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  selector:
    matchLabels:
      type: aws-pv
```



