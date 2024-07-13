document.addEventListener("DOMContentLoaded", () => {
  const processNameElement = document.querySelector("#process-name");
  const processName = processNameElement.textContent;
  if (
    !processName.includes("Update Profile Image") &&
    !processName.includes("Sign Up")
  ) {
    return;
  }
  // Update Profile Imageの場合のみ以下の処理を実行
  const fileInput = document.querySelector("#id_profile_image");
  const previewImage = document.querySelector("#image-preview");

  fileInput.addEventListener("change", () => {
    const updatedFile = fileInput.files[0];
    if (updatedFile) {
      const reader = new FileReader(); // FileReaderはファイルを非同期で読み取るためのAPI
      reader.onload = (event) => {
        previewImage.src = event.target.result;
        previewImage.style.display = "block";
      };
      reader.readAsDataURL(updatedFile);
    } else {
      previewImage.style.display = "none";
    }
  });
});
