document.addEventListener("DOMContentLoaded", () => {
  console.log("hello");
  document.body.addEventListener("click", (event) => {
    if (
      event.target.tagName === "A" &&
      event.target.classList.contains("async-link")
    ) {
      console.log("success");
      event.preventDefault();
      const url = event.target.href;
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          return response.text();
        })
        .then((html) => {
          // console.log(html);
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newContent = doc.querySelector("#content-placeholder");
          const currentContent = document.querySelector("#content-placeholder");
          if (newContent && currentContent) {
            console.log("newContent true");
            currentContent.innerHTML = newContent.innerHTML;
            history.pushState({ path: url }, "", url);
          }
        })
        .catch((error) => console.error("Failed to fetch:", error));
    }
  });
});
