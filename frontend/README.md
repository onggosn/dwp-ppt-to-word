# NEW DWP

## Aplikasi yang Dibutuhkan

- NodeJS : ^18.xx

## Pemasanan
- download project dari git
    ```sh
    git clone https://github.com/gramadhan19/new-dwp.git
    ```
- buka folder new-dwp
    ```sh
    cd new-dwp
    ```
- install aplikasi
    ```sh
    npm install
    ```
- install ck-editor
    ```sh
    cd src/v2/components/side-project/ckeditor/
    ```
     ```sh
    npm install
    ```
- kembali ke root project dan running aplikasi (env development)
    ```sh
    npm run serve-development
    ```
- jalankan aplikasi env staging
    ```sh
    npm run serve-staging
    ```
- jalankan aplikasi env testing
    ```sh
    npm run serve-testing
    ```
- generate aplikasi untuk build
    ```sh
    npm run build-development
    ```

## Peraturan Koding
### Github
- `master` merupakan branch utama
- `p7-development` merupakan branch utama development DWP Kebijakan
- `p9-development` merupakan branch utama development DWP Om Pro Market
- Format nama branch silakan berkreasi sesuai dengan keinginan kalian.
- commit message rule types must be one of [feat, fix, hotfix, bugfix, WIP, docs, chore, style, refactor, ci, test, revert, perf, build] [type-enum] example, "feat: add new button to ....."

### Penamaan
- `File` menggunakan `PascalCase`
- `Folder` menggunakan `camelCase`
- `variable` menggunakan `camelCase`
- `component` yang di import menggunakan `PascalCase`
- `icon` menggunakan `kebab-case`
- `key` menggunakan `snake_case`
- `type` menggunakan awalan `T` dan `PascalCase`

### Directory
- `src` berisikan main codingan
- `src/assets` berisikan asset - asset aplikasi
- `src/components` berisikan component aplikasi
- `src/views` bersikan halaman aplikasi
- `src/v2` berisikan module NEW DWP
- `src/v2/component/side-project` berisikan custom dependency seperti ckeditor
- `src/v2/modules/omPro` berisikan module P9 OM PRO turunan dari P7 Kebijakan




