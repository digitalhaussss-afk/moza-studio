# Moza Studio — White Sakura Edition (Prototype UI + preserved Atelier editor)

Nama aplikasi resmi: **Moza Studio**. Tidak lagi menggunakan Petal.

## Isi paket

- `index.html`: dashboard putih dominan, aksen dusty rose/terracotta, layout desktop/tablet/mobile, tombol menuju dua editor.
- `atelier/index.html`: Atelier Studio v30.68 milik pengguna, tetap memakai JavaScript inti asli. Hanya judul browser dan CSS tambahan yang dimodifikasi.
- `tools/retint_figcraft.py`: warna dan branding baru untuk source FigCraft yang sudah dipatch sebelumnya. Script tidak mengubah canvas/data/commands.
- `tools/merge_figcraft.py`: gabungkan hasil build FigCraft (folder `dist/web`) ke `web/` aplikasi ini.
- `03_REBUILD_DAN_GABUNG_WINDOWS.bat`: proses tema dan build FigCraft di PC Windows pengguna.

## Yang dipertahankan

Seluruh fitur logika Atelier, termasuk editor visual, responsive controls, RSVP, Google Sheets, Supabase, media, proyek, dan ekspor, **tidak diedit** oleh revisi ini. Ketersediaan integrasi cloud tetap bergantung pada konfigurasi lama dan host.

## Memasang di GitHub Pages

1. Simpan backup repository dan konfigurasi layanan terlebih dahulu.
2. Upload isi folder ini ke **root** repository `mosa-studio` (nama repo tidak perlu berubah). Timpa `index.html` di root, tambahkan `atelier/`, `assets/`, manifest dan pendukung.
3. **Jangan hapus folder `web/`**, karena isinya adalah FigCraft ter-compile yang sudah kamu upload sebelumnya. Jika `web/` hilang, pakai `python tools/merge_figcraft.py "C:\...\figcraft\dist\web"`.
4. GitHub Pages harus menerbitkan root repository, bukan hanya folder `web/`. Jika workflow khusus memakai path `./web`, ubah workflow deployment supaya menerbitkan root.
5. Uji `/`, `/atelier/`, `/web/` setelah deploy. `index.html` harus diakses melalui web server, bukan `file://`.

## Membuat tema FigCraft ikut Moza

Dari folder ini jalankan `03_REBUILD_DAN_GABUNG_WINDOWS.bat` dan masukkan lokasi folder source FigCraft di PC. Alternatif: `python tools/merge_figcraft.py "C:\...\figcraft\dist\web"` untuk memakai build lama (warna di canvas FigCraft belum otomatis ikut).

## Batasan saat ini

- **Dua editor tetap terpisah** di satu situs dan navigasi yang sama, bukan satu canvas/editor data tunggal.
- Kartu contoh di dashboard hanyalah ilustrasi, tidak menyatakan terdapat proyek atau data RSVP tertentu.
- Hasil `.wasm` FigCraft tidak ikut ZIP ini; gunakan folder `web/` hasil build di repository milikmu.
- Fungsi internal Atelier tidak diubah, tetapi seluruh kemungkinan perilaku runtime/semua layanan backend tidak bisa dijamin tanpa tes integrasi end-to-end pada domain dan kredensial pengguna.
- Perubahan asal/domain dapat mengubah akses data yang tersimpan di browser (localStorage) dan callback OAuth. Backup proyek sebelum deploy publik.

## Lisensi

Paket menyertakan source Atelier yang kamu unggah. Periksa hak distribusinya sebelum membuka repository publik. Source FigCraft asli perlu mempertahankan pemberitahuan lisensi upstream.
