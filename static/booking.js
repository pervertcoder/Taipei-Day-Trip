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
    // console.log(data.data);
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
let aId = null;
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
    aId = attractionData.id;

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

// 拿會員的資料
const accessFun = async function () {
  const answer = await checkState();
  console.log(answer);
  const accessName = document.getElementById("userName");
  const accessMail = document.getElementById("email");
  accessName.value = answer.name;
  accessMail.value = answer.email;
};
accessFun();

// 登出
document.body.addEventListener("click", (e) => {
  if (e.target.classList.contains("logout")) {
    e.stopImmediatePropagation();
    localStorage.removeItem("token");
    window.location.reload();
  }
});

// 處理時間
const dateDeal = function (y, a, b) {
  let A = String(a);
  let B = String(b);
  let Y = String(y);
  if (A.length === 1) {
    A = "-" + "0" + A;
  } else {
    A = "-" + A;
  }
  if (B.length === 1) {
    B = "-" + "0" + B;
  } else {
    B = "-" + B;
  }
  return Y + A + B;
};
const dateTest = new Date();
const dateY = dateTest.getFullYear();
const dateM = dateTest.getMonth() + 1;
const dateD = dateTest.getDate();
const currentDate = dateDeal(dateY, dateM, dateD);

// 串接金流

// 初始化設定
TPDirect.setupSDK(
  166455,
  "app_q3TDhCMqAZ8ym6YDOgArHrEJORKc25munVXfXsGHlnww9TPJpDJVXjpc0WzY",
  "sandbox"
);

// input外觀設定
let fields = {
  number: {
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    element: "#card-expiration-date",
    placeholder: "MM/YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "ccv",
  },
};
TPDirect.card.setup({
  fields: fields,
  styles: {
    // Style all elements
    input: {
      color: "gray",
    },
    // style valid state
    ".valid": {
      color: "green",
    },
    // style invalid state
    ".invalid": {
      color: "red",
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    "@media screen and (max-width: 400px)": {
      input: {
        color: "black",
      },
    },
  },
  // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

// onUpdate監聽使用者輸入狀態
const resetClass = function (a) {
  a.classList.add("error__off");
};

TPDirect.card.onUpdate(function (update) {
  // update.canGetPrime === true
  // --> you can call TPDirect.card.getPrime()
  if (update.canGetPrime) {
    // Enable submit Button to get prime.
    comfirmBtn.removeAttribute("disabled");
  } else {
    // Disable submit Button to get prime.
    comfirmBtn.setAttribute("disabled", true);
  }

  // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unknown']
  if (update.cardType === "visa") {
    // Handle card type visa.
  }

  // number 欄位是錯誤的
  if (update.status.number === 2) {
    const tpfieldErrorCard = document.querySelector(".error__card");
    resetClass(tpfieldErrorCard);
    tpfieldErrorCard.classList.remove("error__off");
  } else if (update.status.number === 0) {
    const tpfieldErrorCard = document.querySelector(".error__card");
    resetClass(tpfieldErrorCard);
    tpfieldErrorCard.classList.add("error__off");
  } else {
    const tpfieldErrorCard = document.querySelector(".error__card");
    resetClass(tpfieldErrorCard);
    tpfieldErrorCard.classList.add("error__off");
  }

  if (update.status.expiry === 2) {
    const tpfieldErrorExp = document.querySelector(".error__exp");
    resetClass(tpfieldErrorExp);
    tpfieldErrorExp.classList.remove("error__off");
  } else if (update.status.expiry === 0) {
    const tpfieldErrorExp = document.querySelector(".error__exp");
    resetClass(tpfieldErrorExp);
    tpfieldErrorExp.classList.add("error__off");
  } else {
    const tpfieldErrorExp = document.querySelector(".error__exp");
    resetClass(tpfieldErrorExp);
    tpfieldErrorExp.classList.add("error__off");
  }

  if (update.status.ccv === 2) {
    const tpfieldErrorCCV = document.querySelector(".error__ccv");
    resetClass(tpfieldErrorCCV);
    tpfieldErrorCCV.classList.remove("error__off");
  } else if (update.status.ccv === 0) {
    const tpfieldErrorCCV = document.querySelector(".error__ccv");
    resetClass(tpfieldErrorCCV);
    tpfieldErrorCCV.classList.add("error__off");
  } else {
    const tpfieldErrorCCV = document.querySelector(".error__ccv");
    resetClass(tpfieldErrorCCV);
    tpfieldErrorCCV.classList.add("error__off");
  }
});

// 呼叫getPrime函式，取得prime字串 + 呼叫API
const comfirmBtn = document.querySelector(".comfirmBtn");
comfirmBtn.addEventListener("click", async () => {
  const phoneN = document.querySelector("#phone").value;
  if (phoneN === "") {
    alert("請輸入電話號碼");
    return;
  }

  // 拿資料
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();

  if (tappayStatus === false) {
    alert("can not get prime");
    return;
  }

  TPDirect.card.getPrime(async (result) => {
    const name = document.querySelector(".attraction__title").textContent;
    const priceStr = document.querySelector(".attraction__price").textContent;
    const priceS = priceStr.split(" ");
    const address = document.querySelector(".attraction__address").textContent;
    const imgA = document.querySelector(".atImg").src;
    // const date = document.querySelector(".attraction__date").textContent;
    const time = document.querySelector(".attraction__time").textContent;
    const userN = document.querySelector("#userName").value;
    const emailN = document.querySelector("#email").value;
    if (result.status !== 0) {
      alert("get prime error " + result.msg);
      return;
    }
    const cardPrime = result.card.prime;
    alert("get prime 成功，prime: " + result.card.prime);

    const payload = {
      prime: cardPrime,
      order: {
        price: priceS[1],
        trip: {
          attraction: {
            id: aId,
            name: name,
            address: address,
            image: imgA,
          },
          date: currentDate,
          time: time,
        },
        contact: {
          name: userN,
          email: emailN,
          phone: phoneN,
        },
      },
    };

    const url = "/api/orders";
    const req = await fetch(url, {
      method: "post",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const response = await req.json();
    console.log(response);

    // 跳轉至thankyou頁面
    window.location.reload();
  });
});

// setTimeout(() => {
//   const priceStr = document.querySelector(".attraction__price").textContent;
//   const priceS = priceStr.split(" ");
//   console.log(priceS[1]);
// }, 500);
