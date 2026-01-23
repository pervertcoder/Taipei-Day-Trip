"use strict";

// 檢查token
const scheduleBtn = document.querySelector(".topbar__right--booking");
const token = localStorage.getItem("token");
const loginButton = document.querySelector(".loginButton");
const checkState = async function () {
  const req = await fetch("/api/user/auth", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await req.json();

  if (data?.data?.email) {
    loginButton.removeEventListener("click", removeClass);
    loginButton.classList.add("logout");
    loginButton.textContent = "登出系統";
    scheduleBtn.addEventListener("click", () => {
      window.location.href = "/booking";
    });
    console.log(data.data);
  } else {
    console.log("未登入");
    localStorage.removeItem("token");
    popUp(scheduleBtn);
    return;
  }
};

checkState();

const removeClass = function () {
  coverlayer.classList.remove("coverlayer--off");
};

// 彈出式視窗
const loginRigist = document.querySelector(".pop");
const closingBtn = document.querySelector(".cdia");
const closingBtn2 = document.querySelector(".cdia2");
const coverlayer = document.querySelector(".coverlayer");
const popup1 = document.querySelector(".popup");
const popup2 = document.querySelector(".popup2");
const toLogin = document.getElementById("to_login");
const toRegist = document.getElementById("to_regist");

const popUp = function (btn) {
  btn.addEventListener("click", removeClass);

  closingBtn.addEventListener("click", () => {
    coverlayer.classList.add("coverlayer--off");
  });

  closingBtn2.addEventListener("click", () => {
    coverlayer.classList.add("coverlayer--off");
  });

  toLogin.addEventListener("click", () => {
    popup1.classList.add("state--off");
    popup2.classList.remove("state--off");
  });

  toRegist.addEventListener("click", () => {
    popup2.classList.add("state--off");
    popup1.classList.remove("state--off");
  });
};
popUp(loginRigist);

const attractionContent = document.querySelector(".attraction__content");

// 生成DOM
const renderAttractions = function (data) {
  // const fragment = document.createDocumentFragment();

  for (let i = 0; i < data.length; i++) {
    const attractionContentUnit = document.createElement("div");
    const imageShell = document.createElement("div");
    const attractionImage = document.createElement("img");
    const attractionInfo = document.createElement("div");
    const attractionInfoText = document.createElement("p");
    const attractionData = document.createElement("div");
    const attractionDataRight = document.createElement("p");
    const attractionDataLeft = document.createElement("p");

    attractionContentUnit.setAttribute("class", "attraction__content--unit");
    attractionContentUnit.setAttribute("data-id", `${data[i].id}`);
    imageShell.setAttribute("class", "imageShell");
    attractionImage.setAttribute("class", "aImage");
    attractionInfo.setAttribute("class", "attractionInfo");
    attractionData.setAttribute("class", "attractionData");
    attractionDataRight.setAttribute("class", "attractionDataRight");
    attractionDataLeft.setAttribute("class", "attractionDataLeft");

    attractionContent.appendChild(attractionContentUnit);
    attractionContentUnit.appendChild(imageShell);
    imageShell.appendChild(attractionImage);
    imageShell.appendChild(attractionInfo);
    attractionInfo.appendChild(attractionInfoText);
    attractionContentUnit.appendChild(attractionData);
    attractionData.appendChild(attractionDataLeft);
    attractionData.appendChild(attractionDataRight);

    attractionImage.src = data[i].image[0];
    attractionInfoText.textContent = data[i].name;
    attractionDataLeft.textContent = data[i].mrt;
    attractionDataRight.textContent = data[i].category;

    attractionContentUnit.addEventListener("click", () => {
      const id = attractionContentUnit.dataset.id;
      window.location.href = `/attraction/${id}`;
    });

    // fragment.appendChild(attractionContentUnit);
  }

  // attractionContent.appendChild(fragment);
};

// 狀態
const state = {
  page: 0,
  keyword: "",
  category: "",
};

// 統一build URL
function buildUrl() {
  const params = new URLSearchParams();
  params.set("page", state.page);

  if (state.keyword !== "") {
    params.set("keyword", state.keyword);
  }

  if (state.category !== "") {
    params.set("category", state.category);
  }
  return `/api/attractions?${params.toString()}`;
}

// 抓取景點資料，並回傳下一頁的頁數
const getAttractionData = async function () {
  let url = buildUrl();
  const req = await fetch(url);
  const response = await req.json();
  const data = response.data;
  const pageField = response.nextPage;
  // console.log(url);
  console.log(pageField);

  renderAttractions(data);
  // state.page = pageField;

  return pageField;
};

// 讀取下一頁資料的函式
const sentinel = document.querySelector("#scrollSentinel");
let isLoading = false;

const loadNextPage = async function () {
  if (isLoading) return;
  if (state.page === 0) return;
  isLoading = true;

  const nextPage = await getAttractionData();

  if (nextPage !== null) {
    state.page = nextPage;
  } else {
    observer.unobserve(sentinel);
    console.log("已經沒有更多資料");
  }

  isLoading = false;
};

// 建立intersection observer
const observer = new IntersectionObserver(
  async (entries) => {
    const entry = entries[0];
    if (entry.isIntersecting) {
      loadNextPage();
    }
  },
  {
    root: null,
    rootMargin: "0px",
    threshold: 0.9,
  },
);

// 畫面生成
async function init({ keyword = "", category = "" } = {}) {
  observer.unobserve(sentinel);
  state.keyword = keyword;
  state.category = category;
  state.page = 0;

  attractionContent.innerHTML = "";
  isLoading = true;
  let page = await getAttractionData();
  isLoading = false;

  if (page !== null) {
    state.page = page;
  }
  // requestAnimationFrame(() => {
  //   observer.observe(sentinel);
  // });
  setTimeout(() => {
    observer.observe(sentinel);
  }, 100);
}

init();

// 分類部分
// 生成DOM
const categoryAlign = function (data) {
  for (let i = 0; i < data.length; i++) {
    const filterRoom = document.createElement("div");
    const filterBtn = document.createElement("button");

    filterRoom.classList.add("filter__room");
    filterBtn.classList.add("filter__button");
    filterBtn.classList.add(`filter__button${i}`);
    filterBtn.type = "button";

    filterCategory.appendChild(filterRoom);
    filterRoom.appendChild(filterBtn);

    filterBtn.textContent = data[i];
  }
};

// 獲取API資料
const filterCategory = document.querySelector(".filter__category--structure");

const getCategory = async function () {
  let url = "/api/categories";
  const req = await fetch(url);

  const response = await req.json();
  let categoryData = response.data;
  // console.log(categoryData);

  let newCategoryData = ["全部分類"];
  for (const i of categoryData) {
    newCategoryData.push(i);
  }
  // console.log(newCategoryData);

  categoryAlign(newCategoryData);
};

getCategory();

// 顯示開關
const allCategory = document.querySelector(".filter__btn");
const filterPanel = document.querySelector(".filter__category--structure");

let stat = false;
const pointer = function () {
  if (!stat) {
    filterPanel.classList.remove("filter__state--off");
    filterPanel.classList.add("filter__state--on");
    stat = true;
  }
};
allCategory.addEventListener("click", pointer);

filterPanel.addEventListener("click", (e) => {
  if (e.target.classList.contains("filter__button")) {
    const text = e.target.textContent;

    switch (text) {
      case "全部分類":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "養生溫泉":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "藍色公路":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "歷史建築":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "藝文館所":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "單車遊蹤":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "戶外踏青":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "宗教信仰":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "其他":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
      case "親子共遊":
        allCategory.textContent = text;
        if (stat) {
          filterPanel.classList.remove("filter__state--on");
          filterPanel.classList.add("filter__state--off");
          const arrow = document.createElement("span");
          arrow.classList.add("arrow");
          allCategory.append(arrow);
          stat = false;
        }
        break;
    }
  }
});

// 捷運部分
const mrtBar = document.querySelector(".mrt__container--p");
const arrowLeft = document.querySelector(".arrow_left");
const arrowRight = document.querySelector(".arrow_right");

const getDataDom = function (data) {
  for (let i = 0; i < data.length; i++) {
    const mrtd = document.createElement("div");
    const mrtp = document.createElement("button");

    mrtd.classList.add("mrt__container");
    mrtp.classList.add("mrt__para");

    mrtBar.appendChild(mrtd);
    mrtd.appendChild(mrtp);

    mrtp.textContent = data[i];
  }
};
const getMrtsData = async function () {
  let url = "/api/mrts";
  let req = await fetch(url);

  let response = await req.json();
  let data = response.data;
  // console.log(data);

  getDataDom(data);
  const oneItemWidth = document.querySelector(".mrt__para").offsetWidth + 12;
  arrowLeft.addEventListener("click", () => {
    mrtBar.scrollLeft -= oneItemWidth;
  });
  arrowRight.addEventListener("click", () => {
    mrtBar.scrollLeft += oneItemWidth;
  });

  const items = document.querySelectorAll(".mrt__para");
  items.forEach((item) => {
    item.addEventListener("click", () => {
      const searchCat = document
        .querySelector(".filter__btn")
        .textContent.trim();
      if (searchCat !== "全部分類") {
        init({
          category: searchCat,
          keyword: item.textContent.trim(),
        });
        console.log(searchCat, item.textContent.trim());
      } else {
        init({ category: undefined, keyword: item.textContent.trim() });
        console.log(searchCat, item.textContent.trim());
      }
    });
  });
};
getMrtsData();

// 篩選搜尋事件
const search = document.getElementById("search");

search.addEventListener("click", () => {
  const searchCategory = document
    .querySelector(".filter__btn")
    .textContent.trim();
  const searchWord = document.getElementById("filter__ip").value;

  const cateparam = searchCategory !== "全部分類" ? searchCategory : undefined;
  const keyparam = searchWord || undefined;

  init({ category: cateparam, keyword: keyparam });
});

const clickE = document.querySelector(".clickE");

clickE.addEventListener("click", () => {
  window.location.href = "/";
});

// 會員系統註冊
const error = document.querySelector(".eror");
const registBtn = document.getElementById("regist");

// 檢查input格式
const checkFormat = function (strParam) {
  const searchAt = strParam.indexOf("@");
  const searchCom = strParam.indexOf(".com");
  if (searchAt === -1 || searchCom === -1) {
    return false;
  } else {
    return true;
  }
};

// 按鈕
registBtn.addEventListener("click", async () => {
  const inputName = document.getElementById("user");
  const inputMail = document.getElementById("mail");
  const inputPass = document.getElementById("pass");

  error.textContent = "";
  const payload = {
    name: inputName.value.trim(),
    email: inputMail.value.trim(),
    password: inputPass.value.trim(),
  };
  const checkInputFormat = checkFormat(payload.email);
  if (!payload.name || !payload.email || !payload.password) {
    error.textContent = "請輸入姓名、信箱和密碼";
  } else if (checkInputFormat === false) {
    error.textContent = "email格式不符";
  } else {
    const url = "/api/user";
    let response = await fetch(url, {
      method: "post",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    console.log(data);

    if (data.ok) {
      error.textContent = "註冊成功";
    } else {
      error.textContent = data.message;
    }
  }
});

// 登入程序
const loginBtn = document.getElementById("login");
const error2 = document.querySelector(".eror2");

loginBtn.addEventListener("click", async () => {
  const mail2 = document.getElementById("mail2").value.trim();
  const pass2 = document.getElementById("pass2").value.trim();

  error2.textContent = "";
  const payload = { email: mail2, password: pass2 };
  // console.log(payload);
  if (!payload.email || !payload.password) {
    error2.textContent = "請輸入帳號或密碼";
    return;
  }

  const url = "/api/user/auth";
  const response = await fetch(url, {
    method: "put",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  console.log(data);
  error2.textContent = data.message;
  if (data.token) {
    localStorage.setItem("token", data.token);
    window.location.reload();
  }
});

// 登出
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("logout")) {
    e.stopImmediatePropagation();
    localStorage.removeItem("token");
    window.location.reload();
  }
});
