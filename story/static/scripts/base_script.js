function scrollToTop() {
    let scrollToTopButton = document.getElementById('js-top');

    let scrollFunc = () => {
        let y = window.scrollY;

        if (y > 100) {
            scrollToTopButton.classList.remove('hide');
            scrollToTopButton.classList.add('show');
        } else {
            scrollToTopButton.classList.remove('show');
            scrollToTopButton.classList.add('hide');
        }
    };

    window.addEventListener("scroll", scrollFunc);

    let scrollToTop = () => {
        let c = document.documentElement.scrollTop || document.body.scrollTop;

        if (c > 0) {
            window.requestAnimationFrame(scrollToTop);
            window.scrollTo(0, c - c / 10);
        }
    };

    scrollToTopButton.onclick = function (e) {
        e.preventDefault();
        scrollToTop();
    }
}