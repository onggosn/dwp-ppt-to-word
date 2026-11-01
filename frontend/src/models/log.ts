import client from "@/library/ApiClient";
import store from "@/store/index";

interface Log {
  traceId: string;
  documentId: string;
  documentName: string;
  fileSize: number;
  timeExecution: number;
  description: string;
}

export function insertLog(
  _traceId,
  _documentId,
  _documentName,
  _fileSize,
  _timeStart,
  _timeEnd,
  _description
): void {
  const log: Log = {} as Log;
  log.traceId = _traceId;
  log.documentId = _documentId;
  log.documentName = _documentName;
  log.fileSize = _fileSize;
  log.timeExecution = _timeEnd - _timeStart;
  log.description = _description;

  client
    .writeLog({
      store: store,
      data: log,
    })
    .then(() => {
      switch (true) {
        case _description.toLowerCase().includes("download"): {
          console.log("A download log has been written");
          break;
        }
        case _description.toLowerCase().includes("preview"): {
          console.log("A preview log has been written");
          break;
        }
        case _description.toLowerCase().includes("render"): {
          console.log("A render preview log has been written");
          break;
        }
        case _description.toLowerCase().includes("upload"): {
          console.log("An upload log has been written");
          break;
        }
        case _description.toLowerCase().includes("approval"): {
          console.log("An approval log has been written");
          break;
        }
        case _description.toLowerCase().includes("create"): {
          console.log("A create document log has been written");
          break;
        }
      }
    })
    .catch(() => {
      switch (true) {
        case _description.toLowerCase().includes("download"): {
          console.log("A download log not written");
          break;
        }
        case _description.toLowerCase().includes("preview"): {
          console.log("A preview log not written");
          break;
        }
        case _description.toLowerCase().includes("render"): {
          console.log("A render preview log not written");
          break;
        }
        case _description.toLowerCase().includes("upload"): {
          console.log("An upload log not written");
          break;
        }
        case _description.toLowerCase().includes("approval"): {
          console.log("An approval log not written");
          break;
        }
        case _description.toLowerCase().includes("create"): {
          console.log("A create document log not written");
          break;
        }
      }
    })
    .finally(() => {
      console.info(log);
    });
}

export function consoleLog(params) {
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "devdigiworkplace"
  ) {
    console.log("source: " + window.location.hostname);
    console.log(params);
  }
}

export function consoleTable(params) {
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "devdigiworkplace.corp.bi.go.id"
  ) {
    console.log("source: " + window.location.hostname);
    console.table(params);
  }
}

export function consoleJSON(params) {
  if (
    window.location.hostname === "localhost" ||
    window.location.hostname === "devdigiworkplace.corp.bi.go.id"
  ) {
    console.log("source: " + window.location.hostname);
    console.log(JSON.stringify(params, null, 4));
  }
}
