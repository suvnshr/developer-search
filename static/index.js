const tabs = document.querySelector(".tabs");
M.Tabs.init(tabs, {});

function prepareForLightTheme(themeToggle) {
  themeToggle.textContent = "🌞 Day Mode";
  themeToggle.href = LIGHT_THEME_URL;
  themeToggle.style.opacity = 1;
}

function prepareForDarkTheme(themeToggle) {
  themeToggle.textContent = "🌙 Night Mode";
  themeToggle.href = DARK_THEME_URL;
  themeToggle.style.opacity = 1;
}

function prepareForNextTheme(themeToggle) {
  const pageStyle = window.getComputedStyle(document.body);

  if (pageStyle["backgroundColor"] === "rgb(34, 34, 34)") {
    prepareForLightTheme(themeToggle);
  } else {
    prepareForDarkTheme(themeToggle);
  }
}

function clearThemeQueryParameter() {
  const currentUrlParams = window.location.search.toString();

  const urlSearchParamObj = new URLSearchParams(currentUrlParams);

  urlSearchParamObj.delete("theme");

  let newParams = urlSearchParamObj.toString();

  if (newParams.length) newParams = "?" + newParams;

  const newUrl = window.location.pathname + newParams + window.location.hash;

  window.history.replaceState({}, document.title, newUrl);
}

document.addEventListener("DOMContentLoaded", function () {
  const searchField = document.querySelector("#search-field");
  const footer = document.querySelector("footer");
  const themeToggle = document.querySelector("#theme-toggle");
  const darkModeMediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

  setTimeout(() => prepareForNextTheme(themeToggle), 600);

  clearThemeQueryParameter();

  darkModeMediaQuery.addEventListener("change", (e) => {
    if (!overide_preferred_color_scheme) {
      const darkModeOn = e.matches;

      darkModeOn
        ? prepareForLightTheme(themeToggle)
        : prepareForDarkTheme(themeToggle);
      // console.log(`Dark mode is ${darkModeOn ? "🌒 on" : "☀️ off"}.`);
    }
  });

  function setListenerToHideFooter() {
    searchField.addEventListener("focus", function () {
      if (screen.width < 600) {
        footer.style.opacity = 0;
      }
    });

    searchField.addEventListener("blur", function () {
      footer.style.opacity = 1;
    });
  }

  setListenerToHideFooter();
});
