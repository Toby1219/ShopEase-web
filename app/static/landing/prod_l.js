document.addEventListener("DOMContentLoaded", async () => {
    const product_name = document.querySelectorAll("#prod_name");
    const check_boxes_h = document.getElementById("check-b-h");
    const check_boxes_l = document.getElementById("check-b-l");
    const filter_btn = document.getElementById("filter-btn");
    const dropDownCategory = document.getElementById("categoryFilter");
    const dropDownTag = document.getElementById("tagFilter");
    const nextBtn = document.getElementById("next-btn");  
    const prevBtn = document.getElementById("prev-btn");
    const pageNum = document.querySelectorAll("#pag-num");
    
    let url_search = window.location.search;
    let currentPage = Number(url_search.split("=")[1]) || 1;
    let current_url = `${window.location.origin}/web/products`;
    let filter_args;
    
    let new_url = new URL(current_url);


    function checkBoxHandler(){        
        check_boxes_h.addEventListener("click", () => {
            check_boxes_l.checked = false;
            filter_args = "desc";
            localStorage.setItem("sort", "desc");
            new_url.searchParams.set("sort", filter_args.trim());
        })

        check_boxes_l.addEventListener("click", () => {
            check_boxes_h.checked = false;
            filter_args = "asc";
            localStorage.setItem("sort", "asc");
            new_url.searchParams.set("sort", filter_args.trim());

        })
        if (localStorage.getItem("sort")){
            if (localStorage.getItem("sort") == "desc"){
                check_boxes_h.checked = true;
            }else if (localStorage.getItem("sort") == "asc"){
                check_boxes_l.checked = true;
            }
        }

    }

    function productsHandler(){
        product_name.forEach(element => {
            let word = element.innerText.split(" ");
            let short_text = word.length >= 2 ? `${word.slice(0, 2).join(" ")} ...` : word;
            element.innerText = short_text;
        });
    }

    function dropDownHandler(){
        dropDownCategory.addEventListener("click", () => {
            filter_args = dropDownCategory.value;
            localStorage.setItem("category", dropDownCategory.value);
            new_url.searchParams.set("category", filter_args.trim());
        
        })

        dropDownTag.addEventListener("click", () => {
            filter_args = dropDownTag.value;
            localStorage.setItem("tag", dropDownTag.value);
            new_url.searchParams.set("tag", filter_args.trim());
        
        })

        if (localStorage.getItem("category")){
            dropDownCategory.value = localStorage.getItem("category");
        }
        if (localStorage.getItem("tag")){
            dropDownTag.value = localStorage.getItem("tag");
        }
    }

    function paginator_handler(){
        let count = 1
        let page_url = window.location.href;
        pageNum.forEach(ele => {
            if (ele.classList.contains("active")){
                ele.classList.remove("active")
            }
            if (ele.innerText == currentPage){
                ele.classList.add("active")
            }
            let aTag = ele.querySelector("a");
            if (aTag){    
                aTag.href = `${page_url.replace("&page=1", "")}&page=${count++}`;
            }
        })

        if (nextBtn){
            nextBtn.addEventListener("click", () => {
                new_url.searchParams.set("page", currentPage+1);
                window.location.href = new_url
            })
            if (currentPage == 5){
                nextBtn.style.display = "none";
            }
        }

        if (prevBtn){
            prevBtn.addEventListener("click", () => {
                new_url.searchParams.set("page", currentPage-1);
                window.location.href = new_url       
            })
            if (currentPage == 1){
                prevBtn.style.display = "none";

            }
        }
    }
    
    filter_btn.addEventListener("click", () => {
        new_url.searchParams.set("page", 1);
        window.location.href = new_url;
    })

    if (check_boxes_h && check_boxes_l){
        checkBoxHandler();
    }

    productsHandler();
    dropDownHandler();
    paginator_handler();

})

