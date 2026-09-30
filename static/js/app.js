/* =================================
   PocketSmart AI - Global JavaScript
   Used by all HTML pages
================================= */

document.addEventListener("DOMContentLoaded", () => {

    console.log("PocketSmart AI loaded");

    /* ===============================
       Helper
    =============================== */

    function escapeHtml(value) {
        return String(value ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }


    /* ===============================
       Planner Submit
    =============================== */

    async function submitPlanner(form, endpoint, resultBox) {

        const formData = new FormData(form);

        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        resultBox.innerHTML = `
            <div class="stat">
                <span>Generating recommendations...</span>
                <span>⏳</span>
            </div>
        `;

        try {

            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.detail || "Something went wrong"
                );
            }

            displayResult(result, resultBox);

        } catch (error) {

            console.error(error);

            resultBox.innerHTML = `
                <div class="error">
                    <strong>Error:</strong>
                    ${escapeHtml(error.message)}
                </div>
            `;
        }
    }


    /* ===============================
       Display Recommendation
    =============================== */

    function displayResult(result, resultBox) {

        let html = "";

        if (typeof result === "string") {

            html = `
                <article>
                    ${escapeHtml(result)}
                </article>
            `;

        } else if (result.recommendations) {

            html += `
                <article>
                    <h2>✨ AI Recommendations</h2>
            `;

            if (Array.isArray(result.recommendations)) {

                result.recommendations.forEach((item) => {

                    html += `
                        <div class="row">

                            <div>
                                <strong>
                                    ${escapeHtml(
                                        item.name ||
                                        item.title ||
                                        "Recommendation"
                                    )}
                                </strong>

                                <p>
                                    ${escapeHtml(
                                        item.description || ""
                                    )}
                                </p>
                            </div>

                            ${
                                item.price
                                    ? `<strong>₹${escapeHtml(
                                        String(item.price)
                                    )}</strong>`
                                    : ""
                            }

                        </div>
                    `;
                });

            } else {

                html += `
                    <p>
                        ${escapeHtml(
                            String(result.recommendations)
                        )}
                    </p>
                `;
            }

            html += `</article>`;

        } else {

            html = `
                <article>
                    <h2>✨ Recommendation</h2>

                    <pre>${escapeHtml(
                        JSON.stringify(result, null, 2)
                    )}</pre>
                </article>
            `;
        }

        resultBox.innerHTML = html;
    }


    /* ===============================
       Home Planner
    =============================== */

    const homeForm = document.getElementById("home-form");
    const homeResult = document.getElementById("result");

    if (homeForm && homeResult) {

        homeForm.addEventListener("submit", (event) => {

            event.preventDefault();

            submitPlanner(
                homeForm,
                "/generate-home",
                homeResult
            );
        });
    }


    /* ===============================
       Party Planner
    =============================== */

    const partyForm = document.getElementById("party-form");
    const partyResult = document.getElementById("result");

    if (partyForm && partyResult) {

        partyForm.addEventListener("submit", (event) => {

            event.preventDefault();

            submitPlanner(
                partyForm,
                "/generate-party",
                partyResult
            );
        });
    }


    /* ===============================
       Jewelry Planner
    =============================== */

    const jewelryForm =
        document.getElementById("jewelry-form");

    const jewelryResult =
        document.getElementById("result");

    if (jewelryForm && jewelryResult) {

        jewelryForm.addEventListener(
            "submit",
            async (event) => {

                event.preventDefault();

                const formData =
                    new FormData(jewelryForm);

                jewelryResult.innerHTML = `
                    <div class="stat">
                        <span>
                            Analyzing your jewelry preferences...
                        </span>
                        <span>💎</span>
                    </div>
                `;

                try {

                    const response = await fetch(
                        "/generate-jewelry",
                        {
                            method: "POST",
                            body: formData
                        }
                    );

                    const result =
                        await response.json();

                    if (!response.ok) {

                        throw new Error(
                            result.detail ||
                            "Jewelry recommendation failed"
                        );
                    }

                    displayResult(
                        result,
                        jewelryResult
                    );

                } catch (error) {

                    console.error(error);

                    jewelryResult.innerHTML = `
                        <div class="error">
                            <strong>Error:</strong>
                            ${escapeHtml(
                                error.message
                            )}
                        </div>
                    `;
                }
            }
        );
    }


    /* ===============================
       Logout
    =============================== */

    const logoutButtons =
        document.querySelectorAll("[data-logout]");

    logoutButtons.forEach((button) => {

        button.addEventListener(
            "click",
            async (event) => {

                event.preventDefault();

                try {

                    await fetch(
                        "/logout",
                        {
                            method: "POST"
                        }
                    );

                    window.location.href =
                        "/login";

                } catch (error) {

                    console.error(
                        "Logout failed:",
                        error
                    );
                }
            }
        );
    });


    /* ===============================
       Mobile Menu / General Buttons
    =============================== */

    const menuButton =
        document.getElementById("menu-button");

    const mobileMenu =
        document.getElementById("mobile-menu");

    if (menuButton && mobileMenu) {

        menuButton.addEventListener(
            "click",
            () => {

                mobileMenu.classList.toggle(
                    "show"
                );
            }
        );
    }

});