

## Tugas 6:

# 1. Apa perbedaan antara **synchronous request** dan **asynchronous request**?

Synchronous request adalah pola komunikasi antara client dan server di mana browser harus menunggu response dari server sebelum bisa melanjutkan proses lain. Ketika sebuah request synchronous dilakukan, halaman akan "freeze" atau berhenti interaktif sampai server mengembalikan responnya, biasanya berupa reload penuh dari seluruh halaman. Sebaliknya, asynchronous request memungkinkan data dikirim ke server dan diproses di latar belakang tanpa menghentikan aktivitas pengguna di halaman. Dengan asynchronous request (misalnya AJAX), hanya bagian tertentu dari halaman yang diperbarui, sementara pengguna tetap bisa berinteraksi dengan halaman web. Dengan kata lain, synchronous lebih sederhana tapi membuat user experience lambat, sedangkan asynchronous lebih dinamis dan cepat.

---

# 2. Bagaimana **AJAX bekerja di Django** (alur request–response)?

Dalam Django, AJAX berjalan dengan menggunakan JavaScript di sisi client untuk mengirim permintaan HTTP (umumnya dengan fetch atau XMLHttpRequest) ke server. Alurnya dimulai ketika sebuah event di client (misalnya klik tombol atau submit form) memicu AJAX request. Request tersebut diarahkan ke URL atau endpoint Django tertentu yang di-handle oleh sebuah view. View Django kemudian memproses request tersebut, misalnya melakukan query database atau logika bisnis tertentu, lalu biasanya mengembalikan data dalam format JSON. Response JSON tersebut diterima kembali oleh JavaScript di client, dan hasilnya dipakai untuk memperbarui tampilan halaman secara selektif, tanpa reload penuh. Dengan alur ini, Django tetap menjalankan logika backend seperti biasa, hanya saja pengembalian datanya lebih ringan (JSON, bukan HTML lengkap).

---

# 3. Apa keuntungan menggunakan **AJAX** dibandingkan render biasa di Django?

Penggunaan AJAX dalam Django memiliki beberapa keunggulan dibanding render biasa. Pertama, dari sisi performa, AJAX lebih efisien karena hanya mengirim dan menerima data yang dibutuhkan, sehingga response lebih cepat dan hemat bandwidth. Kedua, dari sisi UX, AJAX membuat website terasa lebih responsif: bagian tertentu dari halaman bisa segera berubah tanpa reload penuh. Hal ini mendukung interaktivitas yang lebih baik, misalnya saat pengguna ingin melihat daftar komentar baru, notifikasi real-time, atau pencarian instan. Ketiga, AJAX mendukung pengembangan fitur modern seperti infinite scroll atau form validation langsung, yang sulit dicapai dengan full page reload. Dengan demikian, AJAX membuat aplikasi Django terasa lebih cepat, ringan, dan lebih dekat dengan standar aplikasi web modern. 

---

# 4. Bagaimana cara memastikan **keamanan** saat menggunakan AJAX untuk fitur **Login dan Register** di Django?

Meski AJAX meningkatkan interaktivitas, penggunaan untuk fitur sensitif seperti login dan register harus tetap memperhatikan keamanan. Beberapa cara yang bisa dilakukan antara lain: pertama, gunakan CSRF token, karena Django memiliki mekanisme bawaan yang wajib disertakan dalam setiap request POST agar tidak rentan terhadap serangan Cross-Site Request Forgery. Kedua, gunakan HTTPS untuk mengenkripsi data sensitif seperti username dan password, sehingga tidak mudah disadap. Ketiga, lakukan validasi input di server, karena validasi di sisi client bisa dilewati. Django sudah menyediakan forms dan authentication system yang dapat dipakai untuk validasi dan keamanan password secara aman (hashing). Keempat, batasi metode request hanya untuk POST saat login atau register, jangan izinkan GET. Dengan langkah-langkah ini, keamanan tetap terjaga meskipun komunikasi dilakukan secara asynchronous dengan AJAX.

---

## 5. Bagaimana AJAX mempengaruhi **pengalaman pengguna (UX)** pada website?

AJAX memiliki pengaruh sangat besar pada pengalaman pengguna sebuah website. Dengan AJAX, halaman web terasa lebih cepat dan interaktif, karena pengguna tidak perlu menunggu reload penuh hanya untuk melihat perubahan kecil. Misalnya, pada aplikasi chat, komentar, atau notifikasi, AJAX memungkinkan data baru ditampilkan secara real-time tanpa berpindah halaman. Hal ini membuat alur interaksi terasa lebih lancar dan natural. Selain itu, pengguna dapat melakukan banyak aktivitas secara paralel tanpa terhenti oleh request ke server. Hasilnya, website menjadi lebih modern, responsif, dan user-friendly. Secara keseluruhan, AJAX meningkatkan kepuasan pengguna karena mereka merasakan performa dan pengalaman yang sebanding dengan aplikasi desktop atau mobile native.




---

## Tugas 5:




# Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

Jika terdapat beberapa CSS selector untuk elemen yang sama, maka browser memilih berdasarkan tingkat spesifisitas. Urutannya: inline style memiliki prioritas tertinggi, kemudian ID selector, lalu class/attribute/pseudo-class, lalu tag/pseudo-element, dan terakhir universal/inheritance. Jika spesifisitas sama, maka aturan yang ditulis paling terakhir di CSS yang akan dipakai. !important bisa mengoverride semua aturan ini.

# Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design, serta jelaskan mengapa!

Responsive design adalah konsep penting dalam pengembangan aplikasi web karena memastikan tampilan dan fungsi aplikasi tetap nyaman digunakan di berbagai perangkat dengan ukuran layar berbeda, mulai dari ponsel hingga desktop. Dengan desain yang responsif, pengalaman pengguna menjadi lebih baik, aksesibilitas meningkat, performa lebih efisien, serta mendukung SEO.

Contoh situs yang sudah menerapkan responsive design adalah MDN Web Docs atau web.dev, di mana layout, menu navigasi, dan tipografi secara otomatis menyesuaikan dengan ukuran layar perangkat yang dipakai. Hal ini membuat situs tetap mudah diakses baik di desktop maupun perangkat mobile.

Sebaliknya, ada situs yang belum menerapkan responsive design, misalnya https://www.berkshirehathaway.com/ dan https://www.yahoo.co.jp/. Desain kedua situs tersebut tidak berubah meskipun layar di-resize atau resolusi diubah, bahkan tidak memiliki tampilan berbeda ketika diakses melalui perangkat mobile. Akibatnya, pengalaman pengguna di perangkat kecil menjadi kurang nyaman karena harus melakukan zoom in atau scrolling berlebihan.


# Jelaskan perbedaan antara *margin*, *border*, dan *padding*, serta cara untuk mengimplementasikan ketiga hal tersebut!

Dalam CSS box model, terdapat tiga elemen penting: margin, border, dan padding. Margin adalah ruang luar elemen untuk memberi jarak dengan elemen lain, border adalah garis tepi yang membungkus elemen, sementara padding adalah ruang dalam antara konten dan border. Kombinasi ketiga aspek ini menentukan jarak dan keterbacaan antar elemen.



# Jelaskan konsep *flex box* dan *grid layout* beserta kegunaannya!

Untuk mengatur tata letak modern, terdapat dua teknik utama yaitu flexbox dan grid layout. Flexbox bersifat satu dimensi (baris atau kolom) dan sangat cocok digunakan untuk menyusun item seperti menu navigasi atau kartu yang sejajar. Sebaliknya, grid layout memungkinkan pengaturan dua dimensi (baris dan kolom sekaligus), sehingga lebih ideal untuk membuat struktur layout halaman, seperti header, main content, sidebar, dan footer dalam satu grid terorganisasi. Dengan memanfaatkan responsive design, box model, flexbox, dan grid secara bersama, developer dapat membangun aplikasi web yang adaptif, teratur, dan nyaman di semua perangkat.


# Jelaskan bagaimana cara kamu mengimplementasikan *checklist* di atas secara *step-by-step* (bukan hanya sekadar mengikuti tutorial)!

(1) Saya menambahkan background gradien dan memastikan halaman responsif menggunakan Tailwind.

(2) Saya menambahkan kondisi di template {% if not product_list %} untuk membuat empty state berisi ilustrasi dan tombol add.

(3) Jika produk ada, saya menuliskan loop {% for product %} untuk menampilkan tiap produk dalam card.

(4) Card product saya desain dengan efek glassmorphism (semi transparan, blur belakang, border tipis, shadow) agar terlihat modern.

(5) Saya buat grid produk menggunakan Tailwind responsive classes (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3).

(6) Saya menambahkan tombol filter “All" dan “My Products” dengan kondisi warna aktif.

(7) Terakhir, saya testing dengan produk kosong dan dengan beberapa produk untuk memastikan checklist terpenuhi.



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
