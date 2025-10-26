document.addEventListener("DOMContentLoaded", () => {
    const Search_Btn = document.getElementById("search-btn");
    const input_text = document.getElementById("searchInput");
    let current_url = `${window.location.origin}/web/products`;

    const navItems = document.querySelectorAll("a.nav-link");

    const cartCount = document.getElementById('cartCount');
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    // const cartBtn = document.getElementById("cartIcon");
    let count = 0;

    // cartBtn.addEventListener("click"){

    // }

    addToCartButtons.forEach(button => {
        button.addEventListener('click', () => {
            count++;
            cartCount.textContent = count;
            cartCount.style.display = 'block';
        });
    });


    function searcher () {
        Search_Btn.addEventListener("click", () => {
            let new_url = new URL(current_url)
            new_url.searchParams.set("s", input_text.value.trim())
            console.log(new_url)
            window.location.href = new_url;
        })  

        input_text.addEventListener("keydown", (event) => {
            if (event.key == "Enter"){
                let new_url = new URL(current_url)
                new_url.searchParams.set("s", input_text.value.trim())
                console.log(new_url, "New URL ...")
                window.location.href = new_url;
            }
        });
    }
    
    function navHandler(){
        navItems.forEach(element => {
            element.classList.remove("active")
        })
        if (window.location.pathname === "/web/"){
            navItems[0].classList.add("active");
        }
        if (window.location.pathname === "/web/products"){
            navItems[1].classList.add("active");
        }
    }
    
    searcher();
    navHandler();

    // if (window.location.href.includes("/web/")){
    //     localStorage.removeItem("category");
    //     localStorage.removeItem("tag");
    //     localStorage.removeItem("sort");
    // }
})