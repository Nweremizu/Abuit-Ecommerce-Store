// JavaScript to toggle mobile menu visibility
document.getElementById('mobile-menu-button').addEventListener('click', function () {
    let mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.toggle('tw-opacity-100');
    mobileMenu.classList.toggle('tw-pointer-events-auto');
});

// JavaScript to close mobile menu when close button is clicked
document.getElementById('close-menu-button').addEventListener('click', function () {
    let mobileMenu = document.getElementById('mobile-menu');
    mobileMenu.classList.remove('tw-opacity-100');
    mobileMenu.classList.remove('tw-pointer-events-auto');
});

function togglesearch() {
    console.log("fjddfkjfdkjfd")
    document.querySelector('.search').classList.toggle('open-search');
    document.querySelector('.s-holder').classList.toggle('hide-now')
}

s = document.querySelector('#search-icon')
s.addEventListener('click', togglesearch)


function toggleCart() {
    document.querySelector('.sidecart').classList.toggle('open-cart');
}

cart = document.querySelector('.cart_button')
cart.addEventListener('click', toggleCart)

function togglefilter() {
    document.querySelector('.sidefilter').classList.toggle('open-filter');
}

let filter_btn = document.querySelector('.filter-btn')
filter_btn.addEventListener('click', togglefilter)

// get all filter articles header
const filter_article_header = document.querySelectorAll('.filter-group header')
// if any of the filter article header is clicked toggle the collapse
filter_article_header.forEach(header => {
    header.addEventListener('click', () => {
        header.nextElementSibling.classList.toggle('collapse')
    })
})



