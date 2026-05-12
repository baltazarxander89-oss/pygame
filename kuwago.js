document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", function(e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {
            const navHeight = document.querySelector(".navbar").offsetHeight;

            window.scrollTo({
                top: target.offsetTop - navHeight,
                behavior: "smooth"
            });
        }
    });
});