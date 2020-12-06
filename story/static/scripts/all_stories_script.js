function show_category() {
    let allStories = document.querySelectorAll('.c-story-link');
    let storyWrapperElement = document.querySelector('.c-stories-wrapper');

    let btnsWrapperElements = document.querySelectorAll('.c-categories-wrapper');
    let btnsElements = document.querySelectorAll('.c-btn');

    let searchBarElement = document.getElementById('c-search-bar');
     searchBarElement.value = '';

    let headerElement = document.querySelector('.c-stories-section h2');

    btnsWrapperElements.forEach(x => x.addEventListener('click', (e) => {
            if (e.target.classList.contains('c-btn')) {
                btnsElements.forEach(x => x.classList.remove('c-btn--light'));
                searchBarElement.value = '';

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

    searchBarElement.addEventListener('input', (e) => {
        btnsElements.forEach(x => x.classList.remove('c-btn--light'));
        let searchWord = e.target.value;

        console.log(searchWord)

        if (searchWord === '') {
            headerElement.textContent = 'All stories';

            storyWrapperElement.innerHTML = '';
            allStories.forEach(x => {
                storyWrapperElement.appendChild(x);
            })
        } else {
            headerElement.textContent = `Results for: ${searchWord}`;

            storyWrapperElement.innerHTML = '';
            allStories.forEach(x => {
                if (x.querySelector('.c-story-title').textContent.toLowerCase().includes(searchWord)) {
                    storyWrapperElement.appendChild(x);
                }
            })
        }
    })
}