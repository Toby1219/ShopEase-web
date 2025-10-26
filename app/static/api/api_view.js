// let current_url = window.location.href;
const txtArea = document.getElementById("txt-data");
const paganationButtons = document.getElementById("pag");
const menu = document.getElementById('menuBox');
let icon_m = document.getElementById("menu-toggle_b");
const search_input = document.getElementById("searchInput");
const loader = document.getElementById("loader");


function copyJSON() {
  const copy_tag = document.getElementById("smallBtn");
  const pre = document.getElementById("txt-data");
  const text = pre.textContent || pre.innerText;

  navigator.clipboard.writeText(text)
  // .then(() => {
  //   alert('JSON copied to clipboard!');

  // })
  // .catch(err => {
  //   console.error('Copy failed', err);
  //   alert('Failed to copy JSON.');
  // });

  copy_tag.addEventListener("click", () => {
    copy_tag.innerText = "✓ Copied";
    setTimeout(() => {
      copy_tag.innerText = "copy";
    }, 1500)
  })

}


// all API Calls

document.addEventListener("DOMContentLoaded", async () => {
  const code_box = document.getElementById("txt-data");
  const status_text = document.getElementById("status-text");
  const profile = document.getElementById("profile");
  const email = localStorage.getItem("email");
  // const password = localStorage.getItem("password");
  let token = localStorage.getItem("access_token");

  const btn_logout = document.getElementById("log-out");
  
  // Pagination
  let pageNum;
  const pag_box = document.getElementById("paginator");
  const next_btn = document.getElementById("pag-btnNext");
  const prev_btn = document.getElementById("pag-btnPrev");
  let total_item = document.getElementById("total-item");
  let total_page = document.getElementById("total-page");
  let current_page = document.getElementById("curpage");

  let url_params = {};

  const all_prod = document.getElementById("all-prod");

  const options_1 = document.getElementById("option-1");
  const options_2 = document.getElementById("option-2");
  const options_3 = document.getElementById("option-3");
  const options_4 = document.getElementById("option-4");
  const filterBtn = document.getElementById("filter");
  const Notify = document.getElementById("api-notifi");
  const searchInput = document.getElementById("searchInput");
  const searchBtn = document.getElementById("search-btn");

  const radio_btns = document.getElementsByName("priceOpt");

  let caller;

  prev_btn.style.display = "none"
  pag_box.style.display = "none";

  // Helper function for requests
  async function fetchData(url, method = "GET", body = null, token = null) {
    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (token) {
      options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (body) {
      options.body = JSON.stringify(body);
    }
    // console.log(options)
    const response = await fetch(url, options);
    const data = await response.json();
    // If token expired, you can handle it below
    if (response.status === 401 && data.msg?.includes("expired")) {
      console.log("TokenExpired");
      Notify.innerText = "All Token have Expired.";
      status_text.innerText = response.status;
      status_text.style.color = "red";
    }
    return { data, status: response.status };
  }

  async function login(email, password) {
    const { data, status } = await fetchData("/api/auth", "POST", { email });
    if (status === 200) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("access_token_exp", data.access_token_exp * 1000);
      localStorage.setItem("refresh_token_exp", data.refresh_token_exp * 1000);
      Notify.innerText = "✅ Logged in";
    } else {
      Notify.innerText = "❌ Login failed";
      status_text.innerText = response.status;
      status_text.style.color = "red";
    }
  }

  async function refreshToken() {
    const refresh = localStorage.getItem("refresh_token");
    const { data, status } = await fetchData("/api/auth", "PUT", body=null, token=refresh);
    if (status === 200) {
      localStorage.setItem("access_token", data.access_token);
      Notify.innerText = "✅ Token refreshed!";
    } else if (status === 401) {
      Notify.innerText = "❌ Refresh failed, please log in again.";
      localStorage.removeItem("access");
      status_text.innerText = response.status;
      status_text.style.color = "red";
    }
  }

  // get profile
  async function getProfile() {
    let access = localStorage.getItem("access_token");
    try {
      const {data, status} = await fetchData("/api/auth", "GET", null, access);
      status_text.innerText = status;
      Notify.innerText = "👤 Profile";
      code_box.textContent = JSON.stringify(data, null, 2);
      Prism.highlightElement(code_box);
    } catch (err) {
      if (err.message === "TokenExpired" || Date.now() > localStorage.getItem("access_token_exp")) {
        status_text.innerText = s;
        Notify.innerText = "🔁 Access token expired, refreshing...";
        await refreshToken();
        return getProfile(); // retry after refresh
      } else {
        console.error(err);
      }
    }
  }

  // search api
  async function search(params, method="GET") {
    let url_param = new URLSearchParams(params);
    let url = `/api/search?${url_param.toString()}`
    console.log(url)
    let access = localStorage.getItem("access_token");
    Notify.innerText = `Search ${params.name || params.tag || params.category || params.sku}`;
    try{
      const {data, status} = await fetchData(url, method, body=null, token=access);
      status_text.innerText = status;
      code_box.textContent = JSON.stringify(data, null, 2);
      current_page.innerText = data.page;
      total_page.innerText = data.total_pages;
      total_item.innerText = `Total product: ${data.total_items}`;
      pag_handler(Number(current_page.innerText), Number(total_page.innerText))
    }catch (err){
      if (err.message === "TokenExpired" || Date.now() > localStorage.getItem("access_token_exp")) {
        await refreshToken();
        return get_all_prod();
      }
    }
    Prism.highlightElement(code_box);
    caller = search;
    
  }

  async function get_all_prod(params){
      let access = localStorage.getItem("access_token");
      let url_param = new URLSearchParams(params)
      let url = `/api?${url_param.toString()}`

      Notify.innerText = "Get all Products";
      try{
        const {data, status} = await fetchData(url, method="GET", body=null, token=access);
        status_text.innerText = status;
        code_box.textContent = JSON.stringify(data, null, 2);
        current_page.innerText = data.page;
        total_page.innerText = data.total_pages;
        total_item.innerText = `Total product: ${data.total_items}`;
        pag_handler(Number(current_page.innerText), Number(total_page.innerText))

      } catch (err){
        if (err.message === "TokenExpired" || Date.now() > localStorage.getItem("access_token_exp")) {
          await refreshToken();
          return get_all_prod();
        }
      }
    Prism.highlightElement(code_box);
    caller = get_all_prod;

    
  }

  function pag_handler(c, t){
    prev_btn.style.display = "inline";
    next_btn.style.display = "inline";
    if (c == t){
      next_btn.style.display = "none";
    }
    if (c == 1){
      prev_btn.style.display = "none";
    }
    if (c == 1 && t == 1) {
      prev_btn.style.display = "none";
      next_btn.style.display = "none";
    }

  }
  
  options_1.addEventListener("change", async () => {
    selectedValue = options_1.value;
    url_params["name"] = selectedValue;
    delete url_params.sku;
    delete url_params.category;
    delete url_params.tag;  
  });
  
  options_2.addEventListener("change", () => {
    selectedValue = options_2.value;
    url_params["sku"] = selectedValue;
    delete url_params.name;
    delete url_params.category;
    delete url_params.tag;
  });
  
  options_3.addEventListener("change", () => {
    selectedValue = options_3.value;
    url_params["category"] = selectedValue;
    delete url_params.name;
    delete url_params.sku;
    delete url_params.tag;
  });
  
  options_4.addEventListener("change", () => {
    selectedValue = options_4.value;
    url_params["tag"] = selectedValue;
    delete url_params.name;
    delete url_params.sku;
    delete url_params.category;
  });
  
  radio_btns.forEach(element => {
    element.addEventListener("change", () => {
      url_params['sort'] = element.value;
    })  
  });

  filterBtn.addEventListener("click", async () => {
    current_page.innerText = "";
    total_page.innerText = "";
    pag_box.style.display = "block";
    await search(url_params);
  })

  window.addEventListener("keydown", async (event) => {
    if (event.key == "Enter"){
      url_params["query"] = searchInput.value;
      delete url_params.name;
      delete url_params.sku;
      delete url_params.tag;
      delete url_params.category;
      await search(url_params);
    }
    
  })

  searchBtn.addEventListener("click", async () => {
    url_params["query"] = searchInput.value;
    delete url_params.name;
    delete url_params.sku;
    delete url_params.tag;
    delete url_params.category;
    await search(url_params);
  })
  
  prev_btn.addEventListener("click", async () => {
    let pp = Number(current_page.innerText) - 1;
    url_params["page"] = pp;
    await caller(url_params);
    pag_handler(Number(current_page.innerText), Number(total_page.innerText));

  })
  
  next_btn.addEventListener("click", async () => {
    let np = Number(current_page.innerText) + 1;
    url_params["page"] = np;
    await caller(url_params);
    pag_handler(Number(current_page.innerText), Number(total_page.innerText));
    
  })

  if (btn_logout){
    btn_logout.addEventListener("click", () => {
      localStorage.removeItem("email");
      localStorage.removeItem("password");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("access_token_exp");
      localStorage.removeItem("refresh_token_exp");
    })
  }
   
  all_prod.addEventListener("click", () => {
    url_params["page"] = 1
    console.log(url_params)
    get_all_prod(url_params);
    pag_box.style.display = "block";
  })

  profile.addEventListener("click", () => {
    getProfile();
  })
  
  if (!localStorage.getItem("access_token")){
    await login(email);
  }

  if (Date.now() > localStorage.getItem("refresh_token_exp")){
    await login()
  }
  
  if (Date.now() > localStorage.getItem("access_token_exp")){
    await refreshToken()
  }
  

  await getProfile();
})












//end all api call

function to_checkValue(arg) {
  let op = document.getElementsByName("priceOpt");
  op.forEach(option => {
    if (current_url.includes(arg) & option.value === arg) {
      option.checked = true;
    }
  });
}



