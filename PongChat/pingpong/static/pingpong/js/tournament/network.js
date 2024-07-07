function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export function sendWinner(winner_id) {
  fetch("tournament_play", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ winner_id: winner_id }),
  }).then((response) => {
    if (response.redirected) {
      setTimeout(() => {
        window.location.href = response.url;
      }, 2000);
    }
  });
  // .then((data) => {
  //   console.log(data);
  // })
  // .catch((error) => {
  //   console.error(
  //     "There has been a problem with your fetch operation:",
  //     error
  //   );
  // }
  // );
}
