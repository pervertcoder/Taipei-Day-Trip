"use strict";

const removeClass = function () {
  coverlayer.classList.remove("coverlayer--off");
};

const toHomepage = document.querySelector(".clickE");

toHomepage.addEventListener("click", () => {
  window.location.href = "/";
});

const scheduleMessage = document.querySelector(".scheduleMessage");

// 判斷token
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
  // console.log(data);

  if (data?.data?.email) {
    loginButton.removeEventListener("click", removeClass);
    loginButton.classList.add("logout");
    loginButton.textContent = "登出系統";
    scheduleMessage.textContent = `您好，${data.data.name}，待預訂的行程如下`;
    console.log(data.data);
  } else {
    console.log("未登入");
    localStorage.removeItem("token");
    window.location.href = "/";
  }
};

checkState();

// 抓景點資料
const attraction_render = async function () {
  const url = "/api/booking";
  const req = await fetch(url, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const response = await req.json();
  console.log(response);
};
attraction_render();
// 判斷內文
const scheduleState = document.querySelector(".scheduleState");
let contentState = false;

if (!contentState) {
  scheduleState.textContent = "目前沒有任何待預訂的行程";
}

// 登出
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("logout")) {
    e.stopImmediatePropagation();
    localStorage.removeItem("token");
    window.location.reload();
  }
});
