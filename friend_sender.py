# ═══════════════════════════════════════════════════════════════
# friend_sender.py — Standalone Friend Request Sender
# Dev: @ags_owner_atif
# ═══════════════════════════════════════════════════════════════

import asyncio
import aiohttp
import time
import os

# Tomar folder er login_engine theke login function ta import korche
try:
    import login_engine
except ImportError:
    print("❌ Error: 'login_engine.py' file ta same folder e nei! Eita chara login hobe na.")
    exit()

from byte import Encrypt_ID
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

async def send_friend_request(target_uid, token):
    try:
        # UID encrypt kora hocche
        encrypted_id = Encrypt_ID(target_uid)
        payload = f"08a7c4839f1e10{encrypted_id}1801"
        
        # Packet encryption keys
        kb = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        ib = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        
        cipher = AES.new(kb, AES.MODE_CBC, ib)
        ep = cipher.encrypt(pad(bytes.fromhex(payload), AES.block_size)).hex()
        
        # API request pathano
        url = "https://loginbp.ppmainecoonghj.com/RequestAddingFriend"
        headers = {
            "Authorization": f"Bearer {token}", 
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1", 
            "ReleaseVersion": "OB55",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=bytes.fromhex(ep), ssl=False) as r:
                if r.status == 200:
                    return True, "✅ Friend request successfully sent!"
                else:
                    return False, f"❌ Failed! Status Code: {r.status}"
                    
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

async def main():
    print("═══════════════════════════════════════════════════")
    print("           KHUSHI FRIEND REQUEST SENDER")
    print("═══════════════════════════════════════════════════")
    
    # Input newa
    bot_uid = input("Enter Your UID: ").strip()
    bot_pw  = input("Enter Your Password: ").strip()
    target_uid = input("Enter Target UID (Friend request pathate hobe): ").strip()
    
    if not bot_uid or not bot_pw or not target_uid:
        print("❌ Error: Sob information dite hobe!")
        return

    print("\n[*] Logging in to your account...")
    # Login_engine diye login
    result = await login_engine.do_login(bot_uid, bot_pw, "BD")
    
    if not result:
        print("❌ Login Failed! Check your UID/Password.")
        return
        
    print(f"✅ Login Successful! Name: {result['account_name']}")
    print(f"[*] Sending friend request to UID: {target_uid} ...")
    
    token = result["token"]
    success, msg = await send_friend_request(target_uid, token)
    
    print(f"\n{msg}")
    print("═══════════════════════════════════════════════════")

if __name__ == "__main__":
    asyncio.run(main())