# WebServer Without CloudFormation

- Hands-on'umuzun ilk bolumunde `CloudFormation` kullanmadan yayin yapan bir websitesi ayaga kaldiracagiz.
- Makina ayaga kaldirirkenki aciklamalar:

```txt
1. Default olan VPC Public; guvenli degil.
    DB barindiracaksa VPC ni Custom secmeli ve Private olarak configure etmelisin.

2. IAM Role: Makinaya rol atamak istersen burada kullanacagin rolu secmen gerekir. Burada rol secimi git sunu yap seklinde degil git sunu yapabil seklinde olur. Mesela: Bu makina gidip S3 bucket'tan veri cekebilsin gibi..
```

Makinamiz icin `User data`: Designer websitesi icin:


```bash
#! /bin/bash
yum update -y
yum install -y httpd
yum install git -y
systemctl start httpd
systemctl enable httpd
git clone https://github.com/techproedu/designer.git
cd /designer
chmod -R 777 /var/www/html
cp -R . /var/www/html
```
- `httpd`: Apache Server demek
- `systemctl enable httpd` makinayi her acip kapattigimiz zaman tekrar tekrar `systemctl start httpd` yazmamizi engeller.
- `cd /designer`: cd designer'a girdik
- `chmod -R 777 /var/www/html`: designerdaki dosyalari html'e kopyalabilmek icin bu komutu kullandik; izin duzenlemesi yaptik yani. `-R` Recursive demek.
- `cp -R . /var/www/html`: designer'daki dosyalari html'e kopyaladik
```txt
Tags: 
   Name: WebServerManual
```

```txt
Security Group: Name: web-server-SG / Description: web-server-SG
  TCP Anywhere
  HTTP Anywhere
```

- Public IP sine gir ve web sitesini gor
- Makinana baglan
- `cd /designer` deyip designer klasorunu kesfedebilirsin.
- Sonrasinda makineye terminate et.

- **NOT!**: `yml` da `|` baska satirlarda birden fazla veri girisi yapilirken kullanilir. `""` da ayni satirda birden fazla veri girisi yapilirken kullanilir. `>` yorumlar & paragraflar icin kullanilir.

-------------------------------------------------------------
- Slaytlara giris zamani
- `classnotes.txt` deki uzantilari VSCOde'a kur.
# WebServer With CloudFormation

bosluga `cfn` yaz ve sonrasinda altta beliren ilk secenege(`cfn`) tikla; soyle bir ciktin olacak:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: |
  
Parameters:
  
Metadata:
  
Mappings:
  
Conditions:
  
Resources:
  
Transform:
  
Outputs:
```

- Ciktidaki `Parameters` kisminin altina(tab'li) `parameter-type-keypair-keyname` yaz ve enter'a bas(gelen secenege git yani).
- Ciktin suna evrilecek:

```yaml
AWSTemplateFormatVersion: 2010-09-09
Description: |

Parameters:
  KeyPairName:
    Description: 
    Type: AWS::EC2::KeyPair::KeyName
    Default: 
  
Metadata:
  
Mappings:
  
Conditions:
  
Resources:
  
Transform:
  
Outputs:
```

- Aciklama:
```yaml
Parameters:
  KeyPairName: # Hangi tur key'i kullanmak istiyorsun??
    Description: 
    Type: AWS::EC2::KeyPair::KeyName # bu tur..
    Default:
```

- Directory'ne `ec2-website-installation-template.yml` isimli bir yaml dosyasi olustur ve asagidaki yaml kodunu dosyaya yapistir:

```yaml
AWSTemplateFormatVersion: 2010-09-09

Description: >
  This Cloudformation Template creates Web Server on EC2 Instance. 
  This will run on Amazon Linux 2 (ami-026dea5602e368e96) EC2 Instance with
  custom security group allowing SSH connections from anywhere on port 22.
Parameters:
  KeyPairName:
    Description: Enter the name of your Key Pair for SSH connections.
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: Must one of the existing EC2 KeyPair

Resources:
  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH for WebServer
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
  WebServer:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-09d95fab7fff3776c
      InstanceType: t2.micro
      KeyName: !Ref KeyPairName
      SecurityGroupIds:
        - !GetAtt WebServerSecurityGroup.GroupId
      Tags:                
        -                        
          Key: Name
          Value: !Sub WebServer of ${AWS::StackName}   
      UserData:
        Fn::Base64: |
          #! /bin/bash
          yum update -y
          yum install -y httpd
          yum install git -y
          systemctl start httpd
          systemctl enable httpd
          git clone https://github.com/techproedu/designer.git
          cd /designer
          chmod -R 777 /var/www/html
          cp -R . /var/www/html
          systemctl restart httpd
         
Outputs:
  WebsiteURL:
    Description: WebServer DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt WebServer.PublicDnsName
```

- Sonrasinda `CloudFormation > Create Stack > Template is ready > Upload a template file` deyip yaml dosyasini upload et.
- Bakin gordugunuz gibi direk S3 Bucket'ta ilgili template'i olusturdu.(`S3 URL`)
- Sonrasinda `view in designer` deyip gorsel olarak template'i degerlendir. Hata olsaydi burada gorurduk!

```txt
Specify stack details
  Stack name: webserver-with-cloudformation
  Parameters: <key-pairiniz>
```
- Sonrasinda `create stack` deyip stack'i olustur.

- Gordugun gibi stack gitmis static webdesign'i hostlayan EC2 cihazi ayaga kaldirmis; bu cihazin Public IP'sinden de websitesine erisebilirsin..

- Sonrasinda cihazi ve cloudformation stack'ini sil.

- Yukaridaki template'in aciklamasi:


```yaml
AWSTemplateFormatVersion: 2010-09-09
# Description kismi aslinda aciklama, istediginiz seyi yazabilirsiniz aciklayici olmasi kosuluyla
Description: >
  This Cloudformation Template creates Web Server on EC2 Instance. 
  This will run on Amazon Linux 2 (ami-026dea5602e368e96) EC2 Instance with
  custom security group allowing SSH connections from anywhere on port 22.
Parameters:
  KeyPairName: # Parametremiz key-pair ile ilgili. Yani burada ne diyoruz giris sartimiz key-pair
    Description: Enter the name of your Key Pair for SSH connections.
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: Must one of the existing EC2 KeyPair

Resources: # Zorunlu burasi, bunun disindaki hicbir sey zorunlu degil.
  WebServerSecurityGroup: # Security Group olusturalim, 80 ve 22 portlarini acalim
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH for WebServer
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
  WebServer: # Instance'i burada olusturuyoruz. 
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-09d95fab7fff3776c # bu imajdan turetelim instance'i
      InstanceType: t2.micro # t2.micro olsun instance'imiz
      KeyName: !Ref KeyPairName
      SecurityGroupIds:
        - !GetAtt WebServerSecurityGroup.GroupId
      Tags:                
        -                        
          Key: Name
          Value: !Sub WebServer of ${AWS::StackName}   
      UserData:
        Fn::Base64: |
          #! /bin/bash
          yum update -y
          yum install -y httpd
          yum install git -y
          systemctl start httpd
          systemctl enable httpd
          git clone https://github.com/techproedu/designer.git
          cd /designer
          chmod -R 777 /var/www/html
          cp -R . /var/www/html
          systemctl restart httpd
# Yukaridaki kisim tahmin edilecegi uzere instance'imizin user data'si         
Outputs: # Cikti olarak'ta user data'da instance'in icerisine kurdugumuz web sitesi yayin yapsin dedik asagida
  WebsiteURL:
    Description: WebServer DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt WebServer.PublicDnsName
```

- CloudFormation'dan Stack'lara gel: `CloudFormation > Stacks > Create Stack > Specify Template > Use a Sample Template`

```txt
Multi_AZ_Simple: Birden fazla Availability Zone'da olustulurmus ornek CloudFormation template'leri
    AZ'nin birine girdi kullanici, hata alinca direk diger AZ deki replikasina yonlendiriyor.
LAMP Stack: Icerisinde Linux Kernel'i, DB ve Python yuklu olan ornek template'ler
WordPress Blog: Icerisinde WordPress yuklu olan ornek template'ler 
```

- `Use a Sample TEmplate >  Simple > WordPress blog` deyince yine template'i direk `S3 URL` de goreceginiz uzere S3 Bucket'ta sakladi.
- `View in Designer` dersek 2 tane sey karsimiza cikacak: `Web Server` ve `Security Group`. DB vs de hepsi muhtemelen `Web Server`'da kurulu. View in Designer genelde ornek kodu ve **varsa hatayi** gormek icin kullaniliyor.
- `View in Designer` kismindan ornek Wordpresss template'inin `JSON` formatini alalim ve directory'mize olustiracagimiz `cfn-example.json` un icerisine yapistiralim.
- Sonrasinda `cfn-example.json` a sag tiklayip `Convert to YAML` secenegini secip `JSON` formatindaki kodu `YAML` formatina donusturebiliriz.
- AWS Consoluna geri gelip next diyelim, DB Username, passport ve key-pair'i secelim. Sonraki sayfada `Stack Failure Options = Roll back all stack resources` diyelim ki hata aliesak nereden aldigimizi gorup duzeltelim. Sonrasinda Stack'i ve stack'e bagli olusturulmus ec2makinesini gozlemleyebiliriz. Public IP'sini de tarayiciya kopyalarsak yayin yapan websitesiyle karsilasmamiz mumkun.

- Olusturdugumuz stack'leri silelim.