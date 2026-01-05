"use strict";

const scheduleBtn = document.querySelector(".topbar__right--booking");
const scheduleStart = document.querySelector(".scheduleStart");
// 檢查token
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
    scheduleStart.addEventListener("click", () => {
      // console.log(window.location.href);
      window.location.href = "/booking";
    });
    console.log(data.data);
  } else {
    console.log("未登入");
    localStorage.removeItem("token");
    popUp(scheduleBtn);
    popUp(scheduleStart);
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

const attractionName = document.querySelector(".attractionName");
const categoryMrt = document.querySelector(".categoryMrt");

const mainDes = document.querySelector(".mainDes");
const address = document.querySelector(".address");
const transport = document.querySelector(".transport");

// 首頁連結
const clickE = document.querySelector(".clickE");
clickE.addEventListener("click", () => {
  window.location.href = "/";
});

// 價錢依據時段改變
const radioAll = document.getElementsByName("time");
const price = document.querySelector(".priceS");
const priceChanged = function () {
  if (radioAll[0].checked) {
    price.textContent = "新台幣 2000 元";
  }
  if (radioAll[1].checked) {
    price.textContent = "新台幣 2500 元";
  }
};
for (let i = 0; i < radioAll.length; i++) {
  radioAll[i].addEventListener("change", () => {
    priceChanged();
  });
}

// API獲取+畫面渲染
const imgSlider = document.querySelector(".imgSlider");
const arrowRight = document.getElementById("nextBtn");
const arrowLeft = document.getElementById("prevBtn");
const indicators = document.getElementById("indicators");
const getAttractionIdData = async function () {
  const hRef = window.location.href;
  const hRefAr = hRef.split("/");
  const id = hRefAr[4];

  let url = `/api/attraction/${id}`;
  const res = await fetch(url);
  const data = await res.json();
  const attraction = data.data;
  console.log(attraction);

  attractionName.textContent = attraction.name;
  categoryMrt.textContent = `${attraction.category} at ${attraction.mrt}`;

  mainDes.textContent = attraction.description;
  address.textContent = attraction.address;
  transport.textContent = attraction.transport;

  // 圖片
  const imgArr = attraction.image;
  imgSlider.src = imgArr[0];

  // 指示器
  const imgArrLen = imgArr.length;
  for (let i = 0; i < imgArrLen; i++) {
    const sonIndi = document.createElement("div");
    sonIndi.setAttribute("class", "sonIndi");
    sonIndi.dataset.id = i;

    indicators.appendChild(sonIndi);
  }

  const sons = document.querySelectorAll(".sonIndi");
  const coloredSon0 = Array.from(sons).filter((son) => son.dataset.id === "0");
  coloredSon0[0].classList.add("sonIndi__stat--on");

  // 輪播
  let currentPos = 0;
  const lengthAr = imgArr.length;

  arrowRight.addEventListener("click", () => {
    if (currentPos < lengthAr - 1) {
      imgSlider.src = imgArr[currentPos + 1];
      currentPos += 1;
      const coloredSons = Array.from(sons).filter(
        (son) =>
          son.dataset.id === String(currentPos) ||
          son.dataset.id === String(currentPos - 1)
      );
      coloredSons[0].classList.remove("sonIndi__stat--on");
      coloredSons[1].classList.add("sonIndi__stat--on");
    }
    if (currentPos === lengthAr - 1) {
      console.log("no more data");
    }
  });

  arrowLeft.addEventListener("click", () => {
    if (currentPos !== 0) {
      imgSlider.src = imgArr[currentPos - 1];
      currentPos -= 1;
      const coloredSons = Array.from(sons).filter(
        (son) =>
          son.dataset.id === String(currentPos) ||
          son.dataset.id === String(currentPos + 1)
      );
      coloredSons[0].classList.add("sonIndi__stat--on");
      coloredSons[1].classList.remove("sonIndi__stat--on");
    } else {
      console.log("no more image");
    }
  });
};

getAttractionIdData();

// 會員系統註冊
const error = document.querySelector(".eror");
const registBtn = document.getElementById("regist");

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

  if (
    !inputName.value.trim() ||
    !inputMail.value.trim() ||
    !inputPass.value.trim()
  ) {
    error.textContent = "請輸入姓名、信箱和密碼";
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
