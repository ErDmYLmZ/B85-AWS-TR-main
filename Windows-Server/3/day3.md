- Windows Server 2012 makinani ac
- Sag ustteki `Tools`tan `Active Directory Users and Computers` i ac.

---------------------------------------------------------------
- Rastgele Bilgi: Simdi mesela kendi bilgisayarindaki administrator ile degil de numarasi `10.98.0.52` olan bilgisayarin administrator'una baglanmak istiyorsun Windows Server ile. Bu noktada

```txt
Kullanici Adi: 10.98.0.52\administrator
Sifre: <10.98.0.52 Admininin Sifresi>
```

- Eger configure etmediysen `Win10` makinenin `Tercih Edilen DNS Sunucusu`nu Windows Server makinenin IP si olarak degistir!! (Win10 Makinedesin > `Denetim Masasi` > `Tum Denetim Masasi Ogeleri` > `Ag Baglantilari` > `Ethernet0` > `Ozellikler` > `Tercih Edilen DNS Sunucusu` > `<Windows Server Makinenin IPsi>`)
- Teyit etmek icin Win10 makinenden devops.com'a ping at:

```win
ping devops.com
```

- Win10 makineye domain'e katma:

- `Bu bilgisayar > Bilgisayar adi, etki alani ve calisma grubu ayarlari > Ayarlari Degistir > Bilgisayar Adi/Etki Alani Degisiklikleri > Etki Alani > devops.com > <Kullanici Adi ve Sifreni Gir>`
---------------------------------------------------------------

## Arka Arkaya Parolayi Yanlis Giren Kullanicinin Hesabini Kitlemeye Dair Group Policy

- `Server Manager > Tools > Group Policy Management > Forest > Domains > devops.com`

- `Default Domain Policy > Sag Klik > Edit > Computer Configuration`

```txt
Preferences: Script gerektirebilecek islemler bunu altinda yapilir. Burada genellikle Policies ve Group Policy'lerle cozemedigimiz isleri hallederiz.

Bazi seyleri hem Policy ile hem de Preferences ile yapabilirsiniz.
    Policy ile yaptiginiz degisiklikler Group Policy yi kaldirdiginizda eski haline geri gelir.
    Preferences ile yaptiginiz degisiklikler Group Policy yi kaldirsaniz dahi Preferences ayarlarini guncellemediginiz taktirde ayni kalir.
```
------------------------------------------------------

### Group Policy Ornegimize Devam Edelim:

- Oncelikle kurban olarak secegimiz kullaniciyi ekleyelim Default Group Policy'ye: `Default Domain Policy'ye Cift Tikla` > `Delegation` > Add > <Admin Adminova>
- `Computer Configuration > Policies > Windows Settings > Security Settings > Account Policies > Account Lockout Policy`

```txt
Account lockout duration: Ne kadar sureli bu hesabi kitleyeyim? 30 dk icin kitle

Account lockout threshold: Kacinci denemeden sonra hesabi kitleyeyim? 3 inci denemeden sonra..

Reset account lockout counter after: Peki ben bu hesabi kac kere kitleyeyim? Yani biz 30 dk boyunca kitle dedik ya, 30 dk da bu 3 kere yanlis girdi parolayi, 30 dk sonra tekrar 3 kere daha yanlis girdi; hesap tekrar kitlendi. Bu senaryoda buraya karsilik gelen deger 2
```

- `cmd > gpupdate /force` ile Group Policy'mizi aktive ettik.
- Istersek `gpresult /r` ile de yapilan degisiklikleri gorebiliriz. 

- Kobay olarak kullanacagimiz kullanicinin hesabina giris yapalim `Win10` dan. Parolayi 3 kere yanlis gir ve hesabin kitlenmesini izle..

- E peki nasil acacagiz hesabi? Soyle: `Windows Server Makineye gel> Active Directory Users and Computers` > `devops.com` > `Kullanicinin kayitli oldugu OU'ya gel` > `Kullaniciya eris` > `Sag Klik` > `Properties` > `Account` > `Unlock account. This account is currently locked out on this Active Directory Domain Controller. i sec` > `OK` 

-----------------------------------------------------

## Parolalarla Ilgili Diger Group Policy'ler Olusturma:

- `Group Policy Management Editor` > `Computer Configuration` > `Security Settings` > `Account Policies` > `Password Policy`

```txt
- Enforce password history: Kullanici Sifre Degistirirken Yeni Sifresi Son <> Parolayla Ayni Olmasin

- Maximum password age: Kullanici Parolasini <> gun sonra degistirebilsin

- Minimum password age: Ne kadar sure gectikten sonra parolasini degistirebilsin?

- Minimum password length: Minimum sifre uzunlugu

- Password must meet complexity requirements: Sifre ne kadar komplike olsun?

- Store passwords using reversible encyription: Parolayi encripted edelim mi?
```
- Kurban kullaniciya sag tikla ve `account` daki `password never expires` tikini kaldir
- Kurban kullanicina gir: CRTL + ALT + DEL: Parolayi degistir de ve yukarida koydugumuz kurallari test et..

-------------------------------------------------------

### System Erisimleri

- **Kullanici CMD ye erisemesin**: `System > Prevent access to the command prompt > disabled` 
    - Burada ayrica mesela kullanicinin calistirmasini istemediginiz programlari da belirtebilirsiniz. Nasil? `Options > Show..` deyip cikan pencereye program ekleyebilirsiniz. (`calc.exe` dersem hesap makinesini calistiramaz mesela)

- **Kullanicinin sadece calistirabilecegi uygulamalari da buradan belirleyebiliriz:** `Systeme cift tikla > Run only specified Windows applications`
- **Kullanici CD & DVD Rom'u Kullanamasin:** `System > Removable Storage Access > CD and DVD: Deny Write Access`
- **USBleri de Engelleyelim:** `System > Removable Storage Access > All Removable Storage classes: Deny all access`

### Network Erisimleri

- **Kullanici IP & TCP sini Degistiremesin:** `Network > Network Connections > Prohibit TCP/IP advanced configuration`
---------------------------------------------------------
- Yukaridaki izinlerin hepsini `Default Domain Policy` den yaptigimiz icin butun kullanicilar icin gecerli oldular. Spesifik policy olusturup onun uzerinden de soyle yapabiliriz:

- `Group Policy Management Editor` > Deneme isimli bir Group Policy Olustur > Denemeye cift tikla > Policy'ye OU ata > `Spain'i sec` > `Sag tikla`> 
    - **Daha onceden Olusturulmus Policy'yi Uygulamak Istersen:** `Link an Existing GPO` > `Deneme'yi Sec`> `User Configuration` > `System` > `Prevent access to the command prompt` > Enabled
    - **Ben Yeni Bir Policy Olusturup Onu Uygulayacagim Dersen"** > `Create a GPO in this domain, and Link it here` > `Isim = CMD_BAN` > Kaydet > `CMD_BAN'a Sag tikla` > Edit > `Polcies` > `Administrative Templates` > `System` > `Prevent access to the command prompt` > Enabled

- Sonrasinda kullanicidan giris yapip(Hem kurban Hem admin) cmd'yi acmayi dene