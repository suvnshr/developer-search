const tabs = document.querySelector(".tabs");
M.Tabs.init(tabs, {});



document.addEventListener("DOMContentLoaded", function () {

    const searchField = document.querySelector("#search-field");
    const footer = document.querySelector("footer");
    const themeToggle = document.querySelector("#theme-toggle");

    const pageStyle = window.getComputedStyle(document.body);

    if(pageStyle['backgroundColor'] === "rgb(34, 34, 34)") {
        themeToggle.textContent = "🌞 Day Mode";
        themeToggle.href =  LIGHT_THEME_URL;
    } else {
        themeToggle.textContent = "🌙 Night Mode";
        themeToggle.href =  DARK_THEME_URL;
    }

    if(screen.width < 600) {

        searchField.addEventListener("focus", function () {
            footer.style.opacity = 0;
        });
    
        searchField.addEventListener("blur", function () {
            footer.style.opacity = 1;
        })

    }
    
});


