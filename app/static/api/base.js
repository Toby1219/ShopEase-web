document.addEventListener("DOMContentLoaded", () => {
    const menu = document.getElementById("menuBox");
    const open_btn = document.getElementById("menu-btn");

    function close_menu() {
        menu.style.display = "none";
        open_btn.innerHTML = '<i class="fa fa-bars" style="font-size: 27px;"></i>'
        open_btn.dataset.status = "open"
    }

    open_btn.addEventListener("click", () => {
        if (open_btn.dataset.status == "open") {
            menu.style.display = "flex";
            open_btn.innerHTML = '<i class="fa fa-times" style="font-size: 27px;"></i>'
            open_btn.dataset.status = "close"
        }
        else {
            close_menu();
        }

    })

})