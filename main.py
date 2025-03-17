import re
import random
import string
import streamlit as st

COMMON_PASSWORDS = {'password', 'password123', 'hello123', 'abcde123', 'welcome123', 'karachi123', 'pakistan123'}

def generate_strong_password():
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+=-{}[]:;\"'<>,.?/~`|"

    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()_+=-{}[]:;\"'<>,.?/~`|")
    ] 

    password += random.choices(characters, k=length - 4)

    random.shuffle(password)

    return "".join(password)

def check_password_strength(password):
    score = 0
    issues = []
    
    # Length Check
    if 8 <= len(password) <= 80:
        score += 1
    else:
        issues.append("❌ Password should be at least 8 characters long and should not exceed 80 characters.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        issues.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        issues.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*()\-_=+|{}\[\]<>\"':;,.?/]", password):
        score += 1
    else:
        issues.append("❌ Include at least one special character (!@#$%^&*).")

    # A digit or char repeats more than 3 times
    if not re.search(r"(.)\1{3,}", password):
        score += 1
    else:
        issues.append("❌ Avoid repeated characters more than 3 times")
    
    if not re.search(r"012|123|1234|234|456|567|678|789|890|abc|abcd|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz", password.lower()):
        score += 1
    else:
        issues.append("❌ Avoid sequential patterns like '1234' or 'abcd'.")
    
    if password.lower() in COMMON_PASSWORDS:
        issues.append("❌ This is a common password. Choose a more unique password.")
    else:
        score += 1
    
    # Strength Rating
    if score >= 5 and not issues:
        # print("✅ Strong Password!")
        st.success("✅ Strong Password!")
    elif 3 <= score < 5:
        st.warning("⚠️ Moderate Password - Consider adding more security features.")
        for issue in issues:
            st.write(issue)
    else:
        st.error("❌ Weak Password - Improve it using the suggestions below")
        for issue in issues:
            st.write(issue)
        
        
        # suggest a strong password
        new_password = generate_strong_password()
        st.info(f"\n\n🔐 Suggested Strong Password: **{new_password}**")



title = st.title("Password Checker")

# Get user input
password = st.text_input("Enter your password", type="password")


btn = st.button("Check Password Strength")

if btn:
    check_password_strength(password)

