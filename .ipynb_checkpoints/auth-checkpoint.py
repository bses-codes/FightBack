import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['78910']).generate()
print(hashed_passwords)