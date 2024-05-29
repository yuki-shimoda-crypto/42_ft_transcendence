document.addEventListener("DOMContentLoaded", () => {
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
