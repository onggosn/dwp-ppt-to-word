const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { remove } = require("lodash");

// Environment Configuration
// BI TEST Environment - [Harap Ganti dengan Environment ID, API Secret, dan Application Endpoint milik Anda]
const environmentId = "5b1d7f2f9f25efd315b7";
const apiSecret = "c95da15b1b7f542ac4f74b2a978669b0cc2b6ea62a982ad4e7521f0a613b6374f0d73467de03dc7fdc6814db832ab01196de5c307fbe0e1fdb9b00c8";
const applicationEndpoint = "http://collab-test-ckeditor.apps.development.corp.bi.go.id";

// URL Endpoint
const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/editors/`;

// Reading Bundle File
const editorBundle = fs.readFileSync(path.resolve("./build/ckeditor-inline.js"));

// Generate Unique Version String
const uniqueVersion = `bundleversion-46.0.0-testing`;

const testData = "<p><strong>test</strong> <i>data</i> editor inline bundle data</p>";

const body = {
  bundle: editorBundle.toString(),
  config: {
    removePlugins: ["Eqneditor5"],
    cloudServices: {
      bundleVersion: uniqueVersion, // Set a unique name for the uploaded bundle
    },
    toolbar: {
      items: [
        "undo",
        "redo",
        "heading",
        "|",
        "bold",
        "italic",
        "underline",
        "strikethrough",
        "formatPainter",
        "superscript",
        "subscript",
        "removeFormat",
        "|",
        "link",
        "imageInsert",
        // "ckboxImageEdit",
        "ckbox",
        "insertTable",
        // "insertTableLayout",
        {
          label: "Fonts",
          icon: "text",
          items: [
            "fontFamily",
            "fontSize",
            "fontColor",
            "caseChange",
            "fontBackgroundColor",
          ],
        },
        "alignment",
        "|",
        "bulletedList",
        "numberedList",
        "outdent",
        "indent",
        "|",
        "findAndReplace",
        "specialCharacters",
        "blockQuote",
        "highlight",
        "revisionHistory",
        "comment",
        "commentsArchive",
        "importWord",
        "trackChanges",
      ],
      shouldNotGroupWhenFull: true,
    },
    list: {
      properties: {
        styles: true,
        startIndex: true,
        reversed: true,
      },
    },
    sidebar: {
      preventScrollOutOfView: true,
    },
    link: {
      addTargetToExternalLinks: true,
      defaultProtocol: "https://",
      decorators: {
        toggleDownloadable: {
          mode: "manual",
          label: "Downloadable",
          attributes: {
            download: "file",
          },
        },
      },
    },
    alignment: {
      options: ["left", "right", "center", "justify"],
    },
    image: {
      styles: ["alignCenter", "alignLeft", "alignRight"],
      resizeOptions: [
        {
          name: "resizeImage:original",
          label: "Original",
          value: null,
        },
        {
          name: "resizeImage:25",
          label: "25%",
          value: "25",
        },
        {
          name: "resizeImage:50",
          label: "50%",
          value: "50",
        },
        {
          name: "resizeImage:75",
          label: "75%",
          value: "75",
        },
        {
          name: "resizeImage:100",
          label: "100%",
          value: "100",
        },
      ],
      toolbar: [
        "linkImage",
        "|",
        "imageTextAlternative",
        "toggleImageCaption",
        "|",
        "imageStyle:inline",
        "imageStyle:wrapText",
        "imageStyle:breakText",
        "|",
        "resizeImage",
        // "|",
        // "ckboxImageEdit",
      ],
      insert: {
        integrations: ["upload", "assetManager", "url"],
      },
    },
    htmlSupport: {
      allow: [
        {
          name: "li",
          classes: ["type-heading"],
          styles: true,
        },
        {
          name: "div",
          classes: [
            "title-level-1",
            "title-level-2",
            "title-level-3",
            "title-level-4",
            "title-level-5",
            "content-level-1",
            "content-level-2",
            "content-level-3",
            "content-level-4",
            "content-level-5",
            "title-document",
          ],
        },
        {
          name: "p",
          classes: ["spacing-1", "spacing-1-5", "spacing-2"],
          styles: true,
        },
        {
          name: /^h[1-6]$/,
          styles: true,
        },
        {
          name: "table",
          classes: ["table-kop-surat", "section-header-letter"],
          styles: true,
        },
        {
          name: "ol",
          styles: true,
          attributes: {
            start: true,
          },
        },
      ],
      disallow: [],
    },
    table: {
      contentToolbar: [
        "toggleTableCaption",
        "tableColumn",
        "tableRow",
        "mergeTableCells",
        "tableCellProperties",
        "tableProperties",
      ],
      // tableLayout: {
      //   preferredExternalTableType: "content", // or 'layout'
      // },
    },
    pagination: {
      pageWidth: "21cm",
      pageHeight: "29.7cm",
      pageMargins: {
        top: "20mm",
        bottom: "20mm",
        left: "12mm",
        right: "12mm",
      },
    },
    comments: {
      editorConfig: {
        extraPlugins: [],
        mention: {
          feeds: [
            {
              marker: "@",
              feed: [],
            },
          ],
        },
      },
    },
    mediaEmbed: {
      toolbar: ["comment"],
    },
    caseChange: {
      titleCase: {
        excludeWords: [
          "a",
          "an",
          "and",
          "as",
          "at",
          "but",
          "by",
          "en",
          "for",
          "if",
          "in",
          "nor",
          "of",
          "on",
          "or",
          "per",
          "the",
          "to",
          "vs",
          "vs.",
          "via",
        ],
      },
    },
    style: {
      definitions: [
        {
          name: "Line Spacing 1",
          element: "p",
          classes: ["spacing-1"],
        },
        {
          name: "Line Spacing 1.5",
          element: "p",
          classes: ["spacing-1-5"],
        },
        {
          name: "Line Spacing 2",
          element: "p",
          classes: ["spacing-2"],
        },
      ],
    },
    heading: {
      options: [
        { model: "paragraph", title: "Paragraph", class: "ck-heading_paragraph" },
        {
          model: "heading1",
          view: "h1",
          title: "Heading 1",
          class: "ck-heading_heading1",
        },
        {
          model: "heading2",
          view: "h2",
          title: "Heading 2",
          class: "ck-heading_heading2",
        },
        {
          model: "heading3",
          view: "h3",
          title: "Heading 3",
          class: "ck-heading_heading3",
        },
        {
          model: "heading4",
          view: "h4",
          title: "Heading 4",
          class: "ck-heading_heading4",
        },
        {
          model: "heading5",
          view: "h5",
          title: "Heading 5",
          class: "ck-heading_heading5",
        },
        {
          model: "heading6",
          view: "h6",
          title: "Heading 6",
          class: "ck-heading_heading6",
        },
      ],
    },
    fontFamily: {
      supportAllValues: false,
      options: [
        "default",
        "Arial, Helvetica, sans-serif",
        "Courier New, Courier, monospace",
        "Optima",
        "Frutiger 45 Light",
        "Tahoma",
      ],
    },
    fontSize: {
      options: [
        {
          title: "10",
          model: "10pt",
        },
        {
          title: "11",
          model: "11pt",
        },
        {
          title: "12",
          model: "12pt",
        },
        {
          title: "14",
          model: "14pt",
        },
        {
          title: "16",
          model: "16pt",
        },
        {
          title: "18",
          model: "18pt",
        },
        {
          title: "20",
          model: "20pt",
        },
      ],
      supportAllValues: true,
    },
    htmlEmbed: {
      showPreviews: true,
    },
    exportPdf: {
      stylesheets: ["src/style.css", "src/fonts.css"],
      converterOptions: {
        format: "A4",
        margin_top: "20mm",
        margin_bottom: "20mm",
        margin_right: "24mm",
        margin_left: "24mm",
        page_orientation: "portrait",
      },
    },
    exportWord: {
      stylesheets: ["src/style.css", "src/fonts.css"],
      converterOptions: {
        document: {
          size: "A4",
          margin: {
            top: "20mm",
            bottom: "20mm",
            right: "12mm",
            left: "12mm",
          },
        },
      },
    },
    importWord: {
      formatting: {
        resets: "inline",
        defaults: "none",
        styles: "inline",
      },
    },
  },
  test_data: testData,
};

const CSTimestamp = Date.now();
const axiosConfig = {
  headers: {
    "X-CS-Timestamp": CSTimestamp,
    "X-CS-Signature": generateSignature(
      apiSecret,
      "POST",
      apiEndpoint,
      CSTimestamp,
      body
    ),
  },
};

axios
  .post(apiEndpoint, body, axiosConfig)
  .then((response) => {
    console.log("Upload Success! "+uniqueVersion);
    console.log("Status:", response.status);
    console.log("Response:", response.data);
  })
  .catch((error) => {
    console.log("Upload Failed! "+uniqueVersion);
    console.log("Error Message:", error.message);
    if (error.response) {
      console.log("Server Response:", error.response.data);
    }
  });

function generateSignature(apiSecret, method, uri, timestamp, body) {
  const url = new URL(uri);
  const path = url.pathname + url.search;
  const hmac = crypto.createHmac("SHA256", apiSecret);

  hmac.update(`${method.toUpperCase()}${path}${timestamp}`);

  if (body) {
    hmac.update(Buffer.from(JSON.stringify(body)));
  }

  return hmac.digest("hex");
}