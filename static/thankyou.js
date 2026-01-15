"use strict";

const removeClass = function () {
  coverlayer.classList.remove("coverlayer--off");
};

const toHomepage = document.querySelector(".clickE");
const scheduleBtn = document.querySelector(".topbar__right--booking");

toHomepage.addEventListener("click", () => {
  window.location.href = "/";
});

scheduleBtn.addEventListener("click", () => {
  window.location.href = "/booking";
});

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

    return {
      name: data.data.name,
      email: data.data.email,
    };
  } else {
    console.log("未登入");
    localStorage.removeItem("token");
    window.location.href = "/";
  }
};

//驗證
checkState();

// 登出
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("logout")) {
    e.stopImmediatePropagation();
    localStorage.removeItem("token");
    window.location.reload();
  }
});
