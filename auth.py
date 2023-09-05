import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['fightback@123']).generate()
print(hashed_passwords)