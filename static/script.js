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
  const searchButton = searchForm.querySelector("button[type='submit']");
  const originalButtonText = {};

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
        const categoryCard = document.createElement("div");
        categoryCard.classList.add("card");

        const cardHeader = document.createElement("div");
        cardHeader.classList.add("card-header");
        cardHeader.textContent = category;
        categoryCard.appendChild(cardHeader);

        const cardBody = document.createElement("div");
        cardBody.classList.add("card-body");

        courts[category].forEach((court) => {
          const checkbox = document.createElement("div");
          checkbox.classList.add("form-check");
          checkbox.innerHTML = `
                        <input class="form-check-input" type="checkbox" value="${court}" id="court-${court}">
                        <label class="form-check-label" for="court-${court}">
                            ${court.toUpperCase()}
                        </label>
                    `;
          cardBody.appendChild(checkbox);
        });

        categoryCard.appendChild(cardBody);
        courtsList.appendChild(categoryCard);
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

  // Loading state helper
  const setLoading = (button, isLoading) => {
    if (isLoading) {
      originalButtonText[button.id] = button.innerHTML;
      button.disabled = true;
      // Use Font Awesome 7 spinner + pulse animation
      button.innerHTML = `<i class="fa-solid fa-spinner fa-spin-pulse"></i> Carregando...`;
      resultsContainer.style.opacity = "0.5";
    } else {
      button.disabled = false;
      button.innerHTML = originalButtonText[button.id];
      resultsContainer.style.opacity = "1";
    }
  };

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

    setLoading(checkStatusButton, true);

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
        const grid = document.createElement("div");
        grid.classList.add("status-grid");

        for (const court in results) {
          const item = document.createElement("div");
          item.classList.add("status-item");
          const status = results[court].success
            ? '<span class="text-success"><i class="fa-solid fa-circle-check"></i> Online</span>'
            : '<span class="text-danger"><i class="fa-solid fa-circle-xmark"></i> Offline</span>';
          item.innerHTML = `<strong>${court.toUpperCase()}</strong>: ${status}`;
          grid.appendChild(item);
        }
        resultsContainer.appendChild(grid);
        resultsContainer.classList.add("fade-in");
      })
      .finally(() => {
        setLoading(checkStatusButton, false);
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

    setLoading(searchButton, true);

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
                        <div class="card-header d-flex justify-content-between align-items-center">
                            ${result.tribunal}
                            <span class="badge bg-${
                              result.grau === "1º Grau"
                                ? "primary"
                                : "secondary"
                            }">${result.grau}</span>
                        </div>
                        <div class="card-body">
                            <p><strong>Número:</strong> ${
                              result.numeroProcesso
                            }</p>
                            <p><strong>Classe:</strong> ${
                              result.classe.nome
                            }</p>
                            <p><strong>Data de Ajuizamento:</strong> ${new Date(
                              result.dataAjuizamento
                            ).toLocaleDateString()}</p>
                            <button class="btn btn-sm btn-outline-primary" data-bs-toggle="collapse" data-bs-target="#details-${sanitizedId}">
                                <i class="fa-solid fa-circle-info"></i> Show Details
                            </button>
                            <div id="details-${sanitizedId}" class="collapse mt-3">
                                <pre>${JSON.stringify(result, null, 2)}</pre>
                            </div>
                        </div>
                    `;
          resultsContainer.appendChild(resultElement);
        });
        resultsContainer.classList.add("fade-in");
      })
      .finally(() => {
        setLoading(searchButton, false);
      });
  });
});
