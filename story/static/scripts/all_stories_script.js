function show_category() {
    let allStories = document.querySelectorAll('.c-story-link');
    let storyWrapperElement = document.querySelector('.c-stories-wrapper');

    let btnsWrapperElements = document.querySelectorAll('.c-categories-wrapper');
    let btnsElements = document.querySelectorAll('.c-btn')

    let headerElement = document.querySelector('.c-stories-section h2');

    console.log(btnsWrapperElements)

    btnsWrapperElements.forEach(x => x.addEventListener('click', (e) => {
            if (e.target.classList.contains('c-btn')) {
                btnsElements.forEach(x => x.classList.remove('c-btn--light'));

                e.target.classList.add('c-btn--light');

                let currCategory = e.target.textContent.toLowerCase();
                headerElement.textContent = currCategory;
                storyWrapperElement.innerHTML = '';
                allStories.forEach(x => {
                    if (x.classList.contains(currCategory.split(' ').join('-'))) {
                        storyWrapperElement.appendChild(x);
                    }
                })
            }

        }
    ))
}