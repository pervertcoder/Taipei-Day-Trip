from pydantic import BaseModel
from typing import List

# 捷運/分類資料回傳格式
class DataResponse(BaseModel):
	data: List[str]

class ErrorResponse(BaseModel):
    error: bool
    message: str

class AttractionResponse(BaseModel):
	data: dict

class AttractionDataResponse(BaseModel):
	nextPage: int | None
	data: list

# 成功狀態格式
class stateResponse(BaseModel):
	ok : bool

# 註冊request格式
class registDataRequest(BaseModel):
	name : str
	email : str
	password : str

# 登入request格式
class loginDataRequest(BaseModel):
	email :str
	password : str

#登入路由回傳格式
class loginDataResponse(BaseModel):
	token : str

# 登入狀態驗證資料格式
class userData(BaseModel):
	id : int
	name : str
	email : str

# 登入狀態驗證
class loginDataCheck(BaseModel):
	data : userData

# 行程資料details
class bookingData(BaseModel):
	id : int
	name : str
	address : str
	image : str
	

# 行程資料
class booking(BaseModel):
	attraction : bookingData
	date : str
	time : str
	price : int

# 行程
class bookingResponse(BaseModel):
	data : booking | None

# 建立新的行程
class createBooking(BaseModel):
	attractionId : int
	date : str
	time : str
	price : int

# 訂單資料details
class orderData(BaseModel):
	attraction : bookingData
	date : str
	time : str

# 客戶資料
class memContact(BaseModel):
	name : str
	email : str
	phone : str

# 訂單資料
class orderInfo(BaseModel):
	price : int
	trip : orderData
	contact : memContact

# 建立新的訂單
class createOrder(BaseModel):
	prime : str
	order : orderInfo
	
# 付款訊息
class payMessage(BaseModel):
	status : int
	message : str

# 訂單回應格式details
class orderResDetail(BaseModel):
	number : str
	payment : payMessage

# 訂單回應格式details-付款失敗
class orderResDetailFalse(BaseModel):
	number : str
	error : bool
	message : str

# 訂單回應格式
class orderResponse(BaseModel):
	data : orderResDetail | orderResDetailFalse

# 取得訂單資料格式詳細
class getOrderDetail(BaseModel):
	number : str
	price : int
	trip : orderData
	contact : memContact
	status : int


# 取得訂單資料格式
class getOrderResponse(BaseModel):
	data : getOrderDetail | None