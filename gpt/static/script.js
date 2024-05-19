document.addEventListener('DOMContentLoaded', function() {
    const themeSelector = document.getElementById('themeSelector');

    themeSelector.addEventListener('change', function() {
        const selectedTheme = themeSelector.value;
        if (selectedTheme === 'dark') {
            document.getElementById('html-tag').classList.add('dark-theme');
        } else {
            document.getElementById('html-tag').classList.remove('dark-theme');
        }
    });
});

/* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.getElementById("main").style.marginRight = "250px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.getElementById("main").style.marginRight = "0";
  }