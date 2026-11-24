# BUILD LOG, news-image-20261123 v2

Tanggal build: 24 November 2026.
Bounty: make.fun, Sum up 23 November's world news in one image.

## Desain v2, dan bedanya dari v1

v1 memakai grid 3x2 dengan 6 cerita sama besar, tanpa hierarki. Kritiknya,
semua cerita berebut perhatian dan headline jadi kecil.

v2 memakai hierarki koran klasik:

- Masthead serif THE WORLD TODAY, baris tanggal Monday 23 November 2026,
  lalu deck satu baris.
- HERO STORY dominan di atas. Cerita CLIMATE, COP31 runtuh di Antalya,
  mendapat ilustrasi lebar penuh dan headline paling besar, satu baris.
- 5 cerita lain di bawah dalam grid 3 di baris pertama dan 2 di baris
  kedua, masing-masing dengan tag kategori merah, headline tebal, dan
  sub-caption.
- Halaman krem seperti koran, footer sumber di bawah.
- Font adaptif, headline mengecil sampai muat, maksimal 3 baris.

## Ilustrasi

6 ilustrasi editorial flat baru dibuat dengan media image tool, semuanya
tanpa teks, huruf, atau angka di dalam gambar:

1. Hero CLIMATE. Aula sidang kosong, meja panjang, delegasi berjalan
   pergi ke arah jendela, awan badai di luar, kertas berserakan.
2. HORMUZ. Dua tanker di selat berbatu, asap tipis, helikopter.
3. POLAND. Langit malam, benda jatuh dengan jejak asap oranye, siluet
   desa dan menara gereja.
4. KOREA. Aula ujian kosong, pejabat membungkuk di podium, reporter.
5. INDIA. Dua pemimpin berjabat tangan, bendera Nepal di kiri dan
   bendera India di kanan.
6. LISBON. Kerumunan di tengah hujan dengan payung, trem kuning,
   fasad ubin biru.

Verifikasi visual tiap ilustrasi dilakukan sebelum compose. Satu cacat
ditemukan dan diperbaiki. Crop pertama pada kartu India memotong kedua
bendera sehingga tidak lagi dikenali. Perbaikan, gambar baris kedua
dibuat lebih tinggi (140 px dari 108 px) sehingga bendera Nepal,
panji ganda merah dengan matahari dan bulan putih, dan bendera India,
tiga warna dengan roda biru, tampil utuh dan mudah dibedakan.

## Compose

Compose dilakukan dengan Python dan Pillow lewat script build-time di
work-v2/build_v2.py. Script itu bukan bagian repo, hanya entry.png,
main.py, dan BUILD_LOG.md yang masuk repo-v2. Font, Noto Serif Black
untuk masthead, Noto Serif Bold untuk headline, Noto Serif Italic
untuk deck, Noto Sans Bold untuk tag dan tanggal, Noto Sans Regular
untuk sub-caption dan footer. Layout akhir berakhir di y=1008 dari 1024.

## main.py

Ditulis dari nol berdasarkan spesifikasi, tanpa membaca main.py v1.
Program ini validator plus copier, Python stdlib saja, tanpa network.
Langkahnya, cari entry.png di samping main.py, cek magic PNG, cek
ukuran file maksimal 1048576 byte, telusuri chunk dan baca IHDR,
tolak dimensi di atas 1024 px, cek IEND tanpa byte sisa, lalu salin
byte-for-byte ke $MAKEFUN_OUTPUT_DIR/entry.png. Semua kegagalan
keluar dengan exit 1 dan pesan ke stderr.

## Verifikasi

- entry.png, 1024x1024, 551997 byte, di bawah batas 1 MiB.
- main.py dijalankan 2x ke direktori berbeda, sha256 output identik:
  5f0fb996e06d2e3d4b49ce09e10d9d6abb9b9d27082f7456a414fdca429b9fb1
- Tes negatif 1, file bukan PNG ditolak, exit 1.
- Tes negatif 2, PNG 1200x1200 ditolak, exit 1.
- Tes tambahan, MAKEFUN_OUTPUT_DIR tidak diset ditolak, exit 1.
- Isi repo-v2 hanya entry.png, main.py, dan BUILD_LOG.md. Tidak ada
  README, LICENSE, atau script build di dalam repo.
- Tidak ada angka korban di teks mana pun, tidak ada spekulasi yang
  disajikan sebagai fakta, tidak ada em-dash.

## Verifikasi koordinator (24 Nov ~07:35 WIB)
- Baca visual entry.png: masthead, tanggal, deck, hero CLIMATE dominan, 5 cerita bawah (Hormuz, Poland, Korea, India, Lisbon), bendera Nepal dan India tampil utuh dan berbeda, footer sumber. Tanpa cacat teks, tanpa angka korban, tanpa em-dash.
- main.py 2x run ke dir berbeda, sha256 output identik dengan file repo (5f0fb996...). Tes negatif non-PNG exit 1.
- Edit koordinator: tambah cek CRC32 untuk chunk IHDR dan IEND (import zlib). Output tidak berubah, sha256 tetap 5f0fb996.
