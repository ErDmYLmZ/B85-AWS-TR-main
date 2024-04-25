# Hands-on SNS, SQS
# SQS

- SQS ekranina gel.
- Create Quee

```bash
Type: Standard
Name: my-first-Queue


Configuration
    Visibility Timeout: 30 Second # Ben seni aldigim zaman 30 saniye benimsin, 30 sn boyunca kimseye gorunemezsin
    Message Retention Period: 4 days # mesaji kac gun sureyle muhafaza edeceksin
    Delivery Delay: 0 # Mesaj ne kadar beklesin
    Max Message time: 256 KB
    Receive message wait time: 0 Seconds # Mesaji almak icin x sn bekle, alamazsan diger mesaja gec. 

Access Policy: Default

Dead-letter queue: Disabled # Eksta bekleme suresi
Redrive allow policy: Default # Hangi kaynaklar dead-letter queue yu kullansin

Create
```

- Kuyrugu olusturdum, benim isim buraya kadar. Sonrasi SQS in isi. Ama manuel olarak surecin nasil isledigini gorelim beraber.
- `my-first-queue` ya tikla
```bash
Send and receive messages

Message Body: Bu benim ilk kuyruk mesajim > Send Message
```
- Mesaj suan bekliyor. `Poll For Messages`diyelim ki mesaji ceksin.
- Mesaji cekince mesajin ID sine tiklayarak gorebiliriz. Detaylarini incele mesajin.

- Bir mesaj daha gonder(Bu da benim ikinci mesajim) Yine pull edip ikinci mesaji da gorebilirsin.

## Lambda'dan Function Olustur

- `AWS Lambda`ya gel.

```bash
Create Function

Use a blueprint # Lambdanin kendi olusturdugu taslaklar
    sqs-poller
Configure
    Function name: sqs-poller
    Role name: sqs-role-for-lambda
SQS Trigger # Hangi SQS ten alacak
    my-first-queue
    In oder to read from the SQS trigger, your execution role must have proper permissions # kismi isaretli olsun
# Nodejs fonksiyonu olusturdugumuz mesaji poll edip ilgili log'a yazacak

Create Function
```
- Sonrasinda fonksiyonun `Configuration` bolumune git ve `SQS: my-first-queue` yi `enable` et.(bu biraz surebilir)

- SQS e tekrar gel ve `my-first-queue` den `Send and receive messages` i sec:

```bash
MEssage Body: Bu benim ilk lambda mesajimdir.
Send messages

Poll ettigin mesajlari sil # bunun normali budur.

Yeni mesaji goremiyoruz(messages available 0) cunku lambda mesaji aldi halletti.
```
- E mesaji nasil gorecegiz? `Cloudwatch > Logs > Log Groups> /aws/lambda-sqs-poller` deyip mesajlari gorebiliriz.

# SNS
## Part 1 - Creating Topic, Subscription and Publishing Message

### Step 1 : Create Topic

- Go to `SNS` service on AWS console.

- Click `Topics` >> `Create topic`.

- `Details`.
    - Type: Standart
    - Name: Demo-topic
    - Display Name: My-First-Topic `mesajin epostamiza gelecegi baslik`
- Keep rest default.

- Click `Create`.

### Step 2 : Create Subscription

- On Demo-topic page Click `Create subscription`. Bu topige bagli aboneler kimler olacak??

- `Details`.
    - Topic ARN: arn:aws:sns:us-east-1:046402772087:Demo-topic (comes default)
    - Protocol: Email
    - Endpoint: test@example.com (your mail here)

- Keep rest default.

- Click `Create subscription`.

- Show `Status` >> `Pending Confirmation`.

### Step 3 : Confirm subscription

- Go to your mail and check inbox.

- Open mail from `My-First-Topic`.

- Click `Confirm subscription`.

- Go back to Demo-topic subscription and refresh the page.

- Show `Status` >> `Confirmed`.

### Step 4 : Publish message

- Select `Topics` from the left-hand menu and click on `Demo-topic`.

- Click `Publish message`.

- `Message details`.
    - Subject: sns-test
    - Time to Live (TTL) : -

- `Message body`.
    - Message structure: Identical payload for all delivery protocols.
    - "This is a test message for sns inclass session".

- Keep rest default.

- Click `Publish message`.

- Go to your mail and check inbox.

- Open mail from `My-First-Topic`.

- Show the topic and the test message sent from SNS.

## Part 2 - Creating a CloudWatch Event to Invoke SNS 

### Step 1 : Create Rule

- Go to `CloudWatch` service on AWS console.

- Click `Events` >> `Rules` from the left-hand menu.

- Click `Create Rule`.

- `Event Source`
    - Event Pattern
    - Service Name : EC2
    - Event Type : EC2 Instance State-change Notification

- `Targets` >> Add target
    - SNS topic
    - Topic : Demo-topic
    
- Click `Configure details`.
    - Name:  Instance-State-Change
    - Keep rest default.

- Click `Create Rule`.

### Step 2 : Invoke SNS

- Go to `EC2` service on AWS console.

- Change state of any available instance like starting a stopped one (Launch a new one if you don't have any).

- Go to your mail and check inbox.

- Open mail from `My-First-Topic`.

- Show the topics and the messages sent from SNS.

- Delete/terminate the resources created.
