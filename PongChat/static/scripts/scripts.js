document.addEventListener("DOMContentLoaded", () => {
  loadContent(window.location.href);

  document.body.addEventListener("click", handleClick);

  // ブラウザの戻る/進むボタンの対応
  window.addEventListener("popstate", (event) => {
    if (event.state && event.state.path) {
      // pushStateがtrueだと進む戻るの履歴が消されていまうのでfalse
      loadContent(event.state.path, false);
    }
  });
});

function handleClick(event) {
  if (
    event.target.tagName === "A" &&
    event.target.classList.contains("async-link") // async-linkクラスを持つリンクのみloadContentを呼び出す
  ) {
    event.preventDefault();
    const url = event.target.href;
    loadContent(url);
  }
}

function loadContent(url, pushState = true) {
  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }
      return response.text();
    })
    .then((html) => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      const newContent = doc.querySelector("#content-placeholder");
      const currentContent = document.querySelector("#content-placeholder");
      if (newContent && currentContent) {
        currentContent.innerHTML = newContent.innerHTML;

        // タイトルを更新
        const newTitle = doc.querySelector("title");
        if (newTitle) {
          document.title = newTitle.textContent;
        }
        // URLを更新
        if (pushState) {
          history.pushState({ path: url }, "", url);
        }
        // スクロール位置をトップに戻す、引数によって戻すかどうかを判定した方が良いかも
        window.scrollTo(0, 0);
        // ドロップダウンを閉じる
        const openDropdowns = document.querySelectorAll(".dropdown-menu.show");
        openDropdowns.forEach((dropdown) => {
          dropdown.classList.remove("show");
          const dropdownToggleButton = dropdown.previousElementSibling; // ドロップダウンのボタン要素を取得
          if (
            dropdownToggleButton &&
            dropdownToggleButton.classList.contains("dropdown-toggle")
          ) {
            dropdownToggleButton.classList.remove("show");
            dropdownToggleButton.setAttribute("aria-expanded", "false");
          }
        });
      }
    })
    .catch((error) => console.error("Failed to fetch:", error));
}
