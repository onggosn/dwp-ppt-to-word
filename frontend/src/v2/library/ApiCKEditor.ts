import axios from "axios";
import CryptoJS from "crypto-js";

const environmentId = "5b1d7f2f9f25efd315b7";
const apiSecret =
  "c95da15b1b7f542ac4f74b2a978669b0cc2b6ea62a982ad4e7521f0a613b6374f0d73467de03dc7fdc6814db832ab01196de5c307fbe0e1fdb9b00c8";
const applicationEndpoint =
  "http://dev-collab-http.apps.development.corp.bi.go.id";

function generateSignature(apiSecret, method, uri, timestamp, body) {
  const url = new URL(uri);
  const path = url.pathname + url.search;
  const hmac = CryptoJS.HmacSHA256(
    `${method.toUpperCase()}${path}${timestamp}`,
    apiSecret
  );

  if (body) {
    const textEncoder = new TextEncoder();
    const encodedBody = textEncoder.encode(JSON.stringify(body));
    hmac.update(encodedBody);
    // hmac.update(CryptoJS.enc.Utf8.parse(JSON.stringify(body)));
    // hmac.update(Buffer.from(JSON.stringify(body)));
  }

  return hmac.toString(CryptoJS.enc.Hex);
}

export async function ExportDocument(documentId) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/documents/${documentId}`;
  const CSTimestamp = Date.now();
  const config = {
    headers: {
      "X-CS-Timestamp": CSTimestamp,
      "X-CS-Signature": generateSignature(
        apiSecret,
        "GET",
        apiEndpoint,
        CSTimestamp,
        ""
      ),
    },
  };
  const response = await axios.get(apiEndpoint, config);
  return response.data;
}

export async function GetDocumentContentFromStorage(documentId) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/storage/${documentId}`;
  const CSTimestamp = Date.now();
  const config = {
    headers: {
      "X-CS-Timestamp": CSTimestamp,
      "X-CS-Signature": generateSignature(
        apiSecret,
        "GET",
        apiEndpoint,
        CSTimestamp,
        ""
      ),
    },
  };
  const response = await axios.get(apiEndpoint, config);
  return response.data;
}

export async function ExportTheContentFromASession(documentId) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/collaborations/${documentId}`;
  const CSTimestamp = Date.now();
  const config = {
    headers: {
      "X-CS-Timestamp": CSTimestamp,
      "X-CS-Signature": generateSignature(
        apiSecret,
        "GET",
        apiEndpoint,
        CSTimestamp,
        ""
      ),
    },
  };
  const response = await axios.get(apiEndpoint, config);
  return response.data;
}

export async function ExportRevision(documentId) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/revisions?document_id=${documentId}`;
  const CSTimestamp = Date.now();
  const config = {
    headers: {
      "X-CS-Timestamp": CSTimestamp,
      "X-CS-Signature": generateSignature(
        apiSecret,
        "GET",
        apiEndpoint,
        CSTimestamp,
        ""
      ),
    },
  };
  const response = await axios.get(apiEndpoint, config);
  return response.data;
}

export async function ExportSuggestion(documentId) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/suggestions?document_id=${documentId}&limit=1000&include_deleted=true&sort_by=updated_at&order=asc`;
  const CSTimestamp = Date.now();
  const config = {
    headers: {
      "X-CS-Timestamp": CSTimestamp,
      "X-CS-Signature": generateSignature(
        apiSecret,
        "GET",
        apiEndpoint,
        CSTimestamp,
        ""
      ),
    },
  };
  const response = await axios.get(apiEndpoint, config);
  return response.data;
}

export async function UploadBundle(bundleVersion) {
  const apiEndpoint = `${applicationEndpoint}/api/v5/${environmentId}/editors/`;
  let bundle = "";
  try {
    const response = await fetch("/doc/ckeditor-inline.js");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    bundle = (await response.text()).toString();
  } catch (error) {
    undefined;
  }

  const body = {
    bundle: bundle,
    config: {
      cloudServices: {
        bundleVersion: bundleVersion, // Set a unique name for the uploaded bundle
      },
      toolbar: {
        items: [
          "fontFamily",
          "fontColor",
          "caseChange",
          "fontSize",
          "|",
          "previousPage",
          "nextPage",
          "pageNavigation",
          "|",
          "bold",
          "underline",
          "italic",
          "strikethrough",
          "link",
          "insertTemplate",
          "bulletedList",
          "numberedList",
          "heading",
          "|",
          "highlight",
          "fontBackgroundColor",
          "formatPainter",
          "horizontalLine",
          "|",
          "superscript",
          "subscript",
          "alignment",
          "outdent",
          "indent",
          "specialCharacters",
          "|",
          "imageInsert",
          "imageUpload",
          "insertTable",
          "mediaEmbed",
          "undo",
          "redo",
          "|",
          "code",
          "codeBlock",
          "htmlEmbed",
          "todoList",
          "|",
          "pageBreak",
          "eqneditor5Button",
          "|",
          "ckbox",
          "comment",
          "commentsArchive",
          "ckboxImageEdit",
          "|",
          "importWord",
          "|",
          "findAndReplace",
          "textPartLanguage",
          "blockQuote",
          "revisionHistory",
          "trackChanges",
        ],
        shouldNotGroupWhenFull: true,
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
            name: "resizeImage:50",
            label: "50%",
            value: "50",
          },
          {
            name: "resizeImage:75",
            label: "75%",
            value: "75",
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
        tableToolbar: ["comment", "comment"],
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
            name: "Article category",
            element: "h3",
            classes: ["category"],
          },
          {
            name: "Subtitle",
            element: "h3",
            classes: ["document-subtitle"],
          },
          {
            name: "Info box",
            element: "p",
            classes: ["info-box"],
          },
          {
            name: "Side quote",
            element: "blockquote",
            classes: ["side-quote"],
          },
          {
            name: "Marker",
            element: "span",
            classes: ["marker"],
          },
          {
            name: "Spoiler",
            element: "span",
            classes: ["spoiler"],
          },
          {
            name: "Code (dark)",
            element: "pre",
            classes: ["fancy-code", "fancy-code-dark"],
          },
          {
            name: "Code (bright)",
            element: "pre",
            classes: ["fancy-code", "fancy-code-bright"],
          },
        ],
      },
      template: {
        definitions: [
          {
            title: "The title of the template",
            description: "A longer description of the template",
            data: () => "<p>Data inserted into the content</p>",
          },
        ],
      },
      heading: {
        options: [
          {
            model: "paragraph",
            title: "Paragraph",
            class: "ck-heading_paragraph",
          },
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
        supportAllValues: true,

        options: [
          "default",
          "Arial, Helvetica, sans-serif",
          "Courier New, Courier, monospace",
          "Georgia, serif",
          "Lucida Sans Unicode, Lucida Grande, sans-serif",
          "Tahoma, Geneva, sans-serif",
          "Times New Roman, Times, serif",
          "Trebuchet MS, Helvetica, sans-serif",
          "Verdana, Geneva, sans-serif",
          "Optima",
          "Frutiger 55",
          "Frutiger 56",
          "Frutiger 65",
          "Frutiger 66",
          "Frutiger 46 Light",
          "Frutiger 45 Light",
          "Frutiger 75 Black",
          "Frutiger 76 Black",
          "Frutiger 95 Ultra Black",
        ],
      },
      fontSize: {
        options: [10, 12, 14, "default", 18, 20, 22],
        supportAllValues: true,
      },
      htmlEmbed: {
        showPreviews: true,
      },
      importWord: {
        converterUrl:
          "https://docx-ckeditor-ckeditor.apps.development.corp.bi.go.id/v2/convert/docx-html",
        formatting: {
          resets: "none",
          defaults: "none",
          styles: "inline",
        },
      },
      exportPdf: {
        stylesheets: ["EDITOR_STYLES", "./style.css", "./fonts.css"],
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
        stylesheets: ["EDITOR_STYLES", "./style.css", "./fonts.css"],
        converterOptions: {
          format: "A4",
          margin_top: "20mm",
          margin_bottom: "20mm",
          margin_right: "24mm",
          margin_left: "24mm",
          page_orientation: "portrait",
        },
      },
      removePlugins: ["Eqneditor5"],
    },
  };

  const CSTimestamp = Date.now();
  const config = {
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
  const response = await axios.post(apiEndpoint, body, config);
  return response.data;
}
