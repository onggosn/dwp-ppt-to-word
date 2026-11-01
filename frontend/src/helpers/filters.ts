const filters = {
  getDocumentExtension(value) {
    const temp = value.split(".");
    return temp[temp.length - 1];
  },
};
export default filters;
