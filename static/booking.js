"use strict";

const removeClass = function () {
  coverlayer.classList.remove("coverlayer--off");
};

const toHomepage = document.querySelector(".clickE");

toHomepage.addEventListener("click", () => {
  window.location.href = "/";
});

const titleInside = document.querySelector(".title__inside");

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
    titleInside.textContent = `您好，${data.data.name}，待預訂的行程如下：`;
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

  const emptyMessage = document.querySelector(".emptyMessage");

  const footer = document.querySelector(".footer");
  const data = response.data;
  const attractionInfo = document.querySelector(".attraction__info");
  const seperateLineInside = document.querySelectorAll(".seperateLine__inside");
  const access = document.querySelector(".access");
  const credit = document.querySelector(".credit");
  const payCheck = document.querySelector(".payCheck");

  if (data === null) {
    emptyMessage.classList.remove("state__off");
    const scheduleState = document.querySelector(".scheduleState");
    scheduleState.textContent = "目前沒有任何待預訂的行程";
    footer.classList.remove("footer__height--off");
    footer.classList.add("footer__height--on");
  } else {
    const attractionData = data.attraction;

    attractionInfo.classList.remove("state__off");
    for (let i = 0; i < seperateLineInside.length; i++) {
      seperateLineInside[i].classList.remove("state__off");
    }
    access.classList.remove("state__off");
    credit.classList.remove("state__off");
    payCheck.classList.remove("state__off");

    const deleteBtn = document.getElementById("delete");
    const atImg = document.querySelector(".atImg");
    const attractionTitle = document.querySelector(".attraction__title");
    const attractionDate = document.querySelector(".attraction__date");
    const attractionTime = document.querySelector(".attraction__time");
    const attractionPrice = document.querySelector(".attraction__price");
    const attractionAddress = document.querySelector(".attraction__address");
    const priceCheck = document.querySelector(".priceCheck");
    atImg.src = attractionData.image;
    attractionTitle.textContent = attractionData.name;
    attractionDate.textContent = data.date;
    attractionTime.textContent = data.time;
    attractionPrice.textContent = `新台幣 ${data.price} 元`;
    attractionAddress.textContent = attractionData.address;
    priceCheck.textContent = `總價：新台幣 ${data.price} 元`;
    deleteBtn.addEventListener("click", async () => {
      const url = "/api/booking";
      const req = await fetch(url, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const response = await req.json();
      window.location.href = "/booking";
    });
  }
};
attraction_render();

// 登出
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("logout")) {
    e.stopImmediatePropagation();
    localStorage.removeItem("token");
    window.location.reload();
  }
});
