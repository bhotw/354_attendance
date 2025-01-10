from werkzeug.security import generate_password_hash, check_password_hash

# password = "ghouse354Admin"
# hashed_password = generate_password_hash(password)
# print("hashed password:", hashed_password)

hashed_password = "scrypt:32768:8:1$JCfJPo1OaVurhfGH$0c5ed909597a400a0587fc3e91fcb3209694de79b47fa9bd2869325825abd30501586149bf2a24ae9aaa7620527cba4370fc404d59d31614b1fd49ded37cea39"

is_valid = check_password_hash(hashed_password, "ghouse354Admin")
print(is_valid)

