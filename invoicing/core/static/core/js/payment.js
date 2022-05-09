let RESULT_BOX;
window.onload = () => {
  RESULT_BOX = document.getElementById("results");
}

const process = () => {
  helcimProcess().then(resp => {
    const parse = new DOMParser();
    const xml = parse.parseFromString(resp, "text/html");
    const code = xml.getElementById("response").value;
    const msg = xml.getElementById("responseMessage").value;
    if (code === "0") { // if failed
      RESULT_BOX.innerHTML = msg;
    } else { // if successful
      RESULT_BOX.innerHTML = msg;
    }
    console.log(code + ": " + msg);
  }).catch(error => {
    if (error){
      console.err(error);
    }
  });
}
