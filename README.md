Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!


Mengapa *responsive design* menjadi konsep yang penting dalam pengembangan aplikasi *web*? Berikan contoh aplikasi yang sudah dan belum menerapkan *responsive design*, serta jelaskan mengapa!

Responsive design adalah konsep penting dalam pengembangan aplikasi web karena membuat tampilan dan fungsi aplikasi tetap nyaman digunakan di berbagai perangkat dengan ukuran layar berbeda, mulai dari ponsel hingga desktop. Dengan desain yang responsif, pengalaman pengguna menjadi lebih baik, aksesibilitas meningkat, performa lebih efisien, serta mendukung SEO. Contoh situs yang sudah menerapkan responsive design adalah MDN Web Docs atau web.dev, di mana layout dan tipografinya menyesuaikan otomatis dengan ukuran layar. Sebaliknya, situs lama dengan layout fixed-width atau dashboard yang tabelnya tidak menyesuaikan layar merupakan contoh yang belum responsif, sehingga sulit diakses di perangkat mobile.


Jelaskan perbedaan antara *margin*, *border*, dan *padding*, serta cara untuk mengimplementasikan ketiga hal tersebut!

Dalam CSS box model, terdapat tiga elemen penting: margin, border, dan padding. Margin adalah ruang luar elemen untuk memberi jarak dengan elemen lain, border adalah garis tepi yang membungkus elemen, sementara padding adalah ruang dalam antara konten dan border. Kombinasi ketiga aspek ini menentukan jarak dan keterbacaan antar elemen.



Jelaskan konsep *flex box* dan *grid layout* beserta kegunaannya!

Untuk mengatur tata letak modern, terdapat dua teknik utama yaitu flexbox dan grid layout. Flexbox bersifat satu dimensi (baris atau kolom) dan sangat cocok digunakan untuk menyusun item seperti menu navigasi atau kartu yang sejajar. Sebaliknya, grid layout memungkinkan pengaturan dua dimensi (baris dan kolom sekaligus), sehingga lebih ideal untuk membuat struktur layout halaman, seperti header, main content, sidebar, dan footer dalam satu grid terorganisasi. Dengan memanfaatkan responsive design, box model, flexbox, dan grid secara bersama, developer dapat membangun aplikasi web yang adaptif, teratur, dan nyaman di semua perangkat.


Jelaskan bagaimana cara kamu mengimplementasikan *checklist* di atas secara *step-by-step* (bukan hanya sekadar mengikuti tutorial)!





### Sumber Referensi
https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design

https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_box_model
https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Flexbox
https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Grids

https://alistapart.com/article/responsive-web-design/



---









## Apa itu Django `AuthenticationForm`? Jelaskan juga kelebihan dan kekurangannya.
`AuthenticationForm` adalah form bawaan Django yang digunakan untuk proses login user. Form ini otomatis menyediakan field username dan password, serta validasi untuk memastikan user benar-benar ada di database dan password yang dimasukkan valid. Form ini biasanya dipakai bersama dengan view LoginView atau view custom.

Kelebihan yang didapatkan berupa tidak perlu membuat form manual untuk login, sudah dilengkapi validasi autentikasi, terhubung langsung dengan backend Django, dan mudah diimplementasikan di file HTML. Tetapi kekurangannya juga ada seperti sangat susah untuk menambahkan form tambahan (seperti login dengan verifikasi CAPTCHA), tidak mudah dimodifikasi untuk desain User Interface-nya, dan membatasi integrasi login seperti Oauth/JWT tanpa mengubah dari bentuk awalnya.

## Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?
Autentikasi merujuk pada proses menverifikasi identitas user, sedangkan otorisasi berfokus pada proses memastikan hak akses user ke tempat-tempat tertentu (seperti akses admin atau halaman yang butuh izin khusus).

Contohnya: 
Autentikasi dilakukan lewat Django dengan menggunakan `User` model, `AuthenticationForm`, dan view `LoginView`. Lalu Sistem login memakai session + cookies untuk melacak keadaan pengguna. Sedangkan Otorisasi dilakukan lewat Django dengan menggunakan middleware seperti AuthenticationMiddleware untuk menempelkan data pengguna pada `request.user`. 


## Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?
Dalam penyimpanan state aplikasi web, session lebih aman karena datanya disimpan di server dan tidak bisa dimodifikasi langsung oleh user. Session juga fleksibel untuk menyimpan data kompleks. Namun, session membutuhkan penyimpanan di server (database, cache, atau file) dan menambah tantangan skalabilitas, terutama pada sistem dengan banyak server.

Sementara itu, cookies lebih ringan karena disimpan di browser user sehingga tidak membebani server, cocok untuk data kecil seperti preferensi bahasa atau fitur "remember me". Kekurangannya, cookies rentan dimodifikasi, terbatas ukurannya (±4KB), dan berisiko terhadap serangan seperti XSS atau session hijacking jika tidak diamankan dengan benar.


## Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?

Secara default, cookies tidak sepenuhnya aman karena dapat dimodifikasi oleh user, dicegat melalui session hijacking jika tidak terenkripsi, dan terekspos lewat serangan XSS bila properti keamanannya tidak diatur. Untuk mengurangi risiko ini, Django menyediakan beberapa mekanisme bawaan, seperti pengaturan SESSION_COOKIE_HTTPONLY agar cookie tidak bisa diakses JavaScript, SESSION_COOKIE_SECURE dan CSRF_COOKIE_SECURE supaya hanya dikirim melalui HTTPS, serta penggunaan SESSION_ENGINE agar data session disimpan di server, bukan langsung di cookie. Selain itu, middleware seperti CsrfViewMiddleware juga diaktifkan secara default untuk memberikan perlindungan tambahan terhadap serangan CSRF.

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).

Pertama, saya mengikuti langkah yang sudah tersedia di website PBP. saya mencoba untuk menambahkan setiap fungsi pada `views.py` dan membuat file HTML baru di /main/templates.
Jika saya memiliki kesalahan saat menjalankan aplikasinya, saya akan mencoba kembali lagi ke langkah sebelumnya untuk memastikan tidak ada hal yang ditinggalkan.

Saya mencoba melihat error semantik atau logika jika ternyata aplikasi saya tidak berjalan. Lalu saya akan mengecek ulang jika tidak ada lagi yang error.-
