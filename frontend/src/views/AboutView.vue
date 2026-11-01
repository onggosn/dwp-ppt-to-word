<template>
  <div id="app" ref="document" style="background: grey; justify-items: center">
    <!-- <v-btn @click="exportToPDF" class="text-center ma-10">Export to PDF</v-btn>
    <div style="justify-items: center" id="luaran">
      <div id="element-to-convert">
        <div class="ck-content">
          <table
            class="table content-table ck-table-resized"
            style="border-color: hsl(0, 0%, 100%); width: 100%"
          >
            <colgroup>
              <col style="width: 32.32%" />
              <col style="width: 35.17%" />
              <col style="width: 32.51%" />
            </colgroup>
            <tbody>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)">&nbsp;</td>
                <td style="border-color: hsl(0, 0%, 100%)">&nbsp;</td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  POLICY NOTE<br />PN/MON/XX/TAHUN
                </td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)" colspan="3">
                  <p
                    style="
                      text-align: center;
                      font-family: 'cursive';
                      font-weight: bold;
                      font-size: 16pt;
                    "
                  >
                    JUDUL:<br />JUDUL POLICY NOTE XXXXXX
                  </p>
                  <p style="text-align: center">&nbsp;</p>
                  <p style="text-align: center">&nbsp;</p>
                </td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)" colspan="3">
                  <p style="text-align: center">
                    Nama Penyusun 1<br />Nama Penyusun 2<br />Nama Penyusun 3<br />dst
                  </p>
                  <p style="text-align: center">&nbsp;</p>
                  <p style="text-align: center">&nbsp;</p>
                </td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)" colspan="3">
                  <p style="text-align: center"><strong>SATKER</strong></p>
                  <p style="text-align: center">&nbsp;</p>
                </td>
              </tr>
            </tbody>
          </table>
          <table
            class="table content-table ck-table-resized"
            style="border-color: hsl(0, 0%, 100%); width: 100%"
          >
            <colgroup>
              <col style="width: 50%" />
              <col style="width: auto" />
              <col style="width: 50%" />
            </colgroup>
            <tbody>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)"></td>
                <td style="border-color: hsl(0, 0%, 100%)">&nbsp;</td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">
                    <span style="font-size: 11pt"
                      >Jakarta, Tanggal Bulan Tahun</span
                    >
                  </p>
                </td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">
                    <span style="font-size: 11pt">[ Jabatan ]</span>
                  </p>
                </td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">&nbsp;</p>
                </td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">
                    <span style="font-size: 11pt">[ Jabatan ]</span>
                  </p>
                </td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)"></td>
                <td style="border-color: hsl(0, 0%, 100%)"></td>
                <td style="border-color: hsl(0, 0%, 100%)"></td>
              </tr>
              <tr>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">
                    <span style="font-size: 11pt"> <u>[ Nama ]</u> </span>
                    <br />
                    <span style="font-size: 11pt">[ Pangkat ]</span>
                  </p>
                </td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">&nbsp;</p>
                </td>
                <td style="border-color: hsl(0, 0%, 100%)">
                  <p style="text-align: center">
                    <span style="font-size: 11pt"> <u>[ Nama ]</u> </span>
                    <br />
                    <span style="font-size: 11pt">[ Pangkat ]</span>
                  </p>
                </td>
              </tr>
            </tbody>
          </table>
          <p style="page-break-after: always"></p>
          <div class="ck-content">
            <div class="title-level-1" id="section-form-15">
              <p>
                <strong
                  ><span
                    style="font-family: 'Frutiger 45 Light'; font-size: 11pt"
                    >1. Abstraksi</span
                  ></strong
                >
              </p>
            </div>
            <div class="content-level-1">
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetur adipiscing elit,
                    sed do eiusmod tempor incididunt ut labore et dolore magna
                    aliqua. Et netus et malesuada fames ac turpis. Felis
                    imperdiet proin fermentum leo vel orci. Tristique senectus
                    et netus et malesuada fames ac turpis egestas. Penatibus et
                    magnis dis parturient. At varius vel pharetra vel turpis
                    nunc eget. Diam ut venenatis tellus in metus vulputate eu
                    scelerisque felis. Quam elementum pulvinar etiam non quam
                    lacus. Donec et odio pellentesque diam volutpat commodo sed
                    egestas. Volutpat diam ut venenatis tellus in metus.
                    Ullamcorper malesuada proin libero nunc consequat. Phasellus
                    vestibulum lorem sed risus.</span
                  ></span
                >
              </p>
              <p style="line-height: 115%; margin: 12pt 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Keywords:</strong>&nbsp;Lorem ipsum dolor sit amet,
                    consectetur adipiscing elit, sed do eiusmod tempor
                    incididunt ut labore et dolore magna aliqua.</span
                  ></span
                >
              </p>
            </div>
            <div class="title-level-1" id="section-form-15">
              <p>
                <strong
                  ><span
                    style="font-family: 'Frutiger 45 Light'; font-size: 11pt"
                    >2. Pertanyaan Penelitian</span
                  ></strong
                >
              </p>
            </div>
            <div class="content-level-1">
              <p style="line-height: 115%; margin: 6pt 0cm 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Review Literatur</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula.&nbsp;</span
                  ><span lang="EN-US" dir="ltr"
                    >Donec hendrerit, felis et imperdiet euismod, purus ipsum
                    pretium metus, in lacinia nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <figure class="table">
                <table
                  style="
                    border-collapse: collapse;
                    border-style: none;
                    margin-left: 21.3pt;
                  "
                >
                  <tbody>
                    <tr>
                      <td
                        style="
                          padding: 0cm 5.4pt;
                          vertical-align: top;
                          width: 205.2pt;
                        "
                      >
                        <p
                          style="
                            line-height: normal;
                            margin: 0cm;
                            text-align: center;
                          "
                        >
                          <span style="font-size: 9pt"
                            ><span lang="EN-US" dir="ltr"
                              ><strong>Gambar 1.</strong></span
                            ></span
                          >
                        </p>
                        <p
                          style="
                            line-height: normal;
                            margin: 0cm;
                            text-align: center;
                          "
                        >
                          <span style="font-size: 9pt"
                            ><span lang="EN-US" dir="ltr"
                              ><strong
                                >Sinergi Kebijakan Moneter dan
                                Makroprudensial</strong
                              ></span
                            ></span
                          >
                        </p>
                      </td>
                      <td
                        style="
                          padding: 0cm 5.4pt;
                          vertical-align: top;
                          width: 212.7pt;
                        "
                      >
                        <p
                          style="
                            line-height: normal;
                            margin: 0cm;
                            text-align: center;
                          "
                        >
                          <span style="font-size: 9pt"
                            ><span lang="EN-US" dir="ltr"
                              ><strong>Gambar 2.</strong></span
                            ></span
                          >
                        </p>
                        <p
                          style="
                            line-height: normal;
                            margin: 0cm;
                            text-align: center;
                          "
                        >
                          <span style="font-size: 9pt"
                            ><span lang="EN-US" dir="ltr"
                              ><strong
                                >Skema PLN dan ULN Berdasarkan FA BoP</strong
                              ></span
                            ></span
                          >
                        </p>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </figure>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: center;
                  text-indent: -7.1pt;
                "
              >
                <span style="font-size: 10.5pt"
                  ><picture
                    ><source
                      srcset="
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/80.webp   80w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/160.webp 160w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/240.webp 240w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/320.webp 320w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/400.webp 400w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/480.webp 480w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/560.webp 560w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/640.webp 640w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/720.webp 720w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/747.webp 747w
                      "
                      sizes="(max-width: 747px) 100vw, 747px"
                      type="image/webp" />
                    <img
                      src="https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/trGVVXG1Ji6S/images/747.png"
                      width="747"
                      height="279" /></picture
                ></span>
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
            </div>
            <div class="title-level-1" id="section-form-15">
              <p>
                <strong
                  ><span
                    style="font-family: 'Frutiger 45 Light'; font-size: 11pt"
                    >3. Landasan Teori</span
                  ></strong
                >
              </p>
            </div>
            <div class="content-level-1">
              <ol style="padding-left: 18.93px">
                <li>
                  <h2 id="e41d565c8a0ef842fcedab87293ca4f5c">
                    <span style="color: windowtext; font-size: 10.5pt"
                      ><span lang="EN-US" dir="ltr"
                        ><strong>Hasil Pengolahan Data</strong></span
                      ></span
                    >
                  </h2>
                </li>
              </ol>
              <p style="line-height: 115%; margin: 6pt 0cm 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    ><strong
                      >Prospek Perekonomian Global 2023-2027</strong
                    ></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas. Proin pharetra nonummy
                    pede. Mauris et orci. Aenean nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p style="line-height: 115%; margin: 0cm">&nbsp;</p>
              <p style="line-height: 115%; margin: 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>New Normal</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula.&nbsp;</span
                  ><span lang="EN-US" dir="ltr"
                    >Donec hendrerit, felis et imperdiet euismod, purus ipsum
                    pretium metus, in lacinia nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p style="line-height: 115%; margin: 0cm">&nbsp;</p>
              <ol style="padding-left: 18.93px" start="2">
                <li>
                  <h2 id="e8cadc7d768c7cdc044da3d6a4470ef27">
                    <span style="color: windowtext; font-size: 10.5pt"
                      ><span lang="EN-US" dir="ltr"
                        ><strong>Analisis</strong></span
                      ></span
                    >
                  </h2>
                </li>
              </ol>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: normal;
                  margin: 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 9pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Gambar 3.</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: normal;
                  margin: 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 9pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Policy Gap Kebijakan Makroprudensial</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><picture
                    ><source
                      srcset="
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/80.webp   80w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/160.webp 160w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/240.webp 240w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/320.webp 320w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/400.webp 400w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/480.webp 480w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/492.webp 492w
                      "
                      sizes="(max-width: 492px) 100vw, 492px"
                      type="image/webp" />
                    <img
                      src="https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/ZSdGD2Gn5fD8/images/492.png"
                      width="492"
                      height="282" /></picture
                ></span>
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas. Proin pharetra nonummy
                    pede. Mauris et orci. Aenean nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede. Suspendisse dapibus
                    lorem pellentesque magna. Integer nulla. Donec blandit
                    feugiat ligula.&nbsp;</span
                  ><span lang="EN-US" dir="ltr"
                    >Donec hendrerit, felis et imperdiet euismod, purus ipsum
                    pretium metus, in lacinia nulla nisl eget sapien.</span
                  ></span
                >
              </p>
            </div>
            <div class="title-level-1" id="section-form-15">
              <p>
                <strong
                  ><span
                    style="font-family: 'Frutiger 45 Light'; font-size: 11pt"
                    >4. Asesmen</span
                  ></strong
                >
              </p>
            </div>
            <div class="content-level-1">
              <p style="line-height: 115%; margin: 6pt 0cm 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    ><strong
                      >Prospek Perekonomian Global 2023-2027</strong
                    ></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas. Proin pharetra nonummy
                    pede. Mauris et orci. Aenean nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p style="line-height: 115%; margin: 0cm">&nbsp;</p>
              <p style="line-height: 115%; margin: 0cm">
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>New Normal</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna. Nunc viverra imperdiet enim.
                    Fusce est. Vivamus a tellus. Pellentesque habitant morbi
                    tristique senectus et netus et malesuada fames ac turpis
                    egestas. Proin pharetra nonummy pede. Mauris et orci. Aenean
                    nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula.&nbsp;</span
                  ><span lang="EN-US" dir="ltr"
                    >Donec hendrerit, felis et imperdiet euismod, purus ipsum
                    pretium metus, in lacinia nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p style="line-height: 115%; margin: 0cm">&nbsp;</p>
              <ol style="padding-left: 18.93px">
                <li>
                  <h2 id="e9b55e36631ac45aec5578b684f51754a">
                    <span style="color: windowtext; font-size: 10.5pt"
                      ><span lang="EN-US" dir="ltr"
                        ><strong>Analisis</strong></span
                      ></span
                    >
                  </h2>
                </li>
              </ol>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: normal;
                  margin: 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 9pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Gambar 3.</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: normal;
                  margin: 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 9pt"
                  ><span lang="FR" dir="ltr"
                    ><strong>Policy Gap Kebijakan Makroprudensial</strong></span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: center;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><picture
                    ><source
                      srcset="
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/80.webp   80w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/160.webp 160w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/240.webp 240w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/320.webp 320w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/400.webp 400w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/480.webp 480w,
                        https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/492.webp 492w
                      "
                      sizes="(max-width: 492px) 100vw, 492px"
                      type="image/webp" />
                    <img
                      src="https://dev-ckbox-ckeditor.apps.development.corp.bi.go.id/ef811b1a5ad0599a5c99/assets/K7FCTdfhDLjz/images/492.png"
                      width="492"
                      height="282" /></picture
                ></span>
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                    Maecenas porttitor congue massa. Fusce posuere, magna sed
                    pulvinar ultricies, purus lectus malesuada libero, sit amet
                    commodo magna eros quis urna.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus.
                    Pellentesque habitant morbi tristique senectus et netus et
                    malesuada fames ac turpis egestas. Proin pharetra nonummy
                    pede. Mauris et orci. Aenean nec lorem.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="EN-US" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede.&nbsp;</span
                  ><span lang="FR" dir="ltr"
                    >Suspendisse dapibus lorem pellentesque magna. Integer
                    nulla. Donec blandit feugiat ligula. Donec hendrerit, felis
                    et imperdiet euismod, purus ipsum pretium metus, in lacinia
                    nulla nisl eget sapien.</span
                  ></span
                >
              </p>
              <p
                style="
                  line-height: 115%;
                  margin: 6pt 0cm 0cm;
                  text-align: justify;
                  text-indent: 1cm;
                "
              >
                <span style="font-size: 10.5pt"
                  ><span lang="FR" dir="ltr"
                    >In porttitor. Donec laoreet nonummy augue. Suspendisse dui
                    purus, scelerisque at, vulputate vitae, pretium mattis,
                    nunc. Mauris eget neque at sem venenatis eleifend. Ut
                    nonummy. Fusce aliquet pede non pede. Suspendisse dapibus
                    lorem pellentesque magna. Integer nulla. Donec blandit
                    feugiat ligula.&nbsp;</span
                  ><span lang="EN-US" dir="ltr"
                    >Donec hendrerit, felis et imperdiet euismod, purus ipsum
                    pretium metus, in lacinia nulla nisl eget sapien.</span
                  ></span
                >
              </p>
            </div>
          </div>
        </div>
      </div> 
    </div>-->
  </div>
</template>

<script setup lang="ts">
// import html2pdf from "html2pdf.js";

// const exportToPDF = () => {
//   const options = {
//     margin: [20.0, 10.0, 10.0, 10.0],
//     filename: "dokumen_word_style.pdf",
//     image: { type: "jpeg", quality: 0.98 },
//     html2canvas: {
//       scale: 2, // Meningkatkan resolusi gambar
//       useCORS: true, // Diperlukan jika ada gambar dari domain lain
//     },
//     jsPDF: {
//       unit: "mm",
//       format: "a4",
//       orientation: "portrait",
//     },
//   };

//   // Ambil elemen yang akan dikonversi
//   const element = document.getElementById("element-to-convert");

//   // Jalankan fungsi untuk membuat PDF
//   html2pdf().set(options).from(element).save();
// };
</script>

<style scoped>
#luaran {
  width: 800px;
  background-color: #fff;
  border: 1px solid #ccc;
}
/* Gaya untuk tampilan di layar */
#element-to-convert {
  padding-top: 20mm;
  padding-left: 10mm;
  padding-bottom: 10mm;
  padding-right: 10mm;
}

/* * SOLUSI: Reset padding/margin saat mencetak atau membuat PDF.
         * Blok ini akan diterapkan oleh html2pdf.
        */
@media print {
  body {
    margin: 0;
    padding: 0;
  }
  #element-to-convert {
    padding: 0 !important; /* Hapus padding saat PDF dibuat */
    margin: 0 !important; /* Hapus margin saat PDF dibuat */
    border: none !important; /* Hapus border jika tidak diinginkan di PDF */
  }
}

.btn {
  display: block;
  margin: 20px auto;
  padding: 10px 20px;
  font-size: 16px;
}
</style>
