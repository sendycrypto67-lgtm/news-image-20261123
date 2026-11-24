# BUILD LOG, news-image-20261123 v3

Tanggal build: 24 November 2026.
Bounty: make.fun, Sum up 23 November's world news in one image.

## Desain v3, dan bedanya dari v2

v2 memakai hero full-width di atas (CLIMATE) plus grid 3+2 di bawah.
v3 adalah desain ulang yang nyata, bukan tweak:

- Hero baru: POLAND, bukan CLIMATE. Headline terbesar di halaman,
  "MISSILES LAND IN POLAND", dua baris 52pt.
- Layout baru: hero di kolom KIRI yang lebar (612 px), bukan pita
  full-width. Kolom kanan adalah rail vertikal berisi dua cerita
  bertumpuk (CLIMATE, HORMUZ), dipisah dari hero oleh garis vertikal.
  Baris bawah berisi tiga kolom (KOREA, INDIA, LISBON).
- Hierarki lebih kuat dari v2: headline hero jauh lebih besar dari
  headline cerita lain (52pt vs 23pt rail dan 21pt baris bawah),
  tag kategori merah yang konsisten, garis pemisah antar kolom dan
  antar seksi, dan ruang kosong di bawah sub hero sebagai napas.
- Masthead serif THE WORLD TODAY, baris tanggal Monday 23 November
  2026, lalu deck satu baris. Halaman krem seperti koran, footer
  sumber di bawah.
- Font adaptif, headline mengecil sampai muat, maksimal 2 baris untuk
  hero dan rail, maksimal 3 baris untuk sub-caption.

## Ilustrasi

6 ilustrasi editorial flat baru dibuat dengan media image tool, semuanya
tanpa teks, huruf, atau angka di dalam gambar, dan tidak ada satu pun
yang dipakai ulang dari v2:

1. Hero POLAND. Langit malam di atas desa Polandia, dua misil dengan
   jejak asap oranye jatuh dari langit, menara gereja dan atap rumah
   sebagai siluet.
2. CLIMATE. Aula sidang COP yang kosong, meja panjang dengan kertas
   berserakan, delegasi berjalan pergi ke arah jendela, awan badai.
3. HORMUZ. Dua tanker di selat berbatu saat senja, asap tipis, dan
   sebuah helikopter di atas.
4. KOREA. Aula ujian kosong dengan deretan meja, pejabat membungkuk
   di podium, dua reporter dengan kamera.
5. INDIA. Dua pemimpin berjabat tangan, bendera Nepal di kiri dan
   bendera India di kanan.
6. LISBON. Kerumunan di tengah hujan dengan payung, trem kuning,
   fasad ubin biru.

Verifikasi visual tiap ilustrasi dilakukan sebelum compose. Dua cacat
potensial dicek dan ditangani saat crop, bukan dengan generate ulang:

- Crop hero Poland diposisikan (x0=300) supaya kedua misil dan menara
  gereja tetap masuk frame; crop tengah akan memotong ujung misil kanan.
- Crop India diukur dulu dengan scan piksel: bendera Nepal (merah)
  membentang y 227 sampai 1148 dari 1280, jadi crop bawah memakai
  jendela y 90 sampai 1208 agar kedua bendera tampil utuh. Hasil
  akhir: bendera Nepal, panji ganda merah dengan bulan sabit dan
  matahari putih, dan bendera India, tiga warna dengan roda biru,
  tampil utuh dan mudah dibedakan.
- Crop Hormuz diposisikan (y0=300) supaya lambung kapal dekat tampil
  utuh; helikopter dikorbankan karena di luar frame crop.

## Compose

Compose dilakukan dengan Python dan Pillow lewat script build-time di
work-v3/build_v3.py. Script itu bukan bagian repo, hanya entry.png,
main.py, dan BUILD_LOG.md yang masuk repo-v3. Font, Noto Serif Black
untuk masthead, Noto Serif Bold untuk headline, Noto Serif Italic
untuk deck, Noto Sans Bold untuk tag dan tanggal, Noto Sans Regular
untuk sub-caption dan footer. Layout akhir berakhir di y=1012 dari 1024.

## main.py

Ditulis dari nol berdasarkan spesifikasi, tanpa membaca main.py v1
atau v2. Program ini validator plus copier, Python stdlib saja, tanpa
network. Langkahnya, cari entry.png di samping main.py, cek magic PNG,
cek ukuran file maksimal 1048576 byte, telusuri chunk dan baca IHDR,
tolak dimensi di atas 1024 px, cek bit depth dan colour type yang
valid, cek CRC32 chunk IHDR dan IEND, wajibkan IEND yang well-formed
di akhir file tanpa byte sisa, lalu salin byte-for-byte ke
$MAKEFUN_OUTPUT_DIR/entry.png. Semua kegagalan keluar dengan exit 1
dan pesan ke stderr.

## Verifikasi

- entry.png, 1024x1024, 583260 byte, di bawah batas 1 MiB, sha256
  327e2fd3af48f3cc16b6c56ffe4ce06f350b710b5856f99792f562ddeb79ccd4.
- main.py dijalankan 2x ke direktori berbeda, sha256 output identik
  dengan file repo (327e2fd3...).
- Tes negatif 1, file bukan PNG ditolak, exit 1.
- Tes negatif 2, PNG 1200x1200 ditolak, exit 1.
- Tes negatif 3, MAKEFUN_OUTPUT_DIR tidak diset ditolak, exit 1.
- Tes negatif 4, PNG di atas 1 MiB (3151216 byte) ditolak, exit 1.
- Tes negatif 5, byte sisa setelah IEND ditolak, exit 1.
- Tes negatif 6, CRC32 IHDR yang rusak ditolak, exit 1.
- Isi repo-v3 hanya entry.png, main.py, dan BUILD_LOG.md. Tidak ada
  README, LICENSE, atau script build di dalam repo.
- Tidak ada angka korban di teks mana pun, tidak ada spekulasi yang
  disajikan sebagai fakta, tidak ada em-dash.
- Verifikasi visual akhir: masthead, tanggal, deck, hero POLAND
  dominan di kiri, rail CLIMATE dan HORMUZ di kanan, baris bawah
  KOREA, INDIA, LISBON, bendera Nepal dan India utuh dan berbeda,
  footer sumber. Tanpa cacat teks, tanpa teks terpotong, tanpa teks
  bertumpuk.

## Verifikasi koordinator (24 Nov ~22:00 WIB)
- Baca visual entry.png: masthead, tanggal, deck, hero POLAND dominan,
  rail kanan dan baris bawah sesuai brief, bendera Nepal dan India utuh
  dan berbeda, footer sumber. Tanpa cacat teks, tanpa angka korban,
  tanpa em-dash di teks mana pun (satu kemunculan byte E2 80 94 di file
  adalah data piksel terkompresi IDAT, bukan teks: PNG ini tidak punya
  chunk teks sama sekali).
- main.py 2x run ke dir berbeda, sha256 output identik dengan file repo
  (327e2fd3...). Tes negatif non-PNG exit 1.
- Edit koordinator (perbaikan validasi asli, perilaku output tidak
  berubah): main.py kini juga menolak PNG tanpa chunk IDAT dan
  memvalidasi bit depth terhadap colour type sesuai spesifikasi PNG.
  Setelah edit, main.py 2x run tetap menghasilkan sha256 output
  327e2fd3... yang sama.
