# Use Case for Input Variables

* Birden fazla config file ımız için birden fazla environmentta kullanılmak üzere her bir environment a farklı bir variable file I set etmek üzere daha efektif kullanabiliriz.
* Name i de variable a bağla:
```bash
variable "environment" {
  description = "environment" 
}

Name: var.environment

terraform.tfvars/ environment = "development"

![environments](environments.png)
```

* Güncel kod:

```bash
provider "aws" {
    region = "us-east-1"
}

variable "subnet_cidr_block" {
  description = "subnet cidr block"
}

variable "vpc_cidr_block" {
  description = "vpc cidr block" 
}

variable "environment" { # değişti
  description = "environment"  # değişti
} # değişti

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = var.vpc_cidr_block
    tags = { 
        Name: var.environment # değişti
        vpc_env = "dev" 
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = var.subnet_cidr_block 
    availability_zone = "us-east-1a"
    tags = { 
        Name:"subnet-1-dev"
    } 
}

resource "aws_subnet" "dev-subnet-2"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.20.0/24"
    availability_zone = "us-east-1b"
        tags = { 
        Name:"subnet-2-default" 
    } 
}

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
}

output "dev-subnet-id" {
    value = aws_subnet.dev-subnet-1.id
}
```

# Default Values
* subnet_cidr_block dışındaki bütün variable ları sil. Tabiki resource ların ve terraform-dev.tfvars ın içindeki değerleri de silmeyi unutma.

* Variable ların iki karakteristik özelliği daha var:
    1)	Variable ların içine default değer atayabiliriz.Bunun için de default değer atamak istediğin variable ın içine default = “10.0.10.0/24” yaz.

```bash
variable "subnet_cidr_block" {
  description = "subnet cidr block"
  default = "10.0.10.0/24"
}
```
* Eğer terraform atanan değeri bulamazsa default değeri döndürür. 

* Variable ların türünü de set edebiliriz. Variable türünü de string, number, boolean, list, set, map, object veya tuple olarak set etmek mümkün. Biz örneğimizde string ile devam edelim.  type = string yaz.  Terraform-dev.tfvars ın içindeki değer string olduğu için hatasız çalışması lazım. terraform apply yaz(Çıkan kısma yes yazıyoruz). 

    2)	type = list i ekle:

```bash
variable "subnet_cidr_block" {
  description = "subnet cidr block"
  default = "10.0.31.0/24"
  type = string
}

type = list(string) olarak değiştir
variable "subnet_cidr_block" {
  description = "subnet cidr block"
  default = ["10.0.0.0/17","10.0.31.0/24"] # değişti
  type = list(string)
}
```
* ve terraform-dev.tfvars ın içindeki değeri şu yap: 

```bash
cidr_blocks = ["10.0.0.0/16","10.0.10.0/24"]
```
* Ancak biz sadece list in içindeki ikinci değere ulaşmak istiyoruz. Nasıl yaparız? Şöyle:

```bash
provider "aws" {
    region = "us-east-1"
}

variable "cidr_blocks" { //değişti
  description = "subnet cidr block"
  default = ["10.0.0.0/17","10.0.31.0/24"] # değişti
  type = list(string)
}

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = var. cidr_blocks [0] # değişti
    tags = { 
        Name: "environment" # değişti
        vpc_env = "dev" 
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = var. cidr_blocks 1] # değişti
    availability_zone = "us-east-1a"
    tags = { 
        Name:"subnet-1-dev"
    } 
}

resource "aws_subnet" "dev-subnet-2"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.20.0/24"
    availability_zone = "us-east-1b"
        tags = { 
        Name:"subnet-2-default" 
    } 
}

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
}

output "dev-subnet-id" {
    value = aws_subnet.dev-subnet-1.id
}

```
* Cmd ye terraform apply -var-file terraform-dev.tfvars yaz. AWS Subnets sayfasını yenile. Gördüğünüz gibi değer değişmiş arkadaşlar.

* Terraformda variable olarak object i de kullanabiliriz arkadaşlar. Terraform-dev.tfvars I şu şekilde güncelle:

```bash 
cidr_blocks = [{cidr_block = "10.0.0.0/16", name = "dev-vpc"},
                {cidr_block = "10.0.10.0/24", name = "dev-subnet"}
]
```

* Sonrasında main.tf e gel ve kodu şu şekilde güncelle:

```bash
provider "aws" {
    region = "us-east-1"
}

variable "cidr_blocks" { 
  description = "cidr blocks and name tags for vpc and subnets" # değişti
  default = [{cidr_block:"10.0.0.0/17", name:"default-vpc"}, # değişti
  {cidr_block ="10.0.31.0/24", name: "default-subnet"}] # değişti
  type = list(object({ # değişti
      cidr_block = string # değişti
      name = string # değişti
  }))
}

resource "aws_vpc" "gelistirici-vpc" {
    cidr_block = var.cidr_blocks[0].cidr_block # değişti
    tags = { 
        Name: var.cidr_blocks[0].name # değişti
        vpc_env = "dev" 
    }
}

resource "aws_subnet" "dev-subnet-1"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = var.cidr_blocks[1].cidr_block # değişti
    availability_zone = "us-east-1a"
    tags = { 
        Name:var.cidr_blocks[1].name # değişti
    } 
}

resource "aws_subnet" "dev-subnet-2"{
    vpc_id = aws_vpc.gelistirici-vpc.id
    cidr_block = "10.0.20.0/24"
    availability_zone = "us-east-1b"
        tags = { 
        Name:"subnet-2-default" 
    } 
}

output "dev-vpc-id" {
    value = aws_vpc.gelistirici-vpc.id
}

output "dev-subnet-id" {
    value = aws_subnet.dev-subnet-1.id
}
```
