# ÖN BAKIŞ

- Infrastucture un otome etmek istiyoruz. Uygulamalarımızı calıştırmak çin kullandığımız tüm alt yapının devamlı farklı nedenlerden ötürü, aynı şekilde, hatasız olarak oluşturulması için yazılan bir deklerasyonü, bir script, veya bir kod parçacığına Infrastructure as Code(IAC) diyoruz. Terraform ise bir IAC tool’u. Modül boyunca;

    * Terraform'a giriş
    * Providers
    * Resources & Data Sources
    * Terraform State
    * Output
    * Variables
    * Enviroment Variables
    * Modules
Konularını öğrenecek, ayrıca EC2 Server'ı Oluşturma ve Provision EKS Cluster isimli iki adet projeyi de beraber tamamlayacağız.
 

# TERRAFORM'A GİRİŞ

# Terraform nedir?

* Terraform senin
    - Infastructure ını
    - Platform unu
    - Platformunda çalıştırdığın servisleri(AWS, Jenkins gibi) yönetmene izin verir. 
* 	Açık kaynak kodludur.
* 	“Declaretive” dir. Yani her bir adımı teker teker manuel olarak kodlamazsın da ideal durumu verirsin. Terraform varolan kodu ideal duruma uyarlar.
  
# Terraform’u Ne Zaman Kullanırız?

* Diyelim ki elinde iki adet iş ve bunları gerçekleştirecek iki adet takım var:
    -	Provisioning infostructure(DevOps) ve 
    -	Application Deploying(Developer Takımı).
* Terraform’u Provisioning infrastructure kısmında kullanırsın.

* Daha detaylı ifade etmek gerekirse, Terraform u 
    -	VPC(Amazon Virtual Private Cloud) oluştururken, 
    -	AWS kullanıcısı oluştururken ve kullanıcıyla bağlantılı izinleri yönetirken
    -	Sunucuları spin ederken(Spinning Up the Servers)
    -	ve Docker I yüklerken kullanırız.
* Terraform la ayrıca yukarıdaki görevlerin doğru bir sırada yapıldığına emin oluruz.  

# Ansible ve Terraform’un Arasındaki Fark Nedir?

* Benzerlikler
    -	İkisi de IAC tool’u olarak kullanılır. Yani ikisiyle de altyapıyı sağlarız, yapılandırırırz ve yönetiriz. 

* Farklar

  * Terraform
    -	Genellikle Infrastructure provisioning tool(Altyapı sağlama aracı) olarak kullanılır. 
    -	Görece daha yenidir. 
    -	Orchestration yeteneği daha gelişmiştir. Orchestration, bilgisayar sistemlerinin, uygulamaların ve hizmetlerin otomatik yapılandırması, yönetimi ve koordinasyonudur. IT departmanının karmaşık görevleri ve iş akışlarını daha kolay yönetmesine yardımcı olur.


  * Ansible
    -	Genellikle configuration tool olarak kullanılır. Yani önce infrastructure u oluşturursun. Sonra onu configure etmek için Ansible I kullanırsın. 
    -	Terraforma göre daha eskidir.

* Common Practice de ikisini de aynı anda kullanmamız daha evla. Terraform un kullanım alanlarına geri dönelim. 

* Diyelim ki oluşturulan server hariç 5 farklı server daha oluşturuldu. Bu noktada tabiki bu serverlar için security düzenlemeleri de yapılması gerekir. Bu aşamada varolan infrastructure I yönetmemiz, birşeyler çıkarıp eklememiz gerekiyor. Bunu da Terraform u kullanarak rahat bir şekilde yapabiliriz. 


* Şimdi bu infrastructure ı oluştururken veya süreç boyunca sürekli değiştirirken(ki bu çoğu zaman yapılıyor) bazı adımları tekrar tekrar manuel olarak yapmak insanı ciddi seviyede yoruyor ve zaman kaybetmesine yol açıyor. Bu yüzden süreci automate etmemiz gerekiyor ki terraform’u bu yüzden kullanıyoruz.

* Development aşamasında infrastucture u replicate etmen(kopyalaman) gereken durumlar oluyor. Bu gibi durumlarda bir yandan replicate edilen infrastructure I development aşamasında kullanıp optimize etmeye devam edebilir(staging enviroment’ta), diğer yandan da eski kopyayı bir kenarda saklayabilir, işlerin ters gitmesi durumunda diğer kopyayı kullanmaya devam edebilirsin. Bu noktada terraform senin infrastructure I replicate etmeni kolaylaştırıyor. 

# Terraform Nasıl Çalışır?

* Terraform platform sağlayıcıya nasıl bağlanır? 

* Terraform'un platform sağlayıcıya bağlanması için, kullanması gereken iki ana bileşen’I var: 
    
    1)	Core. Core’da da iki ayrı bileşenimiz var: 
        -  TF-Config(Configuration dosyamız). TF-Config de ne düzenlenir veya oluşturur?”  Sorusunun cevabı verilir yani ideal durum oluşturulur. ve
	
    2) State. “State ise ortaya çıkan durumdur. 

* Terraform ile TF-Config ve State karşılaştırılır ve birbirlerine yakınlaştırılır. Bunun için neleri oluşturmalı, güncellemeli veya ortadan kaldırmalıyız onlar belirlenir.

* Terraform ayrıca Providers’I kullanarak  ve bu kullanımı kolaylaştırarak application setup aşamasının tümünde sana destek olur. 100 den fazla providersı kullanmaya açıktır. Bu providerlardan bazıları AWS- Azure(Provisioning Tool’lar; terraform’un güçlü olduğu alan), Kubernetes- PaaS, Fastly-SaaS dir.

* Terraform çalışırken declarative approach I kullanır. Yani sen config file’ında baştan aşağı tüm adımları tanımlamaktansa sadece end result’u -işler bittiği zaman nasıl görüneceğini-tanımlarsın. Biraz daha açmak gerekirse terraform’la iki server oluştur, firewall I şöyle config et, sonrasında şunu yap vs demezsin de benim ideal durumum-işin olması gereken şekli- 7 serverlı, şöyle ayarlanmış firewall, şu kullanıcılara tanımlanmış şu izinler. İdeal durumumu elde etmen için ne gerekiyorsa yap adersin ve yapılır. Config file ın end result olduğu için end result isimli başka bir file oluşturmana da gerek yok; config file ını aç orda yazar zaten. 

  
Özetle;
-	Terraform is a tool for creating and configuring infrastructure
-	It is an infrastructure as Code tool
-	Use Terraform to integrate all those different technologies.



# KURULUM

* Terraform’u indir(https://www.terraform.io/downloads.html)
* Aws cli ını indir(yoksa)
* main.tf I ve terraform klasörünü burada oluştur. Ayrıca VS Code içi Terraform plug-in ini de yüklemeyi unutma. HashiCorp Terraform isimli başka bir plug in de var ama Terraform plug-in inin arayüzü daha güzel.

 * Cmd ye şunları yaz: 
!! Kendileri de kullanıcı oluşturmuş olabilir. Oluşturmamışlarsa
setx AWS_PROFILE user1 : user1 isimli kullanıcıyı oluşturur.
aws configure --profile "user1": Oluşturulan user1 in bilgilerini girer, region’dur, access key’dir, user key’dir vs. Bunlar zaten AWS accountlarında var. Eser Hocanın attığı csv dosyasında veya .aws teki .config .credentials ta bulabilirsin
Kullanıcı oluşturmuş olanlar & aws hesabı olanlar (.aws/credidentials’I açsınlar) buradan devam edebilirler
aws configure list: varolan kullanıcıları döndürür.

* ŞİMDİ ŞÖYLE: Ben mesela provider ın içine neredeyse hiçbir şey tanımlamayacağım. Terraform böyle olunca napacak; .aws den ilgili bilgiyi otomatik olarak çekecek.. Bu credidentials ı tanımlamanın 3 farklı yolu var:
      * 1) cmd den tanımlarsın
      * 2) main.tf in içindeki providers bloğuna tanımlarsın--ÖNERİLMEZ, GÜVENLİ DEĞİLDİR!!--
      * 3).aws in içindeki credidentials ın içine tanımlarsın. -2. yola göre daha güvenlidir ancak birinci yola göre daha fazla uğraştırır--
  
Note: If you delete your AWS credentials from provider block, Terraform will automatically search for saved API credentials (for example, in ~/.aws/credentials) or IAM instance profile credentials. 
				

# PROVIDERS

* Provider = Python daki “import library” gibi bir şeydir. Spesifik bir teknolojiyle veya platformla nasıl konuşulacağını bilir. Seçilen platformun API ının anlaşılmasından sorumludur.

* Daha Fazla Açıklama: Provider kaynakları oluşturmak ve yönetmekten sorumlu olan bizim durumumuzda "aws" yi adını yapılandırır. Provider, Terraform'un hizmetle API etkileşimlerini çevirmek için kullandığı bir eklentidir. API etkileşimlerini anlamaktan ve kaynakları açığa çıkarmaktan provider sorumludur. Terraform herhangi bir API ile etkileşime girebildiğinden, hemen hemen her altyapı türünü Terraform'da bir kaynak olarak temsil edebilirsiniz. 
  
 * https://registry.terraform.io/browse/providers a git ve providers I keşfet. AWS provider I mesela AWS ile Terraform un iletişimini sağlar. Şimdi AWS çok güçlü bir tool, aynı zamanda cmd de kullanması da oldukça çetrefilli. Bu yüzden AWS kullanımının automate edilmesi gerekiyor. Burada devreye de Terraform giriyor. Visual Studio’nu aç.  


```bash
terraform init: (File/New Window-- Bunu terraform’u yüklediğin directory’yi set ettikten ve main.tf i oluşturduktan sonra yap)
```

 
```bash
provider "aws" {
    region = "us-east-1"   
}
```

 * Yukarıda tanımladık, aynı zamanda bunu cmd de yüklememiz de gerekir: terraform init
		
 * Visual Studio yu aç 

 * Sonrasında bir gizli dosya bulacak(terraform.lock.hcl), onunla hangi
  providersların yüklü olduğu falan yazar. 
  Provider “aws” ile(.terraform un içinde) AWS teki herşeye erişebiliriz..

# RESOURCES

* "Resource" , bir altyapı parçasını tanımlar. "Resource",
 EC2 Instance gibi fiziksel bir bileşen olabilir.
* resource kütüphaneden fonksiyon tanımalamak gibidir. 

* Resource EC2 için gerekli iki veriye sahip olmalıdır:
  "resource type" ve the "resource name". Mesela, resource type
   "aws_vpc" ve local name "gelistirici-vpc" olsun. Instance önceki sağlayıcıya eşlenir.
   Bizim durumumuzda "aws_vpc", Terraform'a otomatik olarak "aws"
   sağlayıcısı tarafından yönetildiğini söyler.

* Resource a ilişkin argümanlar resource block'un içindedir.
 Argümanlar, makine boyutları, disk görüntüsü adları veya VPC kimlikleri 
 gibi şeyler olabilir. EC2 bulut sunucunuz için 'Amazon Linux 2' için 
 bir AMI belirledik ve bulut sunucusu tipi 't2.micro' olacak.

```bash

   resource "aws_vpc" "gelistirici-vpc" {

    # "aws_pc" is the resource name that I want to reach.
    # Bunu da terraform un aws ile ilgili documentation’ununda bulabiliriz.
    #( https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc)
    # Linkteki argument reference kısmında ekleyebileceğin diğer şeyler de var aklında bulunsun.
    # “gelistirici-vpc” : değişken adı bu istediğimiz ismi verebiliyoruz

    # Buranın altına parametre tanımlarız. Vpc içi mesela;
        cidr_block = "10.0.0.0/16" # Private IP adress aralığı	 
    } 
```

* Bir resource daha oluşturalım; 

```bash

  resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id # Yukarıdaki resource a da refer edelim
    # Ne zaman bir subnet oluşturacak olsak vpc sini de set
    # etmeliyiz çünkü subnet vpc nin dışında oluşturulamaz.

    cidr_block = "10.0.10.0/24"
     # Bu bir subnet olduğu için üstte tanımladığımız vpc nin alt kümesi olmalı
  
    availability_zone = "us-east-1a" 
    #dikkat ettiyseniz bu user ımızı oluşturduğumuz regionla aynı ve aynı olması gerekiyor da zaten.
 }
```

* Basically this is how you can create a resource that depends on the other
 resources that we haven’t created yet. 
* Kodun son hali:

```bash
   provider "aws" {
       region = "us-east-1"
   }

   resource "aws_vpc" "gelistirici-vpc" {
       cidr_block = "10.0.0.0/16"
   }

   resource "aws_subnet" "dev-subnet-1"{
       vpc_id = aws_vpc.gelistirici-vpc.id
       cidr_block = "10.0.10.0/24"
       availability_zone = "us-east-1a"
   }
```
   
# Terraform apply

* Resource ları tanımladık, şimdi de Terraform’u kullanarak resource’ları
 nasıl uygulayacağımızdan bahsedelim; Aşağıda yer alan koddaki komutları
  oluşturarak yeni bir VPC tanımlayacağız yani. Bunun için de apply 
  isimli bir Terraform komutunu kullanıyoruz. 
* Peki terraform apply ı çalıştırdığımız zaman ne olur?
      * Terraform source'dan verileri terraform.tfstate adlı bir dosyaya getirir
      Böylece resource'un meta verilerini takip etmiş olur.
* cmd ye dön ve directory’nin teraform.exe in olduğu directory olduğundan emin ol.
* cmd’ye terraform apply komutunu yaz. 
  
* Terraform Apply'ın Çıktısını Değerlendirelim

* öncelikle elimizde "dev-subnet-1" var.  İçinde de 3 adet parametremiz bulunmakta.
 Bazılarını kendimiz set ettik; "cdr_block" veya "avaliability_zone" gibi.
  Bazıları default değerler(false olanlar) Geri kalanı bilinmeyen değerler. 
   Bilinmeyen değerleri de resource u create ettikten sonra oluşturacağız. 

* İkinci resource da “gelistirici-vpc”. Bunda da bazılarını manuel set ettik,
 bazıları default geldi. Bazıları da resource create edildikten sonra oluşturulacak. 
 Burada da “Plan” kısmı yukarıda yaptıklarımızın özeti aslında. 

* Yes e basıp yaptıklarımızı onayladık
 ve kod çalıştıktan sonra şu sayfayı
 (us-east-1.console.aws.amazon.com/vpc/home?=us-east-3#vpcs: / AWS/ Arama Sekmesi / VPC) 
 açıp yeni bir vpc oluşturup oluşturmadığımıza bakıyoruz.

* Gördüğünüz üzere bu oluşturduğumuz vpc(default olup IPv4 CIDR i 10.0.0.0/16 olan).
  Bu VPC ID yi kopyalayıp Subnets sekmesindeki arama bloğuna yapıştırırsak(yanında kalıyor sayfanın)
  resource ların içine tanımladığımız subnetleri de görebiliriz. 


# Döngüler

#  Count and count.index

*  `variables.tf` isimli bir dosya oluştur. İçine de şunları tanımla:

```bash
variable "num_of_buckets" {
  default = 2 # bu i = 2 demek yani 2 kere döndür..
}

variable "s3-bucket-name" {
  default = "oliver-s3-bucket-variable-rararraa"
}
```

*  `main.tf` dosyasına git ve aşağıdaki gibi değiştir

```bash
resource "aws_s3_bucket" "tf-s3" {
  bucket = "${var.s3-bucket-name}-${count.index}"
  acl    = "private" # acl = Access Control List. acl = "private" yani Owner gets FULL_CONTROL. No one else has access rights (default).
  count = var.num_of_buckets
}
```

```bash
terraform plan
```

```bash
terraform apply
```

- AWS console dan S3 buckets'ı kontrol et.


# Loop ları kullanarak Kullanıcı Oluşturma
* Sonuçları şuradan kontrol edebilirsin:  https://s3.console.aws.amazon.com/s3/home?region=eu-central-1


* Varsayılan olarak, bir kaynak bloğu bir gerçek altyapı nesnesini yapılandırır
 (ve benzer şekilde, bir modül bloğu bir alt modülün içeriğini yapılandırmaya bir
  kez dahil eder). Ancak bazen, her biri için ayrı bir blok yazmadan birkaç benzer nesneyi
   (sabit bir bilgi işlem örneği havuzu gibi) yönetmek istersiniz.
    Terraform'un bunu yapmanın iki yolu vardır: count ve for_each.

- `variables.tf` e git ve yeni bir variable ekle.

```bash
variable "users" {
  default = ["yasa", "varol", "harbiye"]
}
```

- `main.tf` e git. IAM role u aşağıdaki gibi değiştir ve IAMFullAccess policy'yi ekle.

```bash
resource "aws_s3_bucket" "tf-s3" {
  # bucket = "var.s3-bucket-name.${count.index}"
  acl = "private"
  # count = var.num_of_buckets
  # count = var.num_of_buckets != 0 ? var.num_of_buckets : 1
  for_each = toset(var.users)
  bucket   = "example-s3-bucket-${each.value}"
}

resource "aws_iam_user" "new_users" {
  for_each = toset(var.users)
  name = each.value
}

output "uppercase_users" {
  value = [for user in var.users : upper(user) if length(user) > 6]
}
```
*  terraform plan ve terraform apply --auto-approve yaz.
*  Sonuçları şuradan kontrol edebilirsin: https://console.aws.amazon.com/iamv2/home?#/users
  

# DATA SOURCES

* Varolan br VPC ye subnet’I nasıl oluşturabiliriz peki? Bu noktada varolan VPC nin
 id sine ihtiyacımız olacak. VPC nin ID sine de aws/ source / dan erişebiliriz ama bu
  efektif olmaz. Alternatif olarak provider ın içinden VPC ID sini çekebiliriz. 
   Bunun için de “data” provider’ını kullanmamız gerekiyor. 

* Data : varolan resource da işlem yapmamızı sağlar
* Resource: yeni bir resource oluşturup onda işlem yapmamızı sağlar
* Data'ya kütüphaneden fonksiyon çağırmakta diyebiliriz.

* Terraform’dan aws_vpc yi seçelim(arama tuşuna aws_vpc yazarak)
( https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc)

```bash
data "aws_vpc" "existing_vpc" {
    default = development
}
data “aws_vpc” “existing_vpc” { # existing_vpc bizim verdiğimiz isim
default = true  # aradığımız şeyi filtre edelim. Filtre için default keyword’ünü kullanıyoruz.
# data mızın içine bir de subnet oluşturalım.
resource "aws_subnet" "dev-subnet-2"{
    vpc_id = data.aws_vpc.existing_vpc.id # Burada data ya reference verdik.
    cidr_block = "172.31.48.0/20" # En son VPC nin subnet ini alıp ufak bir değişiklik yaptık.
    availability_zone = "us-east-1b"
}

```

* cmd ye terraform apply komutunu yaz ve çalıştır.

* AWS Subnets sayfasını geri aç. Gördüğünüz gibi yeni bir vpc miz var. 

* Recap

  * provider = kütüphane import etmek gibi bir şey
  * resource/data = kütüphaneden fonksiyon çağırmak
  * arguments = fonksiyonun parametreleri


* Kodun son hali:
  
```bash
provider "aws" {
    region = "us-east-1"
}

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.10.0/24"
    availability_zone = "us-east-1a"
}

data "aws_vpc" "existing_vpc" {
    default = true
}

resource "aws_subnet" "dev-subnet-2"{
    vpc_id = data.aws_vpc.existing_vpc.id
    cidr_block = "172.31.48.0/20"
    availability_zone = "us-east-1b"
}
```


# Changing Resources

* Şimdi de configuration umuzda birkaç değişiklik yapalım. Yukarıda oluşturduğumuz 
resourcelarımıza henüz isim vermedik; hadi verelim. Bunu da 

```bash
        Tags = {
            Name:”ismi burada veriyoruz”
        # Tags key-value pairleriyle çalışır. Tıpkı Python’daki dict ler gibi…
        # !! Tags’I yeni bir resource olarak değil de varolan resourches ın içine tanımlıyoruz.
            vpc_env = “dev”
        }
}
resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = "10.0.0.0/16"
    tags = { # Değişen yer
        Name:"development" # Değişen yer
        vpc_env = "dev" # Değişen yer
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.10.0/24"
    availability_zone = "us-east-1a"
    tags = { # Değişen yer
        Name:"subnet-1-dev" # Değişen yer
    } # Değişen yer
}

# Burada kronik bir sorun olabilir. Hata alırsan data kısmını comment out yap..
data "aws_vpc" "existing_vpc" {
    default = true
}

resource "aws_subnet" "dev-subnet-2"{
    # vpc_id = aws_vpc.gelistirici-vpc.id # Hata durumunda ikinci opsiyon
    vpc_id = data.aws_vpc.existing_vpc.id
    cidr_block = "172.31.48.0/20"
    availability_zone = "us-east-1a"
    tags = { # Değişen yer
        Name:"subnet-2-default" # Değişen yer
    } # Değişen yer
}
```

* Kaydet ve cmd’ye gel; şunu yaz: terraform apply --auto-approve.
  
* Orada şu simgeyi göreceksin: ~ Bu simge bir şeyleri değiştirdiğimizin göstergesi

* Sonrasında AWS sayfasındaki Your VPCs kısmına gel ve sayfayı yenile. 
Developments’a tıklayıp tags e bastıktan sonra  diğer değişiklikleri de
 görebilirsin. Gördüğünüz gibi isimler değişmiş…

  

# Removing / Destroying Resources

* Bütün resource u ortadan kaldırmak istersek ne yapmalıyız? Bunu iki şekilde yaparız.
    
    1)	İlgili Terraform dosyasından silerek. Sil ve cmd ye terraform apply--auto-approve yaz, sonra çalıştır. 

    2)	Cmd’ye terraform destroy  yazarak. Sonrasında AWS deki Subnets sayfasını yenilemeyi unutma.
	
  * İlk yöntemle gitmek-özellikle takım olarak çalışıyorsan daha mantıklı diyenler var; ama size kalmış tabi.


# Terraform Komutlar

* Zaten kullandık bu komutları ama bi tekrar edelim..
  
* Diyelim ki elinde bir configuration file var(bizim durumumuzda main.tf) ve
 current state & desired state arasındaki farka bakmak istiyorsun. Bunun için 
 cmd de terraform plan komutunu çalıştırabilirsin. Bu komut bir ön gösterim
  gibi aslında. terraform apply komutunun verdiği şeyi veriyor sana ama real time
  server da apply etmeden yapıyor bunu.

* Elindeki komutu confirm etmeden direk uygulamak istiyorsun; use terraform apply -auto-approve
* Elindeki infrastructure tamamen yok etmek istiyorsun => terraform destroy
  

# TERRAFORM STATE
* terraform apply I her uyguladığımızda terraform current state I tutar ve güncellenmiş
 bir şey var mı yok mu diye kontrol eder. Peki Terrafrom her seferinde main.tf in içindeki
  resource ların current state ini nasıl anlıyor?
   
    * Directory mizin içinde main.tf in yanında terraform.tfstate ve 
    terraform.tfstate.backup isimli iki adet dosyamız daha var.
   
    * terraform.tfstate bir JSON dosyası. Bu dosyada terraform infrastructure undaki
     resource ların anlık durumunu saklar. Bu noktada  terraform aws e gider ve 
     oluşturduğun/güncellediğin/yok ettiğin şeyleri iletir. Bunları da terraform.tfstate in
      içinde saklar. Ne zaman bir güncelleme yapsak terraform.tfstate de otomatik olarak kendini günceller. 
	
    * Terraform.tfstate.backup da previous state dir yani resource ların güncellemeden önceki hali.
     Önceki halleri backup olarak kaydeder ki herhangi bir aksilikte yeniden yükleyelim. 
	
    * Unutmayalım ki main.tf de bizim desired state imiz. 

* Cmd ye terraform apply -auto-approve yaz ve çalıştır.
  
* terraform.tfstate e geri gel. Gördüğünüz gibi boş olan [] ın içi dolmuş. Bu noktada elimizde
 çok fazla kod var. Hepsinin arasından istediğimizi bulmak zor olabilir. 
 Bunu kolaylaştırmak için de bazı terraform subcommandlarını kullanıyoruz. 
	
    * Cmd ye terraform state yaz. Subcommand larımızı burada görebiliriz. Bütün subcommand ları deneyelim.
  

*  ! Bundan önceki videoya göre hiçbir şey değişmediği için güncellenmiş kodu burada paylaşmıyorum.


# OUTPUT

* Output Values fonksiyonlardaki return parametresine benzer.Seçilen değerleri konsolda 
çıktı olarak döndürür. Mesela örneğimizde output değeri olarak oluşturduğumuz resource lara id verdirelim.

* Önce elde olan resource’ları şu şekilde ortadan kaldıralım: terraform destroy

```bash

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
    # Not: Birden fazla value değerin olamaz
    # Her attribute için yalnızca tek bir output değerin olmalı
    # Bir output’un içine birden fazla value ekleyebilirsin.
}

output "dev-subnet-id" {
    # Diğelim ki oluşturduğumuz bütün resource ların değerlerini çıktı olarak istiyoruz.
    value = aws_subnet.dev-subnet-1.id
}
```

* Cmd’ye terraform apply -auto-approve yaz. Vaay, gördün mü? Subnet ve vpc id leri konsola yazdırdı.
  
* Kodun son hali:

```bash
provider "aws" {
    region = "us-east-1"
}

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = "10.0.0.0/16"
    tags = { 
        Name:"development" 
        vpc_env = "dev" 
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.10.0/24"
    availability_zone = "us-east-1a"
    tags = { 
        Name:"subnet-1-dev"
    } 
}


resource "aws_subnet" "dev-subnet-2"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block =  "172.31.48.0/20"#"10.0.20.0/24"
    availability_zone = "us-east-1b"
        tags = { 
        Name:"subnet-2-default" 
    } 
}

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
    # Birden fazla value değerin olamaz
}

output "dev-subnet-id" {
    # Diğelim ki oluşturduğumuz bütün resource ların değerlerini çıktı olarak istiyoruz.
    value = aws_subnet.dev-subnet-1.id
}
```


# VARIABLES

* Input variable ları fonksiyonlardaki arguments gibidir. Farklı environmentlarda(development and production)
 kullanmak için de oldukça uygunlar. Biz örneğimizde cidr_block’un subnet I için variable kullanacağız. 
* provider’ın altına 

```bash
variable "subnet_cidr_block" {
  description = "subnet cidr block"
}
.
.
.
resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = var.subnet_cidr_block # harcode yapalım dersek: "10.0.10.0/24"
    availability_zone = "us-east-1a"
    tags = { 
        Name:"subnet-1-dev"
    } 
}
```

 * Şu ana kadar variable ımızı tanımladık, cidr_block a bağladık ama variable’Imıza bir
  değer atamadık. Variable a değer atamanın 3 farklı yolu var: 
    1)  cmd de karşınıza çıkan pencere. Cmd ye terraform apply yazınca 
    Enter a value: diyor ya o. Şunu yazardın: 10.0.33.0/24 Sonrasında Enter a value: yes de .
     Bu efektif bir yol değil. Testing purposes için bu yolu kullanabilirsin ancak uzun vadede 
     yazdığın kodun otomasyonu için değişiklikleri cmd prompt tan yaptığın için bu yolu önermiyorum.
   
    2)	Cmd ye terraform apply -var “subnet_cidr_block=10.0.30/24”  yaz.  Enter a value: yes de . 

    3)	Aralarındaki en efektif yol bu. Variable ları içeren “terraform.tfvars” I directorynin
     içine oluştur. Bu dosyanın içine key-value pairs I tanımlayabiliriz. 
     İlk satıra subnet_cdr_block = "10.0.40.0/24" yaz. Sonrasında cmd ye terraform apply yaz.
      Terraform yazdığın variable I terraform.tfvars tan bulup oluşturacak.
      Enter a value: yes de . Sonrasında AWS subnets dev-subnet-1 in cdr blockunda atadığın değeri görebilirsin
    subnet_cidr_block = "10.0.10.0/24"
    vpc_cidr_block = "10.0.0.0/16"

* Kodların güncel hali

```bash
provider "aws" {
    region = "us-east-1"
}

variable "subnet_cidr_block" { # değişti
  description = "subnet cidr block" # değişti
} # değişti

variable "vpc_cidr_block" { # değişti
  description = "vpc cidr block" # değişti
} # değişti

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = var.vpc_cidr_block # "10.0.0.0/16"//değişti
    tags = { 
        Name:"development" 
        vpc_env = "dev" 
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = var.subnet_cidr_block # değişti
    availability_zone = "us-east-1a"
    tags = { 
        Name:"subnet-1-dev"
    } 
}

resource "aws_subnet" "dev-subnet-2"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "172.31.48.0/20"
    availability_zone = "us-east-1b"
        tags = { 
        Name:"subnet-2-default" 
    } 
}

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
    # Birden fazla value değerin olamaz
}

output "dev-subnet-id" {
    # Diğelim ki oluşturduğumuz bütün resource ların değerlerini çıktı olarak istiyoruz.
    value = aws_subnet.dev-subnet-1.id
}
```
