document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle");
  const caseNumberInput = document.getElementById("case-number");
  const courtsList = document.getElementById("courts-list");
  const selectAllButton = document.getElementById("select-all");
  const deselectAllButton = document.getElementById("deselect-all");
  const checkStatusButton = document.getElementById("check-status");
  const searchForm = document.getElementById("search-form");
  const resultsContainer = document.getElementById("results");
  const validationMessage = document.getElementById("validation-message");

  // Theme toggle
  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");
  });

  // Auto-format case number
  caseNumberInput.addEventListener("input", () => {
    let value = caseNumberInput.value.replace(/\D/g, "");
    if (value.length > 20) {
      value = value.slice(0, 20);
    }

    let formattedValue = "";
    if (value.length > 0) {
      formattedValue = value.slice(0, 7);
    }
    if (value.length > 7) {
      formattedValue += `-${value.slice(7, 9)}`;
    }
    if (value.length > 9) {
      formattedValue += `.${value.slice(9, 13)}`;
    }
    if (value.length > 13) {
      formattedValue += `.${value.slice(13, 14)}`;
    }
    if (value.length > 14) {
      formattedValue += `.${value.slice(14, 16)}`;
    }
    if (value.length > 16) {
      formattedValue += `.${value.slice(16, 20)}`;
    }
    caseNumberInput.value = formattedValue;
  });

  // Fetch and display courts
  fetch("/courts")
    .then((response) => response.json())
    .then((courts) => {
      for (const category in courts) {
        const categoryContainer = document.createElement("div");
        categoryContainer.classList.add("mb-3");
        const categoryTitle = document.createElement("h4");
        categoryTitle.textContent = category;
        categoryContainer.appendChild(categoryTitle);

        courts[category].forEach((court) => {
          const checkbox = document.createElement("div");
          checkbox.classList.add("form-check");
          checkbox.innerHTML = `
                        <input class="form-check-input" type="checkbox" value="${court}" id="court-${court}">
                        <label class="form-check-label" for="court-${court}">
                            ${court.toUpperCase()}
                        </label>
                    `;
          categoryContainer.appendChild(checkbox);
        });
        courtsList.appendChild(categoryContainer);
      }
    });

  // Select/Deselect all courts
  selectAllButton.addEventListener("click", () => {
    courtsList
      .querySelectorAll('input[type="checkbox"]')
      .forEach((checkbox) => {
        checkbox.checked = true;
      });
  });

  deselectAllButton.addEventListener("click", () => {
    courtsList
      .querySelectorAll('input[type="checkbox"]')
      .forEach((checkbox) => {
        checkbox.checked = false;
      });
  });

  // Check court status
  checkStatusButton.addEventListener("click", () => {
    const selectedCourts = Array.from(
      courtsList.querySelectorAll("input:checked")
    ).map((checkbox) => checkbox.value);
    validationMessage.textContent = "";

    if (selectedCourts.length === 0) {
      validationMessage.textContent = "Please select at least one court.";
      return;
    }

    fetch("/status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tribunais: selectedCourts,
      }),
    })
      .then((response) => response.json())
      .then((results) => {
        resultsContainer.innerHTML = "";
        const list = document.createElement("ul");
        list.classList.add("list-group");
        for (const court in results) {
          const listItem = document.createElement("li");
          listItem.classList.add("list-group-item");
          const status = results[court].success ? "Online" : "Offline";
          listItem.innerHTML = `<strong>${court.toUpperCase()}:</strong> ${status}`;
          list.appendChild(listItem);
        }
        resultsContainer.appendChild(list);
      });
  });

  // Search form submission
  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const caseNumber = caseNumberInput.value;
    const selectedCourts = Array.from(
      courtsList.querySelectorAll("input:checked")
    ).map((checkbox) => checkbox.value);
    validationMessage.textContent = "";

    if (!caseNumber || selectedCourts.length === 0) {
      validationMessage.textContent =
        "Please enter a case number and select at least one court.";
      return;
    }

    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        numero: caseNumber,
        tribunais: selectedCourts,
      }),
    })
      .then((response) => response.json())
      .then((results) => {
        resultsContainer.innerHTML = "";
        if (results.length === 0) {
          resultsContainer.innerHTML = "<p>No results found.</p>";
          return;
        }

        results.forEach((result) => {
          const sanitizedId = result.numeroProcesso.replace(
            /[^a-zA-Z0-9]/g,
            ""
          );
          const resultElement = document.createElement("div");
          resultElement.classList.add("card", "mb-3");
          resultElement.innerHTML = `
                    <div class="card-header">
                        ${result.tribunal}
                    </div>
                    <div class="card-body">
                        <p><strong>Número:</strong> ${result.numeroProcesso}</p>
                        <p><strong>Classe:</strong> ${result.classe.nome}</p>
                        <p><strong>Data de Ajuizamento:</strong> ${new Date(
                          result.dataAjuizamento
                        ).toLocaleDateString()}</p>
                        <button class="btn btn-sm btn-primary" data-bs-toggle="collapse" data-bs-target="#details-${sanitizedId}">
                            Show Details
                        </button>
                        <div id="details-${sanitizedId}" class="collapse mt-3">
                            <pre>${JSON.stringify(result, null, 2)}</pre>
                        </div>
                    </div>
                `;
          resultsContainer.appendChild(resultElement);
        });
      });
  });
});
