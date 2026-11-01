export const downloadFileHelper = (response, fileName) => {
  try {
    const link = document.createElement("a");

    const url = window.URL.createObjectURL(response.data);

    link.href = url;
    link.setAttribute("download", `${fileName}`);
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    console.error("Download failed:", e);
  }
};
