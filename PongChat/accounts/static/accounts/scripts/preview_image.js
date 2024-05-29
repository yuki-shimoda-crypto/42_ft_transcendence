document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector("#id_profile_image");
  const previewImage = document.querySelector("#image-preview");

  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        previewImage.src = e.target.result;
        previewImage.style.display = "block";
      };
      reader.readAsDataURL(file);
    } else {
      previewImage.style.display = "none";
    }
  });
});
