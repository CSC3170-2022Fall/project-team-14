from werkzeug.security import check_password_hash, generate_password_hash

print(generate_password_hash("123456"))
print(generate_password_hash("654321"))
print(generate_password_hash("123654"))