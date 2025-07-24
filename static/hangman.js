document.addEventListener("DOMContentLoaded", function () {
  const cells = document.querySelectorAll(".square");
  const guessInput = document.getElementById("guess");
  const stringMessage = document.getElementById("text_string");
  const alphabets = document.querySelectorAll(".square");
  const check = document.getElementById("check");
  const form = document.getElementById("Hangman-form");
  const curr_word = document.querySelector("#current_word");
  const mistakes_str = document.querySelector("#mistakes_string");
  const picture = document.querySelector("#picture");
  form.onsubmit = (event) => {
    event.preventDefault();
    fetch("/", {
      method: "POST",
      body: new FormData(form),
    })
      .then((response) => response.json())
      .then((data) => {
        stringMessage.innerHTML = data.string;
        curr_word.innerHTML = data.curr_word;
        mistakes_str.innerHTML = data.mistakes_str;
        picture.innerHTML = data.pic.trim("\n");
        alphabets.forEach((alphabet, counter) => {
          alphabet.placeholder = data.available_letters[counter];
        });
        guessInput.value = "";
        if (
          data.string === "Congratulations. You won!" ||
          data.string === "Sorry. Game Over. The word was:"
        ) {
          check.style.display = "block";
          disableCells();
        } else {
          check.style.display = "none";
          enableCells();
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };
  cells.forEach((cell) => {
    cell.onclick = () => {
      if (
        stringMessage.textContent.includes("Congratulations. You won!") ||
        stringMessage.textContent.includes("Sorry. Game Over. The word was:")
      ) {
        return;
      }
      guessInput.value = cell.placeholder;
      form.dispatchEvent(new Event("submit", { cancelable: true }));
    };
  });
});

function disableCells() {
  const cells = document.querySelectorAll(".square");
  cells.forEach((cell) => {
    cell.setAttribute("disabled", "disabled");
    cell.style.cursor = "not-allowed";
  });
}

function enableCells() {
  const cells = document.querySelectorAll(".square");
  cells.forEach((cell) => {
    cell.removeAttribute("disabled");
    cell.style.cursor = "pointer";
  });
}
