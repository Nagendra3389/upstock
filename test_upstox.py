
from playwright.sync_api import sync_playwright

from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import parse_qs,urlparse,quote
import pyotp
import requests
# python -m playwright codegen demo.playwright.dev/todomvc
def test():

    with sync_playwright() as p:
        # browser = p.chromium.launch()
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://playwright.dev")
        
        page.screenshot(path="example.png")
        print(page.title())
        browser.close()


API_KEY = "02c721ad-ecf8-4ff2-9828-e5a77dc10172"
SECRET_KEY = "hgwr8xtjkj"
RURL = "https://190.190.0.338:500"
TOTP_KEY = "JMTKUQJDUI2BXDJH3BC3RF6RZZSPS3GF"
MOBILE_NO = '8885951481'
PIN = '338407'

# rurlEncode = quote(RURL,safe="")

AUTH_URL = f'https://api-v2.upstox.com/login/authorization/dialog?response_type=code&client_id={API_KEY}&redirect_uri={RURL}'
url_fix = 'https://api-v2.upstox.com/login/authorization'


def get_token_acess(code):
    url = 'https://api-v2.upstox.com/login/authorization/token' 
 
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded' 
    }

    data = {
        'code' : code,
        'client_id' : API_KEY,
        'client_secret' : SECRET_KEY,
        'redirect_uri' : RURL,
        'grant_type' : 'authorization_code'
    }


    responce = requests.post(url,headers=headers,data=data)
    json_responce = responce.json()
        # Access the response data
    print(f"access_token:  {json_responce['access_token']}")



from playwright.sync_api import Playwright, sync_playwright, Expect

def run(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()  
    req = 'https://api-v2.upstox.com/login/authorization/redirect'  #?code=uCbX_R
    with page.expect_request(f"*{req}?code*") as request: 
        page.goto(AUTH_URL)
        page.locator("#mobileNum").click()
        page.locator("#mobileNum").fill("8885951481")
        page.get_by_role("button", name="Get OTP").click()
        page.locator("#otpNum").click()
        otp = pyotp.TOTP(TOTP_KEY).now()
        page.locator("#otpNum").fill(otp)
        page.get_by_role("button", name="Continue").click()
        page.get_by_label("Enter 6-digit PIN").click()
        page.get_by_label("Enter 6-digit PIN").fill("338407")
        res = page.get_by_role("button", name="Continue").click()
        current_url = page.url
        page.wait_for_load_state()
        
        # print(current_url)
        # browser.close()
    

    url =    request.value.url 
    print(f"Redirect Url with code : {url}")
    parsed = urlparse(url)
    code = parse_qs(parsed.query)['code'][0]
    context.close()
    browser.close()
    return code

def get_fund(access_token):
    url1 = "https://api-v2.upstox.com/user/get-funds-and-margin" 
 
    headers = {"accept" : "application/json",
           "Api-Version" : "2.0",
           "Authorization" : f"Bearer {access_token}"
          }

    params = {'segment' : 'SEC'}  #COM  SEC


    responce = requests.get(url1,headers=headers,params = params)
    print(responce.json())



with sync_playwright() as playwright:
    code = run(playwright)

access_token = get_token_acess(code)

get_fund(access_token)
